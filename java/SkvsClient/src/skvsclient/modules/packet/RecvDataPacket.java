package skvsclient.modules.packet;

import skvsclient.modules.packet.dataelement.DataElement;

public class RecvDataPacket extends RecvPacket {
	
	private DataElement data;
	
	public RecvDataPacket(String _username, String _ip, int _cmdNum, int _sock, DataElement _ele ) {
		super(_username, _ip, _cmdNum, _sock, RecvPacketType.DATA);
		// TODO Auto-generated constructor stub
		
		data = _ele;
		
	}
	
	public DataElement getData() { return data; }

}
