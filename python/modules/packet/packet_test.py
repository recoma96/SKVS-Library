from .Packet import *
from .PacketProtocol import *
from .PacketTypeConverter import *
from .structure.DataElement import *

def test():
    de = DataElement("DataElement", DataType.DT_String, StructType.ST_Element)

    sc = SendCmdPacket("user", "127.0.0.1", 0, 0, "hello world")
    rcd = RecvDataPacket("user", "127.0.0.1", 0, 0, de)
    rcm = RecvMsgPacket("user", "127.0.0.1", 0, 0,"hello msg world")
    ss = SignalPacket("user", "127.0.0.1", 0, 0, SignalType.shutdown)


    scStr = makePacketSerial(sc)
    rcdStr = makePacketSerial(rcd)
    rcmStr = makePacketSerial(rcm)
    ssStr = makePacketSerial(ss)

    print(scStr)
    print(rcdStr)
    print(rcmStr)
    print(ssStr)
    #return

    sc = returnToPacket(scStr)
    rcdStr = returnToPacket(rcdStr)
    rcmStr = returnToPacket(rcmStr)
    ssStr = returnToPacket(ssStr)

    #assert 0
