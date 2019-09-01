package test;

import skvsclient.SkvsCommand;
import skvsclient.modules.packet.exception.CommandFailedException;
import skvsclient.modules.packet.exception.PacketErrorException;
import skvsclient.modules.packet.exception.SizeZeroException;
import skvsclient.modules.packet.exception.SocketSettingException;

public class TestThread {


	public static class runThreadNonQuery extends Thread {
		SkvsCommand cmd = null;
		String target;
		int num;
		public runThreadNonQuery(SkvsCommand _cmd, int _num, String targetContainer) {
			cmd = _cmd;
			target = targetContainer;
			num = _num;
		}
		@Override
		public void run() {
			System.out.println(num+" input thread start");
			try {
				for(int i = 0; i < 100; i++) {
					
					cmd.cmd = "insert "+target+ " " + i;
					cmd.executeNonQuery();
				}
			} catch (NullPointerException | SizeZeroException | SocketSettingException | PacketErrorException
					| CommandFailedException e) {
				e.printStackTrace();
			}
			System.out.println(num+" input thread end");
		}
	}

	public static class runThread extends Thread {
		SkvsCommand cmd = null;
		int num;
		public runThread(SkvsCommand _cmd, int _num, String realCommand) {
			cmd = _cmd;
			cmd.cmd =realCommand;
			num = _num;
		}
		@Override
		public void run() {
			System.out.println(num+" input thread start");
			try {
				cmd.executeReadStream();
			} catch (NullPointerException | SizeZeroException | SocketSettingException | PacketErrorException
					| CommandFailedException e) {
				e.printStackTrace();
			}
			System.out.println(num+" input thread end");
		}
	}



}
