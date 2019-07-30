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


add_teams_input_model = api.model(entity_name+' add teams input data model', {
    'team_name': fields.String(required=True, description='team_name'),
    'description': fields.String(required=True, description='description'),
    'homepage': fields.String(required=True, description='homepage'),
    'users_id_list': fields.List(fields.String(required=False, description='users_id_list'),required=False, description='list'),
    'tag_id_list': fields.List(fields.String(required=False, description='tag_id_list'),required=False, description='list'),
    'machine_group_id_list': fields.List(fields.String(required=False, description='machine_group_id_list'),required=False, description='list'),
    'machine_id_list': fields.List(fields.String(required=False, description='machine_id_list'),required=False, description='list'),
    'parent_entity_du_set_id_list': fields.List(fields.String(required=False, description='parent_entity_du_set_id_list'),required=False, description='list'),
    'parent_entity_id_du_list': fields.List(fields.String(required=False, description='parent_entity_id_du_list'),required=False, description='list'),
    'parent_entity_id_tool_list': fields.List(fields.String(required=False, description='parent_entity_id_tool_list'),required=False, description='list'),
    'parent_entity_set_tag_list': fields.List(fields.String(required=False, description='parent_entity_set_tag_list'),required=False, description='list'),
    'parent_entity_tag_list': fields.List(fields.String(required=False, description='parent_entity_tag_list'),required=False, description='list'),
    'parent_entity_tool_set_id_list': fields.List(fields.String(required=False, description='parent_entity_tool_set_id_list'),required=False, description='list'),
    })

update_teams_input_model = api.inherit(entity_name+' update teams input model', add_teams_input_model, {
    '_id': input_id_oid_model(attribute='_id',required=True, description='')
})

