all:

pull:
	BRANCH=`git rev-parse --abbrev-ref HEAD` docker-compose pull
build:
	BRANCH=`git rev-parse --abbrev-ref HEAD` docker-compose build
up:
	BRANCH=`git rev-parse --abbrev-ref HEAD` docker-compose up -d
down: 
	BRANCH=`git rev-parse --abbrev-ref HEAD` docker-compose down -v
logs:
	docker-compose logs -f

endpoint-run-local:
	go run endpoint/{main.go,utils.go}
endpoint-test-local:
	pushd endpoint && go test -v && popd
endpoint-build:
	pushd endpoint && dep ensure -update -v && popd
	docker build -t joshgree/endpoint:`git rev-parse --abbrev-ref HEAD` endpoint

requests-build:
	docker build -t joshgree/requests:`git rev-parse --abbrev-ref HEAD` requests

kafka-view-response-time-topic:
	docker-compose exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic response-time-per-route --from-beginning