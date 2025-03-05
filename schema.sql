-- dbms = mysql
CREATE DATABASE IF NOT EXISTS WDF_conservation;
USE WDF_conservation;
-- realtime data for lion named kiboche
-- we preserve the datatypes as obtained from data source. 
CREATE TABLE IF NOT EXISTS kibocheRTData(
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp VARCHAR(30) NOT NULL,
    location_long VARCHAR(30) NOT NULL,
    location_lat VARCHAR(30) NOT NULL,
    local_identifier VARCHAR(50) NOT NULL,
    time_interval_hours VARCHAR(30) NOT NULL
);
CREATE TABLE IF NOT EXISTS reportData(
    id INT PRIMARY KEY AUTO_INCREMENT,
    predictions_made INT NOT NULL,
    correct_predictions INT NOT NULL,
    failed_predictions INT NOT NULL,
    success_rate FLOAT NOT NULL
);
CREATE USER IF NOT EXISTS 'wdf_conservatist'@'localhost' IDENTIFIED BY '@WildlifeTech2025'; -- create another user instead of root operations.
GRANT ALL PRIVILEGES ON WDF_conservation.* TO 'wdf_conservatist'@'localhost';
-- end