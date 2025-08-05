#include <iostream>

// Function with range-based loop
int calculateSum(int n) {
    if (n <= 0) return 0;
    
    int sum = 0;
    for (int i = 1; i <= n; ++i) {
        sum += i;
    }
    return sum;
}

// Alternative using std::accumulate (C++17)
#include <numeric>
#include <vector>

int calculateSumModern(int n) {
    if (n <= 0) return 0;
    
    std::vector<int> numbers(n);
    std::iota(numbers.begin(), numbers.end(), 1); // Fill with 1,2,...,n
    return std::accumulate(numbers.begin(), numbers.end(), 0);
}