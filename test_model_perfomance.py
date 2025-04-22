"""model performance test"""
import time
import requests


def model_perfomance():
    """
    testing the model performance\n
    function moves through each row on realtime data\n 
    passes it to the prediction api path and records the results in db.\n
    This results concurrently display in the reports page.
    Only for local development & testing
    Args: 
        int: row_id of the coordinates of realtime data in db.
    """
    start_time = time.time()
    for row_id in range(31, 41, 1):
        # ensure the port is correct as that of running app
        url = f"http://127.0.0.1:5000/predict/location/{row_id}/time/2"

        # make api get requests
        try:
            response = requests.get(url, timeout=20) # 20 seconds timeout if server doesn't respond
            with open("test_log_500.log", mode="a", encoding="utf-8") as log:
                log.write(f"row: {row_id}, response: {response.status_code}, \n")
        except requests.Timeout as e:
            with open("test_log_500.log", mode="a", encoding="utf-8") as log:
                log.write(f"{e}")
            continue
        finally:
            continue
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")

model_perfomance()
