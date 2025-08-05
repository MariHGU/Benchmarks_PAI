#include <iostream>
#include <algorithm>
#include <string>

std::string compare_languages(const std::string& string1, const std::string& string2) {
    if (string1 == string2) return "Ruby";
    else if (string1 == std::string(string2.rbegin(), string2.rend())) return "Python";
    else if (string1.substr(0, string1.size() - 1) == string2 && string1[string1.size() - 1] != string2[string2.size() - 1]) return "C++";
    else if (std::equal(string1.rbegin(), string1.rend(), string2.begin())) return "Java";
    return "";
}

int main() {
    std::string string1 = "Hello";
    std::string string2 = "olleH";
    std::cout << compare_languages(string1, string2) << std::endl; // => "Ruby"

    string2 = "olleh";
    std::cout << compare_languages(string1, string2) << std::endl; // => "Python"

    string2 = "llHe";
    std::cout << compare_languages(string1, string2) << std::endl; // => "C++"

    string2 = "olleo";
    std::cout << compare_languages(string1, string2) << std::endl; // => "Java"

    return 0;
}