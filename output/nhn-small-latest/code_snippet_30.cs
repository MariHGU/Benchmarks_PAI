using System;

class Program {
    static int Factorial(int n) {
        if (n <= 1) return 1;
        return n * Factorial(n - 1);
    }

    static void Main() {
        Console.WriteLine($"Factorial of 5 is {Factorial(5)}");
    }
}