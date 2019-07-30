# AccountDPM Distribution Sync API's - Which will call Master DPM
# distribution Center APIs
'''
Created on Aug 6, 2016
from pip._vendor.requests.exceptions import ConnectionError

@author: sjajula
'''

import json
import traceback
import re

from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request
import requests
from requests.exceptions import ConnectionError, ReadTimeout

from DBUtil import CloneRequest, Machine, DistributionSync, SystemDetails, Config
from Services.AppInitServices import authService
from settings import mongodb, relative_path, dpm_url_prefix


# from Cython.Runtime.refnanny import result
# blueprint declaration
distributionSyncAPI = Blueprint('distributionSyncAPI', __name__)

# get global db connection
db = mongodb


# collections
cloneRequestDB = CloneRequest.CloneRequest(db)
machineDB = Machine.Machine(db)
distributionsyncDB = DistributionSync.DistributionSync(db)
sysdetailsDB = SystemDetails.SystemDetails(db)
configDb = Config.Config(db)
# classes


@distributionSyncAPI.route('/clonerequest/distribution/view/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DistributionSyncAPI/getdistributionsync.yml')
def getdistributionsync():
    
    distributionsync = {}
    impTool = []
    updTool = []
    newTools = distributionsyncDB.getDistributionByImpOperation()
    for newTool in newTools:
        versions_arr = []
        versions = newTool["tool_data"].pop("versions")
        for ver in versions:
            version_data = {}
            version_data["version_name"] = ver["version_name"]
            version_data["version_id"] = ver["source_version_id"]
            versions_arr.append(version_data)
        id = newTool["_id"]
        master_clone_request_id = newTool.get("master_clone_request_id")
        newTool = newTool["tool_data"]
        newTool["_id"] = id
        newTool["versions"] = versions_arr
        if master_clone_request_id:
            newTool["master_clone_request_id"] = master_clone_request_id
        impTool.append(newTool)
    updateTools = distributionsyncDB.getDistributionByUpdOperation()
    for updateTool in updateTools:
        versions_arr = []
        versions = updateTool["tool_data"].pop("versions")
        for ver in versions:
            version_data = {}
            version_data["version_name"] = ver["version_name"]
            version_data["version_id"] = ver["source_version_id"]
            versions_arr.append(version_data)
        id = updateTool["_id"]
        master_clone_request_id = updateTool.get("master_clone_request_id")
        updateTool = updateTool["tool_data"]
        updateTool["_id"] = id
        updateTool["versions"] = versions_arr
        if master_clone_request_id:
            updateTool["master_clone_request_id"] = master_clone_request_id
        updTool.append(updateTool)
    distributionsync["ImportTool"] = impTool
    distributionsync["UpdateTool"] = updTool
    return jsonify(json.loads(dumps({"result": "success", "data": distributionsync}))), 200


@distributionSyncAPI.route('/clonerequest/distribution/view/tool/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DistributionSyncAPI/getdistributionsyncId.yml')
def getdistributionsyncId(id):
    tool = distributionsyncDB.getDistributionIdByOperation(id)
    if not tool:
        raise Exception( "Tool with _id :" + id + " not found")
    tool["tool_data"]["_id"] = tool["_id"]
    master_clone_request_id = tool.get("master_clone_request_id")
    tool = tool["tool_data"]
    if master_clone_request_id:
        tool["master_clone_request_id"] = master_clone_request_id
    tool["all_versions"] = tool.pop("versions")
    tool["version"] = tool.get("all_versions")[0]
    return jsonify(json.loads(dumps({"result": "success", "data": tool}))), 200

# calls Master DPM API - /clonerequest/distribute/add internally
@distributionSyncAPI.route('/clonerequest/distribution/tool', methods=['POST'])
@authService.authorized
def AddorUpdateTooldistributionsync():
    '''
    Format:
    {
        "type":"importtool" /updatetool,"
        "ids":["sfdfdsfdfdsf","sfdfdsfdfdsfds"]
    }
    '''

    try:
        inputRequest = request.get_json()
        inputRequest["tool_list"] = []
        if inputRequest.get("type") not in ["importtool", "updatetool"]:
            raise ValueError("Valid type was not found in input request")
        ids = inputRequest.get("ids")
        if ids:
            inputRequest.pop("ids")
            for rec in ids:
                found = distributionsyncDB.getDistributionIdByOperation(rec)
                if not found:
                    raise Exception( "No such distribution Sync record exists with _id" + rec)
                inputRequest["tool_list"].append(
                    {"status": "requested", "version_id": found["tool_data"]["versions"][0]["source_version_id"]})
        else:
            raise ValueError("List ids were not found in input request")
        # GET IP/ACCOUNT_NAME/MASTER_HOST/MASTER_PORT
        system_details = sysdetailsDB.get_system_details_single()
        if not system_details:
            raise Exception( "System Details not found")
        if not system_details.get("ip"):
            raise Exception( "ip not found in System Details")
        if not system_details.get("master_host"):
            raise Exception("master_host was not found in System Details")
        if not system_details.get("master_port"):
            raise Exception("source_port was not found in System Details")
        inputRequest["ip"] = sysdetailsDB.get_system_details_single().get("ip")
        inputRequest["account_name"] = sysdetailsDB.get_system_details_single().get(
            "account_name")
        # CREATE REQUEST and SUBMIT
        url = dpm_url_prefix + system_details.get("master_host") + ':' + \
            str(system_details.get("master_port")) + \
            '/clonerequest/distribute/add'
        # need to add a secret key for below header
        headers = {'Content-Type': 'application/json'}
        print "Trying to call :" + url
        response = requests.post(url, data=json.dumps(
            inputRequest), headers=headers, timeout=60, verify=False)
        if response.status_code != 200:
            data = json.loads(response._content)
            if data.get("message"):
                raise Exception( "Response from master DPM :" + data.get("message"))
            else:
                raise Exception( "Response from master DPM" + str(response.status_code) + ' ' + response.reason + '. ' + str(response._content).translate(None, '{"}'))
        response = json.loads(response._content)
        for rec in ids:
            data = {"_id": {"oid": rec}}
            data["master_clone_request_id"] = str(response["id"])
            data["status_message"] = "Clone request was accepted by master"
            data["master_clone_request_status"] = "new"
            distributionsyncDB.UpdateDistribution(data)
        return jsonify(json.loads(dumps({"result": "success", "message": "Request is successfully added", "data": "Request is successfully added: " + str(response["id"])}))), 200

    except Exception as e:  # catch *all* exceptions
        if type(e) in [ConnectionError, ReadTimeout]:
            raise Exception("Unable to connect master")
        raise e

# To call master DPM clone request status - and shows the status


@distributionSyncAPI.route('/clonerequest/distribution/tool/status/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DistributionSyncAPI/AddorUpdateToolstatus.yml')
def AddorUpdateToolstatus(id):
    try:
        found = distributionsyncDB.GetDistributeRequest(id)
        if not found:
            raise Exception("No such request exists")
        if not found.get("master_clone_request_id"):
            raise Exception("master_clone_request_id does not exists in request")
        system_details = sysdetailsDB.get_system_details_single()
        if not system_details:
            raise Exception( "System Details not found")
        if not system_details.get("master_host"):
            raise Exception("master_host was not found in System Details")
        if not system_details.get("master_port"):
            raise Exception("source_port was not found in System Details")
        url = dpm_url_prefix + system_details.get("master_host") + ':' + str(system_details.get("master_port")) \
            + '/clonerequest/distribute/status/' + \
            str(found.get("master_clone_request_id"))
        # need to add a secret key for below header
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers, timeout=60, verify=False)
        if response.status_code != 200:
            data = json.loads(response._content)
            if data.get("message"):
                raise Exception( "Response from master DPM :" + data.get("message"))
            else:
                raise Exception( "Response from master DPM" + str(response.status_code) + ' ' + response.reason + '. ' + str(response._content).translate(None, '{"}'))
        data = json.loads(response._content)
        if not data.get("data").get("status"):
            raise Exception( "Status not found in response from master")
        found["master_clone_request_status"] = data.get("data").get("status")
        return jsonify(json.loads(dumps({"result": "success", "message": "Response from master", "data": found}))), 200
    except Exception as e:  # catch *all* exceptions
        if type(e) in [ConnectionError, ReadTimeout]:
            raise Exception("Unable to connect master")
        raise e

# This Account DPM API is called by Master DPM - from the last step of
# Import Tool(update_distribution_sync_data_in_account_dpm) to update the
# distribution status on account when completed

#Swagger not requiered as intenally called for clone. Never exposed to user
@distributionSyncAPI.route('/clonerequest/distribute/update/status', methods=['POST'])
# @authService.authorized
def UpdateDistributionSyncStatus():
    data = request.get_json()
    found = distributionsyncDB.get_distribution_by_filter({"tool_data.name": re.compile(
        data.get("tool_name"), re.IGNORECASE), "status": re.compile("compared", re.IGNORECASE)})
    if not found:
        raise Exception( "No such tool exists , Already completed if you are re requesting")
    for rec in found:
        distributionsyncDB.UpdateDistributionStatus(
            str(rec["_id"]), "completed", "Tool is handled successfully")
    return jsonify(json.loads(dumps({"result": "success", "message": "Status updated "}))), 200
