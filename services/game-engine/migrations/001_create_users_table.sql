-- Create users table for Discord Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    discord_id BIGINT NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster lookups by discord_id
CREATE INDEX idx_users_discord_id ON users(discord_id);