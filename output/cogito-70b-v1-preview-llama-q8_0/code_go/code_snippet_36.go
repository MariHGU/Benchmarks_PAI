// Go
package main

import "fmt"

func Factorial(n int) int64 {
    if n == 0 {
        return 1
    }
    
    result := int64(1)
    for i := 1; i <= n; i++ {
        result *= int64(i)
    }
    return result
}

// Alternative implementation with recursion
func FactorialRecursive(n int) int64 {
    if n == 0 {
        return 1
    }
    return int64(n) * FactorialRecursive(n-1)
}