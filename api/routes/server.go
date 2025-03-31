package routes

import (
	"github.com/gin-gonic/gin"
)

type Server struct {
	Router *gin.Engine
}

func NewServer() Server {
	return Server{
		Router: gin.Default(),
	}
}

func (s Server) Start() {
	freeRoutes := s.Router.Group("")
	freeRoutes.GET("/hello")
	s.Router.Run()
}
