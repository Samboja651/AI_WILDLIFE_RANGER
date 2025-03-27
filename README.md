# Lion Movement Prediction System

A web prototype built with Flask that enables rangers to see the future location of a lion and get email alerts when this location is in a restricted area.

## Overview

AI Lion Ranger is a prototype designed to reduce human wildlife conflicts by increasing the proactive response time of rangers. Given the current location of a lion, it predicts where it will be in the next two hours.

![system-overview](./static/images/system-overview.png)

## Features

- Map display
- Predict locations
- Model performance report
- Email alerts

## System Architecture

### Prediction flow

![prediction-flow](./static/images/prediction-flow.png)

### Component Architecture

![component-architecture](./static/images/component-architecture.png)

## Getting Started

### Prerequisites

- Python3
- Mysql
- vscode

## Installation

### Clone the repository

```bash
git clone https://github.com/Samboja651/KSU_Final_Year_Project.git
cd KSU_Final_Year_Project
```

### Create virtual environment

On windows run

```bash
C:> py -m pip install --upgrade pip
python3 -m venv .venv
.venv\Scripts\activate
```

On Linux run

```bash
python3 -m pip install --upgrade pip
python3 -m venv .venv
.venv\bin\activate
```

### Install dependencies

```bash
pip install requirements.txt
```

### Setup Database

Paste the content of `schema.sql` into your mysql and execute.\
Add the portion of the real_time data to the database by the running command below.\
Run the `main.py` file or `python3 main.py` to seed the database.

## Environment Setup

Create a `.env` file with following variables

```env
# mysql logins for new user as shown in schema.sql
USER = "wdf_conservatist"
PASSWORD = "@WildlifeTech2025"
HOST = "localhost"
DATABASE = "WDF_conservation"

GPS_COLLAR_DATA = "Kiboche_last_500_rows_data.csv"

# google maps javasript api key
API_KEY = "YOUR_MAPS_JAVASCRIPT_API_KEY"

# api from opencage to convert coordinates to location name
OPENCAGE_API_KEY = "YOUR_OPENCAGE_API_KEY"

# emailing
SENDER_EMAIL = "YOUR_GMAIL"
SENDER_PASS = "YOUR_GMAIL_APP_PASSWORD"
RECIP_MAIL = "RECEIVER_EMAIL"
```

## API Documentation

```python
# get homepage
GET /

# get model report
GET /model-report

# display map on home page
GET /display-location

# get current lion location
GET /real-time-location/<int:coordinate_id>

# get the predicted location of the lion
# default time_interval = 2
GET /predict/location/<int:coordinate_id>/time/<int:time_interval>

# send email alert
POST /send-alert

# replace the part inside <...> with a value e.g /predict/location/1/time/2"
```

## Run the App

On the terminal run `flask run --debug`.

## Database Schema

## Useful links

Requires Access Rights\
[Project documentation](https://onedrive.live.com/view?id=43505624473455EF!3340&resid=43505624473455EF!3340&authkey=!ArLn6xbCh_7MAEs&wdo=2&cid=43505624473455ef)\
[Download Lion Kiboche real-time data](https://drive.google.com/uc?id=1N9gEm56eMsf8qcRi3JwQzn2n4cxiuDsA&export=download)\
[Code to ML prediction model](https://colab.research.google.com/drive/1eLzl6sPXAiUuNLhWkPMxFJgJbLa70__4?usp=sharing)

## Troubleshooting tips

Ensure you have installed all dependencies in `requirements.txt` file. Do this in a virtual environment.

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

## Description of workflow

## Directory structure

## Help

If you need to try the system with our development external apis or env data. Send an email to <tumaini736@gmail.com>