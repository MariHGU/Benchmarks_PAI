// C++
#include <cstdint>

class MathOperations {
public:
    static int64_t factorial(int n) {
        if (n == 0) return 1;
        
        int64_t result = 1;
        for (int i = 1; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    // Alternative implementation with recursion
    static int64_t factorialRecursive(int n) {
        if (n == 0) return 1;
        return n * factorialRecursive(n - 1);
    }
};