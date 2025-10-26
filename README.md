# X API - Automated Tweet Posting

Post tweets with images to X (Twitter) using Docker and Python.

## Prerequisites

- Docker and Docker Compose installed
- X (Twitter) Developer Account with an app created

## Setup

### 1. Configure X Developer Portal

1. Go to [X Developer Portal](https://developer.x.com/en/portal/dashboard)
2. Create an app or select your existing app
3. Go to **User authentication settings** → **Set up**
4. Configure authentication:
   - **App permissions**: Select **"Read and Write"**
   - **Type of App**: Select **"Web App, Automated App or Bot"**
   - **Callback URI**: `http://localhost:3000/callback` (placeholder)
   - **Website URL**: Your website URL
5. Save settings
6. Go to **Keys and tokens** tab
7. **Regenerate** Access Token and Access Token Secret (important!)
8. Copy all credentials:
   - API Key (Consumer Key)
   - API Key Secret (Consumer Secret)
   - Access Token
   - Access Token Secret
   - Bearer Token (optional)
   - Client ID (optional, for OAuth 2.0)
   - Client Secret (optional, for OAuth 2.0)

### 2. Configure Application

1. Copy the template config:
   ```bash
   cp config.template.json config.json
   ```
2. Edit `config.json` and fill in your credentials from the X Developer Portal
3. Build the Docker image:
   ```bash
   make build
   ```

**Important**: Make sure your Access Token was generated AFTER setting permissions to "Read and Write". Old tokens won't work even if you change permissions later.

## Usage

### Post a tweet (text only)
```bash
make post TEXT="Hello, world!"
```

### Post a tweet with an image
```bash
make post TEXT="Check out this image!" IMAGE=images/photo.jpg
```

Place your images in the `images/` directory before referencing them.

## File Structure

- `config.json` - API credentials (keep this secure, not in git!)
- `config.template.json` - Template for config.json
- `post.py` - Python script for posting tweets
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Docker Compose setup
- `Makefile` - Convenient commands
- `images/` - Place your images here
- `.gitignore` - Excludes config.json from git

## Other Commands

- `make build` - Build Docker image
- `make clean` - Clean up containers and images
- `make help` - Show all available commands
