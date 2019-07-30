from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import input_id_oid_model

entity_name=str(__name__.replace("Model", ""))

toolModel=api.model(entity_name+' tool model', {
    'tool_id': fields.String(required=True, description='tool_id'),
    'tool_name': fields.String(required=True, description='tool_name'),
    'tool_version': fields.String(required=True, description='tool_version'),
    'version_id': fields.String(required=True, description='version_id'),
    'version_name': fields.String(required=True, description='version_name'),
    'status': fields.String(required=True, description='status'),

    })


add_toolset_input_model = api.model(entity_name+' add toolset input data model', {
    'tool_set': fields.List(fields.Nested(toolModel,required=True, description='tools'),required=True, description='tool_set'),
    'name': fields.String(required=True, description='name'),
    'description': fields.String(required=True, description='description'),
    'tag': fields.List(fields.String(required=False, description='tools'),required=True, description='tool_set')
    })

update_toolset_input_model = api.inherit(entity_name+' update toolset input model', add_toolset_input_model, {
    '_id': input_id_oid_model(attribute='_id',required=True, description='')
})

