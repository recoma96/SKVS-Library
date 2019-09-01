package skvsclient.modules.packet;

import skvsclient.modules.packet.TypeConverter.*;
import skvsclient.modules.packet.dataelement.DataElement;
import skvsclient.modules.packet.dataelement.DataElement.*;
import skvsclient.modules.packet.dataelement.TypeConverter.*;
import skvsclient.modules.packet.exception.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.StringTokenizer;

import skvsclient.modules.packet.*;
import skvsclient.modules.packet.Packet.*;

public class PacketProtocol {
	
	public static String makePacketSerial(Packet _packet) {
		
		String resultStr = new String();
				
		
		resultStr = "pt\t"+ Integer.toString(PacketTypeConverter.toInteger(_packet.getPacketType())) +"\n";
		resultStr += "un\t" + _packet.getUsername() + "\n";
		resultStr += "ip\t" + _packet.getIP() + "\n";
		resultStr += "cn\t" + Integer.toString(_packet.getCmdNum()) + "\n";
		resultStr += "sk\t" + Integer.toString(_packet.getSock()) + "\n";
		
		switch(_packet.getPacketType()) {
			
			//SendCmd
			case SENDCMD:
			{
				SendCmdPacket changePacket = (SendCmdPacket)_packet;
				ArrayList<String> exportedList = changePacket.getCmdList();
				
				resultStr += "cv\t";
				
				for(int i = 0; i < exportedList.size(); i++) {
					resultStr += exportedList.get(i);
					if(i < exportedList.size()-1)
						resultStr += " ";
				}
			}
			break;
			case RECV: //RecvDataPacket
			{
				RecvPacket changeRecvPacket = (RecvPacket)_packet;
				resultStr += "rt\t"+Integer.toString(RecvTypeConverter.toInteger(changeRecvPacket.getRecvType())) +"\n";
				
				//RecvDataPacket
				if(changeRecvPacket.getRecvType() == RecvPacketType.DATA) {
					RecvDataPacket changeDataPacket = (RecvDataPacket)_packet;
					resultStr += "ded\t"+changeDataPacket.getData().getData()+"\n";
					resultStr += "dedt\t"+Integer.toString(DataTypeConverter.toInteger(changeDataPacket.getData().getDataType()))+"\n";
					resultStr += "dest\t"+Integer.toString(StructTypeConverter.toInteger(changeDataPacket.getData().getStructType()));
				} else { //RecvMsgPacket
					
					resultStr += "msg\t"+((RecvMsgPacket)_packet).getMsg();
				}
			}
			break;
			case SIGNAL: //SignalPacket
				resultStr += "sg\t"+Integer.toString(SignalTypeConverter.toInteger(((SignalPacket)_packet).getSignal()));
			break;
			default: 
				return null;
		}
		return resultStr;
	}
	

	public static HashMap<String, String> collectPacketDataFromString(String _str) {
		StringTokenizer tokenizer = new StringTokenizer(_str, "\n");
		
		HashMap<String, String> tokenedMap = new HashMap<>();
		
		while(tokenizer.hasMoreElements()) {

			StringTokenizer tok2 = new StringTokenizer(tokenizer.nextToken(), "\t");
			if(tok2.countTokens() != 2 )
				return null;

			String key = tok2.nextToken();
			String value = tok2.nextToken();
			tokenedMap.put(key, value);
			
		}
		
		return tokenedMap;
	}
	

	public static RecvPacketType checkRecvType(HashMap<String, String> collectedData) {
		try {
			return RecvTypeConverter.toType(Integer.parseInt(collectedData.get("rt")));
		} catch (Exception e) {
			return null;
		}
	}
	


	
	//1. SendCmdPacket
	public static SendCmdPacket returnToSendCmdPacket(HashMap<String, String> collectedData) {
		
		
		if(collectedData == null) return null;
		

		PacketType packetType;
		String userName = new String();
		String ip = new String();
		int cmdNum = 0;
		int sock = 0;
		String cmd = new String();
		
		try {
			

			packetType = PacketTypeConverter.toType(Integer.parseInt(collectedData.get("pt")));
			userName = collectedData.get("un");
			ip = collectedData.get("ip");
			cmdNum = Integer.parseInt(collectedData.get("cn"));
			sock = Integer.parseInt(collectedData.get("sk"));
			cmd = collectedData.get("cv");
			
		} catch (Exception e) {
			return null;
		}
		

		SendCmdPacket returnPacket = null;
		try {
			returnPacket = new SendCmdPacket(
				userName, ip, cmdNum, sock, cmd
			);
		} catch (Exception e) {
			return null;
		}
		
		
		return returnPacket;
	}
	
	public static RecvDataPacket returnToRecvDataPacket(HashMap<String, String> collectedData) {
		if(collectedData == null) return null; //���н� null ��ȯ
		
		PacketType packetType;
		String userName = new String();
		String ip = new String();
		int cmdNum = 0;
		int sock = 0;
		DataElement ele = null;
		
		RecvDataPacket returnPacket = null;
		
		try {
			packetType = PacketTypeConverter.toType(Integer.parseInt(collectedData.get("pt")));
			userName = collectedData.get("un");
			ip = collectedData.get("ip");
			cmdNum = Integer.parseInt(collectedData.get("cn"));
			sock = Integer.parseInt(collectedData.get("sk"));
			
			String data = collectedData.get("ded");
			DataType dataType = DataTypeConverter.toType(Integer.parseInt(collectedData.get("dedt")));
			StructType structType = StructTypeConverter.toType(Integer.parseInt(collectedData.get("dest")));
			
			ele = new DataElement(data, dataType, structType);
		} catch(Exception e) {
			return null;
		}
		

		try {
			returnPacket = new RecvDataPacket(
					userName, ip, cmdNum, sock, ele
					);
		} catch(Exception e) {
			return null;
		}
		
		return returnPacket;
		
	}
	
	//RecvMsgPacket
	public static RecvMsgPacket returnToRecvMsgPacket(HashMap<String, String> collectedData) {
		
		if(collectedData == null) return null;
		
		PacketType packetType;
		String userName = new String();
		String ip = new String();
		int cmdNum = 0;
		int sock = 0;
		String msg = new String();
		
		try {

			packetType = PacketTypeConverter.toType(Integer.parseInt(collectedData.get("pt")));
			userName = collectedData.get("un");
			ip = collectedData.get("ip");
			cmdNum = Integer.parseInt(collectedData.get("cn"));
			sock = Integer.parseInt(collectedData.get("sk"));
			msg = collectedData.get("msg");
			
		} catch (Exception e) {
			return null;
		}
		

		RecvMsgPacket returnPacket = null;
		try {
			returnPacket = new RecvMsgPacket(
				userName, ip, cmdNum, sock, msg
			);
		} catch(Exception e) {
			return null;
		}
		
		return returnPacket;
	}
	
	public static SignalPacket returnToSignalPacket(HashMap<String, String> collectedData) {
		
		if(collectedData == null) return null;
		
		PacketType packetType;
		String userName = new String();
		String ip = new String();
		int cmdNum = 0;
		int sock = 0;
		SignalType sig;
		
		
		try {

			packetType = PacketTypeConverter.toType(Integer.parseInt(collectedData.get("pt")));
			userName = collectedData.get("un");
			ip = collectedData.get("ip");
			cmdNum = Integer.parseInt(collectedData.get("cn"));
			sock = Integer.parseInt(collectedData.get("sk"));
			sig = SignalTypeConverter.toType(Integer.parseInt(collectedData.get("sg")));
		} catch(Exception e) {
			return null;
		}
		
		SignalPacket returnPacket = null;
		try {
			returnPacket = new SignalPacket(
					userName, ip, cmdNum, sock, sig
			);
		} catch(Exception e) {
			return null;
		}
		
		return returnPacket;
	}
	
}
