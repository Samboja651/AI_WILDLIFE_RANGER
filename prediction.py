"""create prediction function"""
import joblib
import numpy as np
from tensorflow.keras.models import load_model

def predict_location(current_location, time_interval, model):

    """
    Predicts the future location of a lion.

    Args:
        current_location: Tuple (longitude, latitude) representing the current location.
        time_interval: The time interval in hours for prediction.
        model: The trained LSTM model.

    Returns:
        Tuple (longitude, latitude) representing the predicted location.
    """
    
    # load the scaler 
    scaler = joblib.load('models/gps_data_scaler.pkl')
    # create input sequence
    input_sequence = np.array([current_location + (time_interval,)])

    # scale the input
    scaled_input = scaler.transform(input_sequence.reshape(1, -1))

    # reshape for lstm
    timestep = 1
    input_data = scaled_input.reshape(1, timestep, 3) # 3 rep number of features in my input

    # make prediction
    predicted_scaled_location = model.predict(input_data)[0] # get the first item in prediction

    # Reshape predicted_scaled_location to a 2D array before inverse transforming
    predicted_scaled_location = predicted_scaled_location.reshape(1, -1)

    # Pad with zeros to match original shape expected by scaler
    predicted_scaled_location_padded = np.pad(predicted_scaled_location, ((0, 0), (0, 1)), 'constant', constant_values=0)

    # inverse transform to get actual coordinate
    predicted_location = scaler.inverse_transform(predicted_scaled_location_padded)[0, :2] # select only first 2 elements

    return str(predicted_location)


# load the trained model
# model = load_model('models/gps_location_prediction_model.keras')

# # # use the prediction function
# # # ONLY EDIT THIS VARIABLE THEN RUN
# current_location = (38.79894688571429, -3.8889102571428573) # replace this part with your coordinates, ofcourse from db.

# TIME_INTERVAL = 2 # hours

# predicted_location = predict_location(current_location, TIME_INTERVAL, model).strip('[]').split()
# print(f"Predicted location: {tuple(predicted_location)}")
