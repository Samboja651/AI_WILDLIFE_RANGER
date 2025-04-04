import requests
from concurrent.futures import ThreadPoolExecutor

# Define the endpoint and number of concurrent requests
ENDPOINT = "https://ai-wildlife-ranger.onrender.com/"
NUM_REQUESTS = 50

def send_request(request_id):
    """Send a GET request to the prediction endpoint."""
    url = ENDPOINT
    try:
        response = requests.get(url, timeout=20)  # 10 seconds timeout
        return f"Request {request_id}: {response.status_code} - {response.json()}"
    except requests.RequestException as e:
        return f"Request {request_id}: Failed - {e}"

def main():
    """Simulate 50 concurrent requests."""
    with ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
        # Submit tasks for concurrent execution
        futures = [executor.submit(send_request, request_id) for request_id in range(1, NUM_REQUESTS + 1)]
        
        # Collect and print results
        for future in futures:
            print(future.result())

if __name__ == "__main__":
    main()
