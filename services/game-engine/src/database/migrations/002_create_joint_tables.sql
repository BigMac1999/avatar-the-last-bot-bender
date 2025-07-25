-- Create user_characters table for character collection
CREATE TABLE user_characters (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_characters_user_id ON user_characters(user_id);
CREATE INDEX idx_user_characters_character_id ON user_characters(character_id);
-- Prevent duplicate character acquisition for the same user
CREATE UNIQUE INDEX idx_user_characters_unique ON user_characters(user_id, character_id);

-- ************************************************************* --

-- Create characters_abilities table for character abilities
CREATE TABLE characters_abilities (
    id SERIAL PRIMARY KEY,
    character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    ability_id INTEGER NOT NULL REFERENCES abilities(id) ON DELETE CASCADE,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_characters_abilities_character_id ON characters_abilities(character_id);
CREATE INDEX idx_characters_abilities_ability_id ON characters_abilities(ability_id);

-- ************************************************************* --

-- Create user_character_abilities table for user character abilities
CREATE TABLE user_character_abilities (
    id SERIAL PRIMARY KEY,
    user_character_id INTEGER NOT NULL REFERENCES user_characters(id) ON DELETE CASCADE,
    ability_id INTEGER NOT NULL REFERENCES abilities(id) ON DELETE CASCADE,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_character_abilities_user_character_id ON user_character_abilities(user_character_id);
CREATE INDEX idx_user_character_abilities_ability_id ON user_character_abilities(ability_id);

-- ************************************************************* --

-- Create ability_prerequisites table for ability prerequisites
CREATE TABLE ability_prerequisites (
    id SERIAL PRIMARY KEY,
    ability_id INTEGER NOT NULL REFERENCES abilities(id) ON DELETE CASCADE,
    prerequisite_ability_id INTEGER NOT NULL REFERENCES abilities(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ability_id, prerequisite_ability_id)
);

CREATE INDEX idx_ability_prerequisites_ability_id ON ability_prerequisites(ability_id);
CREATE INDEX idx_ability_prerequisites_prerequisite_id ON ability_prerequisites(prerequisite_ability_id);