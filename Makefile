# Variables
COMPOSE = docker compose

# Load .env file if it exists to get DB credentials, etc.
ifneq (,$(wildcard .env))
	include .env
	export
endif

# Colors for help menu
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

.PHONY: help up down build restart logs ps exec-backend exec-frontend exec-db migrate makemigrations createsuperuser shell local-up local-run local-setup local-migrate local-makemigrations local-createsuperuser clean-docker clean-pyc

help: ## Show this help message
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  ${YELLOW}%-25s${RESET} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

## Docker Compose Stack:
up: ## Start all services in the background (Docker Compose)
	$(COMPOSE) up -d

down: ## Stop and remove all containers, networks
	$(COMPOSE) down

build: ## Build or rebuild all Docker images
	$(COMPOSE) build

restart: ## Restart all services
	$(COMPOSE) restart

logs: ## Tail logs for all containers
	$(COMPOSE) logs -f

ps: ## View the status of all services
	$(COMPOSE) ps

## Container Execution:
exec-backend: ## Access the shell inside backend container
	$(COMPOSE) exec backend sh

exec-frontend: ## Access the shell inside frontend container
	$(COMPOSE) exec frontend sh

exec-db: ## Connect to PostgreSQL database shell inside container
	$(COMPOSE) exec db psql -U $${POSTGRES_USER:-postgres} -d $${POSTGRES_DB:-iiol}

## Django Management (Docker Compose):
migrate: ## Run Django database migrations in the backend container
	$(COMPOSE) exec backend python manage.py migrate

makemigrations: ## Create new Django migrations in the backend container
	$(COMPOSE) exec backend python manage.py makemigrations

createsuperuser: ## Create a Django superuser in the backend container
	$(COMPOSE) exec backend python manage.py createsuperuser

shell: ## Open Django python shell inside backend container
	$(COMPOSE) exec backend python manage.py shell

## Hybrid / Local Development (DB/Redis in Docker, Apps locally):
local-up: ## Start only DB and Redis containers
	$(COMPOSE) up -d db redis

local-run: ## Run hybrid setup locally (runs DB/Redis in Docker, runs Frontend & Backend locally via run_local.sh)
	chmod +x run_local.sh
	./run_local.sh

local-setup: ## Initial local environment setup (create venv, install Python & npm dependencies)
	@if [ ! -f .env ]; then \
		echo "Copying .env.example to .env..."; \
		cp .env.example .env; \
	fi
	@if [ ! -d "venv" ]; then \
		echo "Creating python venv..."; \
		python3 -m venv venv; \
	fi
	@echo "Installing python requirements..."
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r iiol/requirements/common.txt
	@echo "Installing npm dependencies in frontend..."
	npm install --prefix frontend
	@echo "Setup completed successfully!"

local-migrate: ## Run Django migrations locally (using local venv)
	./venv/bin/python iiol/manage.py migrate

local-makemigrations: ## Run Django makemigrations locally (using local venv)
	./venv/bin/python iiol/manage.py makemigrations

local-createsuperuser: ## Create Django superuser locally (using local venv)
	./venv/bin/python iiol/manage.py createsuperuser

## Cleanup:
clean-docker: ## Stop Docker containers and delete database/redis volumes (Warning: resets db)
	$(COMPOSE) down -v

clean-pyc: ## Delete Python cache files (.pyc, __pycache__)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
