# Computer Systems Project

[link to project documentation](https://onedrive.live.com/view?id=43505624473455EF!3340&resid=43505624473455EF!3340&authkey=!ArLn6xbCh_7MAEs&wdo=2&cid=43505624473455ef)

[link to Kiboche 'real-time' data](https://drive.google.com/uc?id=1N9gEm56eMsf8qcRi3JwQzn2n4cxiuDsA&export=download)

## Setup the environment
Download and add kiboche data to root directory.\
Open mysql, copy, paste and run the schema.sql. **Note- I made changes to the schema.**\

### Install dependencies,
Create virtual environment.
1. On windows run \
   `python3 -m venv .venv` \
   `.venv\Scripts\activate`
2. On Linux run \
   `python3 -m venv .venv` \
   `.venv\bin\activate`

upgrade pip:
- linux `python -m pip install --upgrade pip`
- windows `py -m pip install --upgrade pip`
Run `pip install -r requirements.txt`.

## Running the code
Adding the portion of the real_time data to the database 
- Run the `main.py` file. or on terminal run `python3 main.py`

Displaying the UI
- Run the `app.py` file, or on terminal run `python3 app.py`


## Operation
`prediction.py` - use the trained model to make predictions.

## Troubleshooting tips
First ensure you have installed all dependencies in `requirements.txt` file. Do this in a virtual environment.

## Directory structure
```
Animal_Movement_Prediction_Sys
├── app.py
├── db_operations.py
├── gps_collar_data.csv
├── Kiboche_last_500_rows_data.csv
├── main.py
├── models
│   ├── gps_data_scaler.pkl
│   ├── gps_location_prediction_model.h5
│   └── gps_location_prediction_model.keras
├── prediction.py
├── project-guideline.pdf
├── __pycache__
│   ├── db_operations.cpython-312.pyc
│   ├── main.cpython-312.pyc
│   └── server.cpython-312.pyc
├── README.md
├── requirements.txt
├── schema.sql
├── server.py
├── static
│   └── css
│       └── main.css
├── templates
│   ├── index.html
│   └── report.html
├── Tsavo Lion Study.csv
└── Tsavo_Lion_Study.ipynb


```