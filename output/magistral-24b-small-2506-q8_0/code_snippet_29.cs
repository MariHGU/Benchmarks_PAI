// C#
using System;

public class Program
{
    public static long? Factorial(int n)
    {
        if (n < 0) return null;
        long result = 1;
        for (int i = 2; i <= n; i++)
        {
            result *= i;
        }
        return result;
    }

    public static void Main()
    {
        Console.WriteLine(Factorial(5));
    }
}