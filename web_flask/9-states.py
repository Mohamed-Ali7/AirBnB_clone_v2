#!/usr/bin/python3
"""This module starts a Flask web application on 0.0.0.0 on port 5000"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def list_of_states():
    """
    displays a HTML page that contains a list of states
    """
    return render_template("9-states.html", states=storage.all(State),
                           state=None)


@app.route("/states/<id>", strict_slashes=False)
def state(id):
    """
    displays a HTML page that contains a list of states
    """
    state = storage.find_by_id(State, id)
    return render_template("9-states.html", state=state, states=None)


@app.teardown_appcontext
def teardown(exception):
    """Executes after each request"""

    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
