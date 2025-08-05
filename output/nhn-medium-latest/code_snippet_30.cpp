#include <iostream>

long factorial(int n) {
    if (n <= 1)
        return 1;
    else
        return n * factorial(n - 1);
}

// Example usage:
int main() {
    std::cout << factorial(5) << std::endl;  // Output: 120
    return 0;
}