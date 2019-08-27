from . import SkvsLibException as sl
from . import SkvsConnection as sk

from .modules.packet.Packet import *
from .modules.packet.PacketSerial import *
from .modules.packet.PacketTypeConverter import *

from time import *
import struct

class SkvsCommand:

    # connection = SkvsConnection
    # cmd = str <명령어 입력>

    def __init__(self, _connection, _cmd):
        if type(_connection) is not sk.SkvsConnection:
            raise TypeError("This connection type is not SkvsConnection")
        if type(_cmd) is not str:
            raise TypeError("This cmd type must be str")
        if len(_cmd) == 0:
            raise ValueError("command length is zero")

        #값 삽입
        self.connection = _connection
        self.cmd = _cmd

    def executeNonQuery(self):
        #연결 여부 판정
        if self.connection.isConnected == False:
            raise sl.SkvsSocketSettingError("This server is disconnected")
        
        #커맨드 길이 판정
        if len(self.cmd) == 0:
            raise ValueError("command length is zero")
        
        #시리얼 넘버 연산
        self.connection.calSerialMutex.acquire()
        newSerialNum = self.connection.setCmdSerial()
        self.connection.calSerialMutex.release()

        #패킷 생성
        sendPacket = SendCmdPacket(         \
            self.connection.id,             \
            self.connection.connectIP,      \
            newSerialNum,                   \
            0, self.cmd
        )
        
        #패킷 시리얼 생성
        
        #직렬화
        packetBytes = makePacketSerialToByte(sendPacket)
        #길이구하기
        packetSize = len(packetBytes)

        #리틀엔디안으로 전환
        sizeToLittle = struct.pack('<L', packetSize)
        typeToLittle = struct.pack('<L', PacketTypeConverter.toInteger(sendPacket.packetType))

        #데이터 전송
        self.connection.sendMutex.acquire()

        if self.connection.socket.send(sizeToLittle) <= 0:

            self.connection.sendMutex.release()

            self.connection.socket.close()
            self.connection.isConnected = False

            raise SkvsSocketSettingException("Conenct Failed From Server")

        if self.connection.socket.send(typeToLittle) <= 0:
            
            self.connection.sendMutex.release()

            self.connection.socket.close()
            self.connection.isConnected = False

            raise SkvsSocketSettingException("Conenct Failed From Server")

        if self.connection.socket.send(packetBytes) <= 0:

            self.connection.sendMutex.release()

            self.connection.socket.close()
            self.connection.isConnected = False

            raise SkvsSocketSettingException("Conenct Failed From Server")

        self.connection.sendMutex.release()

        #데이터 받기
        #패킷 큐 탐색
        #10초안에 받지 않으면 close 처리
        counter = 0
        errorMsg = ""
        signal = 0
        while signal != SignalType.recvEnd and signal != SignalType.error and signal != SignalType.shutdown:
            if len(self.connection.packetQueue) > 0: #리스트에 데이터가 존재함

                #시리얼 넘버가 일치하면
                #리스트 최상단에 있는 거 끄집어내기
                self.connection.packetQueueMutex.acquire()
                if self.connection.packetQueue[0].cmdNum == newSerialNum:
                    
                    counter = 0

                    popedPacket = self.connection.packetQueue[0]
                    del self.connection.packetQueue[0]
                    self.connection.packetQueueMutex.release()

                    #데이터 추출
                    #sendcmd, recvdata 필요없음
                    if type(popedPacket) is SendCmdPacket:
                        del popedPacket
                        continue
                    elif type(popedPacket) is RecvDataPacket:
                        del popedPacket
                        continue
                    elif type(popedPacket) is RecvMsgPacket:
                        errorMsg = popedPacket.msg

                    elif type(popedPacket) is SignalPacket:
                        signal = popedPacket.signal
                    else:
                        del popedPacket
                        continue

                    del popedPacket
                    continue

                else: #아니면 그냥 넘어가기
                    self.connection.packetQueueMutex.release()
                    sleep(0.001)
                    counter += 1
                    continue
            else: #리스트가 비어있을 경우
                if counter > 100000: #10초가 지나면
                    #연결이 끊어진 걸로 처리
                    self.connection.close()
                    raise sl.SkvsSocketSettingError("This server is disconnected")
                else:
                    sleep(0.001)
                    counter += 1
                    continue

        #에러 여부 확인하기
        if signal == SignalType.recvEnd:
            return
        elif signal == SignalType.error: #명령 실패
            raise sl.SkvsCommandFaildException(errorMsg)
        elif signal == SignalType.shutdown: #종료
            self.connection.close()
            return
        else: return


    def executeReadStream(self):
       #연결 여부 판정
        if self.connection.isConnected == False:
            raise sl.SkvsSocketSettingError("This server is disconnected")
        
        #커맨드 길이 판정
        if len(self.cmd) == 0:
            raise ValueError("command length is zero")
        
        #시리얼 넘버 연산
        self.connection.calSerialMutex.acquire()
        newSerialNum = self.connection.setCmdSerial()
        self.connection.calSerialMutex.release()

        #패킷 생성
        sendPacket = SendCmdPacket(         \
            self.connection.id,             \
            self.connection.connectIP,      \
            newSerialNum,                   \
            0, self.cmd
        )
        
        #패킷 시리얼 생성
        
        #직렬화
        packetBytes = makePacketSerialToByte(sendPacket)
        #길이구하기
        packetSize = len(packetBytes)

        #리틀엔디안으로 전환
        sizeToLittle = struct.pack('<L', packetSize)
        typeToLittle = struct.pack('<L', PacketTypeConverter.toInteger(sendPacket.packetType))

        #데이터 전송
        self.connection.sendMutex.acquire()

        if self.connection.socket.send(sizeToLittle) <= 0:

            self.connection.sendMutex.release()

            self.connection.socket.close()
            self.connection.isConnected = False

            raise SkvsSocketSettingException("Conenct Failed From Server")

        if self.connection.socket.send(typeToLittle) <= 0:
            
            self.connection.sendMutex.release()

            self.connection.socket.close()
            self.connection.isConnected = False

            raise SkvsSocketSettingException("Conenct Failed From Server")

        if self.connection.socket.send(packetBytes) <= 0:

            self.connection.sendMutex.release()

            self.connection.socket.close()
            self.connection.isConnected = False

            raise SkvsSocketSettingException("Conenct Failed From Server")

        self.connection.sendMutex.release()

        #데이터 받기
        #패킷 큐 탐색
        #10초안에 받지 않으면 close 처리
        counter = 0
        errorMsg = ""
        signal = 0
        dataContainer = [] #받은데이터 보관
        while signal != SignalType.recvEnd and signal != SignalType.error and signal != SignalType.shutdown:
            if len(self.connection.packetQueue) > 0: #리스트에 데이터가 존재함

                #시리얼 넘버가 일치하면
                #리스트 최상단에 있는 거 끄집어내기
                self.connection.packetQueueMutex.acquire()
                if self.connection.packetQueue[0].cmdNum == newSerialNum:
                    
                    counter = 0

                    popedPacket = self.connection.packetQueue[0]
                    del self.connection.packetQueue[0]
                    self.connection.packetQueueMutex.release()

                    #데이터 추출
                    #sendcmd, recvdata 필요없음
                    if type(popedPacket) is SendCmdPacket:
                        del popedPacket
                        continue
                    elif type(popedPacket) is RecvDataPacket:
                        dataDic = {'data':popedPacket.data.data}
                        dataDic['structtype'] = popedPacket.data.structtype
                        dataContainer.append(dataDic)
                        del popedPacket
                        continue
                    elif type(popedPacket) is RecvMsgPacket:
                        errorMsg = popedPacket.msg

                    elif type(popedPacket) is SignalPacket:
                        signal = popedPacket.signal
                    else:
                        del popedPacket
                        continue

                    del popedPacket
                    continue

                else: #아니면 그냥 넘어가기
                    self.connection.packetQueueMutex.release()
                    sleep(0.001)
                    counter += 1
                    continue
            else: #리스트가 비어있을 경우
                if counter > 100000: #10초가 지나면
                    #연결이 끊어진 걸로 처리
                    self.connection.close()
                    raise sl.SkvsSocketSettingError("This server is disconnected")
                else:
                    sleep(0.001)
                    counter += 1
                    continue

        #에러 여부 확인하기
        if signal == SignalType.recvEnd:
            return dataContainer
        elif signal == SignalType.error: #명령 실패
            raise sl.SkvsCommandFaildException(errorMsg)
        elif signal == SignalType.shutdown: #종료
            self.connection.close()
            raise sl.SkvsSocketSettingError("This server is disconnected")
        else:
            raise sl.SkvsLibException("unknown error")