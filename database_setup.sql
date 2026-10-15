-- =========================================================================
-- CityCore-3D : Database Setup Script
-- Author: Vansh Gupta
-- Bhai, ye script saari zaroori tables banayegi jo real-world GPS data, 
-- 3D buildings aur hamari game ki economy ko sambhalengi.
-- MySQL Workbench ya terminal mein ise chala lena bhai!
-- =========================================================================

-- Sabse pehle check karo ki database hai ya nahi, nahi toh naya bana do
CREATE DATABASE IF NOT EXISTS citycore_db;
USE citycore_db;

-- Agar purani tables padi hain toh unhe hatao taaki ekdum fresh start ho sake
DROP TABLE IF EXISTS economy_logs;
DROP TABLE IF EXISTS map_buildings;
DROP TABLE IF EXISTS city_zones;

-- 1. City Zones Table: Jahan ka bhi map load karenge, uska basic data yahan aayega
CREATE TABLE city_zones (
    zone_id INT AUTO_INCREMENT PRIMARY KEY,
    zone_name VARCHAR(150) NOT NULL UNIQUE,     -- Jaise 'Roorkee - Civil Lines' ya 'Mumbai Central'
    latitude FLOAT NOT NULL,                    -- Asli GPS Latitude
    longitude FLOAT NOT NULL,                   -- Asli GPS Longitude
    total_population INT DEFAULT 20000,         -- Wahan ki lagbhag population
    zone_budget FLOAT DEFAULT 10000000.0,       -- Municipal budget simulation ke liye
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Map Buildings Table: Overpass API se jo asli dukaanein aur landmarks aayenge, wo yahan save honge
CREATE TABLE map_buildings (
    building_id INT AUTO_INCREMENT PRIMARY KEY,
    zone_id INT NOT NULL,
    building_name VARCHAR(255) NOT NULL,        -- Dukaan ya landmark ka asli naam
    building_type VARCHAR(100) NOT NULL,        -- Jaise 'Shop', 'Hospital', 'Commercial', 'Residential'
    coordinate_x FLOAT NOT NULL,                -- 3D engine ke andar X position
    coordinate_z FLOAT NOT NULL,                -- 3D engine ke andar Z position
    power_drain FLOAT DEFAULT 50.0,             -- Bijli ki khapat
    water_drain FLOAT DEFAULT 30.0,             -- Paani ki khapat
    pollution_index FLOAT DEFAULT 10.0,         -- Pradushan kitna hai
    google_rating FLOAT DEFAULT 4.5,            -- Agar rating ho toh
    image_url TEXT DEFAULT NULL,                -- Shop ki photo ka link ya path
    status VARCHAR(20) DEFAULT 'Active',
    FOREIGN KEY (zone_id) REFERENCES city_zones(zone_id) ON DELETE CASCADE
);

-- 3. Economy Logs Table: Pandas aur Matplotlib ke graphs ke liye data yahan track hoga
CREATE TABLE economy_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    current_budget FLOAT NOT NULL,
    happiness_index FLOAT DEFAULT 100.0,
    power_usage_kw FLOAT DEFAULT 0.0,
    active_events VARCHAR(255) DEFAULT 'Normal Operations'
);

-- =========================================================================
-- Sample / Default Data (Testing ke liye ek basic entry daal rahe hain)
-- Baki ka asli data jab Python code chalega toh Overpass API se apne aap aa jayega.
-- =========================================================================
INSERT INTO city_zones (zone_name, latitude, longitude, total_population, zone_budget)
VALUES ('Default Exploration Zone', 29.8543, 77.8880, 50000, 25000000.0);

INSERT INTO map_buildings (zone_id, building_name, building_type, coordinate_x, coordinate_z, power_drain, water_drain, pollution_index, google_rating)
VALUES 
(1, 'Main City Square', 'Landmark', 0.0, 0.0, 10.0, 5.0, 2.0, 4.8);