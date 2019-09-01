package skvsclient.modules.packet;

import skvsclient.modules.packet.Packet.*;
import skvsclient.modules.packet.exception.*;

public class TypeConverter {
	
	//1.packetType
	public static class PacketTypeConverter {
		public static int toInteger(PacketType _type) {
			
			switch(_type) {
			case SENDCMD: return 0;
			case RECV: return 1;
			case SIGNAL: return 2;
			case LOG: return 3;
			}
			return -1;
		}
		public static PacketType toType(int _num)  throws ConvertException {
			switch(_num) {
			case 0: return PacketType.SENDCMD;
			case 1: return PacketType.RECV;
			case 2: return PacketType.SIGNAL;
			case 3: return PacketType.LOG;
			default:
				throw new ConvertException("This number is not packet type");
			}
		}
	}
	
	//2.Recv type
	public static class RecvTypeConverter {
		
		public static int toInteger(RecvPacketType _type ) {
			switch(_type) {
			case DATA: return 0;
			case MSG: return 1;
			}
			return -1;
		}
		
		public static RecvPacketType toType(int _num) throws ConvertException {
			switch(_num) {
			case 0: return RecvPacketType.DATA;
			case 1: return RecvPacketType.MSG;
			default:
				throw new ConvertException("This number is not recv packet type");
			}
		}
	}
	
	//3.Signal
	public static class SignalTypeConverter {
		
		public static int toInteger(SignalType _type) {
			switch(_type) {
			case SHUTDOWN : return 0;
			case RECVSTART: return 1;
			case RECVEND: return 2;
			case ERROR: return 3;
			}
			return -1;
		}
		public static SignalType toType(int _num) throws ConvertException {
			switch(_num) {
			case 0: return SignalType.SHUTDOWN;
			case 1: return SignalType.RECVSTART;
			case 2: return SignalType.RECVEND;
			case 3: return SignalType.ERROR;
			default:
				throw new ConvertException("This number is not signal type");
			}
		}
	}

}
