#include "SkvsCommand.hpp"

#include "modules/SockWrapper/SocketManager.hpp"
#include "modules/SockWrapper/ClientSocketManager.hpp"
#include "modules/SockWrapper/NetworkingManager.hpp"
#include "modules/packet/Packet.hpp"
#include "modules/packet/SerialController.hpp"
#include "modules/structure/DataElement.hpp"
#include "modules/structure/TypePrinter.hpp"

#include <string>
#include <vector>
#include <mutex>
#include <iostream>
#include <string.h>
#include <thread>
#include <chrono>
#include <string.h>
#include <map>
#include <vector>

using namespace std;
using namespace SockWrapperForCplusplus;
using namespace PacketSerialData;
using namespace google;
using namespace structure;


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

//결과데이터없는 쿼리문 실행
void SkvsCommand::executeNonQuery(void) {

    //connection 연결 여부 판정
    if(!connection->getAboutConnected())
        throw SkvsSocketSettingException("This Server is Disconnected.");

    //커맨드 길이 판정
    if(cmd.empty())
        throw SkvsCommandFailedException("This cmd is empty.");
    
    //Cmd 시리얼 넘버 연산
    int serialNum = connection->setCmdSerial();

    //패킷 생성
    SendCmdPacket sendPacket(
        connection->getID(),
        connection->useSocket().getIP(),
        serialNum,
        0,
        cmd
    );

    char* sendBuf = makePacketToCharArray<SendCmdPacket>(sendPacket);
    int sendBufSize = strlen(sendBuf);
    PacketType sendPacketType = PACKETTYPE_SENDCMD;

    //전송
    connection->lockSocketMutex();
    if(sendData(&(connection->useSocket()), &sendBufSize, sizeof(int)) <= 0) {
        connection->unlockSocketMutex();
        connection->close();
         SkvsSocketSettingException("Disconnected from server");
    }
    if(sendData(&(connection->useSocket()), &sendPacketType, sizeof(PacketType)) <= 0) {
        connection->unlockSocketMutex();
        connection->close();
        SkvsSocketSettingException("Disconnected from server");
    }
    if(sendData(&(connection->useSocket()), sendBuf, sendBufSize) <= 0) {
        connection->unlockSocketMutex();
        connection->close();
        SkvsSocketSettingException("Disconnected from server");
    }
    connection->unlockSocketMutex();
    delete sendBuf;


    //결과데이터 받기
    //60초가 경과해도 데이터가안들어오는 경우, 스레드 소멸
    int shutdownCounter = 0;
    string errorMsg;
    
    while(true) {
        Packet* recvPacket = nullptr;
        if(!connection->useQueue().empty() && 
            connection->useQueue().front()->getCmdNum() == serialNum ) {
            shutdownCounter = 0; //카운터 초기화
            
            //패킷 추출
            connection->usePacketQueueMutex().lock();
            recvPacket = connection->useQueue().front();
            connection->useQueue().pop();
            connection->usePacketQueueMutex().unlock();
            
            PacketType recvType = recvPacket->getPacketType();

            //패킷 타입 판정
            //LOG와 SEMDCMD는 필요없으므로 소멸
            switch(recvType) {
                case PACKETTYPE_RECV: //recv 
                {
                    if( ((RecvPacket*)(recvPacket))->getRecvPacketType() == RECVPACKETTYPE_DATA ) {
                        //무시
                        delete (RecvDataPacket*)recvPacket;
                    } else {
                        //errorMsg 갱신
                        errorMsg = ((RecvMsgPacket*)(recvPacket))->getMsg();
                        delete (RecvMsgPacket*)recvPacket;

                    }
                }
                break;
                case PACKETTYPE_SIGNAL: //recv signal
                {
                    SignalPacket* signalPacket = (SignalPacket*)recvPacket;
                    auto sig = signalPacket->getSignal();

                    switch(sig) {
                        case SIGNALTYPE_RECVSTART:
                        break;
                        case SIGNALTYPE_RECVEND: 
                            //정상종료

                            delete signalPacket;
                            connection->removeSerialNum(serialNum );
                            return;
                            
                        break;

                        case SIGNALTYPE_ERROR:
                        //명령수행에 있어서 오류 발생
                            delete signalPacket;
                            connection->removeSerialNum(serialNum );

                        //에러메세지가 있으면 송출
                        //없으면 unknown Error
                            if(errorMsg.empty())
                                throw SkvsCommandFailedException("Unknown Error");
                            else
                                throw SkvsCommandFailedException(errorMsg);
                            return;

                        break;
                    }

                    delete signalPacket;
                }
                break;
                case PACKETTYPE_LOG:
                    delete (LogPacket*)recvPacket;
                break;
                case PACKETTYPE_SENDCMD:
                    delete (SendCmdPacket*)recvPacket;
                break;
            }

            recvPacket = nullptr;
            continue;
            
        } else { //비어있음
            if(shutdownCounter == 60000) {
                connection->removeSerialNum(serialNum);
                throw SkvsCommandFailedException("Server does not send Packet to this command");
            } else {
                shutdownCounter++;
                this_thread::sleep_for(chrono::milliseconds(1));
                continue;
            }
        }

    }
    connection->removeSerialNum(serialNum);
}

//결과 데이터값이 존재하는 쿼리문 실행
SkvsReadStream* SkvsCommand::executeReadStream(void) {

    
    //connection 연결 여부 판정
    if(!connection->getAboutConnected())
        throw SkvsSocketSettingException("This Server is Disconnected.");

    //커맨드 길이 판정
    if(cmd.empty())
        throw SkvsCommandFailedException("This cmd is empty.");
    
    //Cmd 시리얼 넘버 연산
    connection->lockCalMutex();
    int serialNum = connection->setCmdSerial();
    connection->unlockCalMutex();

    //패킷 생성
    SendCmdPacket sendPacket(
        connection->getID(),
        connection->useSocket().getIP(),
        serialNum,
        0,
        cmd
    );

    char* sendBuf = makePacketToCharArray<SendCmdPacket>(sendPacket);
    int sendBufSize = strlen(sendBuf);
    PacketType sendPacketType = PACKETTYPE_SENDCMD;

    //전송
    connection->lockSocketMutex();
    if(sendData(&(connection->useSocket()), &sendBufSize, sizeof(int)) <= 0) {
        connection->unlockSocketMutex();
        connection->close();
        SkvsSocketSettingException("Disconnected from server");
    }
    if(sendData(&(connection->useSocket()), &sendPacketType, sizeof(PacketType)) <= 0) {
        connection->close();
        connection->unlockSocketMutex();
        SkvsSocketSettingException("Disconnected from server");
    }
    if(sendData(&(connection->useSocket()), sendBuf, sendBufSize) <= 0) {
        connection->close();
        connection->unlockSocketMutex();
        SkvsSocketSettingException("Disconnected from server");
    }
    connection->unlockSocketMutex();
    delete sendBuf;


    //결과데이터 받기
    //60초가 경과해도 데이터가안들어오는 경우, 스레드 소멸
    int shutdownCounter = 0;
    string errorMsg;
    vector<map<string, string>>* dataContainer = 
        new vector<map<string, string>>();
    
    while(true) {
        Packet* recvPacket = nullptr;
        if(!connection->useQueue().empty() && 
            connection->useQueue().front()->getCmdNum() == serialNum ) {
            shutdownCounter = 0; //카운터 초기화
            
            //패킷 추출
            connection->usePacketQueueMutex().lock();
            recvPacket = connection->useQueue().front();
            connection->useQueue().pop();
            connection->usePacketQueueMutex().unlock();
            
            PacketType recvType = recvPacket->getPacketType();

            //패킷 타입 판정
            //LOG와 SEMDCMD는 필요없으므로 소멸
            switch(recvType) {
                case PACKETTYPE_RECV: //recv 
                {
                    if( ((RecvPacket*)(recvPacket))->getRecvPacketType() == RECVPACKETTYPE_DATA ) {

                        //데이터 수집
                        RecvDataPacket* exportedData = (RecvDataPacket*)recvPacket;
                        DataElement data = exportedData->getData();

                        map<string, string> dataSet;
                        dataSet.insert(pair<string, string>("data", data.getDataToString()));
                        dataSet.insert(pair<string, string>("datatype", convertDataTypeToString(data.getDataType()) ));
                        dataSet.insert(pair<string, string>("structtype", convertStructTypeToString(data.getStructType())));

                        dataContainer->push_back(dataSet);

                        delete exportedData;
                    } else {
                        //errorMsg 갱신
                        errorMsg = ((RecvMsgPacket*)(recvPacket))->getMsg();
                        delete (RecvMsgPacket*)recvPacket;

                    }
                }
                break;
                case PACKETTYPE_SIGNAL: //recv signal
                {
                    SignalPacket* signalPacket = (SignalPacket*)recvPacket;
                    auto sig = signalPacket->getSignal();

                    switch(sig) {
                        case SIGNALTYPE_RECVSTART:
                        break;
                        case SIGNALTYPE_RECVEND: 
                            //정상종료

                            delete signalPacket;
                            connection->lockCalMutex();
                            connection->removeSerialNum(serialNum );
                            connection->unlockCalMutex();
                            return new SkvsReadStream(dataContainer);
                            
                        break;

                        case SIGNALTYPE_ERROR:
                        //명령수행에 있어서 오류 발생
                            delete signalPacket;
                            connection->lockCalMutex();
                            connection->removeSerialNum(serialNum );
                            connection->unlockCalMutex();

                        //에러메세지가 있으면 송출
                        //없으면 unknown Error
                            if(errorMsg.empty())
                                throw SkvsCommandFailedException("Unknown Error");
                            else
                                throw SkvsCommandFailedException(errorMsg);

                        break;
                    }

                    delete signalPacket;
                }
                break;
                case PACKETTYPE_LOG:
                    delete (LogPacket*)recvPacket;
                break;
                case PACKETTYPE_SENDCMD:
                    delete (SendCmdPacket*)recvPacket;
                break;
                default:
                    delete recvPacket;
                    connection->lockCalMutex();
                    connection->removeSerialNum(serialNum );
                    connection->unlockCalMutex();
                    throw SkvsCommandFailedException("Server send unknown flag");
            }

            recvPacket = nullptr;
            continue;
            
        } else { //비어있음
            if(shutdownCounter == 60000) {
                connection->lockCalMutex();
                connection->removeSerialNum(serialNum);
                connection->unlockCalMutex();
                throw SkvsCommandFailedException("Server does not send Packet to this command");
            } else {
                shutdownCounter++;
                this_thread::sleep_for(chrono::milliseconds(1));
                continue;
            }
        }

    }
}