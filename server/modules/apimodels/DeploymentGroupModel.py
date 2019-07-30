'''
Created on Feb 13, 2018

@author: pdinda
'''

from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model, genericId_response_model,oid_model


du_grp_create_response = api.inherit('DU Group Create Response', generic_response_model, {
    'data': fields.Nested(genericId_response_model)
})



du_grp_machine_grp_create_request = api.model('DU Group Model', {
    'machine_group_id': fields.String(required=False, description='Please provide the machine group _id'),
    'machine_group_name': fields.String(required=False, description='Please provide the machine group_name')    
    , 'skip_dep_ind': fields.Boolean(required=False, description='Indicator to suggest if build should be re deployed',default=True)
    , 'check_matching_ind': fields.Boolean(required=False, description='Indicator to suggest if DU and Machine matching should be done',default=False)
    , 'package_state_id': fields.String(required=False, description='Please provide the DU Package State _id')  
    , 'package_state_name': fields.String(required=False, description='Please provide the DU Package State name')
      
})


undeploy_group_deployment_request_input = api.model('un deploy du group input',{
    '_id': fields.Nested(oid_model, required=False, description='DB ID')
})


