package main

import "github.com/gym-weight-tracker/api/routes"

func main() {
	routes.NewServer().Start()
}
