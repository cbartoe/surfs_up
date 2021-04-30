import datetime as dt 
import numpy as np 
import pandas as pd 

#sqlalchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask dependencies
from flask import Flask, jsonify

#setup database engine for FLASK
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect the database 
Base = automap_base()
Base.prepare(engine, reflect=True)

#create variables for he classes
Measurement = Base.classes.measurement
Station = Base.classes.station

#create a session link from python to the database
session = Session(engine)

#Define our Flask app
app = Flask(__name__)

#define the welcome route
@app.route("/")

#define other routes with a function to ensure that viewers know where to go
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!<br/>
    Available Routes:<br/>
    /api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/tobs<br/>
    /api/v1.0/temp/start/end<br/>
    ''')

#create a new routh for precipitation
@app.route("/api/v1.0/precipitation")
#create precipitation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#create a route for the stations
@app.route("/api/v1.0/stations")
#create the function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#create a route for previous year temp
@app.route("/api/v1.0/tobs")
#create function
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) -dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#create the routes for the statistics start and end
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#create the function
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    #determine the starting and ending dates with "if not"
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    #calculate the temp min, avg, max with start and end dates
    results = session.query(*sel).\
       filter(Measurement.date >= start).\
       filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
