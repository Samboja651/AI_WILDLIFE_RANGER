""""application"""
import os
import smtplib
from flask_mail import Message, Mail
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, redirect, url_for
from tensorflow.keras.models import load_model # ignore error, for now
from prediction import predict_location
from server import fetch_gps_coordinates, store_predicted_locations, is_check_rtid_in_db, count_rows

# load variables from .env file
load_dotenv(".env")

app = Flask(__name__)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use Gmail SMTP
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("SENDER_MAIL")
app.config['MAIL_PASSWORD'] = os.environ.get("SENDER_PASS")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("SENDER_MAIL")
recipient_mail = os.environ.get("RECIP_MAIL")

API_KEY = os.environ.get('API_KEY')
OPENCAGE_API_KEY = os.environ.get('OPENCAGE_API_KEY')

mail = Mail(app)

@app.route('/config')
def get_config():
    """sends opencage API to the frontend"""
    return jsonify({"opencage_apiKey": os.environ.get("OPENCAGE_API_KEY")})


@app.get('/')
def main():
    """view func for home"""
    return render_template('index.html', API_KEY = API_KEY)


@app.get('/model-report')
def model_report():
    """function for model reports"""
    return render_template('report.html', predictions_made = count_rows())


@app.get('/display-map')
def display_map():
    """Display Tsavo map"""
    return redirect(url_for('main'))


@app.get("/real-time-location/<int:coordinate_id>")
def get_realtime_coordinates(coordinate_id):
    """
    api path to fetch realtime coordinate
    Args:
        id: int(id) of the coordinate in db
    Returns:
        Tuple: (long, lat) in json format
    """
    try:
        coordinates = fetch_gps_coordinates(coordinate_id)
        longitude, latitude = coordinates
        return jsonify({"coordinates": {"longitude": longitude, "latitude": latitude}})
    except TypeError as e:
        return jsonify({"Error": e})


@app.get("/predict/location/<int:coordinate_id>/time/<int:time_interval>")
def get_predicted_location(coordinate_id, time_interval):
    """
    Get the predicted location of the animal based on current location.
    Args:
        int: time_interval to get next animal location.
        int: coordinate_id for current animal location
    Returns:
        Tuple(str): coordinates (long, lat) in json format
    """
    try:
        model = load_model('models/gps_location_prediction_model.keras')
        long, lat = fetch_gps_coordinates(coordinate_id)

        predicted_location = predict_location((float(long), float(lat)), time_interval, model)
        predicted_location = tuple(predicted_location.strip('[]').split())
        longitude, latitude = predicted_location
        # storing predition to the database
        if is_check_rtid_in_db(int(coordinate_id)) is False:
            store_predicted_locations(longitude, latitude, int(coordinate_id))
        return jsonify({"coordinates": {"longitude": longitude, "latitude": latitude}})
    except FileNotFoundError as e:
        return jsonify({"Error!": e})
    except TypeError as e:
        return jsonify({"Error!": e})

# Endpoint to send alert email
@app.route('/send-alert', methods=['POST'])
def send_alert():
    """Send email to park authority"""
    try:
        msg = Message("Alert!", recipients=[recipient_mail])
        msg.body = """
        Model predicts that 2hrs from now, lion Kiboche would have gone out of the park.\n
        Take proactive measure to reduce the chance of Human-Wildlife conflict from occuring!"""
        mail.send(msg)
        return jsonify({"message": "Alert email sent successfully!"})
    except (ConnectionError, smtplib.SMTPException) as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=3000)
