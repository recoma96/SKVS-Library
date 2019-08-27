import enum

#상위 폴더를 접근해서 import DataElement
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import modules.structure.DataElement as de

#enums

class PacketType(enum.Enum):
    sendCmd = 0
    recv = 1
    signal = 2
    log = 3

class RecvPacketType(enum.Enum):
    data = 0
    msg = 1

class SignalType(enum.Enum):
    shutdown = 0
    recvStart = 1
    recvEnd = 2
    error = 3

#enum Converter


class Packet:
    # string : username, ip
    # int : cmdNum, sock
    # PacketType : packetType
    def __init__(self, _packetType, _username, _ip, _cmdNum, _sock):
        #타입 판정
        if type(_username) != str or type(_ip) != str:
            raise TypeError("username or ip is not string")
        if type(_packetType) != PacketType:
            raise TypeError("packetType is not PacketType")
        if type(_cmdNum) != int or type(_sock) != int:
            raise TypeError("cmdNum or socket number is not integer")
        #판정 끝 값 삽입 시작
        self.packetType = _packetType; self.username = _username
        self.ip = _ip; self.cmdNum = _cmdNum; self.sock = _sock

class SendCmdPacket(Packet):
    def __init__(self, _username, _ip, _cmdNum, _sock, _cmd):
        # packet 클래스 생성
        Packet.__init__(self, PacketType.sendCmd , _username, _ip, _cmdNum, _sock)
        
        #cmd 타입 판정
        if type(_cmd) is not str:
            raise TypeError("command is not string")
        
        #토큰화
        self.cmdVec = _cmd.split(' ')

class RecvPacket(Packet):
    def __init__(self, _username, _ip, _cmdNum, _sock, _recvPacketType):
        Packet.__init__(self, PacketType.recv , _username, _ip, _cmdNum, _sock)
        if type(_recvPacketType) is not RecvPacketType:
            raise TypeError("This packetType is not PacketType")
        self.recvPacketType = _recvPacketType

class RecvDataPacket(RecvPacket):
    def __init__(self, _username, _ip, _cmdNum, _sock, _dataElement ):
        RecvPacket.__init__(self, _username, _ip, _cmdNum, _sock, RecvPacketType.data)
        if type(_dataElement) is not de.DataElement:
            raise TypeError("This dataElement type is not DataElement")
        self.data = _dataElement


class RecvMsgPacket(RecvPacket):
    def __init__(self, _username, _ip, _cmdNum, _sock, _msg ):
        RecvPacket.__init__(self, _username, _ip, _cmdNum, _sock, RecvPacketType.msg)
        if type(_msg) is not str:
            raise TypeError("This dataElement type is not str")
        self.msg = _msg


class SignalPacket(Packet):
    def __init__(self, _username, _ip, _cmdNum, _sock, _sig):
        Packet.__init__(self, PacketType.signal , _username, _ip, _cmdNum, _sock)
        if type(_sig) is not SignalType:
            raise TypeError("This signal type is not SignalType")
        self.signal = _sig

class LogPacket(Packet):
    def __init__(self, _username, _ip, _cmdNum, _sock, _logMsg):
        Packet.__init__(self, PacketType.log, _username, _ip, _cmdNum, _sock)
        if type(_logMsg) is not str:
            raise TypeError("This msg is not str")
        self.logMsg = _logMsg