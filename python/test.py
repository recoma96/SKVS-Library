from SkvsClient.SkvsConnection import *
from SkvsClient.SkvsCommand import *
from SkvsClient.SkvsLibException import *
from time import *
from SkvsClient.modules.packet.Packet import *
from SkvsClient.modules.packet.PacketSerial import *
from SkvsClient.modules.packet.PacketTypeConverter import *


a = SkvsConnection("user", "12345678", "127.0.0.1", 13403)

a.open()

commander = SkvsCommand(a, "insert")
try:
    commander.executeNonQuery()
except SkvsLibException as e:
    print(e)