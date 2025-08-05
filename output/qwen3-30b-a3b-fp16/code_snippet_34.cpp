#include <iostream>
using namespace std;

int Factorial(int n) {
    if (n == 0)
        return 1;
    int result = 1;
    for (int i = 1; i <= n; i++)
        result *= i;
    return result;
}

// Example usage
int main() {
    cout << Factorial(5) << endl;  // Output: 120
    return 0;
}