import enum
import modules.packet.Packet as pk
import modules.structure.DataElementTypeConverter as dc
import modules.structure.DataElement as de
import modules.packet.PacketTypeConverter as pc
import modules.packet.PacketSerial as ps

data = pk.SignalPacket("user", "127.0.0.1", 1, 1, pk.SignalType.shutdown)

d = de.DataElement(123, de.DataType.DT_Number, de.StructType.ST_Element)

print(ps.makeDataElementSerial(d))

p = pk.RecvMsgPacket("user", "127.0.0.1", 1, 1, "msh")
print(ps.makeRecvPacketSerial(p))