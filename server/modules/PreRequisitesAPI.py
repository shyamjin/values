import json
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from DBUtil import PreRequisites
from Services.AppInitServices import authService
from Services import HelperServices
from settings import mongodb, relative_path
from flask_restplus import Resource
from modules.apimodels import PreRequisitesModel
from modules.apimodels.Restplus import api,header_parser
from modules.apimodels.GenericReponseModel import generic_post_response_model,generic_response_model


# blueprint declaration
preRequisitesAPI = Blueprint('PreRequisitesAPI', __name__)
#restplus delaration
preRequisitesAPINs = api.namespace('prerequisites', description='Prerequisites Operations')


# from werkzeug import secure_filename
# get global db connection
db = mongodb


# collections
preRequisitesDB = PreRequisites.PreRequisites(db)

# classes

@preRequisitesAPINs.route('/add', methods=['POST'])
class AddpreRequisites(Resource):
    @api.expect(header_parser,PreRequisitesModel.add_prerequisites_input_model,validate=True)
    @api.marshal_with(PreRequisitesModel.add_prerequisites_response_model)
    @authService.authorized
    def post(self):
        preRequisites = request.get_json()
        if (preRequisites.get("prerequisites_name"))is None:
            raise Exception("Mandatory fields prerequisites_name to create a new prerequisite was not found.")
        HelperServices.validate_name(preRequisites.get("prerequisites_name"),"prerequisite name")
        if preRequisitesDB.get_pre_requisites(preRequisites.get("prerequisites_name")) is not None:
            raise Exception("Prerequisite with name " + preRequisites.get("prerequisites_name") + " already exists")
        if preRequisites["version_command"] == "":
            preRequisites["version_command"] = "--version"
        new_ver_id = preRequisitesDB.add_pre_requisites(preRequisites)
        return {"result": "success", "message": "New preRequisites added successfully", "data": {"id": new_ver_id}}, 200



@preRequisitesAPI.route('/prerequisites/view', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/PreRequisitesAPI/Getprerequisites.yml')
def Getprerequisites():
    return jsonify(json.loads(dumps({"result": "success", "data": preRequisitesDB.get_all_pre_requisites()}))), 200


@preRequisitesAPI.route('/prerequisites/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/PreRequisitesAPI/GetprerequisitesByid.yml')
def GetprerequisitesByid(id):
    return jsonify(json.loads(dumps({"result": "success", "data": preRequisitesDB.get_pre_requisites_by_id(id)}))), 200

@preRequisitesAPINs.route('/update', methods=['PUT'])
class Updateprerequisites(Resource):
    @api.expect(header_parser,PreRequisitesModel.add_prerequisites_input_model,validate=True)
    @api.marshal_with(generic_response_model)
    @authService.authorized
    def put(self):
        preRequisites = request.get_json()
        HelperServices.validate_name(preRequisites.get("prerequisites_name"),"prerequisite name")
        soft = preRequisitesDB.get_pre_requisites(
            preRequisites.get("prerequisites_name"))
        if  soft and soft.get("prerequisites_name"):
            preRequisites["_id"] = soft["_id"]
            preRequisitesDB.update_pre_requisites(preRequisites)
            return {"result": "success", "message": "preRequisites updated successfully"}, 200            
        else:
            raise Exception("Invalid input data")


@preRequisitesAPI.route('/prerequisites/delete/<string:id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/PreRequisitesAPI/Deleteprerequisites.yml')
def Deleteprerequisites(id):
    isDeleted = preRequisitesDB.delete_pre_requisites(id)  # Missing Method
    return jsonify(json.loads(dumps({"result": "success", "message": "The preRequisites was deleted successfully"}))), 200
    