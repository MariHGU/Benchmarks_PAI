#include <iostream>

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Usage
int main() {
    std::cout << factorial(5) << std::endl; // Output: 120
    return 0;
}