from . import Packet as pk
from . import PacketTypeConverter as pc
from . import PacketSerial_pb2 as pb

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
            TypeError("This type is not type of packret")
    
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
