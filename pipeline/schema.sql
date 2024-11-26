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
    plant_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    plant_name VARCHAR(60) NOT NULL,
    scientific_name VARCHAR(60),
    image_URL VARCHAR(255),
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
INSERT INTO epsilon.plant (plant_name, scientific_name, image_URL, location_id) VALUES
('Epipremnum Aureum', 'Epipremnum aureum', 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/og/2560px-Epipremnum_aureum_31082012.jpg', 1),
('Venus flytrap', NULL, NULL, 2),
('Corpse flower', NULL, NULL, 3),
('Rafflesia arnoldii', NULL, NULL, 1),
('Black bat flower', NULL, NULL, 4),
('Pitcher plant', 'Sarracenia catesbaei', 'https://perenual.com/storage/image/upgrade_access.jpg', 5),
('Wollemi pine', 'Wollemia nobilis', 'https://perenual.com/storage/image/upgrade_access.jpg', 6),
('Bird of paradise', 'Heliconia schiedeana ''Fire and Ice''', 'https://perenual.com/storage/image/upgrade_access.jpg', 7),
('Cactus', 'Pereskia grandifolia', 'https://perenual.com/storage/image/upgrade_access.jpg', 8),
('Dragon tree', NULL, NULL, 9),
('Asclepias Curassavica', 'Asclepias curassavica', 'https://perenual.com/storage/species_image/1007_asclepias_curassavica/og/51757177616_7ca0baaa87_b.jpg', 10),
('Brugmansia X Candida', NULL, NULL, 11),
('Canna ''Striata''', NULL, NULL, 12),
('Colocasia Esculenta', 'Colocasia esculenta', 'https://perenual.com/storage/species_image/2015_colocasia_esculenta/og/24325097844_14719030a3_b.jpg', 13),
('Cuphea ''David Verity''', NULL, NULL, 14),
('Euphorbia Cotinifolia', 'Euphorbia cotinifolia', 'https://perenual.com/storage/species_image/2868_euphorbia_cotinifolia/og/51952243235_061102bd05_b.jpg', 15),
('Ipomoea Batatas', 'Ipomoea batatas', 'https://perenual.com/storage/image/upgrade_access.jpg', 16),
('Manihot Esculenta ''Variegata''', NULL, NULL, 17),
('Musa Basjoo', 'Musa basjoo', 'https://perenual.com/storage/image/upgrade_access.jpg', 18),
('Salvia Splendens', 'Salvia splendens', 'https://perenual.com/storage/image/upgrade_access.jpg', 19),
('Anthurium', 'Anthurium andraeanum', 'https://perenual.com/storage/species_image/855_anthurium_andraeanum/og/49388458462_0ef650db39_b.jpg', 20),
('Bird of Paradise', 'Heliconia schiedeana ''Fire and Ice''', 'https://perenual.com/storage/image/upgrade_access.jpg', 21),
('Cordyline Fruticosa', 'Cordyline fruticosa', 'https://perenual.com/storage/species_image/2045_cordyline_fruticosa/og/2560px-Cordyline_fruticosa_Rubra_1.jpg', 22),
('Ficus', 'Ficus carica', 'https://perenual.com/storage/species_image/288_ficus_carica/og/52377169610_b7a247a378_b.jpg', 23),
('Palm Trees', NULL, NULL, 24),
('Dieffenbachia Seguine', 'Dieffenbachia seguine', 'https://perenual.com/storage/species_image/2468_dieffenbachia_seguine/og/24449059743_2aee995991_b.jpg', 25),
('Spathiphyllum', 'Spathiphyllum (group)', 'https://perenual.com/storage/image/upgrade_access.jpg', 26),
('Croton', 'Codiaeum variegatum', 'https://perenual.com/storage/species_image/1999_codiaeum_variegatum/og/29041866364_2c535b2297_b.jpg', 27),
('Aloe Vera', 'Aloe vera', 'https://perenual.com/storage/species_image/728_aloe_vera/og/52619084582_6ebcfe6a74_b.jpg', 28),
('Ficus Elastica', 'Ficus elastica', 'https://perenual.com/storage/species_image/2961_ficus_elastica/og/533092219_8da73ba0d2_b.jpg', 29),
('Sansevieria Trifasciata', 'Sansevieria trifasciata', 'https://perenual.com/storage/image/upgrade_access.jpg', 30),
('Philodendron Hederaceum', 'Philodendron hederaceum', 'https://perenual.com/storage/image/upgrade_access.jpg', 31),
('Schefflera Arboricola', 'Schefflera arboricola', 'https://perenual.com/storage/image/upgrade_access.jpg', 32),
('Monstera Deliciosa', 'Monstera deliciosa', 'https://perenual.com/storage/image/upgrade_access.jpg', 33),
('Tacca Integrifolia', 'Tacca integrifolia', 'https://perenual.com/storage/image/upgrade_access.jpg', 34),
('Psychopsis Papilio', NULL, NULL, 35),
('Saintpaulia Ionantha', 'Saintpaulia ionantha', 'https://perenual.com/storage/image/upgrade_access.jpg', 36),
('Gaillardia', 'Gaillardia aestivalis', 'https://perenual.com/storage/image/upgrade_access.jpg', 37),
('Amaryllis', 'Hippeastrum (group)', 'https://perenual.com/storage/image/upgrade_access.jpg', 38),
('Caladium Bicolor', 'Caladium bicolor', 'https://perenual.com/storage/species_image/1457_caladium_bicolor/og/25575875658_d782fb76f1_b.jpg', 39),
('Chlorophytum Comosum', 'Chlorophytum comosum ''Vittatum''', 'https://perenual.com/storage/species_image/1847_chlorophytum_comosum_vittatum/og/2560px-Chlorophytum_comosum_27Vittatum27_kz02.jpg', 40),
('Araucaria Heterophylla', 'Araucaria heterophylla', 'https://perenual.com/storage/species_image/917_araucaria_heterophylla/og/49833684212_2aff9d7b3c_b.jpg', 41),
('Begonia', 'Begonia ''Art Hodes''', NULL, 2),
('Medinilla Magnifica', 'Medinilla magnifica', 'https://perenual.com/storage/image/upgrade_access.jpg', 42),
('Calliandra Haematocephala', 'Calliandra haematocephala', 'https://perenual.com/storage/species_image/1477_calliandra_haematocephala/og/52063600268_834ebc0538_b.jpg', 43),
('Zamioculcas Zamiifolia', 'Zamioculcas zamiifolia', 'https://perenual.com/storage/image/upgrade_access.jpg', 44),
('Crassula Ovata', 'Crassula ovata', 'https://perenual.com/storage/species_image/2193_crassula_ovata/og/33253726791_980c738a1e_b.jpg', 45);
