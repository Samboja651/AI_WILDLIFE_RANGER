"""config database and app helper functions"""
import os
import urllib.error
import urllib.request
import mysql.connector
from dotenv import load_dotenv


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

def read_gps_collar_data(file):
    """
    reads gps collar data from file.
    returns data in keys(columns) and list(val(tuples))
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = f.readlines()

        # get the column names
        # keys = data[:1][0].strip().split(",")
        values = []
        for val in data[1:]:
            val = val.strip().split(',')
            values.append(tuple(val))
        return values

    except FileExistsError as e:
        print(f"Error! {e}")
        return
    except FileNotFoundError as e:
        print(f"Error! {e}")
        return
    except IndexError as e:
        print(f"Error! {e}")
        return

# read_gps_collar_data("Kiboche_last_500_rows_data.csv")

def seed_db():
    """"populate database with simulated realtime data"""
    # establish connection to db
    db = connect_db()
    cursor = db.cursor()

    # get the gps data
    values = read_gps_collar_data(GPS_COLLAR_DATA)
    try:
        # insert query
        query = """
        INSERT INTO kibocheRTData(
        timestamp, location_long, location_lat, local_identifier, time_interval_hours)
        VALUES(%s, %s, %s, %s, %s)"""

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
# seed_db()

def fetch_gps_collar_data(url):
    """
    fetches gps collar data of an animal
    returns data_file
    """
    try:
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        with open('gps_collar_data.csv', 'w', encoding='utf-8') as f:
            f.write(data)
        print("data downloaded successfully")
        return
    except urllib.error.URLError as e:
        print(f"Error! : {e}")
        return

# fetch_gps_collar_data(URL2)


def fetch_gps_coordinates(coordinate_id):
    """
    fetch the gps coordinates (long, lat) from db.
    Args:
        id: id of the coordinate in the db.

    Returns:
        Tuple (long, lat) representing real animal location
    """

    # connect db
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = "SELECT location_long, location_lat FROM kibocheRTData WHERE id = %s"

        cursor.execute(query, [int(coordinate_id)])
        coordinates = cursor.fetchone()

        # close connection
        cursor.close()
        conn.close()
        return coordinates
    except mysql.connector.Error as e:
        print(f"Error! {e}")
        return

# print(fetch_gps_coordinates(2))
