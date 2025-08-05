package main

import "math"

func sumOfSquares(numbers []float64) float64 {
    var sum float64 = 0
    for _, n := range numbers {
        sum += math.Pow(n, 2)
    }
    return sum
}