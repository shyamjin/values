from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,input_id_oid_model

entity_name=str(__name__.replace("Model", ""))


udc_schedule_req_input_model = api.model(entity_name+' udc_schedule_req_input_model', {
    'enable': fields.String(required=True, description='enable'),
     'type': fields.String(required=True, description='type'),
      'hrs': fields.Float(required=True, description='hrs'),
        'min': fields.Float(required=True, description='min'),
         'intervalGiven': fields.Float(required=True, description='intervalGiven'),    
          '_id': input_id_oid_model(attribute='_id',required=True, description=''),
})



udc_schedule_req_response_model = api.inherit(entity_name+' udc_schedule_req_response_model', generic_response_model, {
    'data': fields.Integer(required=True, description='update count'),
})
