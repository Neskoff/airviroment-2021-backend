from App import db
from App.measurements import measurements_bp
from App.measurements.models import Measurements
import json
from flask import request
from App.measurements.constants import PAGE, PER_PAGE
from sqlalchemy import desc
from werkzeug.exceptions import NotFound
from App.measurements.schemas import MeasurementResponseSchema, MeasurementPostSchema, MeasurementPatchSchema, \
    MeasurementMetaSchema, MeasurementPaginationSchema

measurement_response_schema = MeasurementResponseSchema()
measurement_post_schema = MeasurementPostSchema()
measurement_patch_schema = MeasurementPatchSchema()
measurement_collection_response_schema = MeasurementResponseSchema(many=True)
measurement_meta_schema = MeasurementMetaSchema()
measurement_pagination_schema = MeasurementPaginationSchema()


@measurements_bp.get('')
def getAll():
    schema_load = measurement_meta_schema.load(request.args.to_dict())
    measurements = db.session.query(Measurements).paginate(page=schema_load.get('page'),
                                                           per_page=schema_load.get('per_page'))
    return measurement_pagination_schema.dump(measurements)


@measurements_bp.get("<int:id>")
def getbyid(id):
    measurement = db.session.query(Measurements).filter(Measurements.id == id).first()
    if not measurement:
        return NotFound(description="Measurement not found")
    else:
        return measurement_response_schema.dump(measurement)


@measurements_bp.get("/latest")
def getlast():
    measurement = db.session.query(Measurements).order_by(desc(Measurements.id)).first()
    if not measurement:
        return NotFound(description="Measurement not found")
    if measurement:
        return measurement_response_schema.dump(measurement)


@measurements_bp.post("")
def insertmeasurment():
    data = request.get_json()
    postdata = measurement_post_schema.load(data)
    measurement = Measurements(postdata.temperature, postdata.humidity,
                               postdata.pollution)
    db.session.add(measurement)
    db.session.commit()
    return measurement_response_schema.dump(measurement)


@measurements_bp.patch("<int:id>")
def patchmeasurment(id):
    data = request.get_json()
    patchdata = measurement_patch_schema.load(data)
    measurement = db.session.query(Measurements).filter(Measurements.id == id).first()
    if not measurement:
        return NotFound(description="Measurement not found")
    if patchdata['temperature']:
        measurement.temperature = patchdata['temperature']
    if patchdata['humidity']:
        measurement.humidity = patchdata['humidity']
    if patchdata['pollution']:
        measurement.pollution = patchdata['pollution']
    db.session.commit()
    return measurement_response_schema.dump(measurement)








