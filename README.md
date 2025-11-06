# RoastMaster AI

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

An extremely vulgar AI-powered roast generator that delivers brutally honest, sadistic insults. Enter any name and get verbally demolished by cutting-edge AI technology using the "evil" model.

![RoastMaster AI](https://roast.bimoarifw.me/static/ogimage.png)


## Disclaimer

Look, this ain't your grandma's polite AI. This thing spits out roasts so nasty they'll make you wanna crawl under a rock and die. We're talkin' full-on profanity, personal attacks that'll hit you where it hurts, and enough psychological damage to fund a therapist's vacation. The AI's got no chill - it's programmed to be a total a--hole with zero mercy. If you're the type who gets triggered by mean words or pretends to have feelings, stay the f--- away. You've been warned, princess.

## Live Demo

Visit [roast.bimoarifw.me](https://roast.bimoarifw.me) to try it out!

## Installation

### Prerequisites
- Docker & Docker Compose
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/bimoarifw/roast.git
   cd roast
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Pollinations AI API key
   ```

3. **Launch with Docker**
   ```bash
   docker compose up -d --build
   ```

4. **Access the app**
   - Web UI: http://127.0.0.1:8787
   - API Docs: http://127.0.0.1:8787/docs

## Usage

### Web Interface
1. Open http://127.0.0.1:8787
2. Enter a name in the input field
3. Click "Roast" and prepare for verbal annihilation!

### API Usage

#### POST Endpoint
**Endpoint**: `POST /api/roast`

**Request**:
```json
{
  "name": "John Doe"
}
```

**Response**:
```json
{
  "roast": "John Doe, you're such a worthless piece of shit that even garbage looks down on you."
}
```

**Example with curl**:
```bash
curl -X POST http://127.0.0.1:8787/api/roast \
  -H "Content-Type: application/json" \
  -d '{"name": "Budi"}'
```

#### GET Endpoint
**Endpoint**: `GET /api/{name}`

**Example**:
```bash
curl http://127.0.0.1:8787/api/John%20Doe
```

## Configuration

### Environment Variables
- `POLLINATIONS_API_KEY`: Your Pollinations AI API key (required)

### Port Configuration
- App: 8787 (bound to 127.0.0.1)
- Redis: 6379 (internal), 6380 (external)

## Development

### Local Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run Redis
docker run -d -p 6379:6379 redis:alpine

# Start the app
uvicorn main:app --reload --host 0.0.0.0 --port 8787

# Start Celery worker
celery -A tasks.celery_app worker --loglevel=info
```


## Acknowledgments

- [Pollinations AI](https://pollinations.ai/) for the AI roasting engine
- [Semantic UI](https://semantic-ui.com/) for the beautiful UI components
- [FastAPI](https://fastapi.tiangolo.com/) for the robust backend framework

---

**Made with hate and a dash of venom by [bimoarifw](https://bimoarifw.me)**