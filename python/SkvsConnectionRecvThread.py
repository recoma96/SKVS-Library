from . import SkvsLibException as sl
from . import SkvsConnection as sk

from .modules.packet.Packet import *
from .modules.packet.PacketProtocol import *
from .modules.packet.PacketTypeConverter import *

import threading #mutex 선언을 위한 import
from socket import *
from queue import *
from time import *

def SkvsConnectionRecvThread(_connection):
    
    if type(_connection) is not sk.SkvsConnection:
        return False

    #연걸이 되어 있는 동안 스레드 작동
    while _connection.isConnected == True:

        #서버부터 대기
        #데이터 받는 순서, 데이터크기값, 패킷 타입, 직렬화된 객체데이터

        #recv Nonblocking
        _connection.socket.setblocking(0)
        while True:
            if _connection.isConnected == False:
            #큐비우기
                while len(_connection.packetQueue) > 0 : _connection.packetQueue.pop()
                return

            try:
                dataSize = _connection.socket.recv(4)
            except error as e: #연결댓는데 데이터아직 못받음
                sleep(0.001)
                continue
            else: #데이터를 받음
                #dataSize가 0 == 서버와의 연결이 끊김
                if len(dataSize) == 0:
                    # close() 함수 실행
                    raise sl.SkvsSocketSettingException("Conenct Failed From Server")
                #데이터 int로 형변환
                dataSize = int.from_bytes(dataSize, 'little')
                
                break #while문에서 빠져나오기
        
        #여기서부터 NonBlocking + 10초안에 데이터 못받으면 close() 처리
        _connection.socket.setblocking(1)

        _connection.socket.settimeout(10)
        try:
            bytePacketType = _connection.socket.recv(4)
            intpacketType = int.from_bytes(bytePacketType, 'little')
        except timeout:
            # close() 함수 실행
            raise sl.SkvsSocketSettingException("Conenct Failed From Server")
        
        #함수작동 오류로 패킷타입 숫자화
        try:
            packetType = PacketTypeConverter.toType(intpacketType)
        except ValueError:
            #close() 함수 실행
            raise sl.SkvsProtocolException("Invaild packet type from server")
            

        #문자열 수신
        _connection.socket.settimeout(10)
        try:
            serializedStr = _connection.socket.recv(dataSize).decode('utf-8')
        except timeout:
            # close() 함수 실행
            raise sl.SkvsSocketSettingException("Conenct Failed From Server")

        #패킷 조합
        try:
            receivedPacket = returnToPacket(serializedStr)
        except: #잘못된 데이터는 버리기
            continue

        #패킷을 리스트에 집어넣기
        _connection.packetQueueMutex.acquire()
        _connection.packetQueue.append(receivedPacket)
        _connection.packetQueueMutex.release()
        continue

        




