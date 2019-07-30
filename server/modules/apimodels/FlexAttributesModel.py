from modules.apimodels.Restplus import api
from flask_restplus import fields
from modules.apimodels.GenericReponseModel import generic_response_model, genericId_response_model, response_id_oid_model,input_id_oid_model
from enum import Enum


class Entities(Enum):
    DeploymentUnit = 1
    Machine = 2
    MachineGroup = 3

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)


class FaTypes(Enum):
    String = 1
    Select = 2
    MultiSelect = 3

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)


fa_model = api.model('FA Model', {
    'name': fields.String(required=True, description='Attribute name')
    , 'title': fields.String(required=True, description='Attribute title for display')
    , 'type': fields.String(required=True, description='Attribute field type (String, Integer, ...)')
    , 'entity': fields.String(required=True, description='Attribute related business entity (DeploymentUnit, Machine, ...)')
    , 'default_value': fields.String(required=False, description='Attribute default value')
    , 'description': fields.String(required=True, description='Attribute attribute description')
    , 'is_active': fields.Boolean(required=True, description='Attribute status. True for active. False for inactive')
    , 'is_mandatory': fields.Boolean(required=True, description='Indicates if the attribute should be populated for each entity')
    , 'valid_values': fields.List(fields.String(), required=False, description='Attribute valid values separated by comma')
})

fa_with_id_model = api.inherit('FA_Model_with_DB_ID', fa_model, {
        '_id': response_id_oid_model(attribute='_id',required=True, description='')
})

fa_create_request = api.inherit('FA Create Request', fa_model, {
})

fa_create_response = api.inherit('FA Create Response', generic_response_model, {
    'data': fields.Nested(genericId_response_model)
})

retrieve_fas_by_entity_request = api.model('Retrieve FAs by entity name Request', {
    'entity_name': fields.String(required=True, description='Business Entity name')
})

retrieve_fas_by_entity_response = api.inherit('Retrieve FAs by entity name Response', generic_response_model, {
    'data': fields.List(fields.Nested(fa_with_id_model))
})

fa_update_request = api.inherit('FA Update Request', fa_model, {
    '_id': input_id_oid_model(attribute='_id',required=True, description='')
})

fa_update_response = api.inherit('FA Update Response', generic_response_model, {
    'data': fields.Integer(required=True, description='Modification status. 1: FA updated. 0: FA was not updated.')
})

fa_get_all_response = api.inherit('FA get all response', generic_response_model, {
    'data': fields.List(fields.Nested(fa_with_id_model))
})

retrieve_fa_by_id_response = api.inherit('Retrieve FA by ID Response', generic_response_model, {
    'data': fields.Nested(fa_with_id_model)
})
