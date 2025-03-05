-- dbms = mysql
CREATE DATABASE IF NOT EXISTS WDF_conservation;
USE WDF_conservation;
-- realtime data for lion named kiboche
CREATE TABLE IF NOT EXISTS kibocheRTData(
    id INT PRIMARY KEY AUTO_INCREMENT,
    timestamp DATETIME NOT NULL,
    location_long FLOAT NOT NULL,
    location_lat FLOAT NOT NULL,
    time_interval_hours FLOAT NOT NULL
);
CREATE TABLE IF NOT EXISTS reportData(
    id INT PRIMARY KEY AUTO_INCREMENT,
    predictions_made INT NOT NULL,
    correct_predictions INT NOT NULL,
    failed_predictions INT NOT NULL,
    success_rate FLOAT NOT NULL
);
CREATE USER 'wdf_conservatist'@'localhost' IDENTIFIED BY '@WildlifeTech2025'; -- create another user instead of root operations.
GRANT ALL PRIVILEGES ON WDF_conservation.* TO 'wdf_conservatist'@'localhost';
-- end