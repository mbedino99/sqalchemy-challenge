# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# previous var: 
previous = previous = dt.date(2017,8,23)-dt.timedelta(days=365)

#################################################
# Flask Routes
#################################################
@app.route('/')
def welcome():
    return(
        f"Avaliable Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route('/api/v1.0/precipitation')
def Precipitation():
    # create session link
    session = Session(engine)

    p_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=previous).all()
    return jsonify(p_results)

    session.close()

@app.route('/api/v1.0/stations')
def Stations():
    # create session link
    session = Session(engine)

    s_results = session.query(Station.station, station.name).all()
    return jsonify(s_results)

    session.close()

@app.route('/api/v1.0/tobs')
def Tobs():
    tobs_results = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.station == active_station_max).\
        filter(Measurement.date >= previous).all()
    return jsonify(tobs_results)

    session.close()

@app.route('/api/v1.0/<start>')
def StartDate(date):
    start_t_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs)\
        , func.max(Measurement.tobs)).filter(Measurement.date >= date).all()
    return jsonify(start_t_results)

    session.close()

@app.route('/api/v1.0/<start>/<end>')
def StartEndDate(start,end):
    start_end_t_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs)\
        , func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_t_results)

    session.close()

if __name__ == '__main__':
    app.run(debug=True)