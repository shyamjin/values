# MasterDPM API's for Distribution Center and Distribution SYNC calls from
# Account DPM
'''
Created on Aug 6, 2016

@author: pdinda
'''

import traceback,json
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from DBUtil import Config, CloneRequest, Machine, DistributionMachine, DistributionSync, Tool, Accounts, Versions
from Services import DistributionCenterService
from Services.AppInitServices import authService
from settings import mongodb, relative_path
from flask_restplus import Resource
from modules.apimodels import DistributionCenterModel
from modules.apimodels.Restplus import api,header_parser


# blueprint declaration
distributionCenterAPI = Blueprint('distributionCenterAPI', __name__)
# restplus declaration
distributionCenterAPINs = api.namespace('clonerequest/distribution', description='Distribution Center Operations')

# get global db connection
db = mongodb

# collection
configdb = Config.Config(db)
distributionCenterConfig = configdb.getConfigByName("PushServices")

# collections
cloneRequestDB = CloneRequest.CloneRequest(db)
machineDB = Machine.Machine(db)
distributionMachinetDB = DistributionMachine.DistributionMachine(db)
if distributionCenterConfig:
    distributionCenterService = DistributionCenterService.DistributionCenterService(
        db)
distributionsyncDB = DistributionSync.DistributionSync(db)
tooldb = Tool.Tool(db)
versionsDB = Versions.Versions(db)
accountDB = Accounts.Accounts()
distributionMachinetDB = DistributionMachine.DistributionMachine(db)
# classes


@distributionCenterAPI.route('/clonerequest/distribution/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DistributionCenterAPI/getAllDistributionCenterDistribution.yml')
def getAllDistributionCenterDistribution():
    result = []
    request_data = distributionMachinetDB.GetDistributionMachineAll()
    if request_data:
        for rec in request_data:
            machine=machineDB.GetMachine(
                rec.get("machine_id"))
            if machine:
                rec["machine_name"] = machine.get("machine_name")
            result.append(rec)
    return jsonify(json.loads(dumps({"result": "success", "data": result}))), 200


@distributionCenterAPI.route('/clonerequest/distribution/run/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DistributionCenterAPI/RunAllDistributionCenterDistribution.yml')
def RunAllDistributionCenterDistribution():
    result = distributionMachinetDB.GetAllDistributionMachineRequests("on")
    if not result or result.count() < 1:
        raise Exception("No machines found to distribute to")
    distributionCenterService.job_function(None)
    return jsonify(json.loads(dumps({"result": "success", "Message": "Distribution request is accepted", "data": distributionMachinetDB.GetDistributionMachineAll()}))), 200


@distributionCenterAPI.route('/clonerequest/distribution/run/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DistributionCenterAPI/RunDistributionCenterDistribution.yml')
def RunDistributionCenterDistribution(id):
    rec = distributionMachinetDB.GetDistributionMachineRequest(str(id))
    if not rec:
        raise ValueError("No such distribution request was found")
    distributionCenterService.job_function(str(id))
    rec = distributionMachinetDB.GetDistributionMachineRequest(id)
    return jsonify(json.loads(dumps({"result": "success", "Message": "Request was completed.Status: " + rec.get("distribution_status"), "data": rec}))), 200

@distributionCenterAPINs.route('/add', methods=['POST'])
class addDistributionCenterDistributionRequest(Resource):
    @api.expect(header_parser,DistributionCenterModel.add_dc_input_model,validate=True)
    @api.marshal_with(DistributionCenterModel.add_dc_response_model)
    @authService.authorized 
    def post(self):
        NewCloneRequest = request.get_json()
        if NewCloneRequest.get("host") is None:
            raise Exception ("Host was not found in request")
        if NewCloneRequest.get("machine_id") is None:
            raise Exception ("machine_id was not found in request")
        if NewCloneRequest.get("status") is None or NewCloneRequest.get("status") not in ["on", "off"]:
            raise Exception ("Invalid status was found in request")
        if distributionMachinetDB.GetDistributionMachineRequestByMachineId(str(NewCloneRequest.get("machine_id"))):
            raise Exception ("Request already exists for this machine")
        Clone_request_id = distributionMachinetDB.AddDistributionMachineRequests(
            NewCloneRequest)
        return {"result": "success", "message": "New distribution request has been added successfully", "data": {"id": Clone_request_id}},200



@distributionCenterAPINs.route('/update', methods=['PUT'])
class updateDistributionCenterDistributionRequest(Resource):
    @api.expect(header_parser,DistributionCenterModel.add_dc_input_model,validate=True)
    @api.marshal_with(DistributionCenterModel.add_dc_response_model)
    @authService.authorized 
    def put(self):
        NewCloneRequest = request.get_json()
        if NewCloneRequest.get("host") is None:
            raise Exception("host was not found in request")
        if NewCloneRequest.get("machine_id") is None:
            raise Exception("machine_id was not found in request")
        if NewCloneRequest.get("status") is None or NewCloneRequest.get("status") not in ["on", "off"]:
            raise Exception("Invalid status was found in request")
        distributionMachinetDB.UpdateDistributionMachineRequest(NewCloneRequest)
        return {"result": "success", "message": "Existing distribution request was updated", "data": {"id": NewCloneRequest["_id"]["oid"]}}, 200


@distributionCenterAPI.route('/clonerequest/distribution/cancel/<string:id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/DistributionCenterAPI/cancelDistributionCenterDistributionRequest.yml')
def cancelDistributionCenterDistributionRequest(id):
    try:
        isDeleted = distributionMachinetDB.CancelDistributionMachineRequests(
            str(id))
        if isDeleted == 1:
            return jsonify(json.loads(dumps({"result": "success", "data": isDeleted, "message": "The distribution request was deleted"}))), 200
        else:
            raise Exception("The distribution request is not deleted")
    except Exception as e:  # catch *all* exceptions
        print "Error :" + str(e)
        traceback.print_exc()
        raise Exception(str(e))

# Account DPM - /clonerequest/distribution/tool calls this API

#Swagger not requiered as intenally called for clone. Never exposed to user
@distributionCenterAPI.route('/clonerequest/distribute/add', methods=['POST'])
@authService.unauthorized
def DistributeCloneRequest():

    try:
        data = {}
        new_request = request.get_json()

        # MACHINE DETAILS
        result = machineDB.GetMachinebyIp(new_request.get("ip"))
        if result is None:
            raise ValueError("No machine found with ip :" +
                             str(new_request.get("ip")))
        data["machine_id"] = str(result.get("_id"))

        # ACCOUNT DETAILS
        account_name = accountDB.get_account(result.get("account_id"))
        if account_name is None:
            raise ValueError(
                "Account not found with account_id :" + result.get("account_id"))
        data["account_id"] = result.get("account_id")
        data["account_name"] = new_request.get("account_name")
        if data["account_name"] <> account_name.get("name"):
            raise ValueError(
                "Account not found on masterDPM with account_name :" + data["account_name"])

        # TOOLS DETAILS
        tool_list = new_request.get("tool_list")
        for version in tool_list:
            verresult = versionsDB.get_version(version["version_id"], False)
            if not verresult:
                raise ValueError("Version with _id :" +
                                 version["version_id"] + " was not found")
        data["tool_list"] = new_request.get("tool_list")

        # TYPE DETAILS
        data["type"] = new_request.get("type")
        if data.get("type") not in ["importtool", "updatetool"]:
            raise ValueError("Valid type was not found in input request")

        # ADD REQUEST
        clone_id = cloneRequestDB.AddCloneRequest(data, data["type"])
        if not clone_id:
            raise ValueError("New clone request was not added")
        else:
            return jsonify(json.loads(dumps({"result": "success", "message": "A new clone request was added", "id": clone_id}))), 200
    except Exception as e:  # catch *all* exceptions
        print "Error :" + str(e)
        traceback.print_exc()
        raise Exception(str(e))

# called by Account DPM  - /clonerequest/distribution/tool/status/


@distributionCenterAPI.route('/clonerequest/distribute/status/<string:id>', methods=['GET'])
@authService.unauthorized
@swag_from(relative_path + '/swgger/DistributionCenterAPI/DistributeCloneRequestStatus.yml')
def DistributeCloneRequestStatus(id):
    try:
        Clone_request = cloneRequestDB.GetCloneRequest(id)
        if not Clone_request:
            raise Exception("Clone request with _id :" + id + " was not found")
        else:
            if not Clone_request.get("status"):
                raise Exception("Status not found in request")
            return jsonify(json.loads(dumps({"result": "success", "message": "Status Found", "data": Clone_request}))), 200
    except Exception as e:  # catch *all* exceptions
        print "Error :" + str(e)
        traceback.print_exc()
        raise Exception(str(e))
