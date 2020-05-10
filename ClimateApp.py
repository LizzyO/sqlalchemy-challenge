import numpy as np
import pandas as pd
import datetime as dt

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
Base.prepare(engine, reflect=True)

# # Save reference to the table
me = Base.classes.measurement
st = Base.classes.station

# Flask Setup
#################################################
app = Flask(__name__)

# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

            )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precip for dates
    results = session.query(me.date, me.prcp).\
            filter(me.date >= '2016-08-23').\
            filter(me.date <= '2017-08-23').order_by(me.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    precip_data = []
    for precip in results:
        precip_dict = {}
        precip_dict["Date"] = precip.date
        precip_dict["Precipitation"] = precip.prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all passengers
    results = session.query(func.count(me.station), me.station).\
            group_by(me.station).\
            order_by(func.count(me.station).desc()).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(me.tobs).\
        filter(me.station == 'USC00519281').\
        filter(me.date >= '2016-08-23').all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/<start>")
def temp_for_start(start):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    results = session.query(func.min(me.tobs), func.avg(me.tobs), func.max(me.tobs)).\
        filter(me.date >= start).filter(me.date <= start).all()

    session.close()

       # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/<start>/<end>")
def temp_for_end(start, end):
     # Create our session (link) from Python to the DB
    session = Session(engine)
 
    results = session.query(func.min(me.tobs), func.avg(me.tobs), func.max(me.tobs)).\
        filter(me.date >= start).filter(me.date <= end).all()

    session.close()
   # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

if __name__ == '__main__':
    app.run(debug=True)