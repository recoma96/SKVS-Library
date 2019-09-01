package skvsclient;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;

import skvsclient.modules.packet.Packet;
import skvsclient.modules.packet.Packet.PacketType;
import skvsclient.modules.packet.Packet.RecvPacketType;
import skvsclient.modules.packet.PacketProtocol;
import skvsclient.modules.packet.TypeConverter.*;
import skvsclient.modules.packet.exception.ConvertException;
import skvsclient.modules.packet.exception.SocketSettingException;

public class SkvsConnectionRecvThread extends Thread {
	private SkvsConnection conn;
	
	public SkvsConnectionRecvThread(SkvsConnection _conn) throws NullPointerException, SocketSettingException {

		if(_conn == null)
			throw new NullPointerException("This Connection is Null");
		if(!_conn.checkConnected())
			throw new SocketSettingException("This connection is failed");
		conn = _conn;
	}
	
	@Override
	public void run() {
		

		while(conn.checkConnected()) {
			

			byte[] recvIntegerBuffer = new byte[4];

			
			try {
				conn.getInputStream().read(recvIntegerBuffer);
			} catch (Exception e) {
				conn.close();
				return;
			}
			
			int strSize = SkvsConnection.byteTointFromServer(recvIntegerBuffer);
			
			for(int i = 0; i < 4; i++)
				recvIntegerBuffer[i] = 0;
			
			try {
				conn.getInputStream().read(recvIntegerBuffer);
			} catch (IOException e) {
				conn.close();
				throw new NullPointerException("Connection defused from server");
			}
			
			int integerPacketType = SkvsConnection.byteTointFromServer(recvIntegerBuffer);
			ConvertException failedToPacketType = null; //��ŶŸ�� �����ÿ� �������� ��� ���
			
			PacketType packetType = null;
			try {
				packetType = PacketTypeConverter.toType(integerPacketType);
			} catch (ConvertException e) {
				failedToPacketType = e;
			}
			

			recvIntegerBuffer = null;
			
			byte[] strBuffer = new byte[strSize];
			

			try {
				conn.getInputStream().read(strBuffer);
			} catch (IOException e) {
				conn.close();
				throw new NullPointerException("Connection defused from server");
			}
			
			
			if(failedToPacketType != null) {
				strBuffer = null;
				//�ٽ� ����
				continue;
			}
			
			String packetStr = new String(strBuffer);
			

			Packet inputPacket = null;
			HashMap<String, String> strData = PacketProtocol.collectPacketDataFromString(packetStr);
			if(strData == null) {

				conn.close();
				throw new NullPointerException("Connection defused from server");
				
				
			}

			switch(packetType) {
			case SENDCMD:

				inputPacket = PacketProtocol.returnToSendCmdPacket(strData);

			break;
			case RECV:
				if(PacketProtocol.checkRecvType(strData) == RecvPacketType.DATA)
					inputPacket = PacketProtocol.returnToRecvDataPacket(strData);
				else if(PacketProtocol.checkRecvType(strData) == RecvPacketType.MSG)
					inputPacket = PacketProtocol.returnToRecvMsgPacket(strData);
				else inputPacket = null;
			break;
			case SIGNAL:
				inputPacket = PacketProtocol.returnToSignalPacket(strData);
			break;
			default:
				inputPacket = null;
				
			break;
			}
			
			
			if(inputPacket == null) {
				conn.close();
				throw new NullPointerException("Connection defused from server");
			}
			
			conn.pushInPacketQueue(inputPacket);
			
			continue;
		}
		
		
	}
}
