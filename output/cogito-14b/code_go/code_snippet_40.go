package main

import "fmt"

func printHelloAndNumbers() {
    fmt.Println("Hello, World!")
    for i := 1; i <= 5; i++ {
        fmt.Println(i)
    }
}

// Call the function
func main() {
    printHelloAndNumbers()
}