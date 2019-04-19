FROM golang:stretch as base
RUN curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh && which dep
RUN mkdir -p $GOPATH/src/github.com/joshgree/endpoint
ADD ./src $GOPATH/src/github.com/joshgree/endpoint
WORKDIR $GOPATH/src/github.com/joshgree/endpoint
RUN dep init

FROM golang:stretch as tester
COPY --from=base $GOPATH $GOPATH
WORKDIR $GOPATH/src/github.com/joshgree/endpoint
RUN go test -v

FROM golang:stretch as builder
COPY --from=base $GOPATH $GOPATH
WORKDIR $GOPATH/src/github.com/joshgree/endpoint
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-extldflags "-static"' -o /main .

FROM scratch
COPY --from=builder /main /app/
WORKDIR /app
CMD ["./main"]