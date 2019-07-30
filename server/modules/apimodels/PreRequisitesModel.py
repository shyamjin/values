'''
Created on Feb 13, 2018

@author: pdinda
'''

from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model

entity_name=str(__name__.replace("Model", ""))

prerequisites_input_model = api.model('prerequisitesDataModel', {
    'name': fields.String(required=True, description='name'),
    'version': fields.Float(required=True, description='version')    
})

add_prerequisites_input_model =  api.model(entity_name+' add prerequisites input model', {
    'prerequisites_name': fields.String(required=True, description='prerequisites_name'),
     'display_name': fields.String(required=True, description='display_name'),
      'version_command': fields.String(required=True, description='version_command'),
       'parse_version': fields.String(required=True, description='parse_version'),
        'prerequisites_status': fields.String(required=True, description='prerequisites_status'),
         'version_list': fields.List(fields.Float(required=True, description='version'),required=True, description='version_list')
    })

add_prerequisites_response_model=api.inherit(entity_name+' add prerequisites response model', generic_response_model, {
    'data': fields.Nested( api.model(entity_name+' id model', {
    'id': fields.String(required=True, description='id')
    }), required=True, description='response sys details model')
})
