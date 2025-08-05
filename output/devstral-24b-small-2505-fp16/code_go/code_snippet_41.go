package main

import (
    "fmt"
)

func sumPositiveNumbers(arr []int) int {
    sum := 0
    for _, num := range arr {
        if num > 0 {
            sum += num
        }
    }
    return sum
}

func main() {
    numbers := []int{-1, 2, -3, 4}
    fmt.Println(sumPositiveNumbers(numbers)) // Output: 6
}