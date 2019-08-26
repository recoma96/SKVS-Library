#ifndef SKVSLIBEXCEPTION_HPP
# define SKVSLIBEXCEPTION_HPP

#include <string>

using namespace std;

class SkvsLibException {
private:
    string errorMsg;
public:
    SkvsLibException (string _errorMsg) {
        errorMsg = _errorMsg;
    }
    const string getMsg(void) { return errorMsg; }
};

class SkvsSocketSettingException : public SkvsLibException {
public:
    SkvsSocketSettingException(string _errorMsg) : SkvsLibException(_errorMsg) { }
};

class SkvsLoginFaildException : public SkvsLibException {
public:
    SkvsLoginFaildException(string _errorMsg) : SkvsLibException(_errorMsg) { }
};

class SkvsDataOverReadException : public SkvsLibException {
public:
    SkvsDataOverReadException(string _errorMsg) : SkvsLibException(_errorMsg) {}
};

class SkvsNullptrException : public SkvsLibException {
public:
    SkvsNullptrException(string _errorMsg) : SkvsLibException(_errorMsg) {}
};

class SkvsCommandFailedException : public SkvsLibException {
public:
    SkvsCommandFailedException(string _errorMsg) : SkvsLibException(_errorMsg) {}
};

class SkvsRecvExcept : public SkvsLibException {
public:
    SkvsRecvExcept(string _errorMsg) : SkvsLibException(_errorMsg) { }
};

#endif