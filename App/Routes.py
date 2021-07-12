from App import app
from flask import  render_template
@app.route("/")
def hello_world():
    dictionary = [
        {"temp": 25},
        {"temp": 30}
    ]
    return render_template("home.html", lista=dictionary)
