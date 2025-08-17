-- Migration 003: Update battle table to add battle_type column
-- This migration adds battle_type to differentiate between user vs bot battles

-- Add battle_type column if it doesn't exist
ALTER TABLE battles 
ADD COLUMN IF NOT EXISTS battle_type VARCHAR(20) DEFAULT 'user' NOT NULL;

-- Add index on battle_type for performance
CREATE INDEX IF NOT EXISTS idx_battles_battle_type ON battles(battle_type);

-- Add constraint to ensure only valid battle types
DO $$ 
BEGIN
    -- Check if constraint already exists before adding it
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints 
        WHERE constraint_name = 'check_battle_type' 
        AND table_name = 'battles'
    ) THEN
        ALTER TABLE battles 
        ADD CONSTRAINT check_battle_type 
        CHECK (battle_type IN ('bot', 'user'));
    END IF;
END $$;

-- Update existing records to have proper battle_type (if any exist)
-- This assumes existing battles are user vs user
UPDATE battles SET battle_type = 'user' WHERE battle_type IS NULL;

-- Add comment to document the column
COMMENT ON COLUMN battles.battle_type IS 'Type of battle: user (user vs user) or bot (user vs bot)';