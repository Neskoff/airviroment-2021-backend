from marshmallow import Schema, fields, validate, pre_load, post_load, ValidationError
from App.measurements.view import MeasurementView
from App.measurements.constants import PAGE, PER_PAGE


class MeasurementResponseSchema(Schema):
    id = fields.Integer(required=False)
    temperature = fields.Float()
    humidity = fields.Float()
    pollution = fields.Float()
    created = fields.DateTime()


class MeasurementPostSchema(Schema):
    temperature = fields.Float(required=True, validate=validate.Range(min=-70, max=70))
    humidity = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    pollution = fields.Float(required=True, validate=validate.Range(min=0, max=100))
    created = fields.DateTime()

    @post_load()
    def format_data(self, data, **kwargs):
        return MeasurementView(**data)


class MeasurementPatchSchema(Schema):
    @pre_load()
    def test_input(self, data, **kwargs):
        if not data:
            raise ValidationError("No data found")
        return data
    temperature = fields.Float(required=False, validate=validate.Range(min=-70, max=70))
    humidity = fields.Float(required=False, validate=validate.Range(min=0, max=100))
    pollution = fields.Float(required=False, validate=validate.Range(min=0, max=100))
    created = fields.DateTime()


class MeasurementMetaSchema(Schema):
    page = fields.Integer(required=False, default=PAGE, missing=PAGE)
    per_page = fields.Integer(required=False, default=PER_PAGE, missing=PER_PAGE)
    total = fields.Integer(required=False, missing=0)


class MeasurementPaginationSchema(Schema):
    meta = fields.Method('get_meta')
    items = fields.List(fields.Nested(MeasurementResponseSchema()), data_key='response')

    @staticmethod
    def get_meta(data):
        response = dict()
        response["total"] = data.total
        response["page"] = data.page
        response["per_page"] = data.per_page
        return MeasurementMetaSchema().dump(response)

