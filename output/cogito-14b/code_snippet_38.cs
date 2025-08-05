using System;

public class Program {
    public static void PrintHelloAndNumbers() {
        Console.WriteLine("Hello, World!");
        for (int i = 1; i <= 5; i++) {
            Console.WriteLine(i);
        }
    }

    // Call the function
    public static void Main(string[] args) {
        PrintHelloAndNumbers();
    }
}