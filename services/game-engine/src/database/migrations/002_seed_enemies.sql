-- Seed basic enemies for battle engine testing
INSERT INTO enemies (name, description, enemy_hp, enemy_attack, level, behavior_type, element, xp_drop) VALUES
('Fire Nation Soldier', 'Standard infantry of the Fire Nation army with basic firebending skills', 60, 45, 2, 'aggressive', 'fire', 15),
('Freedom Fighter', 'Rebel warrior fighting against oppression with guerrilla tactics', 55, 40, 2, 'balanced', 'none', 12),
('The Boulder', 'Professional earthbending wrestler who speaks in third person', 80, 50, 3, 'defensive', 'earth', 20);

-- ************************************************************* --

-- Assign abilities to enemies based on their element and behavior
INSERT INTO enemy_abilities (enemy_id, ability_id, behavior_type) VALUES

-- Fire Nation Soldier (ID: 1) - Fire abilities
(1, 6, 'aggressive'),  -- Fire Punch (basic fire attack)
(1, 7, 'defensive'),   -- Fire Shield (defensive fire ability)
(1, 8, 'aggressive'),  -- Fire Blast (stronger fire attack)

-- Freedom Fighter (ID: 2) - Non-bender abilities  
(2, 21, 'aggressive'), -- Boomerang Throw (ranged attack)
(2, 23, 'aggressive'), -- Sword Mastery (melee combat)
(2, 24, 'balanced'),   -- Strategic Planning (tactical ability)

-- The Boulder (ID: 3) - Earth abilities
(3, 16, 'aggressive'), -- Rock Throw (earth attack)
(3, 17, 'defensive'),  -- Earth Armor (defensive ability)
(3, 18, 'balanced');   -- Seismic Sense (utility ability)