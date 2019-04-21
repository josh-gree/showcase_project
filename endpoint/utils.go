package main

import (
	"fmt"
	"math"
	"math/rand"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type KafkaMsg struct {
	route         string
	response_time time.Duration
}

type NormParams struct {
	mu    float64
	sigma float64
}

type Group struct {
	id     int
	params NormParams
}

var groups = []Group{
	{id: 1, params: NormParams{mu: 1.2, sigma: 0.1}},
	{id: 2, params: NormParams{mu: 9.4, sigma: 2.3}},
	{id: 3, params: NormParams{mu: 5.1, sigma: 0.3}},
}

func SetupRouter() *gin.Engine {
	router := gin.Default()
	router.Use(KafkaMiddleware())
	router.GET("/", RouteHandler)
	return router
}

func RouteHandler(c *gin.Context) {
	// choose a random group
	seed := time.Now().UTC().UnixNano()
	grp := groups[rand.Intn(len(groups))]
	params := grp.params

	// get wait duration and wait
	duration := RandomDuration(params, seed)
	time.Sleep(duration)

	// return
	c.JSON(http.StatusOK, gin.H{"message": "success"})
}

func RandomDuration(params NormParams, seed int64) time.Duration {
	rand.Seed(seed)
	normal_draw := math.Abs(rand.NormFloat64()*params.sigma + params.mu)
	duration := time.Duration(normal_draw*1000) * time.Millisecond
	return duration
}

func KafkaMiddleware() gin.HandlerFunc {
	out := gin.DefaultWriter
	return func(c *gin.Context) {
		t := time.Now()

		c.Next()

		response_time := time.Since(t)
		route := c.Request.URL.Path
		msg := KafkaMsg{route: route, response_time: response_time}
		fmt.Fprintf(out, "From kafka middleware - %+v\n", msg)
	}
}
