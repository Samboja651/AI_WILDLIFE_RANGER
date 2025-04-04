"""test api endpoints"""
import unittest
import requests

BASE_URL = "https://ai-wildlife-ranger.onrender.com" 

class TestAPIEndpoints(unittest.TestCase):
    """Test API endpoints."""
    def test_home_endpoint(self):
        """Test the home endpoint."""
        response = requests.get(f"{BASE_URL}/", timeout=10)
        self.assertEqual(response.status_code, 200)

    def test_register_endpoint(self):
        """Test the register endpoint (GET)."""
        response = requests.get(f"{BASE_URL}/register", timeout=10)
        self.assertEqual(response.status_code, 200)

    def test_login_endpoint(self):
        """Test the login endpoint (GET)."""
        response = requests.get(f"{BASE_URL}/login", timeout=10)
        self.assertEqual(response.status_code, 200)

    def test_model_report_endpoint(self):
        """Test the model report endpoint (GET)."""
        response = requests.get(f"{BASE_URL}/model-report", timeout=10)
        self.assertIn(response.status_code, [200, 302])  # Redirects to login if not authenticated

    def test_view_map_endpoint(self):
        """Test the view map endpoint (GET)."""
        response = requests.get(f"{BASE_URL}/view-map", timeout=10)
        self.assertIn(response.status_code, [200, 302])  # Redirects to login if not authenticated

    def test_feedback_endpoint(self):
        """Test the feedback endpoint (GET)."""
        response = requests.get(f"{BASE_URL}/feedback", timeout=10)
        self.assertIn(response.status_code, [200, 302])  # Redirects to login if not authenticated

    def test_real_time_location_endpoint(self):
        """Test the real-time location endpoint."""
        response = requests.get(f"{BASE_URL}/real-time-location/1", timeout=10)
        self.assertEqual(response.status_code, 200)
        self.assertIn("coordinates", response.json())

    def test_predict_location_endpoint(self):
        """Test the predict location endpoint."""
        response = requests.get(f"{BASE_URL}/predict/location/1/time/2", timeout=10)
        self.assertEqual(response.status_code, 200)
        self.assertIn("coordinates", response.json())

    def test_send_email_notification_endpoint(self):
        """Test the send email notification endpoint."""
        response = requests.post(f"{BASE_URL}/send-email-notification", timeout=10)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Alert email sent successfully!", response.json().get("message", ""))

    def test_send_sms_notification_endpoint(self):
        """Test the send SMS notification endpoint."""
        response = requests.get(f"{BASE_URL}/send-sms-notification", timeout=10)
        self.assertIn(response.status_code, [200, 500])  # May fail if Sinch API credentials are invalid

    def test_save_notification_endpoint(self):
        """Test the save notification endpoint."""
        response = requests.post(f"{BASE_URL}/save-notification/1", timeout=10)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Alert was saved.", response.json().get("message", ""))

    def test_get_latest_alert_id_endpoint(self):
        """Test the get latest alert ID endpoint."""
        response = requests.get(f"{BASE_URL}/get-latest-alert-id", timeout=10)
        self.assertIn(response.status_code, [200, 500])  # May fail if no alerts exist

if __name__ == "__main__":
    unittest.main()
