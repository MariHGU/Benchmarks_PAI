package main

import "fmt"

func factorial(n int) int {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

// Example usage:
func main() {
    fmt.Println(factorial(5))  // Output: 120
}