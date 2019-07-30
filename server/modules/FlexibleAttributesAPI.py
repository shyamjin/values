from flask import request
from DBUtil import FlexibleAttributes
from Services.AppInitServices import authService
from settings import mongodb
from modules.apimodels import FlexAttributesModel
from flask_restplus import Resource
from modules.apimodels.Restplus import api, header_parser
from Services import FlexibleAttributesHelper

# get global db connection
db = mongodb
flexAttrDB = FlexibleAttributes.FlexibleAttributes()
flexibleAttributesAPINs = api.namespace('flexattributes', description='Flex Attributes Operations')

@flexibleAttributesAPINs.route('/new', methods=['POST'])
class CreateFA(Resource):
    @api.expect(header_parser, FlexAttributesModel.fa_create_request, validate=True)
    @api.marshal_with(FlexAttributesModel.fa_create_response)
    @authService.authorized
    def post(self):
        """
        Create new FA definition
        """
        fa_create_request_details = request.get_json()
        FlexibleAttributesHelper.validate_fa(fa_create_request_details)
        if FlexibleAttributesHelper.is_fa_exists(fa_create_request_details):
            raise Exception("FA " + fa_create_request_details.get('name') + " already exists for entity " + fa_create_request_details.get('entity'))

        fa_id = flexAttrDB.add(fa_create_request_details)
        return {"result": "success", "message": "FA was created successfully", "data": {"_id": fa_id}}, 200


@flexibleAttributesAPINs.route('/view/entity/<entity>', methods=['GET'])
@api.doc(params={'entity':'Business Entity name'})
class RetrieveFasByEntity(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(FlexAttributesModel.retrieve_fas_by_entity_response)
    @authService.authorized
    def get(self, entity):
        """
        Retrieve FAs by entity
        """
        FlexibleAttributesHelper.validate_entity(entity)
        fa_list = flexAttrDB.get_by_entity(entity)
        fa_list = list(fa_list) if fa_list else []
        return {"result": "success", "message": "FAs were retrieved successfully", "data": fa_list}, 200


@flexibleAttributesAPINs.route('/update', methods=['PUT'])
class UpdateFA(Resource):
    @api.expect(header_parser, FlexAttributesModel.fa_update_request, validate=True)
    @api.marshal_with(FlexAttributesModel.fa_update_response)
    @authService.authorized
    def put(self):
        """
        Update FA definition
        """
        fa_update_request_details = request.get_json()
        FlexibleAttributesHelper.validate_fa_update(fa_update_request_details)
        modify_status = flexAttrDB.update(fa_update_request_details)
        return {"result": "success", "message": "FA updated successfully", "data": modify_status}, 200


@flexibleAttributesAPINs.route('/view/all', methods=['GET'])
class GetAll(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(FlexAttributesModel.fa_get_all_response)
    @authService.authorized
    def get(self):
        """
        Get all flexible attributes
        """
        return {"result": "success", "message": "FAs were retrieved successfully", "data": list(flexAttrDB.get_all())}, 200


@flexibleAttributesAPINs.route('/view/<id>', methods=['GET'])
@api.doc(params={'id':'FA ID'})
class RetrieveFaById(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(FlexAttributesModel.retrieve_fa_by_id_response)
    @authService.authorized
    def get(self, id):
        """
        Retrieve FA by ID
        """
        fa = flexAttrDB.get_by_id(id)
        return {"result": "success", "message": "FA was retrieved successfully", "data": fa}, 200