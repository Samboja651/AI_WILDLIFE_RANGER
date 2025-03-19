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
        connection = mysql.connector.connect(
            user = USER, password = PASSWORD, host = HOST, database = DATABASE)
        print("db connected")
        return connection
    except mysql.connector.Error as e:
        print(f"Connection failed! Error: {e}")
        return e

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
        return e
    except FileNotFoundError as e:
        print(f"Error! {e}")
        return e
    except IndexError as e:
        print(f"Error! {e}")
        return e
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
        return "seeding was successful"
    except mysql.connector.Error as e:
        print(f"Seeding failed, Error! {e}")
        return e
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
        return "data downloaded successfully"
    except urllib.error.URLError as e:
        print(f"Error! : {e}")
        return e
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
        return e
# print(fetch_gps_coordinates(2))

def store_predicted_locations(long:str, lat:str, curr_loc_id:int):
    """
    stores predicted location to the database.
    Args:
        long: predicted longitude
        lat: predicted latitude
        curr_loc_id: current real-time location id

    Returns: 
        None
    """
    # connect db
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO predictionData(rt_id, location_long, location_lat) VALUES(%s,%s,%s)"
        cursor.execute(query, [int(curr_loc_id), long, lat])
        conn.commit()

        #close connection
        cursor.close()
        conn.close()
        print("Predictions saved to Db")
        return "Predictions saved to Db"
    except mysql.connector.Error as e:
        print(f"Error! {e}")
        return e


def fetch_rtid_from_predicton_data():
    """
    fetch current real-time locaion id from prediction table
    Returns:
        List of tuples: [(),()]
    """
    # connect db
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = "SELECT rt_id FROM predictionData"
        cursor.execute(query)
        rt_ids = cursor.fetchall()

        #close connection
        cursor.close()
        conn.close()
        return rt_ids
    except mysql.connector.Error as e:
        print(f"Error! {e}")
        return e
# print(fetch_rtid_from_predicton_data())

def is_check_rtid_in_db(rt_id):
    """
    Returns: 
        bool
    """
    ids = fetch_rtid_from_predicton_data()
    numbers = []
    for val in ids:
        numbers.append(val[0])

    if rt_id in numbers:
        return True
    else:
        return False
# print(is_check_rtid_in_db(1))

def count_rows():
    """
    count number of rows in prediction db -> rep unique predictions.
    Returns:
        str: number of rows in db
    """
    # connect db
    conn = connect_db()
    cursor = conn.cursor()
    try:
        query = "SELECT COUNT(pd_id) FROM predictionData"
        cursor.execute(query)
        count = cursor.fetchall()

        # close conn
        cursor.close()
        conn.close()
        return count[0][0]
    except mysql.connector.Error as e:
        print(f"Error! {e}")
        return e
# print(count_rows())


def calculate_correct_or_failed_predictions(pred_long, pred_lat, rowId):
    """
    pass
    """

    # Connect to the database
    conn = connect_db()
    try:
        cursor = conn.cursor()
        
        query1 = "SELECT location_long, location_lat FROM kibocheRTData WHERE id = %s"

        cursor.execute(query1, [int(rowId)])
        rtl_long_lat = cursor.fetchone()


        # Check prediction accuracy
        if abs(float(pred_long) - float(rtl_long_lat[0])) <= 0.001 and \
            abs(float(pred_lat) - float(rtl_long_lat[1])) <= 0.001:

            query2 = "SELECT correct_predictions FROM reportData WHERE id = 1"
            
            cursor.execute(query2)
            correct_pred_val = cursor.fetchone()
            
            new_correct_pred_val = int(correct_pred_val[0]) + 1

            query3 = "UPDATE reportData SET correct_predictions = %s WHERE id = 1"

            cursor.execute(query3, [int(new_correct_pred_val)])
            conn.commit()
            print("This is a correct pred and we have updated report table.")

        else:
            query4 = "SELECT failed_predictions FROM reportData WHERE id = 1"
            
            cursor.execute(query4)
            correct_pred_val = cursor.fetchone()
            
            new_failed_pred_val = int(correct_pred_val[0]) + 1

            query5 = "UPDATE reportData SET failed_predictions = %s WHERE id = 1"

            cursor.execute(query5, [int(new_failed_pred_val)])
            conn.commit()
            print("This is a failed pred and we have updated report table.")
    finally:
        # Ensure the connection is closed
        cursor.close()
        conn.close()

# print(calculate_correct_or_failed_predictions(38.799088 ,-3.8896475 ,1))

def get_correct_pred_value():
    """
    pass
    """

    # connect db
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = "SELECT correct_predictions FROM reportData WHERE id = 1"
        cursor.execute(query)
        correct_pred_val = cursor.fetchone()

        # close conn
        cursor.close()
        conn.close()
        return correct_pred_val[0]
    except mysql.connector.Error as e:
        print(f"Error! {e}")
        return e
    

def get_failed_pred_value():
    """
    pass
    """

    # connect db
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = "SELECT failed_predictions FROM reportData WHERE id = 1"
        cursor.execute(query)
        failed_pred_val = cursor.fetchone()

        # close conn
        cursor.close()
        conn.close()
        return failed_pred_val[0]
    except mysql.connector.Error as e:
        print(f"Error! {e}")
        return e