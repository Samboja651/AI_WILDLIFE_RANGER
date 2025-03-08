""""application"""
from flask import Flask, render_template, redirect, url_for, request
from server import fetch_gps_coordinates
from prediction import predict_location
from tensorflow.keras.models import load_model

app = Flask(__name__)

@app.get('/')
def main():
    """view func for home"""
    return render_template('index.html')


@app.get('/model-report')
def model_report():
    """function for model reports"""
    return render_template('report.html')

# untested
@app.get("/real-time-location/<id>")
def get_realtime_coordinates(id):
    """
    api path to fetch realtime coordinate
    Args:
        id: int(id) of the coordinate in db
    Returns:
        Tuple: (long, lat)
    """
    try:
        coordinates = fetch_gps_coordinates(int(id))
        return coordinates
    except TypeError as e:
        return f"Error! {e}"
    
# untested
@app.route("/predict-location/<time_interval>", methods=["GET, POST"])
def get_predicted_location(time_interval):
    """
    Get the predicted location of the animal based on current location.
    Args: 
        int: time_interval to get next animal location. 
    Returns:
        Tuple: coordinates (long, lat)
    """
    if request.method == "POST":
        try:
            model = load_model('models/gps_location_prediction_model.keras')
            current_location = redirect(url_for(get_realtime_coordinates))

            predicted_location = predict_location(current_location, int(time_interval), model)
            return predicted_location
        except FileNotFoundError as e:
            return f"Error! {e}"
        except Exception as e:
            return f"Error! {e}"
    
if __name__ == '__main__':
    app.run(debug=True, port=3000)