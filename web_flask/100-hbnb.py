#!/usr/bin/python3
"""This module starts a Flask web application on 0.0.0.0 on port 5000"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.user import User


app = Flask(__name__)


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """
    Renders a HTML page that contains a filter for amenities and states
    and places
    """

    amenities = storage.all(Amenity)
    states = storage.all(State)
    places = storage.all(Place)

    return render_template("100-hbnb.html",
                           amenities=amenities, states=states, places=places)


@app.teardown_appcontext
def teardown(exception):
    """Executes after each request"""

    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
