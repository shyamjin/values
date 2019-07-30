from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model, genericId_response_model, response_id_oid_model,input_id_oid_model




repo_model = api.model('approval status Model', {
    'name': fields.String(required=True, description='Repository name'),
    'handler': fields.String(required=True, description='Repository Handler'),
    'additional_artifacts_upload': fields.String(required=True, description='Allow additional artifacts true/false'),
    'is_default_repo_ind': fields.String(required=False, description='true/false is default repo ind'),
})

repo_with_id_name_model = api.inherit('repo_Model_with_name', repo_model, {
        '_id': response_id_oid_model(attribute='_id',required=True, description='')
})

repo_create_request = api.inherit('approval status Create Request', repo_model, {
})

repo_create_response = api.inherit('approval status Create Response', generic_response_model, {
    'data': fields.Nested(genericId_response_model)
})


repo_update_request = api.inherit('approval status Update Request', repo_model, {      
    '_id': input_id_oid_model(attribute='_id',required=True, description=''),
})

repo_update_response = api.inherit('approval status Update Response', generic_response_model, {                                                                                    
    'data': fields.Integer(required=True, description='Modification status. 1: approval status updated. 0: approval status was not updated.')
})


repo_get_all_response = api.inherit('approval status get all response', generic_response_model, {
    'data': fields.List(fields.Nested(repo_with_id_name_model))
})

retrieve_repo_by_id_name_response = api.inherit('Retrieve approval status by ID Response or Name', generic_response_model, {
    'data': fields.Nested(repo_with_id_name_model, required=True)
})
