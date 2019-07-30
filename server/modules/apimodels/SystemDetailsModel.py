from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,response_id_oid_model
entity_name=str(__name__.replace("Model", ""))

sysdet_model =  api.model(entity_name+' data model', {
    'pipeline': fields.String(required=True, description='pipeline'),
     'build_date': fields.String(required=True, description='build_date'),
      'dpm_version': fields.String(required=True, description='dpm_version'),
       'account_logo': fields.String(required=True, description='account_logo'),
        'hostname': fields.String(required=True, description='hostname'),
         'master_host': fields.String(required=True, description='master_host'),
          'created_by': fields.String(required=True, description='created_by'),
           'account_name': fields.String(required=True, description='account_name'),
            'dpm_type': fields.String(required=True, description='dpm_type'),
             'build': fields.String(required=True, description='build'),
              'master_port': fields.String(required=True, description='master_port'),
               'homepage': fields.String(required=True, description='homepage'),
                'port': fields.String(required=True, description='port'),
                'ondockerInd': fields.String(required=True, description='ondockerInd'),
                 '_id': response_id_oid_model(attribute='_id',required=True, description=''),
                 'allow_new_tools': fields.Boolean(required=True, description='')
    })
get_all_sysdet_response_model=api.inherit(entity_name+' get all sys details response model', generic_response_model, {
    'data': fields.Nested(sysdet_model, required=True, description='response sys details model')
})

acclogo = api.model(entity_name+' logo model', {
    'account_logo': fields.String(required=True, description='account_logo'),
    })
get_logo_response_model=api.inherit(entity_name+' get logo response model', generic_response_model, {
    'data': fields.Nested(acclogo, required=True, description='response sys details model')
})

