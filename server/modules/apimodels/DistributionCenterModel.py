from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model

entity_name=str(__name__.replace("Model", ""))

update_tool_response_model = api.inherit(entity_name+' update tool response model', generic_response_model, {
    'data':fields.Nested(api.model(entity_name+' data model', {
    'version_inserted': fields.List(fields.String(required=False, description='version'),required=True, description='version list')})
                         ,required=True, description='')
})

add_dc_response_model = api.inherit(entity_name+' add dc response model', generic_response_model, {
    'data': fields.Nested(api.model(entity_name+' data model', {
    'id': fields.String(required=True, description='Object id')})
                         ,required=True, description='')
})

add_dc_input_model = api.model(entity_name+' add dc input data model', {
    'machine_id': fields.String(required=True, description='machine id'),
    'host': fields.String(required=True, description='host'),
    'status': fields.String(required=True, description='status'),
    })

update_dc_input_model = api.inherit(entity_name+' update tool input model', add_dc_input_model, {
    '_id': fields.Nested(api.model(entity_name+' Object Id model', {
    'oid': fields.String(required=True, description='Object id')})
                         ,required=True, description='')
})

