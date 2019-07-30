from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,genericId_response_model,input_id_oid_model,response_id_oid_model

entity_name=str(__name__.replace("Model", ""))

add_ep_input_model = api.model(entity_name+' add user input data model', {
    'plugin_name': fields.String(required=True, description='plugin_name'),
    'type': fields.String(required=True, description='type'),
    'repo_provider': fields.String(required=False, description='repo_provider')
    })

ep_update_request = api.inherit('EP Update Request', add_ep_input_model, {
    '_id': input_id_oid_model(attribute='_id',required=True, description='')
})

ep_create_response = api.inherit('EP Create Response', generic_response_model, {
    'data': fields.Nested(genericId_response_model)
})


ep_all_response_model = api.model(entity_name+' add user input data model', {
    'file_path': fields.String(required=True, description='file_path'),
    'plugin_name': fields.String(required=True, description='plugin_name'),
    '_id': response_id_oid_model(attribute='_id',required=True, description=''),
    })

ep_all_response = api.inherit('EP All Response', generic_response_model, {
    'data': fields.List(fields.Nested(ep_all_response_model))
})

