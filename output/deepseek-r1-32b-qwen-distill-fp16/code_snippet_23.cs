using System;

class Program
{
    static int SumOfEvenSquares(int n)
    {
        int sum = 0;
        for (int i = 1; i <= n; i++)
        {
            if (i % 2 == 0)
            {
                sum += i * i;
            }
        }
        return sum;
    }

    static void Main()
    {
        Console.WriteLine(SumOfEvenSquares(4)); // Output: 20
    }
}