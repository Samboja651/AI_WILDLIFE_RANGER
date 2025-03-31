-- dbms = postgresql
-- CREATE DATABASE WDF_conservation;
-- realtime data for lion named kiboche
-- we preserve the datatypes as obtained from data source. 
CREATE TABLE IF NOT EXISTS kibocheRTData(
    id SERIAL PRIMARY KEY,
    timestamp VARCHAR(30) NOT NULL,
    location_long VARCHAR(30) NOT NULL,
    location_lat VARCHAR(30) NOT NULL,
    local_identifier VARCHAR(50) NOT NULL,
    time_interval_hours VARCHAR(30) NOT NULL
);
CREATE TABLE IF NOT EXISTS reportData(
    id SERIAL PRIMARY KEY,
    correct_predictions INT NOT NULL,
    failed_predictions INT NOT NULL
);
INSERT INTO reportData(correct_predictions, failed_predictions) VALUES(0, 0);
CREATE TABLE IF NOT EXISTS predictionData(
    pd_id SERIAL PRIMARY KEY,
    rt_id  INT UNIQUE NOT NULL,
    location_long VARCHAR(30) NOT NULL,
    location_lat VARCHAR(30) NOT NULL,
    FOREIGN KEY (rt_id) REFERENCES kibocheRTData(id)
);
CREATE TABLE IF NOT EXISTS distance_record(
    id SERIAL PRIMARY KEY,
    rt_id INT UNIQUE NOT NULL,
    distance FLOAT,
    FOREIGN KEY (rt_id) REFERENCES kibocheRTData(id)
);
CREATE TABLE IF NOT EXISTS users(
    user_id SERIAL PRIMARY KEY,
    ranger_id VARCHAR(8) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);
CREATE TABLE IF NOT EXISTS alerts(
    alert_id SERIAL PRIMARY KEY,
    pd_id_alert INT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    pd_id INT NOT NULL,
    animal_type VARCHAR(20) NOT NULL,
    action_taken TEXT NULL,
    conflict_avoided BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- create another user instead of root operations.
-- CREATE USER wdf_conservatist WITH PASSWORD '@WildlifeTech2025';
-- GRANT ALL ON DATABASE WDF_conservation TO wdf_conservatist;
-- GRANT CONNECT ON DATABASE WDF_conservation TO wdf_conservatist;