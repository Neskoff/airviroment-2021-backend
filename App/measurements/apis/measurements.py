from App import db
from App.measurements import measurements_bp
from App.measurements.models import Measurements
import json
from flask import request
from App.measurements.constants import PAGE, PER_PAGE
from sqlalchemy import desc
from werkzeug.exceptions import NotFound


@measurements_bp.get('')
def getAll():
    page = int(request.args.get("page", PAGE))
    per_page = int(request.args.get("per_page", PER_PAGE))
    measurements = db.session.query(Measurements).paginate(page=page, per_page=per_page)
    response = []
    for measurement in measurements.items:
        data = {"id": measurement.id,
                "temperature": measurement.temperature,
                "pollution": measurement.pollution,
                "humidity": measurement.humidity}
        response['results'].append(data)
    return json.dumps(response)


@measurements_bp.get("<int:id>")
def getbyid(id):
    measurement = db.session.query(Measurements).filter(Measurements.id == id).first()
    if not measurement:
        return NotFound(description="Measurement not found")
    if measurement:
        data = {"id": measurement.id,
                "temperature": measurement.temperature,
                "pollution": measurement.pollution,
                "humidity": measurement.humidity}
        return json.dumps(data)


@measurements_bp.get("/latest")
def getlast():
    measurement = db.session.query(Measurements).order_by(desc(Measurements.id)).first()
    if not measurement:
        return NotFound(description="Measurement not found")
    if measurement:
        data = {"id": measurement.id,
                "temperature": measurement.temperature,
                "pollution": measurement.pollution,
                "humidity": measurement.humidity}
        return json.dumps(data)


@measurements_bp.post("")
def insertmeasurment():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')
    pollution = data.get('pollution')
    measurement = Measurements(temperature=temperature, humidity=humidity, pollution=pollution)
    db.session.add(measurement)
    db.session.commit()
    if not measurement:
        return NotFound(description="Measurement not found")
    if measurement:
        data = {"id": measurement.id,
                "temperature": measurement.temperature,
                "pollution": measurement.pollution,
                "humidity": measurement.humidity}
        return json.dumps(data)


@measurements_bp.patch("<int:id>")
def patchmeasurment(id):
    data = request.get_json()
    measurement = db.session.query(Measurements).filter(Measurements.id == id).first()
    if not measurement:
        return NotFound(description="Measurement not found")
    if data.get('temperature'):
        measurement.temperature = data.get('temperature')
    if data.get('humidity'):
        measurement.humidity = data.get('humidity')
    if data.get('pollution'):
        measurement.pollution = data.get('pollution')
    db.session.commit()
    data = {"id": measurement.id,
            "temperature": measurement.temperature,
            "pollution": measurement.pollution,
            "humidity": measurement.humidity}
    return json.dumps(data)








