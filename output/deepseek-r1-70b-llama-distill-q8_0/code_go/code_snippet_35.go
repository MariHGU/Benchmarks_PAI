package main

import "fmt"

func sumEvenNumbers(arr []int) int {
    sum := 0
    for _, num := range arr {
        if num % 2 == 0 {
            sum += num
        }
    }
    return sum
}