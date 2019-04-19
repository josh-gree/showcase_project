all:

pull:
	BRANCH=`git rev-parse --abbrev-ref HEAD` docker-compose pull
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
	docker build -t joshgree/endpoint:`git rev-parse --abbrev-ref HEAD` endpoint