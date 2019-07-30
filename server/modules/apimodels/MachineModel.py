from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model, generic_update_date_model,input_id_oid_model
from modules.apimodels.EnvironmentVariableModel import environment_variable_model

entity_name=str(__name__.replace("Model", ""))


machine_response_model = api.inherit(entity_name+'machine add response model', generic_response_model, {
    'data': fields.Nested(api.model(entity_name+' id model', {
    'id': fields.String(required=True, description='machine id')}),required=True, description='update count')
})


sta_input_model = api.model('sta_input_model', {
    'username': fields.String(required=True, description='username'),
    'order': fields.Integer(required=True, description='order'),
    'host': fields.String(required=True, description='host'),
    'password': fields.String(required=True, description='password'),
    'type': fields.String(required=False, description='type',default='SSH'),            
    'port': fields.Integer(required=True, description='port',default=22),
    
})

fav_machine_input_model = api.model('fav machine input model', {
    'user_id': fields.String(required=True, description='user id'),
    'machine_id': fields.String(required=True, description='machine id'),
    'status': fields.Integer(required=True, description='status')
})
fav_machine_response_model = api.inherit(entity_name+'fav machine response model', generic_response_model, {
    'data': fields.Nested(api.model(entity_name+' id model', {
   '_id': fields.String(required=True, description='machine id')}),required=True, description='update count')
})
machine_input_model = api.model('Object array for '+entity_name+' list', {
    'description': fields.String(required=False, description='description'),
    'permitted_users': fields.List(fields.String(), required=False, description='permitted_users',default=[]),
    'included_in': fields.List(fields.String(), required=False, description='included_in',default=[]),
    'permitted_teams': fields.List(fields.String(), required=False, description='permitted_teams',default=[]),
    'port': fields.Integer(required=False, description='port',default=22),
    'shell_type': fields.String(required=False, description='shell_type'),
    'reload_command': fields.String(required=False, description='shell_treload_commandype'),
    'tag': fields.List(fields.String(), required=False, description='tag',default=[]),
    'fav': fields.Boolean(required=False, description='fav'),
    'ip': fields.String(required=True, description='ip'),
    'host': fields.String(required=True, description='host'),
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
    'machine_type': fields.String(required=False, description='machine_type'),
    'account_id': fields.String(required=True, description='account_id'),
    'status': fields.String(required=False, description='status',default="1"),
    'steps_to_auth': fields.List(fields.Nested(sta_input_model), required=False, description='steps_to_auth',default=[]),
    'machine_name': fields.String(required=False, description='machine_name'),
    'auth_type': fields.String(required=True, description='auth_type'),
    'tunneling_flag': fields.Boolean(required=False, description='tunneling_flag'),
    'environment_variables': fields.List(fields.Nested(environment_variable_model), required=False, description='Environment Variables')
})


ping_machine_response_model = api.inherit(entity_name+'ping machine response model', generic_response_model, {})

machine_update_input_model = api.inherit(entity_name+'machine update input model', machine_input_model, {
    '_id': input_id_oid_model(attribute='_id',required=True, description='')
})

machine_update_response_model = api.inherit(entity_name+'machine update response model', generic_response_model, {
    'data': fields.Integer(required=True, description='update count')
})

machine_bulk_input_model = api.model(entity_name+' bulk load request data model', {
    'data': fields.List(fields.Nested(machine_input_model), required=True, description='Array of '+entity_name)
})

machine_bulk_response_model = api.inherit(entity_name+' bulk load response', generic_response_model, {
    'data': fields.List(fields.Nested(machine_response_model), required=True, description='response data model'),
})

deployment_response_model = api.inherit('Deployments model', generic_update_date_model, {
    'requested_by' : fields.String(required=True, description='Requested by name')
})

entity_response_model = api.model('Entity data response model', {
    'name': fields.String(required=True, description='Entity name'),
    'deployments' : fields.List(fields.Nested(deployment_response_model), required=True, description='Entity deployment history response data model')
})

tool_history_response_model = api.model('Tool Deployment History Model', {
    'tools': fields.List(fields.Nested(entity_response_model), required=True, description='Tool deployment history response data model'),
})

du_history_response_model = api.model('Tool Deployment History Model', {
    'dus': fields.List(fields.Nested(entity_response_model), required=True, description='DU deployment history response data model'),
})

history_response_model = api.model('Deployment History Model', {
    'history': fields.Nested(tool_history_response_model, required=False, description='tool history response data model'),
    'history': fields.Nested(du_history_response_model, required=False, description='tool history response data model'),
})

deployment_history_response = api.inherit(entity_name+' bulk load response', generic_response_model, {
    'data': fields.Nested(history_response_model, required=True, description='response data model'),
})
