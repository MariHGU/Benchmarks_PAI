int factorial(int n) {
    if (n <= 1)
        return 1;
    else
        return n * factorial(n - 1);
}

// Usage
#include <iostream>
using namespace std;

int main() {
    cout << factorial(5);  // Output: 120
    return 0;
}