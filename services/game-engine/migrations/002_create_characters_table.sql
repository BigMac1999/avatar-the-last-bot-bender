-- Create characters table for ATLA characters
CREATE TABLE characters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    element VARCHAR(20) NOT NULL CHECK (element IN ('fire', 'water', 'earth', 'air', 'none')),
    rarity INTEGER NOT NULL CHECK (rarity IN (1, 2, 3)),
    hp INTEGER NOT NULL CHECK (hp > 0),
    attack INTEGER NOT NULL CHECK (attack > 0),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_characters_element ON characters(element);
CREATE INDEX idx_characters_rarity ON characters(rarity);