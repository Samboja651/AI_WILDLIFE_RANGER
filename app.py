""""application"""
from flask import Flask, render_template, jsonify, redirect, url_for, session, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from tensorflow.keras.models import load_model # ignore error, for now
from flask_mail import Message, Mail
from sinch import SinchClient
from dotenv import load_dotenv
import smtplib
import mysql
import os
from prediction import predict_location
from server import (
    fetch_gps_coordinates,
    store_predicted_locations,
    is_check_rtid_in_db,
    count_rows,
    calculate_correct_or_failed_predictions,
    get_correct_pred_value,
    get_failed_pred_value, connect_db,
    validate_auth_inputs,
    save_alert,
    get_latest_alert
)

# load variables from .env file
load_dotenv(".env")

API_KEY = os.environ.get('API_KEY')
OPENCAGE_API_KEY = os.environ.get('OPENCAGE_API_KEY')
RECEPIENT_MAIL = os.environ.get("RECIP_MAIL")
ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
KEY_SECRET = os.environ.get("KEY_SECRET")
PROJECT_ID = os.environ.get("PROJECT_ID")
SINCH_NUMBER = os.environ.get("SINCH_NUMBER")
RECEIVER_NUMBER = os.environ.get("RECEIVER_NUMBER")
SESSION_SECRET_KEY = os.environ.get("SESSION_SECRET_KEY")

app = Flask(__name__)
app.secret_key = SESSION_SECRET_KEY

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use Gmail SMTP
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("SENDER_MAIL")
app.config['MAIL_PASSWORD'] = os.environ.get("SENDER_PASS")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("SENDER_MAIL")

mail = Mail(app)

@app.route('/config')
def get_config():
    """sends opencage API to the frontend"""
    return jsonify({"opencage_apiKey": os.environ.get("OPENCAGE_API_KEY")})

@app.get('/')
def home():
    """view func for home"""
    return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    """register a ranger"""
    error = None
    db = connect_db()
    cursor = db.cursor()
    try:
        if request.method == 'POST':
            ranger_id = request.form['rangerId']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirmPassword']

            if not email:
                error = "Email is required."
            elif not password:
                error = "Password is required"
            elif not ranger_id:
                error = "Ranger id is required"

            if error is not None:
                flash(error)
                return redirect(url_for("register"))
            # validation
            message = validate_auth_inputs(
                ranger_id,
                email,
                password,
                confirm_password
            )
            # print(message)
            if message is not None:
                flash(message)
                return redirect(url_for("register"))

            # save user in database
            query = "INSERT INTO users (ranger_id, email, password) VALUES(%s, %s, %s)"
            cursor.execute(query, [ranger_id, email, generate_password_hash(password)])
            db.commit()
            cursor.close()
            db.close()
            print("user created in db")
            return redirect(url_for("login"))
        return render_template('register.html')
    except mysql.connector.IntegrityError:
        error = "User is already registered."
        flash(error)
        cursor.close()
        db.close()
        return redirect(url_for("register"))

@app.route('/login', methods=["GET", "POST"])
def login():
    """login a ranger"""
    try:
        if request.method == 'POST':
            message = None

            ranger_id = request.form['rangerId']
            password = request.form['password']

            # validate inputs
            message = validate_auth_inputs(
                ranger_id=ranger_id,
                password=password
            )

            if message is not None:
                flash(message)
                return redirect(url_for("login"))

            db = connect_db()
            cursor = db.cursor()
            query = "SELECT password FROM users WHERE ranger_id = %s"
            cursor.execute(query, [ranger_id])
            user = cursor.fetchone()

            if user is None:
                message = "Ranger id does not exist"
                flash(message)
                return render_template('login.html')

            if not check_password_hash(user[0], password):
                message = "Incorrect Password"
                flash(message)
                return render_template('login.html')

            if message is None:
                session.clear() # assign a new session
                session['ranger_id'] = ranger_id
                return redirect(url_for('home'))

        return render_template('login.html')
    except Exception as e:
        print(f"{e}")
        flash("An exception occured")
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    """logout"""
    session.clear()
    return redirect(url_for('home'))

@app.get('/model-report')
def model_report():
    """function for model reports"""
    # confirm user is logged in
    ranger_id = session.get('ranger_id')

    if ranger_id is not None:
        predictions_made = count_rows()
        correct_predictions = get_correct_pred_value()
        failed_predictions = get_failed_pred_value()

        # escape zerodivison error
        if int(correct_predictions) == 0:
            return render_template('report.html', predictions_made = predictions_made,
                                   correct_predictions = correct_predictions,
                                   failed_predictions = failed_predictions, success_rate = 0)

        # calculate success rate in percentage
        success_rate = (int(correct_predictions) / int(predictions_made)) * 100
        success_rate = round(success_rate, 2)
        return render_template('report.html', predictions_made = predictions_made,
                               correct_predictions = correct_predictions,
                               failed_predictions = failed_predictions,
                               success_rate = success_rate)
    flash("You have to log in")
    return redirect(url_for('login'))

@app.get('/view-map')
def display_location():
    """Display lion location google map"""
    ranger_id = session.get("ranger_id")
    if ranger_id is not None:
        return render_template("index.html", API_KEY = API_KEY)
    flash("You have to log in")
    return redirect(url_for('login'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    """view func for feedback"""
    ranger_id = session.get("ranger_id")
    if ranger_id is not None:
        try:
            if request.method == "POST":
                location_id = request.form['locID']
                animal_type = request.form['animalType']
                action_taken = request.form['actionTaken']
                conflict_avoided = request.form['conflictAvoided']
                
                if conflict_avoided == "Yes":
                    conflict_avoided = True
                else:
                    conflict_avoided = False

                # save in database
                conn = connect_db()
                cursor = conn.cursor()
                query = "INSERT INTO feedback(pd_id, animal_type, action_taken, conflict_avoided) VALUES(%s, %s, %s, %s)"
                cursor.execute(query, [location_id, animal_type, action_taken, conflict_avoided])
                conn.commit()
                cursor.close()
                conn.close()

                flash("Feedback was saved. Thank you Ranger 🎉.")
                return render_template('feedback.html')
            return render_template('feedback.html')
        except Exception as e:
            flash("🤔 An Error occured. Click above button & Retry")
            print(e)
            cursor.close()
            conn.close()
            return redirect(url_for('feedback'))
    flash("You have to log in.")
    return redirect(url_for('login'))

@app.get("/real-time-location/<int:coordinate_id>")
def _get_realtime_coordinates(coordinate_id): # only for background usage
    """
    api path to fetch realtime coordinate
    Args:
        id: int(id) of the coordinate in db
    Returns:
        Tuple: (long, lat) in json format
    """
    # not sure if to use sessions to authorize API usage
    try:
        coordinates = fetch_gps_coordinates(coordinate_id)
        longitude, latitude = coordinates
        return jsonify({"coordinates": {"longitude": longitude, "latitude": latitude}})
    except TypeError as e:
        return jsonify({"Error": e})


@app.get("/predict/location/<int:coordinate_id>/time/<int:time_interval>")
def _get_predicted_location(coordinate_id, time_interval): # only for background usage
    """
    Get the predicted location of the animal based on current location.
    Args:
        int: time_interval to get next animal location.
        int: coordinate_id for current animal location
    Returns:
        Tuple(str): coordinates (long, lat) in json format
    """
    # not sure if to use sessions to authorize API usage
    try:
        model = load_model('models/gps_location_prediction_model.keras')
        long, lat = fetch_gps_coordinates(coordinate_id)

        predicted_location = predict_location((float(long), float(lat)), time_interval, model)
        predicted_location = tuple(predicted_location.strip('[]').split())
        longitude, latitude = predicted_location

        # storing predition to the database
        if is_check_rtid_in_db(int(coordinate_id)) is False:
            store_predicted_locations(longitude, latitude, int(coordinate_id))
            calculate_correct_or_failed_predictions(longitude, latitude, int(coordinate_id))

        return jsonify({"coordinates": {"longitude": longitude, "latitude": latitude}})

    except FileNotFoundError as e:
        return jsonify({"Error!": e}) # figure out how to return with status code

    except TypeError as e:
        return jsonify({"Error!": e})

@app.post('/send-email-notification')
def _send_email(): # only for background usage
    """Send email to park authority"""
    try:
        msg = Message("Alert!", recipients=[RECEPIENT_MAIL])
        msg.body = """
        System predicts that 2hrs from now, lion Kiboche would have gone out of the park.
        Take proactive measure to mitigate the potential Human-Wildlife conflict.
        """
        mail.send(msg)
        return jsonify({"message": "Alert email sent successfully!"})
    except (ConnectionError, smtplib.SMTPException) as e:
        return jsonify({"error": str(e)}), 500

# send sms alert
@app.get('/send-sms-notification')
def _send_sms(): # only for background usage
    """Send SMS to park authority"""
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT location_long, location_lat FROM predictionData ORDER BY pd_id DESC LIMIT 1"
    cursor.execute(query)
    location = cursor.fetchone()

    message = f"""System predicts that 2hrs from now, lion Kiboche would have gone out of the park.
        Take proactive measure to mitigate the potential Human-Wildlife conflict.
        Exact Location {location}"""
    try:
        sinch_client = SinchClient(ACCESS_KEY_ID, KEY_SECRET, PROJECT_ID)
        sinch_client.sms.batches.send(
            body = message,
            to = [RECEIVER_NUMBER],
            from_ = SINCH_NUMBER,
            delivery_report = "none"
        )
        # return json with status code
        return jsonify({"message": "SMS sent successfully!"})
    except Exception as e:
        err_msg = f"Sms notification Failed\n{e}"
        return err_msg

@app.post('/save-notification/<int:pd_id>')
def _save_notification_in_db(pd_id):
    """save notification"""
    save_alert(pd_id)
    return jsonify({"message": "Alert was saved."}), 200

@app.get('/get-latest-alert-id')
def _get_latest_alert_id():
    """get latest alert id
    Returns
        int: alert id
    """
    response = get_latest_alert()
    if isinstance(response, int):
        return jsonify({"id": response}), 200

    response = 0
    return jsonify({"message": "id not found", "id": response}), 500





if __name__ == '__main__':
    app.run(debug=True)
