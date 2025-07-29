# Avatar: The Last Bot Bender API Overview

## Game Engine API (v1.0.0)

The ATLA Game Engine provides a REST API for managing characters, battles, and user interactions in the Avatar: The Last Airbender companion app.

**Base URL:** `http://localhost:8080`

---

## Health & System Endpoints

### GET `/ping`
Simple health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "message": "Game Engine is running"
}
```

### GET `/health`
Comprehensive health check including database connection status.

**Response:**
```json
{
  "status": "healthy",
  "message": "Database connection successful",
  "test_query": "SELECT 1 executed successfully"
}
```

### GET `/migrations`
Get current database migration status.

**Response:**
```json
{
  "applied_migrations": ["001_create_users_table", "002_create_characters_table"],
  "pending_migrations": [],
  "status": "up_to_date"
}
```

---

## Character Endpoints

### GET `/characters`
Fetch all available characters from the database.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Aang",
    "element": "Air",
    "abilities": ["Air Scooter", "Avatar State"],
    "stats": {
      "health": 100,
      "attack": 85,
      "defense": 70
    }
  }
]
```

### GET `/characters/{character_name}`
Fetch a specific character by name.

**Parameters:**
- `character_name` (string): The name of the character to retrieve

**Response (Success):**
```json
{
  "id": 1,
  "name": "Aang",
  "element": "Air",
  "abilities": ["Air Scooter", "Avatar State"],
  "stats": {
    "health": 100,
    "attack": 85,
    "defense": 70
  }
}
```

**Response (Not Found):**
```json
{
  "error": "Character not found"
}
```

---

## Planned Features

The following endpoints are planned for future implementation:

### User Management
- `POST /users` - Create new user
- `GET /users/{user_id}` - Get user profile
- `GET /users/{user_id}/characters` - Get user's character roster

### Character Collection
- `POST /roll` - Roll for a new character
- `POST /users/{user_id}/characters` - Add character to user's collection

### Battle System
- `POST /battles` - Start a new battle
- `GET /battles/{battle_id}` - Get battle status
- `POST /battles/{battle_id}/actions` - Submit battle action

### Discord Integration
The API is designed to support the following Discord bot commands:
- `!roll` - Character collection system
- `!battle` - Battle system
- `!stats` - Character statistics
- `!roster` - User's character collection
- `!website` - Link to web interface (http://localhost:3001 for now for local dev)

---

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200` - Success
- `404` - Resource not found
- `500` - Internal server error

Error responses follow the format:
```json
{
  "error": "Error description"
}
```

---

## Database

The API uses PostgreSQL with automatic migration management. The database includes tables for:
- Users
- Characters
- User-Character relationships
- Battles
- Character abilities and stats