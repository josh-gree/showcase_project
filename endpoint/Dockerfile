FROM golang:1

RUN mkdir /app 
ADD ./src /app/
WORKDIR /app 
RUN go build -o main .
CMD ["./main"]