// C#
public static class MathUtils
{
    public static long Factorial(int n)
    {
        if (n <= 1)
            return 1;
        
        return n * Factorial(n - 1);
    }
}

// Usage example:
Console.WriteLine(MathUtils.Factorial(5)); // Output: 120