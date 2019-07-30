from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,input_id_oid_model

entity_name=str(__name__.replace("Model", ""))

machinegroup_response_model = api.model(entity_name+' bulk load response data model', {
    '_id': fields.String(required=True, description='_id'),
    'group_name': fields.String(required=True, description='group_name'),
    'message': fields.String(required=True, description='message'),
    'result': fields.String(required=True, description='result')
})

machinegroup_input_model = api.model('Object array for '+entity_name+' list', {
    '_id': input_id_oid_model(attribute='_id',required=True, description=''), 
    'group_name': fields.String(required=True, description='group_name'),    
    'description': fields.String(required=False, description='description'),
    'machine_id_list': fields.List(fields.String(), required=True, description='machine_id_list')
})


machinegroup_bulk_input_model = api.model(entity_name+' bulk load request data model', {
    'data': fields.List(fields.Nested(machinegroup_input_model), required=True, description='Array of Machine Group')
})


machinegroup_bulk_response_model = api.inherit(entity_name+' bulk load response', generic_response_model, {
    'data': fields.List(fields.Nested(machinegroup_response_model), required=True, description='response data model'),
})
