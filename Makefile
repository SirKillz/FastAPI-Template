up:
	docker-compose -f docker/docker-compose.yml build
	docker-compose -f docker/docker-compose.yml up -d

down:
	docker-compose -f docker/docker-compose.yml down

destroy-database:
	docker-compose -f docker/docker-compose.yml down
	docker volume rm -f fastapi_template_db_data

connect-db:
	docker exec -it postgres-db psql -U app_user -d app_db
