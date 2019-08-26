import enum
import modules.packet.Packet as pk
import modules.structure.DataElementTypeConverter as dc
import modules.structure.DataElement as de
import modules.packet.PacketTypeConverter as pc

data = pk.SignalPacket("user", "127.0.0.1", 1, 1, pk.SignalType.shutdown)
