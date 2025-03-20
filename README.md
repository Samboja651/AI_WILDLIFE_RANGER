# Computer Systems Project

[link to project documentation](https://onedrive.live.com/view?id=43505624473455EF!3340&resid=43505624473455EF!3340&authkey=!ArLn6xbCh_7MAEs&wdo=2&cid=43505624473455ef)

[link to Kiboche 'real-time' data](https://drive.google.com/uc?id=1N9gEm56eMsf8qcRi3JwQzn2n4cxiuDsA&export=download)

## Setup the environment

Download and add kiboche data to root directory.\
Open mysql, copy, paste and run the schema.sql. **Note- I made changes to the schema.**\

### Install dependencies

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

### setup db

Paste the content of `schema.sql` into your mysql and execute.
Adding the portion of the real_time data to the database

- Run the `main.py` file. or on terminal run `python3 main.py`

Displaying the UI

- On the terminal run `flask run --debug` file, or run `python3 app.py`

## Operation

`prediction.py` - use the trained model to make predictions.

## Tested API calls

`GET` - `/` returns home page.\
`GET` - `/model-report` returns model report page.\
`GET` - `/display-map`\ returns to home page
`GET` - `/real-time-location/<int:coordinate_id>` returns current location of animal.\
`GET` - `/predict/location/<int:coordinate_id>/time/<int:time_interval>` returns the predicted location of animal.\
**replace the part `<...>` with a value e.g `/predict/location/1/time/2"`**.

## Troubleshooting tips

First ensure you have installed all dependencies in `requirements.txt` file. Do this in a virtual environment.
...

# New updates

Rename `.env_2` to `.env` or create a new `.env` file in root folder.\
Add the following environmen variables along with their values into .env file.

```
USER = "wdf_conservatist"
PASSWORD = "YOUR_USER_PASSWORD"
HOST = "localhost"
DATABASE = "WDF_conservation"
GPS_COLLAR_DATA = "download of lion kiboche last 500 rows data"
API_KEY = "YOUR GCP MAPS JAVASCRIPT API KEY"
```

### How the map is displayed

- fetch real time location of lion from the inbuilt api.
- fetch predicted location of lion from the inbuilt api.
- usi maps javascrip api to load Tsavo park map.
- add markers on map to show current and predicted location of lion.
- run the app to see map.
- hover on the markers for more desription.

### Checking whether the predicted location is within the park(Taita taveta county)

- Try different real time location that we have.
- While changing the real time data we get a predicted location for that real time coodinate. so check message being displayed in the console.

### Send Email alert to park authority if predicted location is outside the park(Kwale county)

- first run `pip install Flask-Mail` to install flask_mail lib.
- when the predicted loc coordinate is outside the park, an email sent to park authority informing then so as to take a proactive measure in mitigating HWC.

### Dynamic change of our real-time data while fetching reponse from server

- Added an input tag in the `index.html` file for accepting row ids from 1 through 500.
- When `try this` button is clicked, the given row id value will be used during fetch from a server endpoint.
- By default if no value is given, we just use row id 1.

**TODO**
document about the following.\

- geopy function
- how each feature in the app works

setting up git for to remove the name `unknown` in commits.

```git Bash
git config --global user.name "Your Name"
git config --global user.email "your github account email"
```

## Directory structure
