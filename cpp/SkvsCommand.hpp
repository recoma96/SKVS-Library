#ifndef SKVSCOMMAND_HPP
# define SKVSCOMMAND_HPP

#include "SkvsConnection.hpp"
#include "SkvsLibException.hpp"
#include <string>

using namespace std;

class SkvsCommand {
private:
    SkvsConnection* connection;
public:
    string cmd;

    explicit SkvsCommand(SkvsConnection* _connection);
    explicit SkvsCommand(SkvsConnection* _connection, const string _cmd);

    void executeNonQuery(void);
    //SkvsStream& executeReadStream(void);
};



#endif