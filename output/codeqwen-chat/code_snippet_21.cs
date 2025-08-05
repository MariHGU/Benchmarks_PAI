using System;

class Program {
    static void Main() {
        string string1 = "Hello";
        string string2 = "olleH";
        Console.WriteLine(CompareLanguages(string1, string2)); // => "Ruby"

        string2 = "olleh";
        Console.WriteLine(CompareLanguages(string1, string2)); // => "Python"

        string2 = "llHe";
        Console.WriteLine(CompareLanguages(string1, string2)); // => "C++"

        string2 = "olleo";
        Console.WriteLine(CompareLanguages(string1, string2)); // => "Java"
    }

    static string CompareLanguages(string string1, string string2) {
        if (string1 == string2) return "Ruby";
        else if (new String(string2.Reverse().ToArray()) == string1) return "Python";
        else if (string1.Substring(0, string1.Length - 1) == string2 && string1[string1.Length - 1] != string2[string2.Length - 1]) return "C++";
        else if (new String(string1.Reverse().ToArray()) == string2) return "Java";
        return "";
    }
}