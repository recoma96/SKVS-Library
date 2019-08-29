from . import Packet as pk
from . import PacketTypeConverter as pc
from . import PacketSerial_pb2 as pb
import google
from google.protobuf import text_format

#상위 폴더를 접근해서 import DataElement
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
import modules.structure.DataElement as de
import modules.structure.DataElementTypeConverter as dc

#기본 요소 패킷 시리얼 만들기
def makePacketSerial(_targetPacket):
    #타입 검사
    if type(_targetPacket) is not pk.Packet and             \
        type(_targetPacket) is not pk.SendCmdPacket and     \
        type(_targetPacket) is not pk.RecvPacket and        \
        type(_targetPacket) is not pk.RecvDataPacket and    \
        type(_targetPacket) is not pk.RecvMsgPacket and     \
        type(_targetPacket) is not pk.SignalPacket and      \
        type(_targetPacket) is not pk.LogPacket: 
            TypeError("This type is not type of packet")
    
    #serial 만들기
    packetSerial = pb.PacketSerial()

    packetSerial.packetType = pc.PacketTypeConverter.toInteger(_targetPacket.packetType)
    packetSerial.username = _targetPacket.username
    packetSerial.IP = _targetPacket.ip
    packetSerial.cmdNum = _targetPacket.cmdNum
    packetSerial.sock = _targetPacket.sock

    return packetSerial

#DataElement 시리얼 제작
def makeDataElementSerial(_targetElement):
    if type(_targetElement) is not de.DataElement:
        TypeError("This type is not type of Element")
    
    elementSerial = pb.DataElementSerial()

    elementSerial.data = str(_targetElement.data) 
    elementSerial.dataType = dc.DataTypeConverter.toInteger(_targetElement.dataType)
    elementSerial.structType = dc.StructTypeConverter.toInteger(_targetElement.structType)
    return elementSerial

#RecvPacket 시리얼 제작
def makeRecvPacketSerial(_targetPacket):
    if type(_targetPacket) is not pk.RecvPacket and        \
        type(_targetPacket) is not pk.RecvDataPacket and    \
        type(_targetPacket) is not pk.RecvMsgPacket:
            TypeError("This type is not type of packret")

    recvPacketSerial = pb.RecvPacketSerial()

    #packet attributed
    packetSerial = makePacketSerial(_targetPacket)  

    recvPacketSerial.packet.packetType = packetSerial.packetType
    recvPacketSerial.packet.username = packetSerial.username
    recvPacketSerial.packet.IP = packetSerial.IP
    recvPacketSerial.packet.cmdNum = packetSerial.cmdNum
    recvPacketSerial.packet.sock = packetSerial.sock

    recvPacketSerial.recvPacketType = pc.RecvPacketTypeConverter.toInteger(_targetPacket.recvPacketType)

    return recvPacketSerial

#직렬화
def makePacketSerialToByte(_targetPacket):
    #기본 패킷 시리얼 생성
    packetSerial = makePacketSerial(_targetPacket)

    #타입에 따른 시리얼 문자열 생성
    #1. SendCmdPacket
    if type(_targetPacket) is pk.SendCmdPacket:
        returnSerial = pb.SendCmdPacketSerial()

        #데이터 입력
        returnSerial.packet.packetType = packetSerial.packetType
        returnSerial.packet.username = packetSerial.username
        returnSerial.packet.IP = packetSerial.IP
        returnSerial.packet.cmdNum = packetSerial.cmdNum
        returnSerial.packet.sock = packetSerial.sock

        for cmdStr in _targetPacket.cmdVec:
            returnSerial.cmdVector.append(cmdStr)
        
        #추출
        return returnSerial.SerializeToString()
    
    #2. RecvDataPacket
    elif type(_targetPacket) is pk.RecvDataPacket:
        returnSerial = pb.RecvDataPacketSerial()

        #데이터 입력
        returnSerial.recvPacket.packet.packetType = packetSerial.packetType
        returnSerial.recvPacket.packet.username = packetSerial.username
        returnSerial.recvPacket.packet.IP = packetSerial.IP
        returnSerial.recvPacket.packet.cmdNum = packetSerial.cmdNum
        returnSerial.recvPacket.packet.sock = packetSerial.sock

        #RecvType 입력
        returnSerial.recvPacket.recvPacketType = pc.RecvPacketTypeConverter.toInteger(_targetPacket.recvPacketType)

        #DataElement 입력
        returnSerial.data.data = str(_targetPacket.data.data)
        returnSerial.data.dataType = dc.DataTypeConverter.toInteger(_targetPacket.data.dataType)
        returnSerial.data.structType = dc.StructTypeConverter.toInteger(_targetPacket.data.structType)
        
        return returnSerial.SerializeToString()
    
    #3. RecvMsgPacket
    elif type(_targetPacket) is pk.RecvMsgPacket:
        returnSerial = pb.RecvMsgPacketSerial()

        #데이터 입력
        returnSerial.recvPacket.packet.packetType = packetSerial.packetType
        returnSerial.recvPacket.packet.username = packetSerial.username
        returnSerial.recvPacket.packet.IP = packetSerial.IP
        returnSerial.recvPacket.packet.cmdNum = packetSerial.cmdNum
        returnSerial.recvPacket.packet.sock = packetSerial.sock

        #RecvDataType 입력
        returnSerial.recvPacket.recvPacketType = pc.RecvPacketTypeConverter.toInteger(_targetPacket.recvPacketType)

        #Msg 입력
        returnSerial.msg = _targetPacket.msg
        return returnSerial.SerializeToString()
    
    #4 SignalPacket
    elif type(_targetPacket) is pk.SignalPacket:
        returnSerial = pb.SignalPacketSerial()

        #데이터 입력
        returnSerial.packet.packetType = packetSerial.packetType
        returnSerial.packet.username = packetSerial.username
        returnSerial.packet.IP = packetSerial.IP
        returnSerial.packet.cmdNum = packetSerial.cmdNum
        returnSerial.packet.sock = packetSerial.sock

        #signal 입력
        returnSerial.signal = pc.SignalTypeConverter.toInteger(_targetPacket.signal)

        return returnSerial.SerializeToString()
    
    #5 LogPacket
    #라이브러리에서 logpacket을 보낼 일은 없으므로
    #dataformat은 아무렇게나 작성
    elif type(_targetPacket) is pk.LogPacket:
        returnSerial = pb.LogPacketSerial()

        #데이터 입력
        returnSerial.packet.packetType = packetSerial.packetType
        returnSerial.packet.username = packetSerial.username
        returnSerial.packet.IP = packetSerial.IP
        returnSerial.packet.cmdNum = packetSerial.cmdNum
        returnSerial.packet.sock = packetSerial.sock

        #log 입력
        returnSerial.dateformat = "None"
        returnSerial.str = _targetPacket.logMsg
        return returnSerial.SerializeToString()
    else: TypeError("This type is not type of packret")

#나머지
# arg 1: 직렬화된 패킷, arg 2: 패킷 타입
def returnToPacket(_targetPacket, _type):
    #타입 판정
    if type(_targetPacket) is not bytes or type(_type) is not pk.PacketType:
        return TypeError("This type is not invalid")
    
    if _type is pk.PacketType.sendCmd: #SendCmdPacket

        returnSerial = pb.SendCmdPacketSerial()
        returnSerial.ParseFromString(_targetPacket)

        cmdVec = []
        for inputStr in returnSerial.cmdVector:
            cmdVec.append(inputStr)


        returnPacket = pk.SendCmdPacket(returnSerial.packet.username,   \
                                        returnSerial.packet.IP,         \
                                        returnSerial.packet.cmdNum,     \
                                        returnSerial.packet.sock,       \
                                        cmdVec)
        return returnPacket
    
    elif _type is pk.PacketType.recv: # RecvPacket
        #data인지 msg인지 다시 판별해야 함

        checkTypeSerial = pb.RecvDataPacketSerial()
        try: #에러나면 msg 그렇지 않으면 data
            print(_targetPacket)
            checkTypeSerial.ParseFromString(_targetPacket)

        except google.protobuf.message.DecodeError: #타입이 msg

            returnSerial = pb.RecvMsgPacketSerial()
            print(_targetPacket)
            returnSerial.ParseFromString(_targetPacket) #Msg로 재 파싱
            #text_format.Parse(_targetPacket, returnSerial)
            returnPacket = pk.RecvMsgPacket(                \
                returnSerial.recvPacket.packet.username,    \
                returnSerial.recvPacket.packet.IP,          \
                returnSerial.recvPacket.packet.cmdNum,      \
                returnSerial.recvPacket.packet.sock,        \
                str(returnSerial.msg)
            )

            return returnPacket

        
        else: #타입이 data

            data = checkTypeSerial.data
            datatype = dc.DataTypeConverter.toType(checkTypeSerial.data.dataType)
            structtype = dc.StructTypeConverter.toType(checkTypeSerial.data.structType)

            if datatype == de.DataType.DT_String:
                data = str(data)
            if datatype == de.DataType.DT_Number:
                data = int(data)
            elif datatype == de.DataType.DT_Float:
                data = float(data)

            element = de.DataElement(data, datatype, structtype)
            
            returnPacket = pk.RecvDataPacket(               \
                checkTypeSerial.recvPacket.packet.username, \
                checkTypeSerial.recvPacket.packet.IP,       \
                checkTypeSerial.recvPacket.packet.cmdNum,   \
                checkTypeSerial.recvPacket.packet.sock,     \
                element
            )

            return returnPacket
    
    elif _type is pk.PacketType.signal: #signal packet

        returnSerial = pb.SignalPacketSerial()
        returnSerial.ParseFromString(_targetPacket)

        returnPacket = pk.SignalPacket(             \
            returnSerial.packet.username,           \
            returnSerial.packet.IP,                 \
            returnSerial.packet.cmdNum,             \
            returnSerial.packet.sock,               \
            pc.SignalTypeConverter.toType(returnSerial.signal)
        )

        return returnPacket
    
    elif _type is pk.PacketType.log: #log

        returnSerial = pb.LogPacketSerial()
        returnSerial.ParseFromString(_targetPacket)

        returnPacket = pk.LogPacket(        \
            returnSerial.packet.username,   \
            returnSerial.packet.IP,         \
            returnSerial.packet.cmdNum,     \
            returnSerial.packet.sock,       \
            str(returnSerial.dateformat) + str(returnSerial.str)
        )
        return returnPacket
    else: raise TypeError("Invalid Packet Type")

