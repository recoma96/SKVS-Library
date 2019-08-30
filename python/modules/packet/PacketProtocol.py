from .Packet import *
from .PacketTypeConverter import *
from .structure.DataElement import *
from .structure.DataElementTypeConverter import *

import sys
import os



#직렬화
def makePacketSerial(_packet):
    
    #상위객체 확
    if type(_packet).mro()[1] is Packet or \
        type(_packet).mro()[2] is Packet: #recv계열은 부모에 부모객체가 Packet

        returnMsg = "pt\t"+str(PacketTypeConverter.toInteger(_packet.packetType))+"\n"
        returnMsg += "un\t"+_packet.username+"\n"
        returnMsg += "ip\t"+_packet.ip+"\n"
        returnMsg += "cn\t"+str(_packet.cmdNum)+"\n"
        returnMsg += "sk\t"+str(_packet.sock)+"\n"

        if type(_packet) is SendCmdPacket:
            returnMsg += "cv\t"
            for strTok in _packet.cmdVec:
                returnMsg += strTok + ' '
            returnMsg = returnMsg[0:-1]
        
        elif type(_packet) is RecvDataPacket:
            returnMsg += "rt\t"+str(RecvPacketTypeConverter.toInteger(_packet.recvPacketType))+"\n"
            returnMsg += "ded\t"+_packet.data.data+"\n"
            returnMsg += "dedt\t"+str(DataTypeConverter.toInteger(_packet.data.dataType))+"\n"
            returnMsg += "dest\t"+str(StructTypeConverter.toInteger(_packet.data.structType))
        
        elif type(_packet) is RecvMsgPacket:
            returnMsg += "rt\t"+str(RecvPacketTypeConverter.toInteger(_packet.recvPacketType))+"\n"
            returnMsg += "msg\t"+_packet.msg
        
        elif type(_packet) is SignalPacket:
            returnMsg += "sg\t"+str(SignalTypeConverter.toInteger(_packet.signal))

        elif type(_paciet) is LogPacket:
            raise TypeError("LogPacket is not used")


        return returnMsg
    else:
        raise TypeError("This type is not packet type")

def returnToPacket(_str):
    if type(_str) is not str:
        raise TypeError("This Serial is not str")
    
    strList = _str.split('\n')

    strMap = {} #해시맵으로 다시 필터링

    for strAtom in strList:
        tokedList = strAtom.split('\t')
        if len(tokedList) != 2:
            raise ValueError("This string is not matched about values")
        strMap[tokedList[0]] = tokedList[1]
    
    #키/값 검토 및 추출 (공통)
    #자료형이 맞지 않을 경우 ValueError 호출
    #해당 키가 없는 경우 KeyError 호출
    #타입을 컨버팅 하는 데 오류가 생길 경우 ValueError 호출

    packetType = PacketTypeConverter.toType(int(strMap['pt']))
    username = strMap['un']
    ip = strMap['ip']
    cmdNum = int(strMap['cn'])
    sock = int(strMap['sk'])

    #CmdPacket
    if packetType is PacketType.sendCmd:
        cmdStr = strMap['cv']
        #패킷 생성
        returnPacket = SendCmdPacket(   \
            username,                   \
            ip,                         \
            cmdNum,                     \
            sock,                       \
            cmdStr                      \
        )
    #recvPacket
    elif packetType is PacketType.recv: 
        recvPacketType = RecvPacketTypeConverter.toType(int(strMap['rt']))
        #recvDataPacket
        if recvPacketType is RecvPacketType.data:
            
            
            #eleData = strMap['ded']
            eleDataType = DataTypeConverter.toType(int(strMap['dedt']))
            eleStructType = StructTypeConverter.toType(int(strMap['dest']))

            if eleDataType is DataType.DT_String:
                eleData = strMap['ded']
            elif eleDataType is DataType.DT_Number:
                eleData = int(strMap['ded'])
            else:
                eleData = float(strMap['ded'])

            #DataElement 생성
            returnElement = DataElement(eleData, eleDataType, eleStructType)

            #패킷 생성
            returnPacket = RecvDataPacket(  \
                username,                   \
                ip,                         \
                cmdNum,                     \
                sock,                       \
                returnElement               \
            )

        else: #msgPacket
            msg = strMap['msg']
            
            #패킷 생성
            returnPacket = RecvMsgPacket(   \
                username,                   \
                ip,                         \
                cmdNum,                     \
                sock,                       \
                msg                         \
            )

    #signalPacket
    elif packetType is PacketType.signal:
        signal = SignalTypeConverter.toType(int(strMap['sg']))
        #패킷 생성
        returnPacket = SignalPacket(    \
            username,                   \
            ip,                         \
            cmdNum,                     \
            sock,                       \
            signal                      \
        )
    else:
        TypeError("LogPacket is not used")

    return returnPacket
    
