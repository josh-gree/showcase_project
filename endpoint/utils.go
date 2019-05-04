package main

import (
	"context"
	"encoding/json"
	"fmt"
	"math"
	"math/rand"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	kafka "github.com/segmentio/kafka-go"
)

type KafkaMsg struct {
	Route            string
	ResponseTime     time.Duration
	RequestTimeStamp string
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
	{id: 1, params: NormParams{mu: 5.1, sigma: 1}},
	{id: 2, params: NormParams{mu: 19.4, sigma: 2}},
	{id: 3, params: NormParams{mu: 10.1, sigma: 3}},
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

var writer = kafka.NewWriter(kafka.WriterConfig{
	Brokers:  []string{"broker:9092"},
	Topic:    "response-time-per-route",
	Balancer: &kafka.LeastBytes{},
})

func KafkaMiddleware() gin.HandlerFunc {
	out := gin.DefaultWriter
	return func(c *gin.Context) {
		request_time := time.Now()

		c.Next()

		response_time := time.Since(request_time)
		route := c.Request.URL.Path
		msg := KafkaMsg{Route: route, ResponseTime: response_time, RequestTimeStamp: request_time.Format(time.RFC3339)}
		json_msg, err := json.Marshal(msg)
		if err != nil {
			fmt.Println(err)
		}
		fmt.Fprintf(out, "From kafka middleware - %s\n", json_msg)

		writer.WriteMessages(context.Background(),
			kafka.Message{
				Key:   []byte("reponse-time-and-route"),
				Value: []byte(json_msg),
			},
		)
	}
}
