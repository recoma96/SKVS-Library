#include "SkvsConnection.hpp"
#include "modules/SockWrapper/SocketManager.hpp"
#include "modules/SockWrapper/ClientSocketManager.hpp"
#include "modules/SockWrapper/NetworkingManager.hpp"
#include "modules/packet/Packet.hpp"
#include "modules/packet/SerialController.hpp"
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
using namespace PacketSerialData;

//cmd 시리얼 넘버 계산
const int SkvsConnection::setCmdSerial(void) {

	int counter = 0;

	if( serialList.empty() ) {

		return 0;
	}
	for( vector<int>::iterator iter = serialList.begin();
			iter != serialList.end(); iter++ ) {

		if( counter < (*iter))
            counter = (*iter);
	}
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

    int shutdownCounter = 0; //서버응답 제한시간
    //0.1초

    //로그인 허용 어부
	bool checkConnect = false;
    while(true) {
	    if( recvData(socket, &checkConnect, sizeof(bool), MSG_PEEK | MSG_DONTWAIT ) <= 0) {
            if(shutdownCounter == 6000)
                throw SkvsRecvExcept("Failed to recv to Server");
            this_thread::sleep_for(chrono::milliseconds(10));
            shutdownCounter++;
	    } else {
            break;
        }
    }

	if(checkConnect == false) {
        closeSocket(socket);
        throw SkvsLoginFaildException("Login Denied");
	}

    //서버에서는 클라이언트에게 UserLevel까지 보내지만 라이브러리에서는 필요 없으므로
    //4바이트 로 받고 버림
    int trash;
    
    shutdownCounter = 0;
    while(true) {
        if( recvData(socket, &trash, sizeof(int), MSG_PEEK | MSG_DONTWAIT) <= 0) {

            if(shutdownCounter == 6000)
                throw SkvsRecvExcept("Failed to recv to Server");
            this_thread::sleep_for(chrono::milliseconds(10));
            shutdownCounter++;

	    } else {
            break;
        }
    }

    //연결 끝
    this->isConnected = true;
    this_thread::sleep_for(chrono::milliseconds(10));
}

void SkvsConnection::close(void) {
    if(!isConnected) return;

    //종료패킷송신

    //cmd넘버 생성
    calSerialMutex.lock();
    int cmdSerial = setCmdSerial();
    calSerialMutex.unlock();

    SendCmdPacket sendPacket(ID, socket->getIP(), cmdSerial, 0, "quit");

    char* sendStr = makePacketToCharArray<SendCmdPacket>(sendPacket);
    int sendStrSize = strlen(sendStr);

    //패킷 전송 (데이터 길이, 데이터 타입, 데이터)
    if( sendData(socket, &sendStrSize, sizeof(int)) <= 0) {
        isConnected=false;
        closeSocket(socket);
        return;
    }

    PacketType sendType = sendPacket.getPacketType();
    if( sendData(socket, &sendType, sizeof(PacketType)) <= 0) {
        isConnected=false;
        closeSocket(socket);
        return;
    }

    if( sendData(socket, sendStr, sendStrSize) <= 0) {
        isConnected=false;
        closeSocket(socket);
        return;
    }

    int shutdownCounter = 0;

    //종료 패킷 수신
    int recvBufSize = 0;
    char* recvBuf = nullptr;
    int size = 0;
    //데이터길이
    while(true) {
        if( (size = recvData(socket, &recvBufSize, sizeof(int), MSG_PEEK | MSG_DONTWAIT)) <= 0 ) {
            if(shutdownCounter == 6000) {
                isConnected = false;
                closeSocket(socket);
                return;
            }
            this_thread::sleep_for(chrono::milliseconds(10));
            shutdownCounter++;
        } else {
            break;
        }
    }
    PacketType recvPacketType;

    shutdownCounter = 0;
    //데이터 타입
    while(true) {
        if( recvData(socket, &recvPacketType, sizeof(PacketType), MSG_PEEK | MSG_DONTWAIT) <= 0 ) {
            if(shutdownCounter == 6000) {
                isConnected = false;
                closeSocket(socket);
                return;
            } else {
                this_thread::sleep_for(chrono::milliseconds(10));
                shutdownCounter++;
            }
        } else {
            break;
        }
    }

    //데이터
    recvBuf = new char[recvBufSize];
    shutdownCounter = 0;
    while(true) {
        if( recvData(socket, recvBuf, recvBufSize, MSG_PEEK | MSG_DONTWAIT) <= 0 ) {
            if(shutdownCounter == 6000) {
                isConnected = false;
                closeSocket(socket);
                return;
            } else {
                this_thread::sleep_for(chrono::milliseconds(10));
                shutdownCounter++;
            }
        } else {
            break;
        }
    }
    isConnected=false;
    closeSocket(socket);
    return;
    this_thread::sleep_for(chrono::milliseconds(10));
    
}

SkvsConnection::~SkvsConnection() {
    if(isConnected)
        this->close();
    delete socket;
}

