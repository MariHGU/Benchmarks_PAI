public class Program {
    public static int Factorial(int n) {
        if (n == 0 || n == 1) return 1;
        return n * Factorial(n - 1);
    }

    public static void Main(string[] args) {
        Console.WriteLine(Factorial(5)); // Output: 120
    }
}