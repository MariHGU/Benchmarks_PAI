package main

import "fmt"

func Factorial(n int) int {
    if n == 0 {
        return 1
    }
    result := 1
    for i := 1; i <= n; i++ {
        result *= i
    }
    return result
}

// Example usage
func main() {
    fmt.Println(Factorial(5))  // Output: 120
}