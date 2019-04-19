package main

import (
	"fmt"
)

func main() {
	router := SetupRouter()
	fmt.Printf("%+v\n", router.Routes())
	router.Run(":80")
}
