'''
Created on Feb 13, 2018

@author: pdinda
'''

from modules.apimodels.Restplus import api
from flask_restplus import fields


doc_input_model = api.model('documentsDataModel', {
    'url': fields.String(required=True, description='url'),
    'logo': fields.String(required=True, description='logo'),
    'type': fields.String(required=True, description='type'),
    'name': fields.String(required=True, description='name'),
    'description': fields.String(required=True, description='description')
})

doc_multi_input_model = api.model('documentsDataModel', {
    'documents': fields.List(fields.Nested(doc_input_model), required=True, description='documents')        
})