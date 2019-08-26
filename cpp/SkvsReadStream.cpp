#include "SkvsReadStream.hpp"
#include "SkvsLibException.hpp"
#include "SkvsCommand.hpp"

#include <vector>
#include <map>
#include <string>

using namespace std;

SkvsReadStream::SkvsReadStream(vector<map<string, string>>* _resultData) {
    resultData = _resultData;
    cursor = resultData->end(); //초기홧 상태 = end()
}
SkvsReadStream::~SkvsReadStream() {
    delete resultData;
}
const bool SkvsReadStream::front(void) noexcept {
    if(resultData->empty()) return false;

    cursor = resultData->begin();
    return true;
}

const bool SkvsReadStream::end(void) noexcept {
    if(resultData->empty()) return false;

    cursor = resultData->end();
    cursor--;
    return true;
    
}

const bool SkvsReadStream::read(void) noexcept {
    if(resultData->empty()) return false;
    //초기화상태인 경우 맨 앞으로 끌어다놓기
    if( cursor == resultData->end()) {
        cursor = resultData->begin();
        return true;
    }

    cursor++;

    //맨 끝부분일 경우 false 반환
    if( cursor == resultData->end()) {
        cursor--; return false;
    }
    return true;
}

const bool SkvsReadStream::readBack(void) noexcept {
    if(resultData->empty()) return false;

    //맨 처음일 경우
    if(cursor == resultData->begin()) return false;
    cursor--;
    return true;
}

map<string, string>& SkvsReadStream::exportData(void)  {
    if(resultData->empty())
        throw SkvsDataOverReadException("This Data Container is empty");
    if( cursor == resultData->end())
        throw SkvsDataOverReadException("This Data Cursor status is inited");
    
    return *cursor;
    
}

const bool SkvsReadStream::isEmpty(void) noexcept {
    return resultData->empty();
}
const unsigned int SkvsReadStream::dataNum(void) noexcept {
    return resultData->size();
}
