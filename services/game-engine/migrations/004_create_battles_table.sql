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