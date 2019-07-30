'''
Created on Feb 26, 2018

@author: vijasing
'''

from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,input_id_oid_model


entity_name=str(__name__.replace("Model", ""))

state_details_model = api.model(entity_name+' token data model', {
    'name': fields.String(required=False, description='token'),
    'approval_status': fields.String(required=False, description='approval status'),
    'deployment_field': fields.Nested(api.model(entity_name+' deployment field data model', {}),required=False, description='deployment field')
    })

additonal_info_model = api.model(entity_name+' addition info data model', {
    'repo_id': fields.String(required=True, description='repo_id'),
    'package': fields.String(required=True, description='package'),
    'file_name': fields.String(required=True, description='file_name'),
    'artifact': fields.String(required=True, description='artifact'),
    'relative_path': fields.String(required=True, description='relative_path'),
    'version': fields.String(required=True, description='version'),
    })

additonal_info_model1 = api.model(entity_name+' addition info data model', {
    'repo_id': fields.String(required=False, description='repo_id'),
    'package': fields.String(required=False, description='package'),
    'file_name': fields.String(required=False, description='file_name'),
    'artifact': fields.String(required=False, description='artifact'),
    'relative_path': fields.String(required=False, description='relative_path'),
    'version': fields.String(required=False, description='version'),
    })

artifacts_model =  api.inherit(entity_name+' artifacts model', additonal_info_model1, {
    'type': fields.String(required=True, description='type'),
    'classifier': fields.String(required=True, description='classifier')
    })

additional_artifacts_model = api.model(entity_name+' addition artifacts data model', {
    'artifacts': fields.List(fields.Nested(artifacts_model,required=True, description='artifacts')),
    'repo_provider': fields.String(required=True, description='repo_provider')
    })

add_build_input_model = api.model(entity_name+' add build input data model', {
    'status': fields.String(required=True, description='status'),
    'build_number': fields.Integer(required=True, description='build_number'),
    'package_name': fields.String(required=True, description='package_name'),
    'package_type': fields.String(required=True, description='package_type'),
    'file_size': fields.String(required=True, description='file_size'),
    'file_path': fields.String(required=True, description='file_path'),
    'parent_entity_id': fields.String(required=True, description='parent_entity_id'),
    'state_details': fields.Nested(state_details_model, required=False, description='response data model'),
    'additional_info': fields.Nested(additonal_info_model,required=True, description='additional_info'),
    'additional_artifacts': fields.Nested(additional_artifacts_model,required=False, description='additional_artifacts')
    })

update_build_input_model=  api.inherit(entity_name+' update build input data model', add_build_input_model, {
    '_id': input_id_oid_model(attribute='_id',required=True, description=''),
    })

