"""
Test ability to predict location based based on input coordinates
"""

import unittest
from prediction import predict_location
import time
from tensorflow.keras.models import load_model

class TestPredictLocation(unittest.TestCase):
    """test able to predict"""
    def setUp(self):
        self.model = load_model('models/gps_location_prediction_model.keras')
        self.current_location = (38.79894688571429, -3.8889102571428573)
        self.time_interval = 2

    def test_predict_location(self):
        """test able to predict"""
        predicted_location = predict_location(self.current_location, self.time_interval, self.model)
        self.assertEqual(predicted_location, "[38.799088  -3.8896475]")

    def test_performance(self):
        """test simulate 100 concurrent requests runs under reasonable time"""
        start_time = time.time()
        for i in range(1, 101):
            predicted_location = predict_location(self.current_location, self.time_interval, self.model)
        end_time = time.time()
        self.assertLess(end_time - start_time, 10)

if __name__ == '__main__':
    unittest.main()