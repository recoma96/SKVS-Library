package skvsclient.modules.packet;

public class Packet {
	
	//packet Type
	public enum PacketType {
		SENDCMD, RECV, SIGNAL, LOG
	}
	public enum RecvPacketType {
		DATA, MSG
	}
	public enum SignalType {
		SHUTDOWN, RECVSTART, RECVEND, ERROR
	}
	

	private PacketType packetType;
	private String username;
	private String IP;
	private int cmdNum;
	private int sock;
	
	protected Packet(PacketType _pType, String _username, String _ip, int _cmdNum, int _sock) {
		packetType = _pType; username = _username; IP = _ip; cmdNum = _cmdNum; sock = _sock;
	}
	
	public PacketType getPacketType() { return packetType; }
	public String getUsername() { return username; }
	public String getIP() { return IP; }
	public int getCmdNum() { return cmdNum; }
	public int getSock() { return sock; }
}
