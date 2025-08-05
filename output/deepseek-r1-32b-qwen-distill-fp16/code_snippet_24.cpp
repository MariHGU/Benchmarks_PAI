#include <iostream>

int SumOfEvenSquares(int n) {
    int sum = 0;
    for (int i = 1; i <= n; ++i) {
        if (i % 2 == 0) {
            sum += i * i;
        }
    }
    return sum;
}

int main() {
    std::cout << SumOfEvenSquares(4) << std::endl; // Output: 20
    return 0;
}