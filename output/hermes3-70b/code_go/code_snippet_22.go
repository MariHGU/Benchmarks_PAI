package main

import "fmt"

func addNumbers(a int, b int) int {
    return a + b
}

func main() {
    result := addNumbers(5, 3)
    fmt.Println(result)  // Output: 8
}