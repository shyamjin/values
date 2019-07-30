from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import response_id_oid_model

entity_name=str(__name__.replace("Model", ""))


reports_model = api.model('reports_model', {
    'url': fields.String(required=True, description='url'),
    'collection_name': fields.String(required=True, description='collection_name'),
    'name': fields.String(required=True, description='name'),
     '_id': response_id_oid_model(attribute='_id',required=True, description=''),
})

get_all_reports_response_model  = api.model(entity_name+' get_all_reports_response_model', {
    'result': fields.String(required=True, description='result'),
    'data': fields.List(fields.Nested(reports_model), required=True, description='response data model')
})
