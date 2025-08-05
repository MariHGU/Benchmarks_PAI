package main

import "fmt"

// Function with traditional loop
func calculateSum(n int) int {
    if n <= 0 {
        return 0
    }
    
    sum := 0
    for i := 1; i <= n; i++ {
        sum += i
    }
    return sum
}

// Alternative using channels (Go's concurrent approach)
func calculateSumConcurrent(n int) chan int {
    result := make(chan int)
    
    go func() {
        if n <= 0 {
            result <- 0
            return
        }
        
        sum := 0
        for i := 1; i <= n; i++ {
            sum += i
        }
        result <- sum
    }()
    
    return result
}