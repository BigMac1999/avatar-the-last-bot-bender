# Avatar: The Last Bot Bender - Architecture Overview

## System Architecture

The Avatar: The Last Bot Bender is a multi-container application built with a microservices architecture. Each service is containerized using Docker and orchestrated with Docker Compose.

```
+----------------+    +----------------+    +----------------+
|  Discord Bot   |    |    Website     |    | External APIs  |
|   (Python)     |    | (Next.js/TS)   |    |   (Future)     |
+-------+--------+    +-------+--------+    +----------------+
        |                     |
        |                     |
        +----------+----------+
                   |
        +----------+----------+
        |    Game Engine      |
        |     (FastAPI)       |
        +----------+----------+
                   |
        +----------+----------+
        |     PostgreSQL      |
        |      Database       |
        +---------------------+
```

## Services Overview

### Game Engine (FastAPI)
- **Port**: 8080
- **Technology**: Python with FastAPI framework
- **Purpose**: Core business logic and API backend
- **Dependencies**: PostgreSQL database
- **Key Features**:
  - RESTful API for character management
  - Database migration system
  - Health monitoring endpoints
  - Battle system logic (planned)

### Website (Next.js)
- **Port**: 3001
- **Technology**: Next.js with TypeScript and Tailwind CSS
- **Purpose**: Web frontend interface
- **Dependencies**: None (standalone)
- **Key Features**:
  - Modern React-based UI
  - TypeScript for type safety
  - Tailwind CSS for styling
  - Server-side rendering capabilities

### Discord Bot (Planned)
- **Technology**: Python with discord.py
- **Purpose**: Discord integration and user interaction
- **Dependencies**: Game Engine API
- **Key Features**:
  - Character collection commands
  - Battle system integration
  - User profile management

### PostgreSQL Database
- **Port**: 5432
- **Technology**: PostgreSQL 16
- **Purpose**: Persistent data storage
- **Key Features**:
  - Automatic migration system
  - Transactional data integrity
  - Optimized for game data queries

## Data Flow

### Character Information Flow
1. Database stores character data and stats
2. Game Engine exposes character data via REST API
3. Website fetches character data for display
4. Discord Bot queries character data for game commands

### User Interaction Flow
1. Users interact via Discord Bot or Website
2. Requests flow through Game Engine API
3. Game Engine processes business logic
4. Database operations are performed
5. Responses are returned to the user interface

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for Python APIs
- **PostgreSQL**: Robust relational database
- **Python**: Primary backend language
- **Docker**: Containerization platform

### Frontend
- **Next.js**: React framework with SSR capabilities
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **React**: Component-based UI library

### DevOps
- **Docker Compose**: Multi-container application orchestration
- **Git**: Version control
- **Automated Migrations**: Database schema management

## Security Considerations

### Database Security
- Environment-based configuration
- Connection pooling and timeouts
- Parameterized queries to prevent SQL injection

### API Security
- CORS configuration
- Input validation
- Rate limiting (planned)
- Authentication system (planned)

### Container Security
- Non-root container users
- Minimal base images
- Security updates through base image updates

## Development Workflow

### Local Development
1. Clone repository
2. Build containers with Docker Compose
3. Start services individually or together
4. Use health endpoints to verify status
5. Access services via localhost ports

### Testing Strategy
- Unit tests for business logic
- Integration tests for API endpoints
- End-to-end tests for complete workflows
- Database migration tests

### Deployment
- Container-based deployment
- Environment-specific configuration
- Health monitoring and logging
- Automated database migrations

## Future Enhancements

### Planned Features
- User authentication and authorization
- Advanced battle system
- Character trading system
- Leaderboards and statistics
- Mobile-responsive website improvements

### Technical Improvements
- Redis caching layer
- API rate limiting
- Comprehensive logging system
- Monitoring and alerting
- CI/CD pipeline integration