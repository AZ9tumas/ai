#include "../include/nparray.hpp"
#include <iostream>

int main(){
    std::vector<int> dataarr = {1, 2, 3, 4};
    NPArray<int> arr(2, 2, dataarr);

    auto s = arr.size();
    int row = s[0];
    int col = s[1];
    std::cout << row << ", " << col << std::endl;
}
