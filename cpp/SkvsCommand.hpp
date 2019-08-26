#ifndef SKVSCOMMAND_HPP
# define SKVSCOMMAND_HPP

#include "SkvsConnection.hpp"
#include "SkvsLibException.hpp"
#include "SkvsReadStream.hpp"
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
    SkvsReadStream* executeReadStream(void);
};



#endif