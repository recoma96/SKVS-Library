package skvsclient.modules.packet;

public class SignalPacket extends Packet {

	private SignalType signal;
	public SignalPacket( String _username, String _ip, int _cmdNum, int _sock, SignalType _sig) {
		super(PacketType.SIGNAL, _username, _ip, _cmdNum, _sock);
		
		signal = _sig;
		// TODO Auto-generated constructor stub
	}
	
	public SignalType getSignal() {  return signal; }
	
}
