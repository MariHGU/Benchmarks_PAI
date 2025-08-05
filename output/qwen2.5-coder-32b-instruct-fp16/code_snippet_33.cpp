#include <iostream>

int factorial(int n) {
    if (n == 0) return 1;
    int result = 1;
    for (int i = 1; i <= n; ++i)
        result *= i;
    return result;
}

int main() {
    std::cout << factorial(5) << std::endl;  // Output: 120
    return 0;
}