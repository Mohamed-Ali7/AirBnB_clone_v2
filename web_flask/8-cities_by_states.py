#!/usr/bin/python3
"""This module starts a Flask web application on 0.0.0.0 on port 5000"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def state_cities():
    """
    displays a HTML page that contains a list of states
    """
    return render_template("8-cities_by_states.html",
                           states=storage.all(State))


@app.teardown_appcontext
def teardown(exception):
    """Executes after each request"""

    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
