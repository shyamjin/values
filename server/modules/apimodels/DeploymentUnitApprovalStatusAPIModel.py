from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model, genericId_response_model, response_id_oid_model,input_id_oid_model




approval_status_model = api.model('repo Model', {
    'name': fields.String(required=True, description='Repository name'),
})

approval_status_with_id_name_model = api.inherit('approval_status_Model_with_name', approval_status_model, {
        '_id': response_id_oid_model(attribute='_id',required=True, description='')
})

approval_status_create_request = api.inherit('repo Create Request', approval_status_model, {
})

approval_status_create_response = api.inherit('repo Create Response', generic_response_model, {
    'data': fields.Nested(genericId_response_model)
})


approval_status_update_request = api.inherit('repo Update Request', approval_status_model, {      
    '_id': input_id_oid_model(attribute='_id',required=True, description=''),
})

approval_status_update_response = api.inherit('repo Update Response', generic_response_model, {                                                                                    
    'data': fields.Integer(required=True, description='Modification status. 1: repo updated. 0: repo was not updated.')
})


approval_status_get_all_response = api.inherit('repo get all response', generic_response_model, {
    'data': fields.List(fields.Nested(approval_status_with_id_name_model))
})

retrieve_approval_status_by_id_name_response = api.inherit('Retrieve repo by ID Response or Name', generic_response_model, {
    'data': fields.Nested(approval_status_with_id_name_model, required=True)
})
