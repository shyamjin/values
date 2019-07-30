from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model, genericId_response_model, oid_model


version_model = api.model('PT Version Model', {
     'version_name': fields.String(required=True, description='Version Details',default="ga")
    ,'version_number': fields.String(required=True, description='Version Details',default="1.0")
    ,'dependent_tools': fields.List(fields.String,required=False, description='Version Details')
    ,'jenkins_job': fields.String(required=False, description='Version Details')
    ,'branch_tag': fields.String(required=False, description='Version Details')
    ,'backward_compatible': fields.String(required=False, description='Version Details')
    ,'mps_certified': fields.String(required=False, description='Version Details')
    ,'deployer_to_use': fields.String(required=False, description='Version Details')
    ,'gitlab_branch': fields.String(required=False, description='Version Details')
    ,'pre_requiests': fields.List(fields.String,required=False, description='Version Details')
    ,'version_date': fields.String(required=False, description='Version Details')
    ,'release_notes': fields.String(required=False, description='Version Details')
})


pa_model = api.model('PT Model', {
    'name': fields.String(required=True, description='Tool name')
    , 'support_details': fields.String(required=True, description='Email address for support')
    , 'request_reason': fields.String(required=False, description='Reason for suggesting this tool')
    , 'description': fields.String(required=True, description='Description for the tool')
    , 'version': fields.Nested(version_model,required=True, description='Version Details')
    , 'thumbnail_logo': fields.String(required=False, description='Tool Details')
    , 'logo': fields.String(required=False, description='Tool Details')
})

pt_with_id_model = api.inherit('PT Model with DB ID', pa_model, {
    '_id': fields.String(required=True, description='DB ID')
})

pt_create_request = api.inherit('PT Create Request', pa_model, {
})

pt_approve_request = api.inherit('PT Approve Request', pa_model, {
    '_id': fields.String(required=True, description='DB ID')
})

pt_create_response = api.inherit('PT Create Response', generic_response_model, {
    'data': fields.Nested(genericId_response_model)
})


pt_get_all_response = api.inherit('PT get all response', generic_response_model, {
    'data': fields.List(fields.Nested(pt_with_id_model))
})

retrieve_pt_by_id_response = api.inherit('Retrieve PA by ID Response', generic_response_model, {
    'data': fields.Nested(pt_with_id_model)
})

reject_pt_by_id_response = api.inherit('Retrieve PA by ID Response', generic_response_model, {
})
