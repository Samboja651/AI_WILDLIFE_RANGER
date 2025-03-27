# Test Plan for the Lion Movement Prediction System

The goal is to test the functionality of each module

## Test Objectives

1. Verify the working of each module in the `server.py` and `prediction.py` files.
2. Verify the working of each api route in the `app.py`.
3. Evaluate the performance of the prediction model.
4. Evaluate the responsive of the UI.

## Test Scope

- The UI pages loads and all components work without errors.
- The code is formatted, well organized and without errors.

## Test Strategy

Unit testing with `pytest`.

### Objective 1

**Verify the working of each module in the `server.py` and `prediction.py` files.**

`server.py` modules:

- `connect_db`
- `read_gps_collar_data`
- `seed_db`
- `fetch_gps_collar_data`
- `fetch_gps_coordinates`
- `store_predicted_locations`
- `fetch_rt_id_from_prediction_data`
- `is_check_rtid_in_db`
- `count_rows`
- `calculate_correct_or_failed_predictions`
- `get_correct_pred_value`
- `get_failed_pred_value`

#### Test Cases

```1. server.connect_db```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_1 | None | mysql connection object | connection to db |
| TC_2 | Incorrect Host - `Jupiter` | Error | db connection Error handling |

```server.read_gps_collar_data```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_3 | file path - `archives/Kiboche_last_500_rows_data.csv` | list of rows - `[(), ()]` | conversion of csv data to a list |
| TC_4 | Incorrect file path | `Error! FileExistError` | file path |
| TC_5 | Incorrect file path | `Error! FileNotFoundError`| file exists |
| TC_6 | empty file | `Error! Empty file.` | no data in the file. |

```server.seed_db```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_7 | None | `seeding was successful` | populate db with gps collar data |
| TC_8 | `Kiboche_last_500_rows_data.csv` | `mysql error` | existense of correct data and format |

```server.fetch_gps_collar_data```

***works if the you have access rights to the data.***

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_9 | `https://drive.google.com/uc?id=1N9gEm56eMsf8qcRi3JwQzn2n4cxiuDsA&export=download` | `data downloaded successfully` | download gps collar data |
| TC_10 | `incorrect path` | `urlerror` | download gps collar data |

```server.fetch_gps_coordinates```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_11 | 2 | `('38.79582624285714', '-3.8786255285714284')` | ability to fetch coordinates from db. |
| TC_12 | '2' | `('38.79582624285714', '-3.8786255285714284')` | ability to fetch coordinates from db. |
| TC_13 | 2.2 | `('38.79582624285714', '-3.8786255285714284')` | ability to fetch coordinates from db. |
| TC_14 | two | `mysql error` | ability to fetch coordinates from db. |

```server.store_predicted_locations```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_15 | `'38.79582624285714', '-3.8786255285714284', 2` | `Predictions saved to Db` | Store predicted location in the database |
| TC_16 | `None, None, None` | `mysql error` | Handle missing input gracefully |

```server.fetch_rt_id_from_prediction_data```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_17 | None | List of tuples: `[(),()]` | Fetch real-time location IDs from the prediction table |

```server.is_check_rtid_in_db```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_18 | `1` | `True` | Check if the real-time location ID exists in the database |
| TC_19 | `999` | `False` | Handle non-existent IDs gracefully |
| TC_20 | `one` | `Type Error! id must be integer` | Handle invalid ID types gracefully |
| TC_21 | None | `Value Error! need to pass id` | Handle missing ID gracefully |

```server.count_rows```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_22 | None | `int` | Count the number of rows in the prediction table |

```server.calculate_correct_or_failed_predictions```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_23 | `pred_long=38.799088, pred_lat=-3.8896475, row_id=1` | None | Update the report table with correct or failed predictions |
| TC_24 | Invalid `row_id=one` | `mysql error` | Handle invalid row IDs gracefully |

```server.get_correct_pred_value```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_25 | None | `int` | Fetch the correct prediction count from the report table |

```server.get_failed_pred_value```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_26 | None | `int` | Fetch the failed prediction count from the report table |

```prediction.predict_location```

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_27 | `(38.79894688571429, -3.8889102571428573), 2, models/gps_location_prediction_model.h5` | `(38.799088, -3.8896475)` | predicting the next location |
| TC_28 | `(38.79894688571429, -3.8889102571428573), 2, Noinput` | `ValueError` | predicting the next location |
| TC_29 | `[38.79894688571429, -3.8889102571428573], 2, models/gps_location_prediction_model.h5` | `TypeError` | predicting the next location |
| TC_30 | `[38.79894688571429, -3.8889102571428573], None, models/gps_location_prediction_model.h5` | `Error! InvalidTime` | predicting the next location |

### Objective 2

Verify the working of each api route in the `app.py`

| Test Case id | Input | Expected Output | Remarks |
| -------- | -------- | -------- | -------- |
| TC_31 | `http://localhost:5000/` | 200 | home page |
| TC_32 | `http://localhost:5000/config` | 200 | api config |
| TC_33 | `http://localhost:5000/model-report` | 200 | model perfomance report page |
| TC_34 | `http://localhost:5000/display-location` | 200 | display map on home page |
| TC_35 | `http://localhost:5000/real-time-location/1` | 200 | get current lion location |
| TC_36 | `http://localhost:5000/predict/location/1/time/2` | 200 | predict the location of lion |
| TC_37 | `http://localhost:5000/send-alert` | 200 | send alert email messages |

### Objective 3

[Test model performance](test_model_perfomance.py)

### Objective 4

Manual usability testing using google chrome dev tools.

## Risk Analysis

??

## Test Environment

python3
venv
pytest
google chrome dev tools

## Entry/Exit Criteria

Entry: `Readme.md` `requirements.txt`
Exit: All test pass.

## Tools

Vscode Testing extension
pylint
