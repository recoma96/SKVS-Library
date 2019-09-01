package skvsclient.modules.packet;

public class RecvPacket extends Packet {
	
	RecvPacketType recvPacketType;
	
	protected RecvPacket(String _username, String _ip, int _cmdNum, int _sock, RecvPacketType _type) {
		super(PacketType.RECV, _username, _ip, _cmdNum, _sock);
		// TODO Auto-generated constructor stub
		
		recvPacketType = _type;
	}
	
	public RecvPacketType getRecvType() {  return recvPacketType; }

}
