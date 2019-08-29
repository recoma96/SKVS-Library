#include <iostream>
#include <thread>
#include <chrono>
#include <string.h>
#include <thread>

#include "SkvsConnection.hpp"
#include "SkvsCommand.hpp"
#include "SkvsReadStream.hpp"


using namespace std;
using namespace SockWrapperForCplusplus;

void test_thread(SkvsCommand* cmd, int num) {
    cout << "start" << endl;
    SkvsReadStream* reader = cmd->executeReadStream();

    delete reader;
    cout << num << " thread complete" << endl;
}


int main(void) {
    
    SkvsConnection conn("user", "12345678", "127.0.0.1", 8000);
    conn.open();
    
    //SkvsCommand myCmd(&conn, "create staticlist mylist number");
    SkvsCommand myCmd(&conn);
    
    /*
    myCmd.executeNonQuery();
    
    
    for(int i = 1; i < 200; i += 1) {
        myCmd.cmd = "insert mylist "+to_string(i);
        myCmd.executeNonQuery();
    }
    */

    myCmd.cmd = "get mylist";


    for(int i = 0; i < 15; i++) {
        thread searchThread(test_thread, &myCmd, i);
        searchThread.detach();
    }
    while(true) {

    }
    

    conn.close();
    
    return 0;
}