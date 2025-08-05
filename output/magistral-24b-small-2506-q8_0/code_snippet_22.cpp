#include <iostream>
   #include <optional>

   std::optional<long long> factorial(int n) {
       if (n < 0) return std::nullopt;
       long long result = 1;
       for (int i = 2; i <= n; ++i) {
           result *= i;
       }
       return result;
   }

   int main() {
       auto res = factorial(5);
       if (res) {
           std::cout << *res << std::endl;
       } else {
           std::cout << "Invalid input" << std::endl;
       }
       return 0;
   }