from . import Packet as pk

class PacketTypeConverter:
    def toType(_integer):
        if type(_integer) != int:
            raise TypeError("This Value is Not integer")
        if _integer == 0: return pk.PacketType.sendCmd
        elif _integer == 1: return pk.PacketType.recv
        elif _integer == 2: return pk.PacketType.signal
        elif _integer == 3: return pk.PacketType.log
        else: raise ValueError("This integer is out of range")
    
    def toInteger(_type):
        if type(_type) != pk.PacketType:
            raise TypeError("This Value is not PacketType")
        if _type is pk.PacketType.sendCmd: return 0
        elif _type is pk.PacketType.recv: return 1
        elif _type is pk.PacketType.signal: return 2
        elif _type is pk.PacketType.log: return 3
        else: raise ValueError("This Type is out of range")


class RecvPacketTypeConverter:
    def toType(_integer):
        if type(_integer) != int:
            raise TypeError("This Value is Not integer")
        if _integer == 0: return pk.RecvPacketType.data
        elif _integer == 1: return pk.RecvPacketType.msg
        else: raise ValueError("This integer is out of range")

    def toInteger(_type):
        if type(_type) != pk.RecvPacketType:
            raise TypeError("This Value is not RecvPacketType")
        if _type is pk.RecvPacketType.data: return 0
        elif _type is pk.RecvPacketType.msg: return 1
        else: raise ValueError("This Type is out of range")


class SignalTypeConverter:
    def toType(_integer):
        if type(_integer) != int:
            raise TypeError("This Value is Not integer")
        if _integer == 0: return pk.SignalType.shutdown
        elif _integer == 1: return pk.SignalType.recvStart
        elif _integer == 2: return  pk.SignalType.recvEnd
        elif _integer == 3: return pk.SignalType.error
        else: raise ValueError("This Type is out of range")

    def toInteger(_type):
        if type(_type) != pk.SignalType:
            raise TypeError("This Value is not SignalType")
        if _type is pk.SignalType.shutdown: return 0
        elif _type is pk.SignalType.recvStart: return 1
        elif _type is pk.SignalType.recvEnd: return 2
        elif _type is pk.SignalType.error: return 3
        else: raise ValueError("This Type is out of range")