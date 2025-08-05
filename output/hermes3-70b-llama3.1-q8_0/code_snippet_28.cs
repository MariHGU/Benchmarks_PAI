using System;

class Program
{
    static int Factorial(int n)
    {
        if (n == 0)
            return 1;
        else
            return n * Factorial(n - 1);
    }

    static void Main(string[] args)
    {
        Console.WriteLine(Factorial(5)); // Output: 120
    }
}