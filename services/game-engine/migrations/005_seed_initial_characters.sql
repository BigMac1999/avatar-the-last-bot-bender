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