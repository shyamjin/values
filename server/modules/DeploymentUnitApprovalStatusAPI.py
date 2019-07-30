import traceback

from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify
from DBUtil import DeploymentUnitApprovalStatus, Users, SystemDetails
from Services.AppInitServices import authService
from settings import mongodb, relative_path
from modules.apimodels.Restplus import api,header_parser
from Services import DeploymentUnitApprovalStatusHelper
from modules.apimodels import DeploymentUnitApprovalStatusAPIModel
from flask_restplus import Resource
from flask import request
import json
# blueprint declaration
deploymentUnitApprovalStatusAPI = Blueprint(
    'deploymentUnitApprovalStatusAPI', __name__)
DeploymentUnitApprovalStatusAPINs = api.namespace('deploymentunitapprovalstatus', description='DeploymentUnitApprovalStatus Operations',path="/deploymentunitapprovalstatus")

# get global db connection
db = mongodb
deploymentUnitApprovalStatusDB = DeploymentUnitApprovalStatus.DeploymentUnitApprovalStatus()
userDB = Users.Users(db)
systemDetailsDB = SystemDetails.SystemDetails(db)


@deploymentUnitApprovalStatusAPI.route('/deploymentunitapprovalstatus/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitApprovalStatusAPI/getallDeploymentUnitApprovalStatus.yml')
def getallDeploymentUnitApprovalStatus():
    return jsonify(json.loads(dumps({"result": "success", "data": deploymentUnitApprovalStatusDB.GetAllDeploymentUnitApprovalStatus()}))), 200
    
    
@DeploymentUnitApprovalStatusAPINs.route('/add', methods=['POST'])
class add_deploymentunitapprovalstatus(Resource):
    @api.expect(header_parser,DeploymentUnitApprovalStatusAPIModel.approval_status_create_request,validate=True)
    @api.marshal_with(DeploymentUnitApprovalStatusAPIModel.approval_status_create_response)
    @authService.authorized
    def post(self):
        approval_status_data = request.get_json()
        approval_status_id = DeploymentUnitApprovalStatusHelper.add_approval_status(approval_status_data)
        return {"result": "success", "message": "DeploymentUnitApprovalStatus was created successfully", "data": {"_id": approval_status_id }}, 200
        

@DeploymentUnitApprovalStatusAPINs.route('/update', methods=['PUT'])
class update_deploymentunitapprovalstatus(Resource):
    @api.expect(header_parser,DeploymentUnitApprovalStatusAPIModel.approval_status_update_request,validate=True)
    @api.marshal_with(DeploymentUnitApprovalStatusAPIModel.approval_status_update_response)
    @authService.authorized
    def put(self):
        approval_status_data = request.get_json()
        update_count = DeploymentUnitApprovalStatusHelper.update_approval_status(approval_status_data)
        return {"result": "success", "message": "DeploymentUnitApprovalStatus was updated successfully", "data": update_count}, 200

@DeploymentUnitApprovalStatusAPINs.route('/delete/<object_id>', methods=['DELETE'])
@api.doc(params={'object_id':'Repo object_id'})
class delete_deploymentunitapprovalstatus(Resource):
    @api.expect(header_parser,validate=True)
    @api.marshal_with(DeploymentUnitApprovalStatusAPIModel.generic_response_model)
    @authService.authorized
    def delete(self,object_id):
        DeploymentUnitApprovalStatusHelper.delete_approval_status(object_id)
        return {"result": "success", "message": "DeploymentUnitApprovalStatus was deleted successfully"}, 200
        
#CALLED BY CLONE
@DeploymentUnitApprovalStatusAPINs.route('/view/name/<name>', methods=['GET'])
@api.doc(params={'name':'Repo Name'})
class deploymentunitapprovalstatus_by_name(Resource):
    @api.expect(header_parser,validate=True)
    @authService.authorized
    def get(self,name):
        data=deploymentUnitApprovalStatusDB.GetDeploymentUnitApprovalStatusByName(name)
        if data:
            return json.loads(dumps({"result": "success",  "data": data})), 200
        else:
            raise Exception("No Approval Status found with name : "+ name )
    
@DeploymentUnitApprovalStatusAPINs.route('/view/<object_id>', methods=['GET'])
@api.doc(params={'object_id':'Repo object_id'})
class deploymentunitapprovalstatus_by_id(Resource):
    @api.expect(header_parser,validate=True)
    @authService.authorized
    def get(self,object_id):
        data= deploymentUnitApprovalStatusDB.GetDeploymentUnitApprovalStatusById(object_id)
        if data:
            return json.loads(dumps({"result": "success","data": data})), 200
        else:
            raise Exception("No Approval Status found with id : "+ object_id)
    
