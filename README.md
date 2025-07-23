# Avatar: The Last Bot Bender

This is a multi-container application that hosts our Avatar the Last Airbender themed Discord bot.

## Architecture

The application consists of three main Docker containers:

- **game-engine** - FastAPI backend service that handles game logic and database operations
- **discord-bot** - Discord bot that interfaces with users and communicates with the game engine
- **website** - Web frontend for the application
- **postgres** - PostgreSQL database for persistent data storage

## Development Setup

### Prerequisites
- Docker and Docker Compose installed

### Building and Running

1. **Build the game engine:**
   ```bash
   docker compose build game-engine
   ```

2. **Start the services:**
   ```bash
   docker compose up postgres game-engine
   ```

3. **Test the game engine:**
   The game engine runs on port 3000. Test endpoints using curl:
   ```bash
   curl http://localhost:3000/ping
   curl http://localhost:3000/health
   curl http://localhost:3000/characters
   curl http://localhost:3000/migrations
   ```

### Available Endpoints
- `/ping` - Basic health check
- `/health` - Database connection health check
- `/characters` - Get all characters
- `/characters/{character_name}` - Get specific character
- `/migrations` - Check migration status

## Database Setup

The application uses PostgreSQL with automatic migrations on startup.

### Migration System
- Migrations are located in `services/game-engine/migrations/`
- They run automatically when the game-engine starts
- Migration files are numbered sequentially (001_, 002_, etc.)
- Check migration status at `/migrations` endpoint

### Database Schema
Current tables:
- `users` - User accounts and profiles
- `characters` - Avatar universe characters
- `user_characters` - User's character collections
- `battles` - Battle history and results

## Project Structure

```
avatar-the-last-bot-bender/
├── services/
│   ├── game-engine/           # FastAPI backend service
│   │   ├── src/
│   │   │   ├── database/      # Database connection and queries
│   │   │   │   ├── connection.py
│   │   │   │   ├── migrations.py
│   │   │   │   └── queries/   # SQL query constants
│   │   │   ├── repositories/  # Data access layer
│   │   │   └── main.py        # FastAPI app entry point
│   │   ├── migrations/        # SQL migration files
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── discord-bot/           # Discord bot service (planned)
│   └── website/               # Web frontend (planned)
├── docker-compose.yml         # Container orchestration
└── README.md                  # This file
```