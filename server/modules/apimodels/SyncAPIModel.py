'''
Created on Apr 04, 2018

@author: vijasing
'''
from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,input_id_oid_model,response_date_model,response_id_oid_model


entity_name=str(__name__.replace("Model", ""))


filter_model = api.model(entity_name+' filter model', {
    'type': fields.String(required=True, description='type'),
    'tags': fields.List(fields.String(required=False, description=''), required=False, description='tags'),
    })

data_model = api.model(entity_name+' data model', {
    'file_name': fields.String(required=False, description='file_name'),
    'user': fields.String(required=False, description='user'),
    'not_exported': fields.List(fields.String(required=False, description=''), required=False, description='not_exported'),
    'export_date': response_date_model(attribute='export_date',required=True, description=''),
    'file_path': fields.String(required=False, description='file_path'),
    'exported': fields.List(fields.String(required=False, description=''), required=False, description='exported'),
    'export_size': fields.String(required=False, description='export_size'),
    'no_of_not_exported': fields.Integer(required=False, description='no_of_not_exported'),
    'filters_to_apply': fields.Nested(filter_model,required=False, description='filters_to_apply'),
    'no_of_exported': fields.Integer(required=False, description='no_of_exported'),
    'target_host': fields.String(required=False, description='target_host'),
    '_id': response_id_oid_model(attribute='_id',required=True, description='')
    })


get_saved_exports_response_model = api.inherit(entity_name+' get saved exports response model', generic_response_model, {
    "data": fields.List(fields.Nested(data_model,required=True, description='data model'))
    })

retry_sync_input_model=api.model(entity_name+' data model', {
    'sync_id': fields.String(required=False, description='sync_id'),
    '_id': fields.String(required=False, description='_id')
    })
    
inner_data_model= api.model(entity_name+' inner_data_model', {
    'date': fields.String(required=True, description='date'),
    'status': fields.String(required=True, description='status'),
    'sync_id': fields.String(required=True, description='sync_id'),
    })

response_data_model= api.model(entity_name+' response_data_model', {
    'page_total': fields.String(required=True, description='page_total'),
    'page': fields.String(required=True, description='page'),
    'total': fields.String(required=True, description='total'),
    "data": fields.List(fields.Nested(inner_data_model,required=True, description='data model'))
    })
dep_view_all_response_model = api.inherit(entity_name+' dep_view_all_response_model', generic_response_model, {
    "data": fields.Nested(response_data_model,required=True, description='data model')
    })