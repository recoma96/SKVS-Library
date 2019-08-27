#ifndef SKVSCONNECTION_HPP
# define SKVSCONNECTION_HPP

#include <string>
#include <vector>
#include <cstring>
#include <mutex>
#include <sys/time.h>
#include <deque>
#include <queue>

#include "modules/SockWrapper/Socket.hpp"
#include "SkvsLibException.hpp"
#include "modules/packet/Packet.hpp"

using namespace std;
using namespace SockWrapperForCplusplus;



class SkvsConnection {
private:
    Socket* socket;
    mutex socketMutex; //Command에서 사용

    string ID;
    string pswd;
    bool isConnected; //close없이 소멸자호출할때 서버에 지장없게 하기 위한 boolean
    vector<int> serialList;
    mutex calSerialMutex; //cmd시리얼넘버 계산할때 사용

    queue<Packet*, deque<Packet*>> packetQueue;
    mutex packetQueueMutex;
public:
    SkvsConnection(const string _ID,
                    const string _pswd,
                    const string _connectIP,
                    const short _port);
    ~SkvsConnection();

    // 왠만하면 사용 금지
    const int setCmdSerial(void);
    const bool removeSerialNum(int removeNum);
    queue<Packet*, deque<Packet*>>& useQueue(void) { return packetQueue; }
    Socket& useSocket(void) { return *socket; }
    mutex& usePacketQueueMutex(void) { return packetQueueMutex; }

    //mutex
    void lockSocketMutex(void) noexcept { socketMutex.lock();}
    void unlockSocketMutex(void) noexcept { socketMutex.unlock();}
    void lockCalMutex(void) noexcept { calSerialMutex.lock(); }
    void unlockCalMutex(void) noexcept { calSerialMutex.unlock();}
    

    //실제로 사용하는 함수
    void open(void);
    void close(void);

    const string getID(void) { return ID; }
    const string getIP(void) { return socket->getIP(); } 
    const bool getAboutConnected() { return isConnected; }
    
    
};


#endif