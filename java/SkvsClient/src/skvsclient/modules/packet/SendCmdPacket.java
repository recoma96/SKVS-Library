package skvsclient.modules.packet;

import java.util.ArrayList;
import java.util.StringTokenizer;

import skvsclient.modules.packet.exception.SizeZeroException;

public class SendCmdPacket extends Packet {
	
	private ArrayList<String> cmdTokenedList;

	public SendCmdPacket(String _username, String _ip, int _cmdNum, int _sock, String _cmd) 
				throws SizeZeroException {
		super(PacketType.SENDCMD, _username, _ip, _cmdNum, _sock);
		// TODO Auto-generated constructor stub
		
		if(_cmd.length() == 0)
			throw new SizeZeroException("This Command size is zero");
		

		StringTokenizer tokenizer = new StringTokenizer(_cmd);
		
		cmdTokenedList = new ArrayList<String>();
		while(tokenizer.hasMoreTokens()) {
			String tok = tokenizer.nextToken();
			this.cmdTokenedList.add(tok);
		}
	}
	

	public SendCmdPacket(String _username, String _ip, int _cmdNum, int _sock, ArrayList<String> _cmdTokened) 
		throws SizeZeroException {
			super(PacketType.SENDCMD, _username, _ip, _cmdNum, _sock);
			
			if(_cmdTokened.isEmpty() )
				throw new SizeZeroException("This Cmd List is Empty");
			
			this.cmdTokenedList = _cmdTokened;
	}

	public ArrayList<String> getCmdList() { return cmdTokenedList; }
	

}
