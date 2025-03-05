"""config database"""
import os
from dotenv import load_dotenv
import mysql.connector
from server import read_gps_collar_data

# load variables from .env file
load_dotenv(".env")

USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')
HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
GPS_COLLAR_DATA = os.environ.get('GPS_COLLAR_DATA')

def connect_db():
    """
    function to connect db
    :returns connection string
    """
    try:
        connection = mysql.connector.connect(user = USER, password = PASSWORD, host = HOST, database = DATABASE)
        print("db connected")
        return connection
    except mysql.connector.Error as e:
        print(f"Connection failed! Error: {e}")
        return

def seed_db():
    """"populate database with simulated realtime data"""
    # establish connection to db
    db = connect_db()
    cursor = db.cursor()

    # get the gps data
    key, values = read_gps_collar_data(GPS_COLLAR_DATA)
    try:
        # insert query
        query = "INSERT INTO kibocheRTData(timestamp, location_long, location_lat, local_identifier, time_interval_hours)VALUES(%s, %s, %s, %s, %s)"

        # execute query
        cursor.executemany(query, values)
        cursor.close()
        db.commit()
        db.close()
        print("seeding was successful")
        return
    except mysql.connector.Error as e:
        print(f"Seeding failed, Error! {e}")
        return