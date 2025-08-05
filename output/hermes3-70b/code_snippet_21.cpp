#include <iostream>

int addNumbers(int a, int b) {
    return a + b;
}

int main() {
    int result = addNumbers(5, 3);
    std::cout << result << std::endl;  // Output: 8
    return 0;
}