'''
Created on Feb 13, 2018

@author: pdinda
'''

from modules.apimodels.Restplus import api
from flask_restplus import fields


fields_input_model = api.model('fieldDataModel', {
    'input_type': fields.String(required=True, description='input_type'),
    'input_name': fields.String(required=True, description='input_name'),
    'order_id': fields.Integer(required=True, description='order_id'),
    #'default_value': fields.Raw(required=True, description='default_value'),
    #'valid_values': fields.Raw(required=False, description='valid_values'),            
    'is_mandatory': fields.Boolean(required=True, description='is_mandatory',default=True),
    'tooltip': fields.String(required=False, description='tooltip')
})

fields_multi_input_model = api.model('fieldsDataModel', {
    'fields': fields.List(fields.Nested(fields_input_model), required=True, description='name')        
})