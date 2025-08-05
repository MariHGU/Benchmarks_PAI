#include <iostream>
#include <numeric>

int sum_even_numbers(const int* arr, size_t size) {
    int sum = 0;
    for (size_t i = 0; i < size; ++i) {
        if (arr[i] % 2 == 0) {
            sum += arr[i];
        }
    }
    return sum;
}