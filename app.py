""""application"""
import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, redirect, url_for
from server import fetch_gps_coordinates
from prediction import predict_location
from tensorflow.keras.models import load_model # ignore error, for now

# load variables from .env file
load_dotenv(".env")

API_KEY = os.environ.get('API_KEY')
OPENCAGE_API_KEY = os.environ.get('OPENCAGE_API_KEY')

app = Flask(__name__)

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
    return render_template('report.html')


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
        return jsonify({"coordinates": {"longitude": longitude, "latitude": latitude}})
    except FileNotFoundError as e:
        return jsonify({"Error!": e})
    except TypeError as e:
        return jsonify({"Error!": e})


if __name__ == '__main__':
    app.run(debug=True, port=3000)
