#!/usr/bin/python3
"""This module starts a Flask web application on 0.0.0.0 on port 5000"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states():
    """
    displays a HTML page that contains a list of states
    """
    states = storage.all(State)
    states = dict(sorted(states.items(), key=lambda item: item[1].name))
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exception):
    """Executes after each request"""

    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
