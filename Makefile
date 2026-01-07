.PHONY: post video build up down logs clean

# Post images to X (Twitter)
post:
	docker compose run --rm x-api

# Post video to X (Twitter)
video:
	VIDEO_MODE=true docker compose run --rm x-api

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
	@echo "  make post      - Post images to X (Twitter)"
	@echo "  make video     - Post video to X (Twitter)"
	@echo "  make build     - Build Docker image"
	@echo "  make up        - Start service"
	@echo "  make down      - Stop service"
	@echo "  make logs      - View logs"
	@echo "  make clean     - Clean up containers and images"
