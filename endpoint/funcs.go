package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func RouteHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "success"})
}

func Add(a int, b int) int {
	return a + b
}
