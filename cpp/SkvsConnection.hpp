#ifndef SKVSCONNECTION_HPP
# define SKVSCONNECTION_HPP

#include <string>
#include <vector>
#include <cstring>
#include <mutex>
#include <sys/time.h>

#include "modules/SockWrapper/Socket.hpp"
#include "SkvsLibException.hpp"

using namespace std;
using namespace SockWrapperForCplusplus;


class SkvsConnection {
private:
    Socket* socket;
    string ID;
    string pswd;
    bool isConnected; //close없이 소멸자호출할때 서버에 지장없게 하기 위한 boolean
    vector<int> serialList;

    mutex calSerialMutex; //cmd시리얼넘버 계산할때 사용

public:
    SkvsConnection(const string _ID,
                    const string _pswd,
                    const string _connectIP,
                    const short _port);
    ~SkvsConnection();

    // 왠만하면 사용 금지
    const int setCmdSerial(void);
    const bool removeSerialNum(int removeNum);
    

    void open(void); //초단위
    void close(void);

    const string getID(void) { return ID; }
    const string getIP(void) { return socket->getIP(); }
    Socket& useSocket(void) { return *socket; }
    const bool getAboutConnected() { return isConnected; }
    
};


#endif