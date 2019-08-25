#include <iostream>
#include <thread>
#include <chrono>
#include "SkvsConnection.hpp"
#include "SkvsCommand.hpp"

int main(void) {
    SkvsConnection conn("user", "12345678", "127.0.0.1", 8000);
    conn.open();
    SkvsCommand dbCommand(&conn);
    
    

    try {
        dbCommand.cmd = "insert dynamiclist mylist";
        dbCommand.executeNonQuery();
        dbCommand.cmd = "insert dynamiclist mylist";
        dbCommand.executeNonQuery();
    } catch(SkvsLibException& e) {
        cout << e.getMsg() << endl;
    }
    conn.close();
    return 0;
}