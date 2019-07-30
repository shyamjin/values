from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model,input_id_oid_model

entity_name=str(__name__.replace("Model", ""))


user_add_response_model =api.model(entity_name+' token data model', {
    'Token': fields.String(required=True, description='token')})

add_user_response_model = api.inherit(entity_name+'add user response model', generic_response_model, {
    'data': fields.Nested(user_add_response_model, required=True, description='response data model')
})

update_user_response_model = api.inherit(entity_name+'User response model', generic_response_model, {
    'data': fields.Integer(required=True, description='update count')
})

gen_accestoken_response_model = api.inherit(entity_name+'Generate Access token response model', generic_response_model, {
    'data': fields.String(required=True, description='Access Token')
})

logout_response_model = api.inherit(entity_name+' Logout response model', add_user_response_model )

ForgotPassword_response_model = api.inherit(entity_name+' Forgot Password model', generic_response_model )

auth_verify_response_model = api.inherit(entity_name+' Forgot Password model', generic_response_model )

add_user_input_model = api.model(entity_name+' add user input data model', {
    'employeeid': fields.Integer(required=True, description='employeeid'),
    'user': fields.String(required=True, description='user'),
    'roleid': fields.String(required=True, description='roleid'),
    'email': fields.String(required=True, description='email'),
    'accountid': fields.String(required=True, description='accountid'),
    'homepage': fields.String(required=True, description='homepage'),
    'included_in': fields.List(fields.String(required=False, description='included_in'),required=True, description='included_in'),
    })

update_user_input_model = api.inherit(entity_name+' update user input model', add_user_input_model, {
    '_id': input_id_oid_model(attribute='_id',required=True, description='')
})

update_password_input_model  =  api.model(entity_name+' update password input data model', {
    '_id': input_id_oid_model(attribute='_id',required=True, description=''),
    'password': fields.String(required=True, description='new password')                                                                      
})

gen_accestoken_input_model =api.model(entity_name+' Generate Access token input data model', {
    '_id': input_id_oid_model(attribute='_id',required=True, description=''),
    'access_exp_date': fields.String(required=False, description='Expiry Timestamp')
                                                                            
})

logout_response_model = api.inherit(entity_name+' Logout response model', add_user_response_model )

ForgotPassword_response_model = api.inherit(entity_name+' Forgot Password model', generic_response_model )

ForgotPassword_input_model =api.model(entity_name+' Forgot Password input data model', {
    'user': fields.String(required=True, description='user')
    })

auth_verify_input_model = api.model(entity_name+' Forgot Password input data model', {
    'token': fields.String(required=True, description='user')
    })