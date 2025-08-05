using System;

public class Program
{
    public static long Factorial(int n)
    {
        if (n <= 1)
            return 1;
        else
            return n * Factorial(n - 1);
    }

    // Example usage:
    public static void Main()
    {
        Console.WriteLine(Factorial(5));  // Output: 120
    }
}