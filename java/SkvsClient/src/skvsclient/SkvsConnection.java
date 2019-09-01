package skvsclient;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Deque;
import java.util.LinkedList;
import java.util.Queue;

import skvsclient.modules.packet.Packet;
import skvsclient.modules.packet.Packet.PacketType;
import skvsclient.modules.packet.PacketProtocol;
import skvsclient.modules.packet.SendCmdPacket;
import skvsclient.modules.packet.TypeConverter;
import skvsclient.modules.packet.exception.LoginFailedException;
import skvsclient.modules.packet.exception.SizeZeroException;
import skvsclient.modules.packet.exception.SocketSettingException;

public class SkvsConnection {
	
	private String id;
	private String pswd;
	private String connectIP;
	private int port;
	private Socket connectSocket;
	private boolean isConnected;
	
	private boolean socketMutex;
	

	private ArrayList<Integer> cmdList;
	private Queue<Packet> packetQueue;
	

	public String getID() { return id; }
	public String getPswd() { return pswd; }
	public String getIP() { return connectIP; }
	public int getPort() { return port; }
	protected Socket useSocket() { return connectSocket; }
	protected OutputStream getOutputStream() throws IOException { return connectSocket.getOutputStream(); }
	protected InputStream getInputStream() throws IOException { return connectSocket.getInputStream(); }
	protected boolean checkConnected() { return isConnected; }
	
	protected void lockSocket() {
		

		while(!socketMutex) { }
		socketMutex = false;
	}
	
	protected void unlockSocket() {
		socketMutex = true;
	}
	

	protected boolean isPacketQueueEmpty() { return packetQueue.isEmpty(); }
	
	protected synchronized void pushInPacketQueue(Packet _packet) { 
		packetQueue.offer(_packet);
	}
	

	protected synchronized Packet popFromPacketQueue(int _cmdNum) {
		
		lockSocket();
		if( _cmdNum == packetQueue.peek().getCmdNum()) {
			unlockSocket();
			return packetQueue.poll();
		}
		else {
			unlockSocket();
			return null;
		}
	}
	
	//byte->integer
	static protected int byteTointFromServer(byte[] arr){
		return (arr[3] & 0xff)<<24 | (arr[2] & 0xff)<<16 | (arr[1] & 0xff)<<8 | (arr[0] & 0xff); 
	}
	
	//integer->byte
	static protected  byte[] intToByteArray(int value) {
		byte[] byteArray = new byte[4];
		byteArray[0] = (byte)(value >> 24);
		byteArray[1] = (byte)(value >> 16);
		byteArray[2] = (byte)(value >> 8);
		byteArray[3] = (byte)(value);
		return byteArray;
	}




	protected synchronized int setCmdSerial() {

		if(cmdList.isEmpty()) {
			cmdList.add(0);
			return 0;
		}
		int counter = 0;

		for(Integer cmdNum : cmdList) {
			if(counter <= cmdNum.intValue() )
				counter = cmdNum.intValue()+1;
		}
		cmdList.add(counter);
		return counter;
	}
	

	public synchronized void removeCmdSerial(int _delNum) {

		for(Integer cmdNum : cmdList) {
			if(cmdNum.intValue() == _delNum) {
				cmdList.remove(cmdNum);
				
				return;
			}
		}
		return;
	}
	
	public SkvsConnection(String _id, String _pswd, String _connectIP, int _port) {
		
		id = _id; pswd = _pswd; connectIP = _connectIP; port = _port;
		isConnected = false;
		connectSocket = null;
		packetQueue = new LinkedList<>();
		socketMutex = true;
		
		
	}
	
	public void open() throws SocketSettingException, UnknownHostException, IOException, LoginFailedException {

		connectSocket = new Socket(connectIP, port);
		cmdList = new ArrayList<>();
		
		
		

		String sendLoginMsg = id + "-" +pswd;
		OutputStream outputStream = null;
		InputStream inputStream = null;
		
		try {
			outputStream = connectSocket.getOutputStream();
		} catch(Exception e) {
			connectSocket.close();
			throw e;
		}
		
		try {
			inputStream = connectSocket.getInputStream();
		} catch(Exception e) {
			connectSocket.close();
			throw e;
		}
		

		try {
			outputStream.write(sendLoginMsg.getBytes());
		} catch( Exception e) {
			connectSocket.close();
			throw e;
		}
		

		byte[] loginBuffer = new byte[1];
		boolean isLogined = false;
		
		
		try {
			inputStream.read(loginBuffer);
		} catch(Exception e) {
			connectSocket.close();
			throw e;
		}
		
		//integer
		int i = loginBuffer[0] & 0xFF;
		if(i == 1) isLogined = true;
		loginBuffer = null;
		
		if(!isLogined)
			throw new LoginFailedException("Login Failed");
		
		

		byte[] userLevelBuffer = new byte[4];
		inputStream.read(userLevelBuffer);
		

		isConnected = true;
		

		SkvsConnectionRecvThread recvThread = new SkvsConnectionRecvThread(this);
		recvThread.start();
	
	}
	
	public void close() {
		

		if(isConnected == false) {
			try {
				connectSocket.close();
			} catch (IOException e1) {
				return;
			}
			return;
		}
		

		int serialNum = setCmdSerial();
		

		SendCmdPacket closePacket = null;
		try {
			closePacket = new SendCmdPacket(id, connectIP, serialNum, serialNum, "quit");
		} catch (SizeZeroException e) {
			
			return;
		}
		

		String closeStr = PacketProtocol.makePacketSerial(closePacket);
		Integer strSize = closeStr.length();
		

		OutputStream outputStream = null;
		try {
			outputStream = connectSocket.getOutputStream();
		} catch (IOException e) {

			isConnected = false;
			try {
				connectSocket.close();
			} catch (IOException e1) {
				return;
			}
			return;
		}

		try {
		 	outputStream.write(intToByteArray(strSize));
		} catch(Exception e) {
			isConnected = false;
			try {
				connectSocket.close();
			} catch(IOException e1) {
				return;
			}
			return;
		}
		

		try {
			Integer sendTypeInt = TypeConverter.PacketTypeConverter.toInteger(PacketType.SENDCMD);
		 	outputStream.write(intToByteArray(sendTypeInt.intValue()));
		} catch(Exception e) {
			isConnected = false;
			try {
				connectSocket.close();
			} catch(IOException e1) {
				return;
			}
			return;
		}
		

		try {
			outputStream.write(closeStr.getBytes());
		} catch(Exception e) {
			isConnected = false;
			try {
				connectSocket.close();
			} catch(IOException e1) {
				return;
			}
			return;
		}
		


		int clockCounter = 0;
		Packet recvPacket = null;
		while(clockCounter < 10000) {
			
			if(!isPacketQueueEmpty()) {
				recvPacket = popFromPacketQueue(serialNum);
				if(recvPacket != null) {
					break; //��Ŷ �߰�
				}
			}
			try {
				Thread.sleep(1);
			} catch (InterruptedException e) {

				break;
			}
			clockCounter++;
		}

		if(recvPacket != null) {
			recvPacket = null;
		}
		

		packetQueue.clear();
		cmdList.clear();
		
		

		try {
			connectSocket.close();
		} catch (IOException e) {
			
		}
		isConnected = false;
		
	}
	
}
