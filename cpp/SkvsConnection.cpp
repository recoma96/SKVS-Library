#include "SkvsConnection.hpp"
#include "modules/SockWrapper/SocketManager.hpp"
#include "modules/SockWrapper/ClientSocketManager.hpp"
#include "modules/SockWrapper/NetworkingManager.hpp"
#include "modules/packet/Packet.hpp"
#include "modules/packet/SkvsProtocol.hpp"
#include "modules/user/User.hpp"
#include "SkvsLibException.hpp"

#include <string>
#include <vector>
#include <mutex>
#include <iostream>
#include <string.h>

#include <chrono>
#include <thread>

using namespace std;
using namespace SockWrapperForCplusplus;
using namespace SkvsProtocol;
extern void RecvThread(SkvsConnection* conn);

//cmd 시리얼 넘버 계산
const int SkvsConnection::setCmdSerial(void) {

	int counter = 0;

	if( serialList.empty() ) {
        serialList.push_back(0);
		return 0;
	}
	for( vector<int>::iterator iter = serialList.begin();
			iter != serialList.end(); iter++ ) {

		if( counter <= (*iter))
            counter = (*iter)+1;
	}
    serialList.push_back(counter);
	return counter;    
}

const bool SkvsConnection::removeSerialNum(int removeNum) {

	for( vector<int>::iterator deleteCursor = serialList.begin();
			deleteCursor != serialList.end();
			deleteCursor++ ) {

		if( (*deleteCursor) == removeNum ) {

			serialList.erase(deleteCursor);
			return true;
		}
	}
	return false;   
}

SkvsConnection::SkvsConnection(const string _ID,
                            const string _pswd,
                            const string _connectIP,
                            const short _port) {
    
    //소켓 생성
    socket = new Socket(_connectIP, _port, false);

    //멤버변수 초기화
    ID = _ID;
    pswd = _pswd;
    isConnected = false;
    
    
}


void SkvsConnection::open(void) {

    //이미연결되어있는지 확인
    if( isConnected )
        throw SkvsSocketSettingException("This Connection is Aleady Connected"); 

    if(!setSocket(socket)) {
        throw SkvsSocketSettingException("Socket Setting Failed");
    }

    if(!connectToServer(socket))
        throw SkvsSocketSettingException("Conenct Failed From Server");
    
    //서버에게 로그인 메세지 전송
    string sendLoginData = this->ID + "-" + this->pswd;

    //로그인 데이터 전송
    if( sendData(socket, (char*)(sendLoginData.c_str()), sendLoginData.length()) <= 0) {
		closeSocket(socket);
        throw SkvsSocketSettingException("Failed to Send Login Data to Server");
	}

    //데이터 수신
	bool checkConnect = false;
	if( recvData(socket, &checkConnect, sizeof(bool)) <= 0) {
		closeSocket(socket);
        throw SkvsRecvException("Failed to recv to Server");
	}

	if(checkConnect == false) {
        closeSocket(socket);
        throw SkvsLoginFaildException("Login Denied");
	}

	UserLevel userLv;
	if( recvData(socket, &userLv, sizeof(UserLevel)) <= 0) {
		closeSocket(socket);
        throw SkvsRecvException("Failed to recv to Server");
	}

    //연결 끝
    this->isConnected = true;
    //recvthread 활성화

    thread recvThread(RecvThread, this);
    recvThread.detach();
    this_thread::sleep_for(chrono::milliseconds(1));
        
}

void SkvsConnection::close(void) {
    if(!isConnected) return;

    //종료패킷송신

    //cmd넘버 생성
    calSerialMutex.lock();
    int cmdSerial = setCmdSerial();
    calSerialMutex.unlock();

    SendCmdPacket sendPacket(ID, socket->getIP(), cmdSerial, cmdSerial, "quit");

    char* sendStr =  makePacketSerial(&sendPacket);
    int sendStrSize = strlen(sendStr);

    //패킷 전송 (데이터 길이, 데이터 타입, 데이터)
    socketMutex.lock();
    if( sendData(socket, &sendStrSize, sizeof(int)) <= 0) {
        socketMutex.unlock();
        isConnected=false;
        closeSocket(socket);
        delete sendStr;
        return;
    }

    PacketType sendType = sendPacket.getPacketType();
    if( sendData(socket, &sendType, sizeof(PacketType)) <= 0) {
        socketMutex.unlock();
        isConnected=false;
        closeSocket(socket);
        delete sendStr;
        return;
    }

    if( sendData(socket, sendStr, sendStrSize) <= 0) {
        socketMutex.unlock();
        isConnected=false;
        closeSocket(socket);
        delete sendStr;
        return;
    }
    socketMutex.unlock();

    int shutdownCounter = 0;

    //종료 패킷 수신

    //수신패킷 받을 때 까지 대기
    //시간안에 못받으면 연결 해제 처리
    while(true) {
        if(packetQueue.empty()) {
            if(shutdownCounter == 60000) {
                isConnected=false;
                closeSocket(socket);
                return;
            } else {
                shutdownCounter++;
                this_thread::sleep_for(chrono::milliseconds(1));
                continue;
                
            }
        } else { //시리얼 넘버 확인
            packetQueueMutex.lock();
            if(packetQueue.front()->getCmdNum() == cmdSerial) {
                break;
            } else {
                packetQueueMutex.unlock();
                shutdownCounter++;
                this_thread::sleep_for(chrono::milliseconds(1));
                continue;
            }
        }
    }
    
    //큐에서 패킷을 받고 연결 끊기

    Packet* endQueue = packetQueue.front();
    packetQueue.pop();
    packetQueueMutex.unlock();
    
    delete endQueue;

    isConnected=false;
    closeSocket(socket);
    this_thread::sleep_for(chrono::milliseconds(1));
    return;
    
}

SkvsConnection::~SkvsConnection() {
    if(isConnected)
        this->close();
    delete socket;
}

