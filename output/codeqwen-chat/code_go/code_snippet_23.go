package main

import (
	"fmt"
	"strings"
)

func compareLanguages(string1, string2 string) string {
	if string1 == string2 {
		return "Ruby"
	} else if string1 == reverseString(string2) {
		return "Python"
	} else If (substring(string1, 0, len(string1)-1) == string2 && string1[len(string1)-1] != string2[len(string2)-1]) {
		return "C++"
	} else If reverseString(string1) == string2 {
		return "Java"
	}
	return ""
}

func reverseString(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func substring(s string, start, end int) string {
	if start < 0 || end > len(s) || start > end {
		panic("Invalid substring range")
	}
	return s[start:end]
}

func main() {
	string1 := "Hello"
	string2 := "olleH"
	fmt.Println(compareLanguages(string1, string2)) // => "Ruby"

	string2 = "olleh"
	fmt.Println(compareLanguages(string1, string2)) // => "Python"

	string2 = "llHe"
	fmt.Println(compareLanguages(string1, string2)) // => "C++"

	string2 = "olleo"
	fmt.Println(compareLanguages(string1, string2)) // => "Java"
}