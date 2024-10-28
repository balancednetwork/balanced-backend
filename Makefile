.PHONY: test help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

test: up-dbs test-unit test-integration  ## Run all tests

up-dbs:  ## Bring up the DBs
	docker compose -f docker-compose.db.yml up -d
	sleep 5
	cd balanced_backend && PYTHONPATH=$PYTHONPATH:`pwd`/.. alembic upgrade head

down-dbs:  ## Take down the DBs
	docker compose -f docker-compose.db.yml down

test-unit:  ## Run unit tests
	python3 -m pytest tests/unit

test-integration:  ## Run integration tests - Need DB compose up
	python3 -m pytest tests/integration

up:  ## Bring everything up as containers
	docker compose -f docker-compose.db.yml -f docker-compose.yml up -d

down:  ## Take down all the containers
	docker compose -f docker-compose.db.yml -f docker-compose.yml down

clean:  ## Clean all the containers and volumes
	docker volume rm $(docker volume ls -q)

build:  ## Build everything
	docker compose build

ps:  ## List all containers and running status
	docker compose -f docker-compose.db.yml -f docker-compose.yml ps

postgres-console:  ## Start postgres terminal
	docker compose -f docker-compose.db.yml -f docker-compose.yml exec postgres psql -U postgres

# install-streaming -> Not used right now
install: install-common install-api install-cron install-dev  ## Install all deps

install-common:
	pip install --upgrade -r requirements-common.txt
install-api:
	pip install --upgrade -r requirements-api.txt
install-cron:
	pip install --upgrade -r requirements-cron.txt
install-streaming:
	pip install --upgrade -r requirements-streaming.txt
install-dev:
	pip install --upgrade -r requirements-dev.txt
