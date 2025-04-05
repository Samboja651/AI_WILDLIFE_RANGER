"""config database and app helper functions"""
import os
import urllib.error
import urllib.request
import mysql.connector
from dotenv import load_dotenv
from geopy.distance import geodesic

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
        return f"Connection failed! Error: {e}"
# print(connect_db())
def read_gps_collar_data(file):
    """
    reads gps collar data from file.
    
    Args: 
        file: contains gps collar data
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
        if len(values) == 0:
            return "Error! Empty file."
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
# print(read_gps_collar_data("archives/Kiboche_last_500_rows_data.csv"))

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

# you'll need access rights to data
DEFAULT_URL = "https://drive.google.com/uc?export=download&id=1N9gEm56eMsf8qcRi3JwQzn2n4cxiuDsA"
def fetch_gps_collar_data(url = DEFAULT_URL):
    """
    downloads gps collar data of the lions.
    Args:
        url: gps collar data
    returns: 
        file: csv
    """
    try:
        with urllib.request.urlopen(url) as f:
            data = f.read().decode('utf-8')
        with open('Kiboche_last_500_rows_data.csv', 'w', encoding='utf-8') as f:
            f.write(data)
        print("data downloaded successfully")
        return "data downloaded successfully"
    except urllib.error.URLError as e:
        print(f"Error! : {e}")
        return e
# fetch_gps_collar_data("url")


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
# print(fetch_gps_coordinates(2.9))

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
    try:
        ids = fetch_rtid_from_predicton_data()
        numbers = []
        for val in ids:
            numbers.append(val[0])

        if rt_id in numbers:
            return True
        else:
            return False
    except TypeError as e:
        print(f"Error! {e}")
        return "Type Error! id must be integer"
    # if rt_id is not passed raise error
    except ValueError as e:
        print(f"Error! {e}")
        return "Value Error! need to pass id"
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


def calculate_correct_or_failed_predictions(pred_long, pred_lat, row_id):
    """
    calculate correct and failed predictions based on coordinate displacement value
    """

    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()      
    try:
        # fetch the next real-time location from db
        query1 = "SELECT location_long, location_lat FROM kibocheRTData WHERE id = %s"
        cursor.execute(query1, [int(row_id) + 1])
        rtl_long_lat = cursor.fetchone()

        # convert to tuple
        predicted_tuple = (pred_lat, pred_long)
        realtime_tuple = (float(rtl_long_lat[1]), float(rtl_long_lat[0]))

        # calculate differential distance between predicted and actual location in meters
        distance = geodesic(predicted_tuple, realtime_tuple).meters
       
        # store distance in db
        query_2 = "INSERT INTO distance_record(rt_id, distance) VALUES(%s, %s)"
        cursor.execute(query_2, [row_id, float(distance)]) 
        conn.commit()
        
        # Check prediction accuracy
        if distance < 500:
            query = "UPDATE reportData SET correct_predictions = (correct_predictions + 1) WHERE id = 1"
            cursor.execute(query)
            conn.commit()
            print("This is a correct pred and we have updated report table.")
            return None
        else:
            query = "UPDATE reportData SET failed_predictions = (failed_predictions + 1) WHERE id = 1"
            cursor.execute(query)
            conn.commit()
            print("This is a failed pred and we have updated report table.")
            return None
    except mysql.connector.Error as e:
        print(f"Error, {e}")
        return e
    finally:
        # Ensure the connection is closed
        cursor.close()
        conn.close()
# print(calculate_correct_or_failed_predictions(38.799088 ,-3.8896475 ,1))

def get_correct_pred_value():
    """
    fetch the correct prediction value from db
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
    fetch the failed prediction value from db
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

# validating user registration data
def validate_auth_inputs(ranger_id: str=None, email: str=None, 
                         password: str=None, confirm_password: str=None
                         )->str:
    """Validate registration and login inputs."""
    message = None
    try:
        while message is None:
            # password mismatch
            if confirm_password is not None and password != confirm_password:
                message = "Passwords do not match!"
                break

            # include a uppercase letters
            if not any(char.isupper() for char in password):
                message = "Password must contain a uppercase letter."
                break

            # include a lowercase letters
            if not any(char.islower() for char in password):
                message = "Password must contain a lowercase letter."
                break

            # include a digit
            if not any(char.isdigit() for char in password):
                message = "Password must contain a numeric digit."
                break

            # include a special char
            if not any(char in '!@#$%^&*()-_=+[]{}|;:\'",.<>?/`~' for char in password):
                message = "Password must contain a special character."
                break

            # ranger id length
            if ranger_id is not None and (len(ranger_id) < 5 or len(ranger_id) > 8):
                message = "Ranger id not in range of 5-8 characters."
                break

            # valid email
            if email is not None and ("@" not in email or "." not in email):
                message = "Email must contain an '@' and '.'"
                break
            break
        return message
    except Exception as e:
        print(e)
        message = "Exception occured. Retry!"
        return message

# store alerts in db;
def save_alert(alert_id: int):
    """saves the alert into db.
    Args:
        alert_id: is the prediction id that raised alert.
    """
    # connect db
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO alerts(pd_id_alert) VALUE(%s)"
        cursor.execute(query, [int(alert_id)])
        conn.commit()
        cursor.close()
        conn.close()
        return "Success", 200

    except mysql.connector.Error as e:
        cursor.close()
        conn.close()
        return e
# print(save_alert(1503))

# fetch latest alert db
def get_latest_alert()->int:
    """get latest alert id from db"""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        query = "SELECT pd_id_alert FROM alerts ORDER BY alert_id DESC LIMIT 1;"
        cursor.execute(query)
        alert_id = cursor.fetchone()
        cursor.close()
        conn.close()

        return alert_id[0]
    except IndexError:
        cursor.close()
        conn.close()
        return "Index out of range"
# print(get_latest_alert())
