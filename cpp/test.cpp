#include <iostream>
#include <thread>
#include <chrono>
#include "SkvsConnection.hpp"
#include "SkvsCommand.hpp"
#include "SkvsReadStream.hpp"

using namespace std;

int main(void) {
    SkvsConnection conn("user", "12345678", "127.0.0.1", 8000);

    //로그인
    conn.open();
    
    SkvsReadStream* reader = nullptr;

    //서버에 요청을 하기 위한 커맨드 클래스 생성
    SkvsCommand connCmd(&conn, "create dynamiclist mylist");
    try {
        //쿼리문 실행
        connCmd.executeNonQuery();


        connCmd.cmd = "insert mylist 001";
        connCmd.executeNonQuery();
        connCmd.cmd = "insert mylist 002";
        connCmd.executeNonQuery();
        connCmd.cmd = "insert mylist 003";
        connCmd.executeNonQuery();
        connCmd.cmd = "insert mylist 004";
        connCmd.executeNonQuery();
        connCmd.cmd = "insert mylist 005";
        connCmd.executeNonQuery();

        //데이터 받아오기
        connCmd.cmd = "get mylist";
        reader = connCmd.executeReadStream();

    //명령문 실행에 실패했을 경우
    //예외처리
    } catch(SkvsLibException& e) {
        cout << e.getMsg() << endl;
        return 0;
    }

    //데이터 정방향으로 조회
    while(reader->read()) {
        cout << reader->exportData()["data"] << endl;
    }


    //맨 앞
    cout << endl;
    reader->front();
    cout << reader->exportData()["data"] << endl;
    reader->front();
    cout << reader->exportData()["data"] << endl;

    //맨 끝
    cout << endl;
    reader->end();
    cout << reader->exportData()["data"] << endl;
    reader->end();
    cout << reader->exportData()["data"] << endl;

    cout << endl;
    cout << endl;

    //역방향
    while(reader->readBack())
        cout << reader->exportData()["data"] << endl;
    
    return 0;
}