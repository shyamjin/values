from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,response_id_oid_model,input_id_oid_model

entity_name=str(__name__.replace("Model", ""))

tag_model=  api.model(entity_name+' tag model', {
    '_id': response_id_oid_model(attribute='_id',required=True, description=''),
    'name': fields.String(required=True, description='name')
    })

get_all_tags_response_model=api.inherit(entity_name+' get all tag response model', generic_response_model, {
    'data': fields.List(fields.Nested(tag_model, required=True, description='response tag model'), required=True, description='response data model')
})

get_tag_by_id = api.inherit(entity_name+' get all tag response model', generic_response_model, {
    'data': fields.Nested(tag_model, required=True, description='response tag model')
})



add_tag_input_model = api.model(entity_name+' add tag input model', {
    'name': fields.String(required=True, description='name')
    })

add_tag_response_model = api.inherit(entity_name+' add tag response model', generic_response_model, {
    'data': fields.Nested(api.model(entity_name+' data model', {'id': fields.String(required=True, description='id')}), required=True, description='response tag model')
})


delete_tag_response_model = api.inherit(entity_name+' delete tag response model', generic_response_model, {
    'data': fields.Integer(required=True, description='is deleted'),
})


update_tag_input_model = api.model(entity_name+' update_tag_input_model', {
    'name': fields.String(required=True, description='name'),  
    '_id': input_id_oid_model(attribute='_id',required=True, description='')
})