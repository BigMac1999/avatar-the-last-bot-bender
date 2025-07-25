-- Create users table for Discord Users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    discord_id BIGINT NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster lookups by discord_id
CREATE INDEX idx_users_discord_id ON users(discord_id);

-- ************************************************************* --

-- Create characters table for ATLA characters
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    element VARCHAR(20) NOT NULL CHECK (element IN ('fire', 'water', 'earth', 'air', 'none')),
    rarity INTEGER NOT NULL CHECK (rarity IN (1, 2, 3)),
    hp INTEGER NOT NULL CHECK (hp > 0),
    attack INTEGER NOT NULL CHECK (attack > 0),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster lookups by name
CREATE UNIQUE INDEX idx_characters_name ON characters(name);
CREATE INDEX idx_characters_element ON characters(element);
CREATE INDEX idx_characters_rarity ON characters(rarity);

-- ************************************************************* --

-- Create battles table for battle records
CREATE TABLE battles (
    id SERIAL PRIMARY KEY,
    challenger_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    opponent_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    winner_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    battle_log TEXT, -- JSON string of battle events
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_battles_challenger ON battles(challenger_id);
CREATE INDEX idx_battles_opponent ON battles(opponent_id);
CREATE INDEX idx_battles_status ON battles(status);

-- ************************************************************* --

-- Create abilities table for character abilities
CREATE TABLE abilities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    attack INTEGER NOT NULL CHECK (attack >= 0),
    defense INTEGER NOT NULL,
    element VARCHAR(20) NOT NULL CHECK (element IN ('fire', 'water', 'earth', 'air', 'none')),
    unlock_cost INTEGER NOT NULL CHECK (unlock_cost >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Create index for faster lookups
CREATE UNIQUE INDEX idx_abilities_unique_name ON abilities(name);
CREATE INDEX idx_abilities_element ON abilities(element);
