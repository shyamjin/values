import ast,copy
import collections
from modules.apimodels.Restplus import api,header_parser
from flask_restplus import Resource
import csv
from datetime import datetime
import json
import os
from time import mktime
import traceback
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from werkzeug import secure_filename
from DBUtil import DeploymentRequest, DeploymentRequestGroup, Machine, Versions, MachineGroups, ToolSet, Tool, DeploymentUnit,State
from Services import DeploymentRequestService
from Services.AppInitServices import authService
from settings import mongodb, import_full_path, relative_path
from modules.apimodels import DeploymentRequestModel


# from time import time
# from collections import OrderedDict
# blueprint declaration
deploymentrequestAPI = Blueprint('deploymentrequestAPI', __name__)

deploymentrequestAPINs = api.namespace('deploymentrequest', description='Deployment Request Operations')
# get global db connection
db = mongodb

# collections

deploymentRequestDB = DeploymentRequest.DeploymentRequest(db)
deploymentRequestGroupDB = DeploymentRequestGroup.DeploymentRequestGroup(db)
machineDB = Machine.Machine(db)
versionsDB = Versions.Versions(db)
machinegroupsDB = MachineGroups.MachineGroups(db)
toolSetDB = ToolSet.ToolSet(db)
deploymentRequestService = DeploymentRequestService.DeploymentRequestService(
    db)
deploymentUnitDB = DeploymentUnit.DeploymentUnit()
toolDB = Tool.Tool(db)
statedb = State.State(db)



@deploymentrequestAPI.route('/deploymentrequest/deploymentfield/upload', methods=['POST'])
@authService.authorized
def upload_csv_json_file():
    # This is the path to the upload directory
    try:
        # Get the name of the uploaded file
        file = request.files['file']
        if file is None:
            raise ValueError("No file selected")
        # Check if the file is one of the allowed types/extensions
        if(file.filename.rsplit('.', 1)[1] in ['csv']):
            filename = secure_filename(file.filename)
            file_path = str(import_full_path + '/' + filename)
            file.save(file_path)
            f = open(file_path, 'r')
            reader = csv.reader(f)
            json1 = {}
            index = 0
            fields = []
            for row in reader:
                if(index is 0):
                    if (str.lower(str(row[0])) <> "key") or (str.lower(str(row[1])) <> "value"):
                        raise ValueError("Invalid data format in csv file")
                else:
                    if str(row[0]).strip() is "":
                        continue
                    json1["input_name"] = str(row[0])
                    json1["default_value"] = str(
                        ast.literal_eval(json.dumps(row[1])))
                    json1["is_mandatory"] = False
                    json1["input_type"] = "text"
                    fields.append(json1)
                    json1 = {}
                index = index + 1
            return jsonify(json.loads(dumps({"result": "success", "message": "Deployment fields uploaded successfully from file", "data": {"fields": fields}}))), 200
        elif (file.filename.rsplit('.', 1)[1] in ['json']):
            filename = secure_filename(file.filename)
            file_path = str(import_full_path + '/' + filename)
            file.save(file_path)
            try:
                json1 = json.loads(open(file_path).read())
                fields = []
                json2 = {}
                for key in json1:
                    json2["input_name"] = str(key)
                    json2["default_value"] = str(
                        ast.literal_eval(json.dumps(json1[str(key)])))

                    json2["is_mandatory"] = False
                    json2["input_type"] = "text"
                    fields.append(json2)
                    json2 = {}
            except Exception as e:  # catch *all* exceptions
                raise ValueError("Invalid format of json")

            return jsonify(json.loads(dumps({"result": "success", "message": "Deployment fields uploaded successfully from file", "data": {"fields": fields}}))), 200

        else:
            raise Exception("Invalid file .Please select file of type 'csv' or 'json")
    finally:
        try:
            f.close()
            os.remove(file_path)
        except Exception as e:
            print e


# DeploymentRequest
@deploymentrequestAPI.route('/deploymentrequest/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentRequestAPI/getAllDeploymentRequests.yml')
def getAllDeploymentRequests():
    filter_condition = {}
    if request.args.get('startdate', None):
        filter_condition["start_time"] = {'$gte': datetime.strptime(
            request.args.get('startdate', None).split(".")[0], "%Y-%m-%dT%H:%M:%S")}
    if request.args.get('enddate', None):
        filter_condition["end_time"] = {'$lte': datetime.strptime(
            request.args.get('enddate', None).split(".")[0], "%Y-%m-%dT%H:%M:%S")}
    limit = int(request.args.get('perpage', "0"))
    page = int(request.args.get('page', "0"))
    skip = page * limit
    deployment_request = deploymentRequestDB.GetDeploymentRequestAll(
        filter_condition, skip, limit)
    req_all = []
    for req in deployment_request:
        if req.get("parent_entity_id"):
            req["version"] = versionsDB.get_version(
                req["parent_entity_id"], False)
            req["du"] = deploymentUnitDB.GetDeploymentUnitById(
                req["parent_entity_id"], False)
            if req.get("version"):
                toolData = toolDB.get_tool_by_id(
                    req.get("version").get("tool_id"), False)
                if toolData:
                    req["parent_entity"] = {"parent_entity_id": str(
                        toolData["_id"]), "parent_entity_name": toolData.get("name")}
            else:
                if req["du"]:
                    req["parent_entity"] = {"parent_entity_id": str(
                        req["du"]["_id"]), "parent_entity_name": req["du"].get("name")}

        if req.get("machine_id"):
            req["machine"] = machineDB.GetMachine(req["machine_id"])
            if req.get("machine"):
                req["machine"] = {"machine_id": str(req["machine"].get(
                    "_id")), "machine_name": req["machine"].get("machine_name")}
        if "logs" in req.keys():
            req.pop("logs")
        if "tool_deployment_value" in req.keys():
            req.pop("tool_deployment_value")
        if "step_details" in req.keys():
            req.pop("step_details")
        if req.get("start_time"):
            req["start_time_iso_format"] = copy.deepcopy(req["start_time"])
            req["start_time"] = mktime(
                datetime.utctimetuple(req["start_time"]))
            req["current_time"] = mktime(
                datetime.utctimetuple(datetime.now()))
        req_all.append(req)
    listOfDeployments = collections.OrderedDict()

    # INITIALIZE COUNT
    failedCount = 0
    inprogressCount = 0
    completedCount = 0
    retryCount = 0
    newCount = 0
    skipped_count = 0

    for rec in req_all:

        # SET STATUS COUNT
        if "Retry".lower() in str(rec.get("status")).lower():
            retryCount = retryCount + 1
        elif "Failed".lower() in str(rec.get("status")).lower():
            failedCount = failedCount + 1
        elif "Done".lower() in str(rec.get("status")).lower():
            if str(rec.get("skipped_ind",False)).lower() == "true":
                skipped_count+=1
            else:    
                completedCount = completedCount + 1
        elif "Processing".lower() in str(rec.get("status")).lower():
            inprogressCount = inprogressCount + 1
        elif "New".lower() in str(rec.get("status")).lower():
            newCount = newCount + 1

        # ADD TO SORT ARRAY
        if str(rec['_id'].generation_time.replace(tzinfo=None).date()) not in listOfDeployments.keys():
            listOfDeployments[str(
                rec['_id'].generation_time.replace(tzinfo=None).date())] = []
            listOfDeployments[str(rec['_id'].generation_time.replace(
                tzinfo=None).date())].append(rec)
        else:
            listOfDeployments[str(rec['_id'].generation_time.replace(
                tzinfo=None).date())].append(rec)

    # NEW FORMAT FOR NEW GUI
    data = {"list": listOfDeployments, "requests_count": {"failed": failedCount,
                                                          "inprogress": inprogressCount,
                                                          "retry": retryCount,
                                                          "new": newCount,
                                                          "done": completedCount,
                                                          "skipped": skipped_count}}

    return dumps({"result": "success", "data": data}), 200 # NOt changed as listOfDeployments gets reversed.Keep as is 


@deploymentrequestAPI.route('/deploymentrequest/view/<string:id>', methods=['GET'])
@authService.authorized
def getDeploymentRequestByID(id):
    deployment_request = deploymentRequestDB.GetDeploymentRequest(id)
    if deployment_request.get("machine_id"):
        deployment_request["machine_details"] = machineDB.GetMachine(
            deployment_request["machine_id"])
        deployment_request["machine_name"] = None
        if deployment_request["machine_details"]:
            deployment_request["machine_name"] = deployment_request["machine_details"]["machine_name"]
    if deployment_request.get("parent_entity_id"):
        version_details = versionsDB.get_version(
            deployment_request["parent_entity_id"], False)
        du_details = deploymentUnitDB.GetDeploymentUnitById(
            deployment_request["parent_entity_id"], False)
        if version_details:
            deployment_request["parent_entity_details"] = version_details
            deployment_request["parent_entity_name"] = toolDB.get_tool_by_id(
                version_details["tool_id"], False)["name"]
        if du_details:
            deployment_request["parent_entity_details"] = du_details
            deployment_request["parent_entity_name"] = du_details["name"]
    dep_group_details = deploymentRequestGroupDB.get_grp_depreq_by_inner_depreq_ids(
            str(deployment_request.get("_id")))
    if dep_group_details:
        deployment_request["dep_group_details"] = {"_id": str(dep_group_details.get("_id")), \
                                               "name": dep_group_details.get("name")}        
    return jsonify(json.loads(dumps({"result": "success", "data": deployment_request}))), 200


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


@deploymentrequestAPINs.route('/retry', methods=['PUT'])
class retryDeploymentRequest(Resource):
    @api.expect(header_parser,DeploymentRequestModel.retry_depreq_input_model,validate=True)
    @api.marshal_with(DeploymentRequestModel.retry_depreq_response_model)
    @authService.authorized 
    def put(self):
        data = request.json
        DeploymentRequest = request.get_json()
        dep_id = DeploymentRequest.get("_id")
        if dep_id is None:
            raise Exception("_id is missing")
        oid = dep_id.get("oid")
        if oid is None:
            raise Exception("oid is missing")
        updated = deploymentRequestService.retryDeploymentRequest(oid)
        if updated == 1:
            return {"result": "success", "message": "The request was updated successfully", "data": updated}, 200
        else:
            raise Exception ("The request is not in failed status")