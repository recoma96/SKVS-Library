#include "SkvsCommand.hpp"

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
#include <thread>
#include <chrono>

using namespace std;
using namespace SockWrapperForCplusplus;
using namespace PacketSerialData;
using namespace google;


SkvsCommand::SkvsCommand(SkvsConnection* _connection) {

    if(_connection == nullptr)
        throw SkvsNullptrException("SkvsConnection is nullptr");
    if(!_connection->getAboutConnected())
        throw SkvsSocketSettingException("This connected is disconnected");

    connection = _connection;

}
SkvsCommand::SkvsCommand(SkvsConnection* _connection, const string _cmd) {

    if(_connection == nullptr)
        throw SkvsNullptrException("SkvsConnection is nullptr");
    if(!_connection->getAboutConnected())
        throw SkvsSocketSettingException("This connected is disconnected");

    connection = _connection;
    cmd = _cmd;

}
void SkvsCommand::executeNonQuery(void) {
}
