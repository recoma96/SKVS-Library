package test;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.ListIterator;

import skvsclient.SkvsCommand;
import skvsclient.SkvsConnection;
import skvsclient.SkvsReadStream;
import skvsclient.modules.packet.exception.CommandFailedException;
import skvsclient.modules.packet.exception.LoginFailedException;
import skvsclient.modules.packet.exception.PacketErrorException;
import skvsclient.modules.packet.exception.SizeZeroException;
import skvsclient.modules.packet.exception.SocketSettingException;





public class Test {

	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		/*
		SkvsConnection conn = new SkvsConnection("user", "12345678", "192.168.0.108", 13403);

		try {
			conn.open();
			//conn.close();	
		} catch (SocketSettingException | IOException | LoginFailedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		SkvsCommand myCmd = new SkvsCommand(conn, "create staticlist mylist1 number");
		//SkvsCommand myCmd = new SkvsCommand(conn);
		try {
			
			
			myCmd.executeNonQuery();
			
			myCmd.cmd = "create staticlist mylist2 number";
			myCmd.executeNonQuery();
			
			TestThread.runThreadNonQuery t1 = new TestThread.runThreadNonQuery(myCmd, 1, "mylist1");
			TestThread.runThreadNonQuery t2 = new TestThread.runThreadNonQuery(myCmd, 2, "mylist2");

			t1.start();		
			
			t1.join();
			
			t2.start();
			t2.join();
			
		
			
			

			//System.out.println("export End");
			
		} catch (NullPointerException | SizeZeroException | SocketSettingException | PacketErrorException | CommandFailedException | InterruptedException e) {

			e.printStackTrace();
			conn.close();
			conn = null;
		}
		conn.close();
		System.out.println("end");
		*/

		
	}

}
