-- Create user_characters table for character collection
CREATE TABLE user_characters (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

CREATE INDEX idx_user_characters_user_id ON user_characters(user_id);
CREATE INDEX idx_user_characters_character_id ON user_characters(character_id);
-- Prevent duplicate character acquisition for the same user
CREATE UNIQUE INDEX idx_user_characters_unique ON user_characters(user_id, character_id);