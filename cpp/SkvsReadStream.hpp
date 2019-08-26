#ifndef SKVSREADSTREAM_HPP
# define SKVSREADSTREAM_HPP

#include <vector>
#include <map>
#include <string>

#include "SkvsLibException.hpp"

using namespace std;

class SkvsReadStream {
private:
    vector<map<string, string>>* resultData;
    vector<map<string, string>>::iterator cursor;

public:
    explicit SkvsReadStream(vector<map<string, string>>* _resultData);
    ~SkvsReadStream();

    const bool front(void) noexcept;
    const bool end(void) noexcept;
    const bool read(void) noexcept;
    const bool readBack(void) noexcept;
    map<string, string>& exportData(void);

    const bool isEmpty(void) noexcept;
    const unsigned int dataNum(void) noexcept;
};
#endif