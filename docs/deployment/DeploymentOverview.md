# Avatar: The Last Bot Bender - Deployment Overview

## Architecture Overview

The Avatar: The Last Bot Bender is a multi-container application consisting of:

- **Game Engine** - FastAPI backend service (Python)
- **Discord Bot** - Discord integration service (Python) 
- **Website** - Next.js web frontend (TypeScript/React)
- **PostgreSQL** - Database for persistent storage

All services are containerized using Docker and orchestrated with Docker Compose.

---

## Local Development Deployment

### Prerequisites

- **Docker** and **Docker Compose** installed on your system
- **Git** for cloning the repository
- **curl** for testing API endpoints (optional)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd avatar-the-last-bot-bender
   ```

2. **Build the game engine:**
   ```bash
   docker compose build game-engine
   ```

3. **Start the core services:**
   ```bash
   docker compose up postgres game-engine
   ```

   This will start:
   - PostgreSQL database on port `5432`
   - Game Engine API on port `8080`

4. **Verify deployment:**
   ```bash
   # Basic health check
   curl http://localhost:8080/ping
   
   # Database health check
   curl http://localhost:8080/health
   
   # Test character endpoints
   curl http://localhost:8080/characters
   
   # Check migration status
   curl http://localhost:8080/migrations
   ```

### Service-Specific Deployment

#### Game Engine Only
```bash
# Build and start just the game engine with database
docker compose up postgres game-engine
```

#### Full Stack (when implemented)
```bash
# Start all services
docker compose up
```

#### Individual Services
```bash
# Database only
docker compose up postgres

# Game engine only (requires database)
docker compose up postgres game-engine

# Website only (when implemented)
docker compose up website

# Discord bot only (when implemented)
docker compose up discord-bot
```

---

## Database Management

### Automatic Migrations

The game engine automatically runs database migrations on startup:

- **Migration files**: Located in `services/game-engine/src/database/migrations/`
- **Naming convention**: Sequential numbering (001_, 002_, etc.)
- **Auto-execution**: Runs when game-engine container starts
- **Status check**: Available at `/migrations` endpoint

### Current Database Schema

The application creates the following tables:

- **users** - User accounts and Discord profiles
- **characters** - Avatar universe characters and stats
- **user_characters** - User's character collection/roster
- **battles** - Battle history and results

### Manual Database Access

```bash
# Connect to PostgreSQL container
docker compose exec postgres psql -U atla_user -d atla_db

# View tables
\dt

# Exit
\q
```

---

## Environment Configuration

### Default Configuration

The `docker-compose.yml` includes default development settings:

```yaml
Database:
  - Host: postgres
  - Port: 5432
  - Database: atla_db
  - User: atla_user
  - Password: password

Game Engine:
  - Port: 8080
  - Database URL: postgres://atla_user:password@postgres:5432/atla_db
```

### Custom Configuration

For production or custom setups, create a `.env` file:

```bash
# Database Configuration
POSTGRES_DB=atla_db
POSTGRES_USER=atla_user
POSTGRES_PASSWORD=your_secure_password

# Game Engine Configuration
DATABASE_URL=postgres://atla_user:your_secure_password@postgres:5432/atla_db
```

---

## Available Endpoints

Once deployed, the Game Engine API provides:

### Health & System
- `GET /ping` - Basic service health check
- `GET /health` - Database connection health check  
- `GET /migrations` - Database migration status

### Characters
- `GET /characters` - Fetch all available characters
- `GET /characters/{character_name}` - Fetch specific character by name

### Planned Endpoints
- User management (`/users`)
- Character collection (`/roll`)
- Battle system (`/battles`)

---

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Check what's using port 8080
netstat -tulpn | grep :8080

# Use different port
docker compose up -p 8081:8080 game-engine
```

**Database connection failed:**
```bash
# Check if postgres is running
docker compose ps

# View postgres logs
docker compose logs postgres

# Restart database
docker compose restart postgres
```

**Migration failures:**
```bash
# Check game-engine logs
docker compose logs game-engine

# Reset database (WARNING: destroys data)
docker compose down -v
docker compose up postgres game-engine
```