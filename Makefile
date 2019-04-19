all:

pull:
	BRANCH=`git rev-parse --abbrev-ref HEAD` docker-compose pull
up:
	BRANCH=`git rev-parse --abbrev-ref HEAD` docker-compose up -d
down: 
	BRANCH=`git rev-parse --abbrev-ref HEAD` docker-compose down -v
logs:
	docker-compose logs