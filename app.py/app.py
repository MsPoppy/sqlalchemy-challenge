from types import prepare_class
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
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

    prcpyear= session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= lastyear).all()

    session.close()

    # Convert list of tuples into normal list
    precip_data = list(np.ravel(prcpyear))

    return jsonify(precip_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    stations= session.query(Station.station)).all()

    session.close()

    all_stations = []
    for stations in stations:
       stations.append(all_stations)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    moststations= session.query(Measurement.station,Measurement.date,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station)).all()all()

    session.close()

    # Convert list of tuples into normal list
    most_active = list(np.ravel(moststations))

    return jsonify(moststations)



    
if __name__ == '__main__':
    app.run(debug=True)