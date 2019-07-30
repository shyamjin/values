from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.PreRequisitesModel import prerequisites_input_model
from modules.apimodels.GenericReponseModel import generic_response_model,input_id_oid_model


duset_response_model = api.model('DU bulk load response data model', {
    '_id': fields.String(required=True, description='_id'),
    'name': fields.String(required=True, description='name'),
    'message': fields.String(required=True, description='message'),
    'result': fields.String(required=True, description='result')
})

du_input_model = api.model('DU List', {    
    'du_id': fields.String(required=True, description='du_id'),
    'dependent': fields.String(required=True, description='dependent'),
    'order': fields.Integer(required=True, description='order')
})

duset_input_model = api.model('Object array for DU Set list', {
    'name': fields.String(required=True, description='name'),    
    'tag': fields.List(fields.String(), required=False, description='tags'),
    'release_notes': fields.String(required=False, description='release_notes'),    
    'pre_requiests': fields.List(fields.Nested(prerequisites_input_model), required=False, description='pre_requiests'),
    'du_set': fields.List(fields.Nested(du_input_model), required=False, description='deployment_field')
})


duset_input_model_for_update = api.inherit('DUSET UPDATE MODEL', duset_input_model, {
    '_id': input_id_oid_model(attribute='_id',required=True, description='')
})

duset_bulk_input_model = api.model('DU Set bulk load request data model', {
    'data': fields.List(fields.Nested(duset_input_model), required=True, description='Array of DUs')
})

duset_bulk_response_model = api.inherit('DU bulk load response', generic_response_model, {
    'data': fields.List(fields.Nested(duset_response_model), required=True, description='response data model'),
})

