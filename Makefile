all:

pull:
	docker-compose pull
build:
	docker-compose build
up:
	docker-compose up -d
down: 
	docker-compose down -v
logs:
	docker-compose logs