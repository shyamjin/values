from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model

entity_name=str(__name__.replace("Model", ""))

update_account_input_model=api.model(entity_name+' account update input model', {
    'old_account_name': fields.String(required=True, description='old_account_name'),
    'new_account_name': fields.String(required=True, description='new_account_name')
    })

idmodel = api.model(entity_name+' id model', {
     'id': fields.String(required=True, description='DB ID')
    })
update_account_response_model = api.inherit(' account update response model', generic_response_model, {
    'data': fields.Nested(idmodel, required=True, description='response sys details model')
})