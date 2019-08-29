#include <string>
#include <list>
#include <thread>
#include <mutex>
#include <chrono>
#include <queue>
#include <deque>
#include <vector>
#include <string.h>

#include "SkvsConnection.hpp"
#include "modules/packet/Packet.hpp"
#include "modules/packet/SkvsProtocol.hpp"
#include "SkvsLibException.hpp"
#include "modules/SockWrapper/NetworkingManager.hpp"

using namespace std;
using namespace SockWrapperForCplusplus;
using namespace SkvsProtocol;


void RecvThread(SkvsConnection* conn) {

    
    while(conn->getAboutConnected()) { //연결 여부

        int recvBufSize = 0;
        char* recvBuf = nullptr;
        PacketType recvType;

        //패킷 수신
        while(true) {
            if(recvData(&(conn->useSocket()), &recvBufSize, sizeof(int), MSG_DONTWAIT) > 0) {
                break;
            } else {
                if(!conn->getAboutConnected()) {
                    return;
                }
                this_thread::sleep_for(chrono::milliseconds(1));
            }
        }
        if(recvData(&(conn->useSocket()), &recvType, sizeof(PacketType)) < 0) {
            conn->close();
            return;
        }

        recvBuf = new char[recvBufSize+1];

        if(recvData(&(conn->useSocket()), recvBuf, recvBufSize) < 0) {
            conn->close();
            return;
        }
        recvBuf[recvBufSize] = '\0';

        //패킷 객체 생성
        Packet* savePacket = nullptr;
        switch( recvType ) {

            case PACKETTYPE_RECV:
            {
                RecvPacketType checkType;
                try {
                    checkType = checkRecvPacketType(recvBuf);
                } catch(SkvsLibException& e) {
                    delete[] recvBuf;
                    continue;
                }
                if( checkType == RECVPACKETTYPE_DATA)
                    savePacket = returnToPacket<RecvDataPacket>(recvBuf);
                else
                    savePacket = returnToPacket<RecvMsgPacket>(recvBuf);
            }
            break;

            case PACKETTYPE_SIGNAL:
            {
                savePacket = returnToPacket<SignalPacket>(recvBuf);
            }
            break;
            default:
                delete[] recvBuf;
                continue;
        }      
        delete[] recvBuf;

        //cout << savePacket->getCmdNum() << endl;
        //cout << aa << endl;
        
        conn->usePacketQueueMutex().lock();
        conn->useQueue().push(savePacket);
        conn->usePacketQueueMutex().unlock();

    }
}