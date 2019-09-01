package skvsclient.modules.packet;

public class RecvMsgPacket extends RecvPacket {

	private String msg;
	
	public RecvMsgPacket(String _username, String _ip, int _cmdNum, int _sock, String _msg) {
		super(_username, _ip, _cmdNum, _sock, RecvPacketType.MSG);
		
		msg = _msg;
		
	}
	
	public String getMsg() { return msg; }

	
}
