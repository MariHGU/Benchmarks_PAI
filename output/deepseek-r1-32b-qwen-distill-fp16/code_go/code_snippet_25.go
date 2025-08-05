package main

import "fmt"

func SumOfEvenSquares(n int) int {
    sum := 0
    for i := 1; i <= n; i++ {
        if i%2 == 0 {
            sum += i * i
        }
    }
    return sum
}

func main() {
    fmt.Println(SumOfEvenSquares(4)) // Output: 20
}