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


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_state(id=""):
    """Function that displays States by id"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    fnd = 0
    state = ""
    for s in states:
        if id == s.id:
            state = s
            fnd = 1
            break
    if fnd:
        states = sorted(state.cities, key=lambda k: k.name)
        state = state.name

    if id and not fnd:
        fnd = 2

    return render_template('9-states.html', state=state, arr=states, fnd=fnd)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
