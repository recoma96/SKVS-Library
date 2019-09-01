package skvsclient;

import java.util.ArrayList;
import java.util.HashMap;

import skvsclient.modules.packet.*;
import skvsclient.modules.packet.Packet.PacketType;
import skvsclient.modules.packet.Packet.RecvPacketType;
import skvsclient.modules.packet.dataelement.TypePrinter;
import skvsclient.modules.packet.exception.CommandFailedException;
import skvsclient.modules.packet.exception.PacketErrorException;
import skvsclient.modules.packet.exception.SizeZeroException;
import skvsclient.modules.packet.exception.SocketSettingException;


public class SkvsCommand {
	private SkvsConnection conn;
	public String cmd;
	
	public SkvsCommand(SkvsConnection _conn, String _cmd) throws NullPointerException {
		if( _conn == null)
			throw new NullPointerException("Connection  is null");
		
		conn = _conn;
		cmd = _cmd;
	}
	
	public SkvsCommand(SkvsConnection _conn) throws NullPointerException {
		if( _conn == null)
			throw new NullPointerException("Connection  is null");
		
		conn = _conn;

	}
	
	
	public void executeNonQuery() throws NullPointerException, SizeZeroException, SocketSettingException, PacketErrorException, CommandFailedException {
		
		if( conn == null)
			throw new NullPointerException("Connection  is null");
		if( cmd == null)
			throw new NullPointerException("Connection  is null");
		if( cmd.isEmpty())
			throw new SizeZeroException("Connection  is null");
		
		int cmdNum = conn.setCmdSerial();
		
		//SendCmdPacket
		SendCmdPacket sendPacket = new SendCmdPacket(
			conn.getID(), conn.getIP(), cmdNum, 0, cmd
		);
		
		//SendCmd
		String sendStr = PacketProtocol.makePacketSerial(sendPacket);
		int sendSize = sendStr.length();
		
		conn.lockSocket();
		
		try {
			conn.getOutputStream().write(SkvsConnection.intToByteArray(sendSize));
		} catch(Exception e) {
			conn.unlockSocket();
			conn.removeCmdSerial(cmdNum);
			conn.close();
			throw new SocketSettingException("Connection defused.");
		}
		
		try {
			Integer sendTypeInt = TypeConverter.PacketTypeConverter.toInteger(PacketType.SENDCMD);
			conn.getOutputStream().write(SkvsConnection.intToByteArray(sendTypeInt.intValue()));
		} catch(Exception e) {
			conn.unlockSocket();
			conn.removeCmdSerial(cmdNum);
			conn.close();
			throw new SocketSettingException("Connection defused.");
		}
		
		try {
			conn.getOutputStream().write(sendStr.getBytes());

		} catch(Exception e) {
			conn.unlockSocket();
			conn.removeCmdSerial(cmdNum);
			conn.close();
			throw new SocketSettingException("Connection defused.");
		}
		
		conn.unlockSocket();
		

		int clockCounter = 0;
		Packet recvPacket = null;
		String errorMsg = new String();
		
		while(clockCounter < 10000) {

			
			if(!conn.isPacketQueueEmpty()) {
				recvPacket = conn.popFromPacketQueue(cmdNum);
				if(recvPacket != null) {
					clockCounter = 0;

					
					switch(recvPacket.getPacketType()) {
					case RECV:
					{
						RecvPacket rePacket = (RecvPacket)recvPacket;
						if(rePacket.getRecvType() == RecvPacketType.DATA) {
							continue;
						} else {

							errorMsg = ((RecvMsgPacket)rePacket).getMsg();
							continue;	
						}
					}
					case SIGNAL:
					{
						SignalPacket sigPacket = (SignalPacket)recvPacket;
						switch(sigPacket.getSignal()) {
						case RECVEND:
							conn.removeCmdSerial(cmdNum);
							return;
						case RECVSTART:
							continue;
						case ERROR:
							conn.removeCmdSerial(cmdNum);
							if(errorMsg.isEmpty())
								throw new CommandFailedException("unknown failed command");
							else
								throw new CommandFailedException(errorMsg);
						case SHUTDOWN:
							conn.removeCmdSerial(cmdNum);
							conn.close();
							return;
						
						}
					}
					break;
					default:
						conn.removeCmdSerial(cmdNum);
						throw new PacketErrorException("Uknown Packet From Server");
					}
					
				} else {
					try {
						Thread.sleep(1);
					} catch (InterruptedException e) {
						
					}
					clockCounter++;
				}
					
			} else {
			
				try {
					Thread.sleep(1);
				} catch (InterruptedException e) {
				
				}
				clockCounter++;
			}
			
		}

		conn.close();
		conn.removeCmdSerial(cmdNum);
		throw new SocketSettingException("No Response From Server");
	}


	public SkvsReadStream executeReadStream() throws NullPointerException, SizeZeroException, SocketSettingException, PacketErrorException, CommandFailedException {
	
		if( conn == null)
			throw new NullPointerException("Connection  is null");
		if( cmd == null)
			throw new NullPointerException("Connection  is null");
		if( cmd.isEmpty())
			throw new SizeZeroException("Connection  is null");
	
		int cmdNum = conn.setCmdSerial();
	
		SendCmdPacket sendPacket = new SendCmdPacket(
			conn.getID(), conn.getIP(), cmdNum, 0, cmd
		);
	
		String sendStr = PacketProtocol.makePacketSerial(sendPacket);
		int sendSize = sendStr.length();
	
		conn.lockSocket();
		try {
			conn.getOutputStream().write(SkvsConnection.intToByteArray(sendSize));
		} catch(Exception e) {
			conn.unlockSocket();
			conn.removeCmdSerial(cmdNum);
			conn.close();
			throw new SocketSettingException("Connection defused.");
		}
	
		try {
			Integer sendTypeInt = TypeConverter.PacketTypeConverter.toInteger(PacketType.SENDCMD);
			conn.getOutputStream().write(SkvsConnection.intToByteArray(sendTypeInt.intValue()));
		} catch(Exception e) {
			conn.unlockSocket();
			conn.removeCmdSerial(cmdNum);
			conn.close();
			throw new SocketSettingException("Connection defused.");
		}
	
		try {
			conn.getOutputStream().write(sendStr.getBytes());
		} catch(Exception e) {
			
			conn.unlockSocket();
			conn.removeCmdSerial(cmdNum);
			conn.close();
	
			throw new SocketSettingException("Connection defused.");
		}
		conn.unlockSocket();

		int clockCounter = 0;
		Packet packet = null;
		String errorMsg = new String();
	
		ArrayList<HashMap<String, String>> container = new ArrayList<>();
	
		while(clockCounter < 10000) {

		
			if(!conn.isPacketQueueEmpty()) {
				packet = conn.popFromPacketQueue(cmdNum);
				if(packet != null) {
					clockCounter = 0;
				
					switch(packet.getPacketType()) {
					case RECV:
					{
						RecvPacket rePacket = (RecvPacket)packet;
						if(rePacket.getRecvType() == RecvPacketType.DATA) {
							RecvDataPacket dataPacket = (RecvDataPacket)rePacket;
						
							HashMap<String, String> dataMap = new HashMap<>();
							dataMap.put("data", dataPacket.getData().getData());
							dataMap.put("datatype", TypePrinter.aboutDataType(dataPacket.getData().getDataType()));
							dataMap.put("structtype", TypePrinter.aboutStructType(dataPacket.getData().getStructType()));
							
							container.add(dataMap);
							continue;
							
						} else {
							errorMsg = ((RecvMsgPacket)rePacket).getMsg();
							continue;	
						}
					}
					case SIGNAL:
					{
						SignalPacket sigPacket = (SignalPacket)packet;
						switch(sigPacket.getSignal()) {
						case RECVEND:
							conn.removeCmdSerial(cmdNum);
							return new SkvsReadStream(container);
						case RECVSTART:
							continue;
						case ERROR:
							if(errorMsg.isEmpty())
								throw new CommandFailedException("unknown failed command");
							else
								throw new CommandFailedException(errorMsg);
						case SHUTDOWN:
							conn.close();
							return null;
					
						}
					}
					break;
					default:
						conn.removeCmdSerial(cmdNum);
						throw new PacketErrorException("Uknown Packet From Server");
					}
				
				} else {
					try {
						Thread.sleep(1);
					} catch (InterruptedException e) {
					
					}
					clockCounter++;
				}
				
			} else {
		
				try {
					Thread.sleep(1);
				} catch (InterruptedException e) {
			
				}
				clockCounter++;
			}
		
		}
		conn.close();
		throw new SocketSettingException("No Response From Server");
	}
}