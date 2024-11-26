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
    ISO_code VARCHAR(2)
);

CREATE TABLE epsilon.botanist (
    botanist_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    full_name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE epsilon.plant (
    plant_id SMALLINT IDENTITY(1,1) PRIMARY KEY,
    plant_name VARCHAR(30) UNIQUE NOT NULL,
    scientific_name VARCHAR(30) UNIQUE NOT NULL,
    image_URL VARCHAR(255) UNIQUE,
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