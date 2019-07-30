from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,input_id_oid_model
entity_name=str(__name__.replace("Model", ""))





retry_depreq_input_model =  api.model(entity_name+' update password input data model', {
    '_id': input_id_oid_model(attribute='_id',required=True, description=''),                                                                        
})


retry_depreq_response_model= get_all_depreq_response_model = api.inherit(entity_name+'get dep req response model', generic_response_model, {
        'data': fields.Integer(required=True, description='update count')  
        })
