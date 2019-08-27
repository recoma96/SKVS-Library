import threading #mutex 선언을 위한 import
from socket import *
from queue import *
from time import *
import struct
from .SkvsLibException import *
from .SkvsConnectionRecvThread import *
from .modules.packet.Packet import *

class SkvsConnection:
    # int ID
    # int pswd
    # string connectIP
    # int port
    # socket
    # sendMutex -> 명령문을 서버에 보낼 때 사용하는 mutex
    # list serialList       / -> cmd번호 리스트 계산용
    # mutex calSerialMutex  /
    # queue packetQueue     / -> 패킷 큐 계산용
    # mutex packetQueueMutex/
    # isConnected

    def __init__(self, _id, _pswd, _connectIP, _port):
        #타입 검사
        if type(_id) != str or type(_pswd) != str:
            raise TypeError("Id or pswd is not str")
        if type(_connectIP) != str:
            raise TypeError("IP must be str")
        if type(_port) != int:
            raise TypeError("port must be integer")

        #저장
        self.id = _id; self.pswd = _pswd; self.connectIP = _connectIP
        self.port = _port
        self.isConnected = False

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.sendMutex = threading.Lock()

        self.serialList = []
        self.calSerialMutex = threading.Lock()  #mutex 선언

        self.packetQueue = [] #C++ 처럼 큐의 맨 앞 부분 참조가 불가능하다.
        self.packetQueueMutex = threading.Lock()

    #커맨드 시리얼 번호 리스트 추가 및 삭제 연산
    def setCmdSerial(self):

        counter = 0

        #리스트에 아무것도 없으면 첫번호 리턴값 0
        if len(self.serialList) == 0:
            return 0

        #가장 큰 값보다 1 이상의 수 생성
        for cmdNum in self.serialList:
            if counter <= cmdNum:
                counter = cmdNum+1
        return counter

    #커맨드 번호 삭제: 성공 시 True, 실패 시 False
    def removeCmdSerial(self, _deleteNum):
        #타입 판정
        if type(_deleteNum) is not int:
            raise TypeError("This number is not int")
        
        #번호 삭제 시작
        for cmdNum in self.serialList:
            if _deleteNum == cmdNum:
                self.serialList.remove(_deleteNum)
                return True        
        #못찾음
        return False

    #서버 접속
    def open(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        if self.isConnected == True: #이미 연결되어 있는 경우
            raise SkvsSocketSettingException("This Connection is Aleady Connected")

        sendLoginData = self.id + '-' + self.pswd

        #로그인 연결
        try:
            self.socket.connect((self.connectIP, self.port))
        except ConnectionRefusedError:
            raise SkvsSocketSettingException("Conenct Failed From Server")


        if self.socket.send(sendLoginData.encode('utf-8')) <= 0:
            raise SkvsSocketSettingException("Conenct Failed From Server")


        self.socket.settimeout(60)
        try:
            isAllowd = bool(self.socket.recv(1)) #로그인 허용 시그널
        except timeout:
            raise SkvsSocketSettingException("Conenct Failed From Server")

        #로그인 거부
        if isAllowd == False:
            self.socket.close()
            raise SkvsLoginFailedException("Login Denied")
        
        #쓸모없는 유저레벨 값 받기
        self.socket.settimeout(60)
        try:
            trash = self.socket.recv(4)
        except timeout:
            raise SkvsSocketSettingException("Conenct Failed From Server")

        #연결 했음
        self.isConnected = True

        #Recv-Thread 생성
        #연결 끊어질 때까지 쓰레드 돌리기
        t1 = threading.Thread(target = SkvsConnectionRecvThread, args=(self,))
        t1.deamon = True
        t1.start()
        

    #연결 끊기
    
    def close(self):
        #이미 연결 끊어진 경우 -> 상관없음
        if self.isConnected == False:
            return
        
        #시리얼 넘버 생성
        self.calSerialMutex.acquire()
        newCmdSerial = self.setCmdSerial()
        self.calSerialMutex.release()

        #SendCmdPacket 생성
        closePacket = SendCmdPacket(self.id, self.connectIP, newCmdSerial, newCmdSerial, "quit")

        #직렬화
        packetBytes = makePacketSerialToByte(closePacket)
        #길이구하기
        packetSize = len(packetBytes)

        #패킷 전송

        #리틀엔디안으로 전환
        sizeToLittle = struct.pack('<L', packetSize)
        typeToLittle = struct.pack('<L', PacketTypeConverter.toInteger(closePacket.packetType))

        if self.socket.send(sizeToLittle) <= 0:
            self.socket.close()
            self.isConnected = False
            raise SkvsSocketSettingException("Conenct Failed From Server")

        if self.socket.send(typeToLittle) <= 0:
            self.socket.close()
            self.isConnected = False
            raise SkvsSocketSettingException("Conenct Failed From Server")

        if self.socket.send(packetBytes) <= 0:
            self.socket.close()
            self.isConnected = False
            raise SkvsSocketSettingException("Conenct Failed From Server")

        #패킷 큐 탐색
        #10초안에 받지 않으면 close 처리
        counter = 0
        while True:
            if len(self.packetQueue) > 0: #리스트에 데이터가 존재함

                #시리얼 넘버가 일치하면
                #리스트 최상단에 있는 거 끄집어내기
                self.packetQueueMutex.acquire()
                if self.packetQueue[0].cmdNum == newCmdSerial:
                    popedPacket = self.packetQueue[0]
                    del self.packetQueue[0]
                    self.packetQueueMutex.release()
                    break

                else: #아니면 그냥 넘어가기
                    self.packetQueueMutex.release()
                    sleep(0.001)
                    counter += 1
                    continue
            else: #리스트가 비어있을 경우
                if counter > 100000: #10초가 지나면
                    #연결이 끊어진 걸로 처리
                    self.isConnected = False
                    self.socket.close()
                    return
                else:
                    sleep(0.001)
                    counter += 1
                    continue
        
        #종료
        print(popedPacket.signal)
        self.isConnected = False
        self.socket.close()
        sleep(0.005)
        return
    