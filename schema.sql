CREATE DATABASE HWC_DB;

USE HWC_DB;

CREATE TABLE kibocheRTData(
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    location_long FLOAT NOT NULL,
    location_lat FLOAT NOT NULL,
    individual_local_identifier VARCHAR(20) NOT NULL, -- i don't think if this column data is important.
    time_interval_hours FLOAT NOT NULL
);

CREATE TABLE reportData(
    id INT AUTO_INCREMENT PRIMARY KEY,
    predictions_made INT NOT NULL,
    correct_predictions INT NOT NULL,
    failed_predictions INT NOT NULL,
    success_rate FLOAT NOT NULL
);