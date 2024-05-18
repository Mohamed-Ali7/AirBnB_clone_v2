#!/usr/bin/python3
"""This module starts a Flask web application on 0.0.0.0 on port 5000"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """displays (Hello HBNB!)"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """displays (HBNB)"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_is_fun(text):
    """displays (C) followed by the value of the text variable"""
    return "C {}".format(text.replace("_", " "))


@app.route("/python/<text>", strict_slashes=False)
@app.route("/python", strict_slashes=False)
def python_is_fun(text="is cool"):
    """displays (Python) followed by the value of the text variable"""
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def n_is_number(n):
    """displays (n) followed by (is a number) if (n) is an Integer"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def render_html_number(n):
    """displays a HTML page if (n) is an Integer"""
    return render_template("5-number.html", number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def even_odd_number(n):
    """
    displays a HTML page if (n) is an Integer and
    prints whether it is even or odd
    """
    return render_template("6-number_odd_or_even.html", number=n)


@app.route("/states_list", strict_slashes=False)
def states():
    """
    displays a HTML page that contains a list of states
    """
    return render_template("7-states_list.html", states=storage.all(State))


@app.teardown_appcontext
def teardown(exception=None):
    """Executes after each request"""

    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
