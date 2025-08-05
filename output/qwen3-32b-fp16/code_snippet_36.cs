using System.Collections.Generic;
using System.Linq;

public class MathUtils 
{
    public static double SumOfSquares(List<double> numbers) 
    {
        return numbers.Select(n => n * n).Sum();
    }
}