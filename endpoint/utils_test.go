package main

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestSetupRouter(t *testing.T) {
	// probably overkill but learning tests
	r := SetupRouter()
	routes := r.Routes()

	expected_num_routes := 1
	assert.Equal(t, len(routes), expected_num_routes)
	// not sure how to test the handler is correct!?
	route := routes[0]
	expected_method := "GET"
	expected_path := "/"

	assert.Equal(t, route.Method, expected_method)
	assert.Equal(t, route.Path, expected_path)
}

func TestRouteHandler(t *testing.T) {
	r := SetupRouter()
	w := httptest.NewRecorder()
	req, _ := http.NewRequest("GET", "/", nil)
	r.ServeHTTP(w, req)
	assert.Equal(t, 200, w.Code)
	assert.Equal(t, `{"message":"success"}`, w.Body.String())
}
