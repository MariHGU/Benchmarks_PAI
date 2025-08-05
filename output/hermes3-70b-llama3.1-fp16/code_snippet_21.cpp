#include <iostream>

int sum(int a, int b) {
    return a + b;
}

int main() {
    int result = sum(5, 7);
    std::cout << result << std::endl;
    return 0;
}