-- Database schema code to create database tables.

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'epsilon')
BEGIN
    EXEC('CREATE SCHEMA epsilon');
END;

DROP TABLE IF EXISTS epsilon.plant_metric;
DROP TABLE IF EXISTS epsilon.plant;
DROP TABLE IF EXISTS epsilon.botanist;
DROP TABLE IF EXISTS epsilon.location;


CREATE TABLE epsilon.location (
    location_id INT IDENTITY(1,1) PRIMARY KEY,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    closest_town VARCHAR(50) UNIQUE NOT NULL,
    ISO_code VARCHAR(2) NOT NULL
);

CREATE TABLE epsilon.botanist (
    botanist_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    full_name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE epsilon.plant (
    plant_id SMALLINT PRIMARY KEY,
    plant_name VARCHAR(60) NOT NULL,
    scientific_name VARCHAR(60),
    location_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES epsilon.location(location_id) ON DELETE CASCADE
);

CREATE TABLE epsilon.plant_metric (
    plant_metric_id BIGINT IDENTITY(1,1) PRIMARY KEY,
    temperature FLOAT NOT NULL,
    soil_moisture FLOAT NOT NULL,
    recording_taken DATETIME2 NOT NULL,
    last_watered DATETIME2 NOT NULL,
    botanist_id SMALLINT NOT NULL,
    plant_id SMALLINT NOT NULL,
    FOREIGN KEY (botanist_id) REFERENCES epsilon.botanist(botanist_id) ON DELETE CASCADE,
    FOREIGN KEY (plant_id) REFERENCES epsilon.plant(plant_id) ON DELETE CASCADE
);

-- Seed Location Data
INSERT INTO epsilon.location (longitude, latitude, closest_town, ISO_code) VALUES
(-41.26, -19.33, 'Resplendor', 'BR'),
(-118.04, 33.95, 'South Whittier', 'US'),
(4.92, 7.66, 'Efon-Alaaye', 'NG'),
(-89.11, 13.70, 'Ilopango', 'SV'),
(84.14, 22.89, 'Jashpurnagar', 'IN'),
(-79.27, 43.87, 'Markham', 'CA'),
(-3.60, 5.27, 'Bonoua', 'CI'),
(11.33, 50.98, 'Weimar', 'DE'),
(16.44, 43.51, 'Split', 'HR'),
(-156.47, 20.89, 'Kahului', 'US'),
(-94.74, 32.50, 'Longview', 'US'),
(8.62, 49.68, 'Bensheim', 'DE'),
(-82.32, 29.65, 'Gainesville', 'US'),
(9.37, 36.08, 'Siliana', 'TN'),
(-73.90, 40.93, 'Yonkers', 'US'),
(109.05, -7.52, 'Wangon', 'ID'),
(13.11, 51.30, 'Oschatz', 'DE'),
(27.46, -21.44, 'Tonota', 'BW'),
(1.11, 41.16, 'Reus', 'ES'),
(-51.50, -29.30, 'Carlos Barbosa', 'BR'),
(10.98, 48.36, 'Friedberg', 'DE'),
(13.29, 52.53, 'Charlottenburg-Nord', 'DE'),
(144.10, 43.83, 'Motomachi', 'JP'),
(34.39, 11.87, 'Ar Ruseris', 'SD'),
(4.63, 36.06, 'El Achir', 'DZ'),
(33.92, 51.68, 'Hlukhiv', 'UA'),
(-69.97, 43.91, 'Brunswick', 'US'),
(136.13, 34.76, 'Ueno-ebisumachi', 'JP'),
(20.23, 30.76, 'Ajdabiya', 'LY'),
(113.82, 23.30, 'Licheng', 'CN'),
(10.55, 52.48, 'Gifhorn', 'DE'),
(78.23, 28.93, 'Bachhraon', 'IN'),
(-71.23, -32.45, 'La Ligua', 'CL'),
(-82.90, 32.54, 'Dublin', 'US'),
(74.48, 30.21, 'Malaut', 'IN'),
(39.25, -6.80, 'Magomeni', 'TZ'),
(139.07, 36.25, 'Fujioka', 'JP'),
(4.90, 44.93, 'Valence', 'FR'),
(88.15, 22.47, 'Pujali', 'IN'),
(24.71, 41.57, 'Smolyan', 'BG'),
(-103.57, 20.23, 'Zacoalco de Torres', 'MX'),
(34.46, -13.78, 'Salima', 'MW'),
(15.07, 37.49, 'Catania', 'IT'),
(121.32, 14.15, 'Calauan', 'PH'),
(-94.91, 17.95, 'Acayucan', 'MX');


-- Seed Botanist Data
INSERT INTO botanist (full_name, email, phone) VALUES
('Carl Linnaeus', 'carl.linnaeus@lnhm.co.uk', '(146)994-1635x35992'),
('Gertrude Jekyll', 'gertrude.jekyll@lnhm.co.uk', '001-481-273-3691x127'),
('Eliza Andrews', 'eliza.andrews@lnhm.co.uk', '(846)669-6651x75948');

-- Seed Plant Data
INSERT INTO epsilon.plant (plant_id, plant_name, scientific_name, location_id) VALUES
(0, 'Epipremnum Aureum', 'Epipremnum aureum', 1),
(1, 'Venus flytrap', NULL, 2),
(2, 'Corpse flower', NULL, 3),
(3, 'Rafflesia arnoldii', NULL, 1),
(4, 'Black bat flower', NULL, 4),
(5, 'Pitcher plant', 'Sarracenia catesbaei', 5),
(6, 'Wollemi pine', 'Wollemia nobilis', 6),
(8, 'Bird of paradise', 'Heliconia schiedeana ''Fire and Ice''', 7),
(9, 'Cactus', 'Pereskia grandifolia', 8),
(10, 'Dragon tree', NULL, 9),
(11, 'Asclepias Curassavica', 'Asclepias curassavica', 10),
(12, 'Brugmansia X Candida', NULL, 11),
(13, 'Canna ''Striata''', NULL, 12),
(14, 'Colocasia Esculenta', 'Colocasia esculenta', 13),
(15, 'Cuphea ''David Verity''', NULL, 14),
(16, 'Euphorbia Cotinifolia', 'Euphorbia cotinifolia', 15),
(17, 'Ipomoea Batatas', 'Ipomoea batatas', 16),
(18, 'Manihot Esculenta ''Variegata''', NULL, 17),
(19, 'Musa Basjoo', 'Musa basjoo', 18),
(20, 'Salvia Splendens', 'Salvia splendens', 19),
(21, 'Anthurium', 'Anthurium andraeanum', 20),
(22, 'Bird of Paradise', 'Heliconia schiedeana ''Fire and Ice''', 21),
(23, 'Cordyline Fruticosa', 'Cordyline fruticosa', 22),
(24, 'Ficus', 'Ficus carica', 23),
(25, 'Palm Trees', NULL, 24),
(26, 'Dieffenbachia Seguine', 'Dieffenbachia seguine', 25),
(27, 'Spathiphyllum', 'Spathiphyllum (group)', 26),
(28, 'Croton', 'Codiaeum variegatum', 27),
(29, 'Aloe Vera', 'Aloe vera', 28),
(30, 'Ficus Elastica', 'Ficus elastica', 29),
(31, 'Sansevieria Trifasciata', 'Sansevieria trifasciata', 30),
(32, 'Philodendron Hederaceum', 'Philodendron hederaceum', 31),
(33, 'Schefflera Arboricola', 'Schefflera arboricola', 32),
(34, 'Aglaonema commutatum', 'Aglaonema commutatum', 19), 
(35, 'Monstera Deliciosa', 'Monstera deliciosa',33),
(36, 'Tacca Integrifolia', 'Tacca integrifolia', 34),
(37, 'Psychopsis Papilio', NULL, 35),
(38, 'Saintpaulia Ionantha', 'Saintpaulia ionantha', 36),
(39, 'Gaillardia', 'Gaillardia aestivalis', 37),
(40, 'Amaryllis', 'Hippeastrum (group)', 38),
(41, 'Caladium Bicolor', 'Caladium bicolor', 39),
(42, 'Chlorophytum Comosum', 'Chlorophytum comosum ''Vittatum''', 40),
(44, 'Araucaria Heterophylla', 'Araucaria heterophylla', 41),
(45, 'Begonia', 'Begonia ''Art Hodes''', 2),
(46, 'Medinilla Magnifica', 'Medinilla magnifica', 42),
(47, 'Calliandra Haematocephala', 'Calliandra haematocephala', 43),
(48, 'Zamioculcas Zamiifolia', 'Zamioculcas zamiifolia', 44),
(49 ,'Crassula Ovata', 'Crassula ovata', 45),
(50, 'Epipremnum Aureum', 'Epipremnum aureum', 1);