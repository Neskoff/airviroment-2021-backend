from App import app, db
from App.models import Measurements
from flask import render_template
@app.route("/")
def hello_world():
    dictionary = db.session.query(Measurements).all()
    return render_template("home.html", lista=dictionary)
