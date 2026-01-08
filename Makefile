.PHONY: post preview blurred build up down logs clean

# Post images to X (Twitter)
post:
	docker compose run --rm x-api

# Post preview video to X (Twitter)
preview:
	VIDEO_MODE=true VIDEO_SELECT=preview docker compose run --rm x-api

# Post blurred video to X (Twitter)
blurred:
	VIDEO_MODE=true VIDEO_SELECT=blurred docker compose run --rm x-api

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
	@echo "  make preview   - Post preview video to X (Twitter)"
	@echo "  make blurred   - Post blurred video to X (Twitter)"
	@echo "  make build     - Build Docker image"
	@echo "  make up        - Start service"
	@echo "  make down      - Stop service"
	@echo "  make logs      - View logs"
	@echo "  make clean     - Clean up containers and images"
