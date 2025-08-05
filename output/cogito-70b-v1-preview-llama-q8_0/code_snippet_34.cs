// C#
public class MathOperations
{
    public static long Factorial(int n)
    {
        if (n == 0) return 1;
        
        long result = 1;
        for (int i = 1; i <= n; i++)
        {
            result *= i;
        }
        return result;
    }

    // Alternative implementation with recursion
    public static long FactorialRecursive(int n)
    {
        if (n == 0) return 1;
        return n * FactorialRecursive(n - 1);
    }
}