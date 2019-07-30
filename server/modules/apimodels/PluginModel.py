from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,response_id_oid_model

entity_name=str(__name__.replace("Model", ""))


deployment_plugin_response_model_inner = api.model(entity_name+' response inner', {
    'name': fields.String(required=True, description='File name')
    , 'path': fields.String(required=True, description='File path')
    , 'file_contents': fields.List(fields.String,required=True, description='File Contents')    
})


deployment_plugin_response_model = api.inherit(entity_name+' response', generic_response_model, {
    'data': fields.List(fields.Nested(deployment_plugin_response_model_inner), required=True, description='response data model'),
})


deployment_plugin_requets_model = api.model(entity_name+entity_name+' request', {
    'file': fields.Raw(required=True, description='file')
})



get_all_plugin_data = api.model(entity_name+' all plugin data', {
    'category': fields.String(required=True, description='category'),
     'status': fields.String(required=True, description='status'),
      'description': fields.String(required=True, description='description'),
        'author': fields.String(required=True, description='author'),
         'version': fields.String(required=True, description='version'),
          'name': fields.String(required=True, description='name'),    
          '_id': response_id_oid_model(attribute='_id',required=True, description=''),
})


get_all_plugin_response_model = api.inherit(entity_name+' get all plugin response', generic_response_model, {
    'data': fields.List(fields.Nested(get_all_plugin_data), required=True, description='response data model'),
})

activate_deactivate_plugin_response_model= api.inherit(entity_name+' activate/deactivate plugin response', generic_response_model, {
    'data': fields.String(required=True, description='data')
})


get__plugin_by_id_response_model = api.inherit(entity_name+' get plugin by id response', generic_response_model, {
    'data': fields.Nested(get_all_plugin_data, required=True, description='response data model'),
})