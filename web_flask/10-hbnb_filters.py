#!/usr/bin/python3
"""
A script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from flask import Flask, render_template
from models.amenity import Amenity
from models.state import State
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """Function to remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filter():
    """Function that displays HBNB Filters"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    sc = []

    for state in states:
        sc.append([state, sorted(state.cities, key=lambda k: k.name)])

    amen = storage.all(Amenity).values()
    amen = sorted(amen, key=lambda k: k.name)

    return render_template('10-hbnb_filters.html', states=sc, amenities=amen)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
