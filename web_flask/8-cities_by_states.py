#!/usr/bin/python3
"""
A script that starts a Flask web application
listening on 0.0.0.0, port 5000
"""
from flask import Flask, render_template
from models.state import State
from models import storage


app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """Function to remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Function that displays States"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Function that displays Cities by States"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    sc = []
    for state in states:
        sc.append([state, sorted(state.cities, key=lambda k: k.name)])
    return render_template('8-cities_by_states.html', states=sc, h1="States")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
