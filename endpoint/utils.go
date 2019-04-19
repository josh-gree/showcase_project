package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func SetupRouter() *gin.Engine {
	router := gin.Default()
	router.GET("/", RouteHandler)
	return router
}

func RouteHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "success"})
}
