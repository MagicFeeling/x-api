.PHONY: post build up down logs clean

# Post a tweet (with optional image)
# Usage: make post TEXT="Your tweet text" IMAGE=path/to/image.jpg
# Or: make post TEXT="Your tweet text" (without image)
post:
	@if [ -z "$(TEXT)" ]; then \
		echo "Error: TEXT is required. Usage: make post TEXT=\"Your tweet text\" [IMAGE=path/to/image.jpg]"; \
		exit 1; \
	fi; \
	docker compose run --rm \
		-e TWEET_TEXT="$(TEXT)" \
		-e IMAGE_PATH="$(IMAGE)" \
		x-api

# Build the Docker image
build:
	docker compose build

# Start the service in detached mode
up:
	docker compose up -d

# Stop the service
down:
	docker compose down

# View logs
logs:
	docker compose logs -f

# Clean up containers and images
clean:
	docker compose down -v
	docker rmi x-api_x-api 2>/dev/null || true

# Help
help:
	@echo "Available commands:"
	@echo "  make post TEXT=\"tweet\" [IMAGE=path]  - Post a tweet with optional image"
	@echo "  make build                            - Build Docker image"
	@echo "  make up                               - Start service"
	@echo "  make down                             - Stop service"
	@echo "  make logs                             - View logs"
	@echo "  make clean                            - Clean up containers and images"
