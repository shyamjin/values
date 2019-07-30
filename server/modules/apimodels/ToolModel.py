from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model

entity_name=str(__name__.replace("Model", ""))

update_tool_response_model = api.inherit(entity_name+' update tool response model', generic_response_model, {
    'data':fields.Nested(api.model(entity_name+' data model', {
    'version_inserted': fields.List(fields.String(required=False, description='version'),required=True, description='version list')})
                         ,required=True, description='')
})

version_model=api.model(entity_name+' version model', {
    '_id': fields.Nested(api.model(entity_name+' Object Id model', {
            'oid': fields.String(required=True, description='Object id')})
                                                ,required=False, description=''),
    'version_date': fields.String(required=True, description='version_date'),
    'version_number': fields.String(required=True, description='version_number'),
    'gitlab_branch': fields.String(required=True, description='gitlab_branch'),
    'tool_id': fields.String(required=False, description='tool_id'),
    'status': fields.String(required=True, description='status'),
    'branch_tag': fields.String(required=True, description='branch_tag'),
    'repository_to_use': fields.String(required=True, description='repository_to_use'),

    })


add_tool_input_model = api.model(entity_name+' add tool input data model', {
    'name': fields.String(required=True, description='name'),
    'support_details': fields.String(required=True, description='support_details'),
    'description': fields.String(required=True, description='description'),
    'status': fields.String(required=True, description='status'),
    'version': fields.List(fields.Nested(version_model,required=False, description='version'),required=True, description='version'),

    })

update_tool_input_model = api.inherit(entity_name+' update tool input model', add_tool_input_model, {
    '_id': fields.Nested(api.model(entity_name+' Object Id model', {
    'oid': fields.String(required=True, description='Object id')})
                         ,required=False, description='')
})

