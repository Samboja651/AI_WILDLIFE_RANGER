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

Run `pip install -r requirements.txt`.

## Running the code
Run the `main.py` file. or terminal run `python3 main.py`

## Directory structure
```
Animal_Movement_Prediction_Sys/
├── .venv
├── .env
├── .gitignore
├── db_operation.py
├── Kiboche_last_500_rows_data.csv
├── main.py
├── README.md
├── requirements.txt
├── schema.sql
└── server.py

```