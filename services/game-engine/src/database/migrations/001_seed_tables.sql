-- Seed initial ATLA characters
INSERT INTO characters (name, element, rarity, hp, attack, description) VALUES
-- Legendary characters (rarity 3)
('Aang', 'air', 3, 120, 85, 'The Avatar and last airbender'),
('Fire Lord Ozai', 'fire', 3, 150, 95, 'Ruler of the Fire Nation'),
('Toph Beifong', 'earth', 3, 140, 90, 'The greatest earthbender in the world'),
('Azula', 'fire', 3, 130, 100, 'Fire Nation princess with blue flames'),

-- Rare characters (rarity 2)  
('Katara', 'water', 2, 100, 75, 'Waterbending master from the Southern Water Tribe'),
('Zuko', 'fire', 2, 110, 80, 'Banished Fire Nation prince'),
('Sokka', 'none', 2, 90, 70, 'Strategic warrior with boomerang'),
('Iroh', 'fire', 2, 120, 85, 'The Dragon of the West'),
('Ty Lee', 'none', 2, 80, 85, 'Acrobat who can block chi'),
('Mai', 'none', 2, 85, 80, 'Expert with throwing knives'),

-- Common characters (rarity 1)
('Suki', 'none', 1, 75, 65, 'Leader of the Kyoshi Warriors'),
('Jet', 'none', 1, 80, 70, 'Freedom fighter with hook swords'),
('Fire Nation Soldier', 'fire', 1, 60, 50, 'Standard Fire Nation infantry'),
('Earth Kingdom Guard', 'earth', 1, 70, 55, 'Ba Sing Se city guard'),
('Water Tribe Warrior', 'water', 1, 65, 60, 'Southern Water Tribe fighter');

-- ************************************************************* --

-- Seed abilities based on ATLA elements and tiers
INSERT INTO abilities (name, description, attack, defense, element,
unlock_cost) VALUES

-- AIR ABILITIES (Tier 1-3)
('Air Swipe', 'Basic air attack that pushes enemies back', 25, 0, 'air', 1),       
('Air Shield', 'Creates protective air barrier', 0, 20, 'air', 1),
('Air Scooter', 'Enhanced mobility with air sphere', 0, 10, 'air', 2),
('Tornado Strike', 'Powerful spinning air attack', 45, 0, 'air', 3),
('Avatar State', 'Ultimate air mastery with glowing eyes', 80, 40, 'air', 5),      

-- FIRE ABILITIES (Tier 1-3)
('Fire Punch', 'Basic fire-enhanced melee attack', 30, 0, 'fire', 1),
('Fire Shield', 'Wall of flames for protection', 0, 25, 'fire', 1),
('Fire Blast', 'Concentrated fire projectile', 50, 0, 'fire', 2),
('Blue Fire', 'Intense blue flames with higher damage', 65, 0, 'fire', 3),
('Lightning Generation', 'Create and direct lightning bolts', 85, 0, 'fire',       
5),

-- WATER ABILITIES (Tier 1-3)
('Water Whip', 'Flexible water tendril attack', 20, 0, 'water', 1),
('Ice Shield', 'Protective barrier of ice', 0, 30, 'water', 1),
('Healing Waters', 'Restore health with healing properties', 0, 0, 'water',        
2),
('Tidal Wave', 'Large water attack covering wide area', 55, 0, 'water', 3),        
('Bloodbending', 'Control water in living beings', 90, 0, 'water', 5),

-- EARTH ABILITIES (Tier 1-3)
('Rock Throw', 'Hurl chunks of earth at enemies', 35, 0, 'earth', 1),
('Earth Armor', 'Stone protection around body', 0, 35, 'earth', 1),
('Seismic Sense', 'Detect enemies through vibrations', 0, 15, 'earth', 2),
('Metalbending', 'Manipulate refined metals', 60, 0, 'earth', 3),
('Earth Prison', 'Trap enemies in stone cage', 40, 20, 'earth', 3),

-- NON-BENDER ABILITIES
('Boomerang Throw', 'Curved weapon that returns', 25, 0, 'none', 1),
('Chi Blocking', 'Disable enemy bending temporarily', 20, 0, 'none', 2),
('Sword Mastery', 'Expert weapon combat techniques', 40, 10, 'none', 2),
('Strategic Planning', 'Boost team coordination', 0, 25, 'none', 1),
('Acrobatics', 'Enhanced mobility and dodging', 15, 20, 'none', 1);

-- ************************************************************* --

-- Map characters to their available abilities based on element and character      
INSERT INTO characters_abilities (character_id, ability_id) VALUES

-- Aang (Air/Avatar) - Can learn from multiple elements
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), -- All air abilities
(1, 6), (1, 8), -- Some fire abilities
(1, 11), (1, 13), -- Some water abilities
(1, 16), (1, 18), -- Some earth abilities

-- Fire Lord Ozai (Fire master)
(2, 6), (2, 7), (2, 8), (2, 9), (2, 10), -- All fire abilities

-- Toph (Earth master + Metalbending)
(3, 16), (3, 17), (3, 18), (3, 19), (3, 20), -- All earth abilities

-- Azula (Fire + Blue flames)
(4, 6), (4, 7), (4, 8), (4, 9), (4, 10), -- All fire abilities

-- Katara (Water master + Healing)
(5, 11), (5, 12), (5, 13), (5, 14), (5, 15), -- All water abilities

-- Zuko (Fire bender)
(6, 6), (6, 7), (6, 8), (6, 10), -- Fire abilities (no blue fire)

-- Sokka (Non-bender strategist)
(7, 21), (7, 24), (7, 25), -- Non-bender abilities

-- Iroh (Fire master)
(8, 6), (8, 7), (8, 8), (8, 10), -- Fire abilities + lightning

-- Ty Lee (Chi blocker)
(9, 22), (9, 25), -- Chi blocking + acrobatics

-- Mai (Weapon specialist)
(10, 23), (10, 24), -- Sword mastery + strategy

-- Common characters get basic abilities of their element
-- Suki (11) - Non-bender warrior
(11, 21), (11, 23), (11, 25),

-- Jet (12) - Non-bender fighter
(12, 21), (12, 23),

-- Fire Nation Soldier (13)
(13, 6), (13, 7),

-- Earth Kingdom Guard (14)
(14, 16), (14, 17),

-- Water Tribe Warrior (15)
(15, 11), (15, 12);

-- ************************************************************* --

-- Ability skill tree prerequisites
INSERT INTO ability_prerequisites (ability_id, prerequisite_ability_id) VALUES

-- Air progression
(3, 1), -- Air Scooter requires Air Swipe
(4, 3), -- Tornado Strike requires Air Scooter
(5, 4), -- Avatar State requires Tornado Strike

-- Fire progression
(8, 6), -- Fire Blast requires Fire Punch
(9, 8), -- Blue Fire requires Fire Blast
(10, 9), -- Lightning requires Blue Fire

-- Water progression
(13, 11), -- Healing requires Water Whip
(14, 13), -- Tidal Wave requires Healing
(15, 14), -- Bloodbending requires Tidal Wave

-- Earth progression
(18, 16), -- Seismic Sense requires Rock Throw
(19, 18), -- Metalbending requires Seismic Sense
(20, 17), -- Earth Prison requires Earth Armor

-- Non-bender progression
(22, 25), -- Chi Blocking requires Acrobatics
(23, 21); -- Sword Mastery requires Boomerang basics

