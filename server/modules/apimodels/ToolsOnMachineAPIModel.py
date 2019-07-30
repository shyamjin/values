from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,input_id_oid_model,\
    generic_date_model, response_date_model,response_id_oid_model

entity_name=str(__name__.replace("Model", ""))

 
date_model  = api.model(entity_name+' Date model', {
    'date': fields.String(required=True, description='date')
    })
deployedToolModel=api.model(entity_name+' Deployed tool model', {
    '_id': response_id_oid_model(attribute='_id',required=True, description=''),
    'status': fields.String(required=True, description='status'),
    'build_id': fields.String(required=True, description='build_id'),
    'machine_id': fields.String(required=True, description='machine_id'),
    'group_deployment_request_id': fields.String(required=True, description='group_deployment_request_id'),
    'previous_build_number': fields.String(required=True, description='previous_build_number'),
    'machine_group_id': fields.String(required=True, description='machine_group_id'),
    'parent_entity_id': fields.String(required=True, description='parent_entity_id'),
    'deployment_request_id': fields.String(required=True, description='deployment_request_id'),
    'host': fields.String(required=True, description='host'),
    'previous_build_id': fields.String(required=True, description='previous_build_id'),
    'build_no': fields.String(required=True, description='build_no'),
    'create_date': response_date_model(attribute='create_date',required=True, description='create_date'),
    'update_date': response_date_model(attribute='update_date',required=True, description='update_date'),

    })


getDeployedtoolResponseModel=api.inherit(entity_name+' Deployed tool response model', generic_response_model, {
    'data': fields.Nested( deployedToolModel, required=True, description='response sys details model')
})

getDeployedtoolResponseModelNone=api.inherit(entity_name+' Deployed tool None response model', generic_response_model, {
    'data': fields.Nested(None, required=True, description='model')
})