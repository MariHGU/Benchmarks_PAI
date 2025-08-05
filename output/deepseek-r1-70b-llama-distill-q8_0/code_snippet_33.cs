using System.Linq;

public class Program {
    public static int SumEvenNumbers(int[] array) {
        return array.Where(num => num % 2 == 0).Sum();
    }
}