package main

import (
    "fmt"
    "errors"
)

func factorial(n int) (int, error) {
    if n < 0 {
        return 0, errors.New("factorial is not defined for negative numbers")
    }
    
    if n == 0 || n == 1 {
        return 1, nil
    }
    
    result, err := factorial(n - 1)
    if err != nil {
        return 0, err
    }
    
    return n * result, nil
}

// Usage
func main() {
    result, _ := factorial(5)
    fmt.Println(result) // Output: 120
}