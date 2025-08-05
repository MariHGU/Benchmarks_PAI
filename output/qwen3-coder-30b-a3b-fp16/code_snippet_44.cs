using System;

public static class MathUtils
{
    public static long Factorial(int n)
    {
        if (n < 0)
            throw new ArgumentException("Factorial is not defined for negative numbers");
        
        if (n == 0 || n == 1)
            return 1;
        
        return n * Factorial(n - 1);
    }
}

// Usage
Console.WriteLine(MathUtils.Factorial(5)); // Output: 120