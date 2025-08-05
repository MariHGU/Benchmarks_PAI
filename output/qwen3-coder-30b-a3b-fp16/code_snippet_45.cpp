#include <stdexcept>
#include <iostream>

long long factorial(int n) {
    if (n < 0) {
        throw std::invalid_argument("Factorial is not defined for negative numbers");
    }
    
    if (n == 0 || n == 1) {
        return 1;
    }
    
    return n * factorial(n - 1);
}

// Usage
int main() {
    std::cout << factorial(5) << std::endl; // Output: 120
    return 0;
}