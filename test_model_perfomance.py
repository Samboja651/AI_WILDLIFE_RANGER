"""automated test """
import requests


def model_perfomance(row_id):
    """
    testing the model performance\n
    function moves through each row on realtime data\n 
    passes it to the prediction api path and records the results in db.\n
    This results concurrently display in the reports page.

    Args: 
        int: row_id of the coordinates of realtime data in db.
    """
    for row_id in range(1, 501, 1):
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
    return
