public class Calculator
{
    public static int CalculateSum(int n)
    {
        if (n <= 0) return 0;
        
        // Using LINQ
        return Enumerable.Range(1, n).Sum();
        
        // Alternative manual implementation
        /*
        int sum = 0;
        for (int i = 1; i <= n; i++)
        {
            sum += i;
        }
        return sum;
        */
    }
}