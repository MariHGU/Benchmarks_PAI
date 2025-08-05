public static int Factorial(int n)
{
    if (n <= 1)
        return 1;
    else
        return n * Factorial(n - 1);
}

// Usage
Console.WriteLine(Factorial(5));  // Output: 120