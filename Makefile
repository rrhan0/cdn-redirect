
dev-setup:
	pip3 install -r requirements.txt

docker-build:
	docker-compose build

docker-up:
	docker-compose up

docker-down:
	docker-compose down

docker-ssh:
	docker exec -it cdn-redirect /bin/bash

health:
	@curl localhost:8080/healthcheck

run:
	@python3 app.py

run-test:
	@pytest tests/app.py