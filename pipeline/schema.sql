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
    image_url VARCHAR(255),
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

CREATE TABLE epsilon.plants_archive (
    plant_archive_id INT IDENTITY(1,1) PRIMARY KEY,
    avg_temperature FLOAT NOT NULL,
    avg_soil_moisture FLOAT NOT NULL,
    watered_count SMALLINT NOT NULL,
    last_recorded DATETIME2 NOT NULL,
    plant_id SMALLINT NOT NULL,
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
INSERT INTO epsilon.plant (plant_id, plant_name, scientific_name, image_url, location_id) VALUES
(0, 'Epipremnum Aureum', 'Epipremnum aureum', 'https://i0.wp.com/deepgreenpermaculture.com/wp-content/uploads/2024/04/Pothos.png?ssl=1' 1),
(1, 'Venus flytrap', NULL, 'https://cdn.shopify.com/s/files/1/0620/2749/7724/files/venus-flytrap-shk-1.jpg?v=1707849605', 2),
(2, 'Corpse flower', NULL, 'https://www.usbg.gov/sites/default/files/images/2021corpseflowerusbg.jpg', 3),
(3, 'Rafflesia arnoldii', NULL, 'https://www.indonesia-tourism.com/bengkulu/images/raflesia-arnoldii-bengkulu.jpg', 1),
(4, 'Black bat flower', NULL, 'https://seed2plant.in/cdn/shop/files/Black_Tacca.SHUT_1024x_4771ba58-7cfb-45ef-845d-cf04079b1455.webp?v=1685181872', 4),
(5, 'Pitcher plant', 'Sarracenia catesbaei', 'https://bunny-wp-pullzone-5vqgtgkbhi.b-cdn.net/wp-content/uploads/2023/04/Green-Pitcher-Plant-1.jpg', 5),
(6, 'Wollemi pine', 'Wollemia nobilis', 'https://cdn.britannica.com/88/199588-050-35511152/Wollemi-pine.jpg', 6),
(8, 'Bird of paradise', 'Heliconia schiedeana ''Fire and Ice''', 'https://5.imimg.com/data5/SELLER/Default/2023/8/333986270/XD/QI/OX/155714667/whatsapp-image-2023-07-14-at-11-41-54-1-500x500.jpeg', 7),
(9, 'Cactus', 'Pereskia grandifolia', 'https://worldofsucculents.com/wp-content/uploads/2014/08/Pereskia-grandifolia-Rose-Cactus4.jpg', 8),
(10, 'Dragon tree', NULL, 'https://www.arboroperations.com.au/wp-content/uploads/2022/07/dragon-tree.jpg', 9),
(11, 'Asclepias Curassavica', 'Asclepias curassavica', 'https://perenual.com/storage/species_image/1007_asclepias_curassavica/small/51757177616_7ca0baaa87_b.jpg', 10),
(12, 'Brugmansia X Candida', NULL, 'https://s3.amazonaws.com/eit-planttoolbox-prod/media/images/Brugmansia_x_Candida_MLSwBdfzt7XS.jpg', 11),
(13, 'Canna ''Striata''', NULL, 'https://apps.rhs.org.uk/plantselectorimages/detail/elbo15016.jpg', 12),
(14, 'Colocasia Esculenta', 'Colocasia esculenta', 'https://perenual.com/storage/species_image/2015_colocasia_esculenta/small/24325097844_14719030a3_b.jpg', 13),
(15, 'Cuphea ''David Verity''', NULL, '', 14),
(16, 'Euphorbia Cotinifolia', 'Euphorbia cotinifolia', 'https://perenual.com/storage/species_image/2868_euphorbia_cotinifolia/small/51952243235_061102bd05_b.jpg',15),
(17, 'Ipomoea Batatas', 'Ipomoea batatas', '', 16),
(18, 'Manihot Esculenta ''Variegata''', NULL, '', 17),
(19, 'Musa Basjoo', 'Musa basjoo', '', 18),
(20, 'Salvia Splendens', 'Salvia splendens', '', 19),
(21, 'Anthurium', 'Anthurium andraeanum', ' https://perenual.com/storage/species_image/855_anthurium_andraeanum/small/49388458462_0ef650db39_b.jpg', 20),
(22, 'Bird of Paradise', 'Heliconia schiedeana ''Fire and Ice''', '', 21),
(23, 'Cordyline Fruticosa', 'Cordyline fruticosa', '', 22),
(24, 'Ficus', 'Ficus carica', 'https://perenual.com/storage/species_image/288_ficus_carica/small/52377169610_b7a247a378_b.jpg', 23),
(25, 'Palm Trees', NULL, '', 24),
(26, 'Dieffenbachia Seguine', 'Dieffenbachia seguine', 'https://perenual.com/storage/species_image/2468_dieffenbachia_seguine/small/24449059743_2aee995991_b.jpg', 25),
(27, 'Spathiphyllum', 'Spathiphyllum (group)', '', 26),
(28, 'Croton', 'Codiaeum variegatum', 'https://perenual.com/storage/species_image/1999_codiaeum_variegatum/small/29041866364_2c535b2297_b.jpg', 27),
(29, 'Aloe Vera', 'Aloe vera', 'https://perenual.com/storage/species_image/728_aloe_vera/small/52619084582_6ebcfe6a74_b.jpg', 28),
(30, 'Ficus Elastica', 'Ficus elastica', '', 29),
(31, 'Sansevieria Trifasciata', 'Sansevieria trifasciata', '', 30),
(32, 'Philodendron Hederaceum', 'Philodendron hederaceum', '', 31),
(33, 'Schefflera Arboricola', 'Schefflera arboricola', '', 32),
(34, 'Aglaonema commutatum', 'Aglaonema commutatum', 'https://perenual.com/storage/species_image/625_aglaonema_commutatum/small/24798632751_3a039ecbc6_b.jpg', 19), 
(35, 'Monstera Deliciosa', 'Monstera deliciosa', '', 33),
(36, 'Tacca Integrifolia', 'Tacca integrifolia', '', 34),
(37, 'Psychopsis Papilio', NULL, '', 35),
(38, 'Saintpaulia Ionantha', 'Saintpaulia ionantha', '', 36),
(39, 'Gaillardia', 'Gaillardia aestivalis', '', 37),
(40, 'Amaryllis', 'Hippeastrum (group)', '', 38),
(41, 'Caladium Bicolor', 'Caladium bicolor', 'https://perenual.com/storage/species_image/1457_caladium_bicolor/small/25575875658_d782fb76f1_b.jpg', 39),
(42, 'Chlorophytum Comosum', 'Chlorophytum comosum ''Vittatum''', 'https://perenual.com/storage/species_image/1847_chlorophytum_comosum_vittatum/small/2560px-Chlorophytum_comosum_27Vittatum27_kz02.jpg', 40),
(44, 'Araucaria Heterophylla', 'Araucaria heterophylla', 'https://perenual.com/storage/species_image/917_araucaria_heterophylla/small/49833684212_2aff9d7b3c_b.jpg', 41),
(45, 'Begonia', 'Begonia ''Art Hodes''', '', 2),
(46, 'Medinilla Magnifica', 'Medinilla magnifica', '', 42),
(47, 'Calliandra Haematocephala', 'Calliandra haematocephala', 'https://perenual.com/storage/species_image/1477_calliandra_haematocephala/small/52063600268_834ebc0538_b.jpg', 43),
(48, 'Zamioculcas Zamiifolia', 'Zamioculcas zamiifolia', '', 44),
(49 ,'Crassula Ovata', 'Crassula ovata', 'https://perenual.com/storage/species_image/2193_crassula_ovata/small/33253726791_980c738a1e_b.jpg', 45),
(50, 'Epipremnum Aureum', 'Epipremnum aureum', 'https://perenual.com/storage/species_image/2773_epipremnum_aureum/small/2560px-Epipremnum_aureum_31082012.jpg', 1);