#include <iostream>
#include <vector>

int sumPositiveNumbers(const std::vector<int>& arr) {
    int sum = 0;
    for (int num : arr) {
        if (num > 0) {
            sum += num;
        }
    }
    return sum;
}

int main() {
    std::vector<int> numbers = { -1, 2, -3, 4 };
    std::cout << sumPositiveNumbers(numbers) << std::endl; // Output: 6
    return 0;
}