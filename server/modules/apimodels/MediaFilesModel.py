from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import input_id_oid_model

entity_name=str(__name__.replace("Model", ""))


media_files_model = api.model(entity_name+' media files model', {
    'name': fields.String(required=True, description='name'),
    'url': fields.String(required=True, description='parent_entity_id'),
    'type': fields.String(required=True, description='type'),
    'tooltip': fields.String(required=False, description='tooltip'),
    'content': fields.String(required=False, description='content'),
    'thumbnail_url': fields.String(required=False, description='thumbnail_url'),
    })


data_model = api.model(entity_name+' data model', {
    '_id': input_id_oid_model(attribute='_id',required=True, description=''),
    'parent_entity_id': fields.String(required=True, description='parent_entity_id'),
    'media_files': fields.List(fields.Nested(media_files_model,required=True, description=''),required=True, description='media_files'),
    })


update_media_files = api.model(entity_name+' input data model', {
    'data': fields.List(fields.Nested(data_model,required=True, description=''),required=True, description='list')   
    })
