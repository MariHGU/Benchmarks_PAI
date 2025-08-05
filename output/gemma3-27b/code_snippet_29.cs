using System;

public class FactorialCalculator
{
    public static long Factorial(int n)
    {
        if (n == 0)
        {
            return 1;
        }
        else
        {
            return n * Factorial(n - 1);
        }
    }

    public static void Main(string[] args)
    {
        Console.WriteLine(Factorial(5)); // Output: 120
    }
}