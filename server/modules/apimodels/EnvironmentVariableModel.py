from Restplus import api
from flask_restplus import fields

environment_variable_model = api.model('Environment Variable', {
    'name': fields.String(required=True, description='Variable name'),
    'value': fields.String(required=False, description='Variable value')
})
