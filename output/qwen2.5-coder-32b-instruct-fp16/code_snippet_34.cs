using System;

class Program {
    static long Factorial(int n) {
        if (n == 0) return 1;
        long result = 1;
        for (int i = 1; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    static void Main() {
        Console.WriteLine(Factorial(5)); // Output: 120
    }
}