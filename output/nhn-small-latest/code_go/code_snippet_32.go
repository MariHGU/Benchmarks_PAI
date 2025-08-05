package main

import (
    "fmt"
)

func factorial(n int) int {
    if n <= 1 {
        return 1
    }
    return n * factorial(n-1)
}

func main() {
    fmt.Printf("Factorial of 5 is %d\n", factorial(5))
}