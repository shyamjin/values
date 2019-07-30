from flask_restplus import fields
from modules.apimodels.PreRequisitesModel import prerequisites_input_model 
from modules.apimodels.DeploymentFieldModel import fields_multi_input_model
from modules.apimodels.Restplus import api
from modules.apimodels.GenericReponseModel import generic_response_model, input_id_oid_model, oid_model

du_input_model = api.model('Object array for DU list', {
    'name': fields.String(required=True, description='name'),
    'type': fields.String(required=True, description='type'),
    'tag': fields.List(fields.String(), required=False, description='tags',default=[]),
    'release_notes': fields.String(required=False, description='release_notes'),
    'branch': fields.String(required=False, description='branch'),
    'pre_requiests': fields.List(fields.Nested(prerequisites_input_model), required=False, description='pre_requiests'),
    'deployment_field': fields.Nested(fields_multi_input_model, required=False, description='deployment_field'),
    'repository_to_use': fields.String(required=True, description='repository_to_use'),
})

du_input_model_for_bulk = api.inherit('DU Model with DB ID', du_input_model, {
    '_id': fields.Nested(oid_model, required=False, description='DB ID')
})


du_bulk_input_model = api.model('DU bulk load request data model', {    
    'data': fields.List(fields.Nested(du_input_model_for_bulk), required=True, description='Array of DUs')
})

du_response_model = api.model('DU bulk load response data model', {
    '_id': fields.String(required=True, description='_id'),
    'name': fields.String(required=True, description='name'),
    'message': fields.String(required=True, description='message'),
    'result': fields.String(required=True, description='result')
})


du_bulk_response_model = api.inherit('Deployment Unit bulk load response', generic_response_model, {
    'data': fields.List(fields.Nested(du_response_model), required=True, description='response data model'),
})

du_update_input_model = api.inherit('du_add_input_model',{
    '_id': input_id_oid_model(attribute='_id',required=True, description='')    
})