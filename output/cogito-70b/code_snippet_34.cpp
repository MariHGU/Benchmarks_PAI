// C++
class MathUtils {
public:
    static long factorial(int n) {
        if (n <= 1)
            return 1;
        
        return n * factorial(n - 1);
    }
};

// Usage example:
std::cout << MathUtils::factorial(5) << std::endl; // Output: 120