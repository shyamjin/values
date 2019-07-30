from datetime import datetime
import traceback,json
from bson.json_util import dumps
from flasgger import swag_from, validate, ValidationError
from flask import Blueprint, jsonify, request
from DBUtil import CloneRequest, Machine, DistributionMachine, Tool, Accounts, Versions
from Services import ToolHelperService
from Services.AppInitServices import authService
from settings import mongodb, relative_path


# blueprint declaration
clonerequestAPI = Blueprint('clonerequestAPI', __name__)

# get global db connection
db = mongodb


# collections
cloneRequestDB = CloneRequest.CloneRequest(db)
machineDB = Machine.Machine(db)
versionsDB = Versions.Versions(db)
tooldb = Tool.Tool(db)
accountDB = Accounts.Accounts()
distributionMachinetDB = DistributionMachine.DistributionMachine(db)


# classes


@clonerequestAPI.route('/clonerequest/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/CloneRequestAPI/getAllCloneRequests.yml')
def getAllCloneRequests():
    
    data = []
    clonerequest_data = cloneRequestDB.GetCloneRequestAll()
    if clonerequest_data is None:
        raise Exception("No clone request was found")
    for rec in clonerequest_data:
        if "logs" in rec.keys():
            rec.pop("logs")
        if rec.get("machine_id") is not None:
            machine = machineDB.GetMachine(rec["machine_id"])
            if machine :
                rec["machine_name"] = machine.get("machine_name")
        data.append(rec)
    return jsonify(json.loads(dumps({"result": "success", "data": data}))), 200


@clonerequestAPI.route('/clonerequest/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/CloneRequestAPI/getCloneRequestByID.yml')
def getCloneRequestByID(id):
    clone_request = cloneRequestDB.GetCloneRequest(id)
    if clone_request.get("machine_id"):
        machine = machineDB.GetMachine(clone_request.get("machine_id"))
        if machine:
            clone_request["machine_name"] = machine.get("machine_name","")
    return jsonify(json.loads(dumps({"result": "success", "data": clone_request}))), 200


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError("Type not serializable")


@clonerequestAPI.route('/clonerequest/add', methods=['POST'])
@authService.authorized
@swag_from(relative_path + '/swgger/CloneRequestAPI/addCloneRequest.yml')
def addCloneRequest():
    data = request.json
    validate(data, 'Clone', relative_path +
             '/swgger/CloneRequestAPI/addCloneRequest.yml')
    NewCloneRequest = request.get_json()
    if NewCloneRequest.get("machine_id") is None:
        raise Exception("machine_id was not found in request")
    if machineDB.GetMachine(NewCloneRequest["machine_id"]) is None:
        raise Exception("Machine was not found")
    result = cloneRequestDB.GetCloneRequestsByMachineId(
        NewCloneRequest["machine_id"])
    if result.count() > 0:
        raise Exception("Request already exists for this machine")

    if NewCloneRequest.get("tool_list") and len(NewCloneRequest.get("tool_list")) > 0:
        # GET ORDER IN WHICH TOOLS SHOULD BE CLONED
        tool_list = []
        tool_names = []
        for req in NewCloneRequest.get("tool_list"):
            version_details = versionsDB.get_version(
                req.get("version_id"), False)
            version_details["source_version_id"] = req.get("version_id")
            process_order, toolNames = ToolHelperService.get_ordered_tools(
                [version_details])
            req["clone_order"] = process_order
            tool_names = list(set(tool_names + toolNames))
            tool_list.append(req)
        NewCloneRequest["tool_list"] = tool_list

        # GET TOOL NAMES TO BE CLONED
        tool_list = []
        for req in NewCloneRequest.get("tool_list"):
            tool_name = tooldb.get_tool_by_version(
                req.get("version_id"), False)["name"]
            if tool_name in tool_names:
                tool_names.remove(tool_name)
            req["tool_name"] = tool_name
            tool_list.append(req)
        NewCloneRequest["tool_list"] = tool_list

        # IF size of tool_names >0 . Then we are missing tools to clone
        if len(tool_names) > 0:
            raise ValueError(
                "Please add missing dependent tools: " + ",".join(tool_names))

        # SET THEM UP IN ORDER
        NewCloneRequest.get("tool_list").sort(
            key=cloneRequestDB.clone_order, reverse=False)

    Clone_request_id = cloneRequestDB.AddCloneRequest(NewCloneRequest)
    return jsonify(json.loads(dumps({"result": "success", "message": "New clone request has been added successfully", "data": {"id": Clone_request_id}}))), 200

@clonerequestAPI.route('/clonerequest/retry', methods=['PUT'])
@authService.authorized
@swag_from(relative_path + '/swgger/CloneRequestAPI/retryCloneRequest.yml')
def retryCloneRequest():
    data = request.json
    validate(data, 'Retry', relative_path +
             '/swgger/CloneRequestAPI/retryCloneRequest.yml')

    clone_request = request.get_json()
    oid = clone_request.get("_id").get("oid")
    data = cloneRequestDB.GetCloneRequest(oid)
    if data is None:
        raise Exception("Request was not found")
    if data.get('status').lower() != 'failed':
        raise Exception("Only failed request can be retried")
    if len(data.get("tool_list")) > 0:
        for version in data.get("tool_list"):
            if (version.get("status") == 'Failed'):
                cloneRequestDB.updateToolList(
                    oid, version.get("version_id"), status='Retry')
    cloneRequestDB.UpdateStepDetails(oid, str(data.get(
        "current_step_id")), step_status='Retry', step_message='Marked for retry')
    retryCount = data.get("retry_count")
    if retryCount is None:
        retryCount = "1"
    else:
        retryCount = str(int(retryCount) + 1)
    data = {}
    data["_id"] = clone_request["_id"]
    data["retry_count"] = retryCount
    data["status"] = "Retry"
    data['status_message'] = 'Marked for retry'
    updated = cloneRequestDB.UpdateCloneRequest(data)
    return jsonify(json.loads(dumps({"result": "success", "message": "The request was updated successfully", "data": updated}))), 200