#pragma once
#include <vector>
#include <stdexcept>
#include <iostream>

template <typename T>
class NPArray {
    std::vector<T> data;
    size_t rows, cols;
    bool istranspose;

public:
    NPArray(size_t r, size_t c, std::vector<T> d)
        : data(std::move(d)), rows(r), cols(c), istranspose(false) {}

    void transpose(){
        this->istranspose = true;
        int temp = this->rows;
        this->rows = this->cols;
        this->cols = temp;
    }
    
    T& operator[](size_t r, size_t c) {
        if (r >= rows || c >= cols) throw std::out_of_range("Index out of bounds");

        // r and c are interchanged in this case
        if (this->istranspose) return data[c * cols + r];

        // while in thise case they're not interchanged
        return data[r * cols + c];
    }

    std::vector<size_t> size(){
        std::vector<size_t> s = {rows, cols};

        return s;
    }
};
