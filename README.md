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

The script reads caption text and image paths from `config.json`. The config is automatically updated by the image generation workflow.

### Post a tweet
```bash
make post
```

This will:
1. Load the caption from the file specified in `config.json` (`caption.file`)
2. Load images from `media.sfw_file` and/or `media.nsfw_file`
3. Post to X with the caption and images

### Configuration Structure

The `config.json` file should contain:
- `project_folder` - Base path to the project folder
- `caption.file` - Relative path to caption text file (e.g., `Prompts/socialmedia.txt`)
- `media.sfw_file` - Path to SFW image
- `media.nsfw_file` - Path to NSFW image

These fields are automatically populated by the `image_prompt_generator_openai.py` and `add_text_to_image.py` scripts.

## File Structure

- `config.json` - API credentials and posting configuration (keep this secure, not in git!)
- `config.template.json` - Template for config.json
- `post.py` - Python script for posting tweets
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Docker Compose setup
- `Makefile` - Convenient commands
- `.gitignore` - Excludes config.json from git

## Other Commands

- `make build` - Build Docker image
- `make clean` - Clean up containers and images
- `make help` - Show all available commands
