using System;
using System.Linq;

public class Program
{
    public static int SumPositiveNumbers(int[] arr)
    {
        return arr.Where(num => num > 0).Sum();
    }

    public static void Main()
    {
        int[] numbers = { -1, 2, -3, 4 };
        Console.WriteLine(SumPositiveNumbers(numbers)); // Output: 6
    }
}