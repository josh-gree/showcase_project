FROM golang:alpine as builder
RUN mkdir /build
ADD ./src /build/
WORKDIR /build 
RUN go build -o main .

FROM alpine
COPY --from=builder /build/main /app/
WORKDIR /app
CMD ["./main"]