package main

import (
	"fmt"
	"os"
)

func main() {
	var variables []string = os.Environ()
	var i int
	for i = 0; i < len(variables); i++ {
		fmt.Println(variables[i])
	}
}
