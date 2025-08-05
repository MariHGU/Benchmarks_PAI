package main

import "fmt"

func factorial(n int) int {
    if n == 0 {
        return 1
    }
    result := 1
    for i := 1; i <= n; i++ {
        result *= i
    }
    return result
}

func main() {
    fmt.Println(factorial(5))  // Output: 120
}