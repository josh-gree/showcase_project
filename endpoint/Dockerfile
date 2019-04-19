FROM golang:stretch as build_test
RUN curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh && which dep
RUN mkdir -p $GOPATH/src/app
ADD . $GOPATH/src/app
WORKDIR $GOPATH/src/app
RUN dep ensure
RUN go test -v
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -ldflags '-extldflags "-static"' -o /main .

FROM scratch
COPY --from=build_test /main /app/
WORKDIR /app
CMD ["./main"]