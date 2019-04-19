package main

import "testing"

func TestAdd(t *testing.T) {
	total := Add(5, 6)
	if total != 11 {
		t.Errorf("Sum was incorrect, got: %d, want: %d.", total, 10)
	}
}
