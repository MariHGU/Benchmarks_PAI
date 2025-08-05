// Go
package main

import (
    "errors"
    "fmt"
)

func factorial(n int) (int64, error) {
    if n < 0 {
        return 0, errors.New("negative input")
    }
    result := int64(1)
    for i := 2; i <= n; i++ {
        result *= int64(i)
    }
    return result, nil
}

func main() {
    res, err := factorial(5)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println(res)
    }
}