from datetime import datetime
from time import mktime
import json
from bson.json_util import dumps
from flasgger import swag_from, validate
from flask import Blueprint, jsonify, request
from DBUtil import Config
from Services import MailerService, DeploymentRequestService, CloneRequestService, SyncServices, PushServices, PullServices, DistributionCenterService, DistributionSyncServices, ContributionGitPushService, CleanerServices
from Services.AppInitServices import authService
from settings import mongodb, relative_path
from flask_restplus import Resource
from modules.apimodels.Restplus import api, header_parser
from modules.apimodels import ConfigModel


# blueprint declaration
configAPI = Blueprint('configAPI', __name__)
configAPINs = api.namespace('config', description='Config Operations')



# get global db connection
db = mongodb

# collection
configdb = Config.Config(db)

mailerConfig = configdb.getConfigByName("MailerService")
deploymentConfig = configdb.getConfigByName("DeploymentRequestService")
cloneConfig = configdb.getConfigByName("CloneRequestService")
syncConfig = configdb.getConfigByName("SyncServices")
pullConfig = configdb.getConfigByName("PullServices")
pushConfig = configdb.getConfigByName("PushServices")
distributionCenterConfig = configdb.getConfigByName("PushServices")
distributionSyncConfig = configdb.getConfigByName("DistributionSyncServices")
contributionGitPushSyncConfig = configdb.getConfigByName("ContributionCenterService")
cleanerServicesConfig = configdb.getConfigByName("CleanerServices")

# SERVICES
if mailerConfig:
    mailerService = MailerService.MailerService()
if deploymentConfig:
    deploymentRequestService = DeploymentRequestService.DeploymentRequestService(
        db)
if cloneConfig:
    cloneRequestService = CloneRequestService.CloneRequestService(db)
if syncConfig:
    syncServices = SyncServices.SyncServices()
if pullConfig:
    pullServices = PullServices.PullServices()
if pushConfig:
    pushServices = PushServices.PushServices()
if distributionCenterConfig:
    distributionCenterService = DistributionCenterService.DistributionCenterService(
        db)
if distributionSyncConfig:
    distributionSyncServices = DistributionSyncServices.DistributionSyncServices()
if contributionGitPushSyncConfig:
    contributionGitPushService = ContributionGitPushService.ContributionGitPushService(
        db)
if cleanerServicesConfig:
    cleanerServices = CleanerServices.CleanerServices(db)


@configAPI.route('/config/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ConfigAPI/getAllConfig.yml')
def getAllConfig():
    conf_list = configdb.GetAllConfig()
    for idx, item in enumerate(conf_list):
        if item.get("start_time"):
            item["utc_start_time"] = mktime(
                datetime.utctimetuple(item["start_time"]))
            item["utc_current_time"] = mktime(
                datetime.utctimetuple(datetime.now()))
        conf_list[idx] = item
    return jsonify(json.loads(dumps({"result": "success", "data": conf_list}))), 200
    

@configAPI.route('/config/sync/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ConfigAPI/getAllSyncConfig.yml')
def getAllSyncConfig():
    configs = []
    conf_list = configdb.GetAllConfig()
    for rec in conf_list:
        if str(rec["configid"]) in ["9", "10", "11"]:
            configs.append(rec)
    return jsonify(json.loads(dumps({"result": "success", "data": configs}))), 200


@configAPI.route('/config/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ConfigAPI/getConfigId.yml')
def getConfigId(id):
    role_list = configdb.get_config_by_id(id)
    return jsonify(json.loads(dumps({"result": "success", "data": role_list}))), 200
    
    
@configAPI.route('/config/view/configid/<string:configid>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ConfigAPI/getConfigByConfigId.yml')
def getConfigByConfigId(configid):
    role_list = configdb.getConfigByConfigId(configid)
    return jsonify(json.loads(dumps({"result": "success", "data": role_list}))), 200

@configAPI.route('/config/distribution/schedule', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ConfigAPI/getDistributionCenterScheduleRequestConfig.yml')
def getDistributionCenterScheduleRequestConfig():
    configs = []
    conf_list = configdb.GetAllConfig()
    for rec in conf_list:
        if str(rec["configid"]) in ["12"]:
            configs.append(rec)
    return jsonify(json.loads(dumps({"result": "success", "data": configs}))), 200


@configAPINs.route('/distribution/schedule/update', methods=['PUT'])
class updateDistributionCenterScheduleRequest(Resource):
    @api.expect(header_parser,ConfigModel.udc_schedule_req_input_model,validate=True)
    @api.marshal_with(ConfigModel.udc_schedule_req_response_model)
    @authService.authorized 
    def put(self):
        data = request.get_json()
        validate = validateConfigData(data)
        if validate is not None:
            return validate
        data = removeExtraData(data)
        data = add_extra_message(data)
        updated = configdb.UpdateConfig(data)
        if updated == 1:
            distributionCenterService.schedule()
            return {"result": "success", "message": "The Config was updated successfully", "data": updated}, 200
        else:
            raise Exception("No difference found")

def add_extra_message(conf_data):
    if conf_data.get("enable"):
        if  str(conf_data.get("enable")).lower() == "true":
            conf_data["run_status"] = "Active"
        elif  str(conf_data.get("enable")).lower() == "false":     
            conf_data["run_status"] = "Suspended"
        conf_data["run_message"] = ""
    
    return conf_data
        
@configAPI.route('/config/update', methods=['PUT'])
@authService.authorized
@swag_from(relative_path + '/swgger/ConfigAPI/updateConfig.yml')
def updateConfig():
    data = request.json
    validate(data, 'Config', relative_path +
             '/swgger/ConfigAPI/updateConfig.yml')
    conf_data = request.get_json()
    validation = validateConfigData(conf_data)
    if validation is not None:
        return validation
    conf_data = removeExtraData(conf_data)
    conf_data = add_extra_message(conf_data)
    updated = configdb.UpdateConfig(conf_data)        
    id = conf_data["_id"]["oid"]
    result = configdb.get_config_by_id(id)
    if str(result["configid"]) == "2":
        mailerService.schedule()
    elif str(result["configid"]) == "3":
        deploymentRequestService.schedule()
    elif str(result["configid"]) == "4":
        cloneRequestService.schedule()
    elif str(result["configid"]) == "9":
        syncServices.schedule()
    elif str(result["configid"]) == "10":
        pullServices.schedule()
    elif str(result["configid"]) == "11":
        pushServices.schedule()
    elif str(result["configid"]) == "12":
        distributionCenterService.schedule()
    elif str(result["configid"]) == "13":
        distributionSyncServices.schedule()
    elif str(result["configid"]) == "14":
        contributionGitPushService.schedule()
    elif str(result["configid"]) == "15":
        cleanerServices.schedule()
    return jsonify(json.loads(dumps({"result": "success", "message": "The Config was updated successfully", "data": updated}))), 200        


def removeExtraData(conf_data):
    for key in conf_data.keys():
        if key in "start_time":
            conf_data.pop("start_time")
        if key in "end_time":
            conf_data.pop("end_time")
        if key in "run_message":
            conf_data.pop("run_message")
        if key in "run_status":
            conf_data.pop("run_status")
    return conf_data


def validateConfigData(conf_data, db_data=None):
    if not db_data:
        db_data = configdb.get_config_by_id(conf_data["_id"]["oid"])
    if db_data.get("enable") is not None and (conf_data.get("enable") is None or conf_data.get("enable").lower() not in ["true", "false"]):
        raise Exception("Invalid enable was found in request")
    if db_data.get("type") is not None and (conf_data.get("type") is None or conf_data.get("type") not in ["interval", "scheduled"]):
        raise Exception("Invalid type was found in request")
    if db_data.get("noOfThreads") is not None and (int(conf_data.get("noOfThreads")) is None or int(conf_data.get("noOfThreads")) <= 0):
        raise Exception("Invalid noOfThreads was found in request")
    if db_data.get("expiration") is not None and (int(conf_data.get("expiration")) is None or int(conf_data.get("expiration")) <= 0):
        raise Exception("Invalid expiration was found in request")
    if db_data.get("remote_dpm_port") is not None and (int(conf_data.get("remote_dpm_port")) is None or int(conf_data.get("remote_dpm_port")) <= 0):
        raise Exception("Invalid remote_dpm_port was found in request")
    if db_data.get("enablelistner") is not None and (conf_data.get("enablelistner") is None or conf_data.get("enablelistner").lower() not in ["true", "false"]):
        raise Exception("Invalid enablelistner was found in request")
    if db_data.get("enablecleaner") is not None and (conf_data.get("enablecleaner") is None or conf_data.get("enablecleaner").lower() not in ["true", "false"]):
        raise Exception("Invalid enablecleaner was found in request")
    if db_data.get("full_sync_flag") is not None and (conf_data.get("full_sync_flag") is None or conf_data.get("full_sync_flag").lower() not in ["true", "false"]):
        raise Exception("Invalid full_sync_flag was found in request")
    if db_data.get("ssl") is not None and (conf_data.get("ssl") is None or conf_data.get("ssl").lower() not in ["true", "false"]):
        raise Exception("Invalid ssl was found in request")
    if db_data.get("tls") is not None and (conf_data.get("tls") is None or conf_data.get("tls").lower() not in ["true", "false"]):
        raise Exception("Invalid tls was found in request")
#     if db_data.get("run_status") is not None and db_data.get("run_status").lower() in ["running"]:
#         raise Exception("The Service is currently running.Please try later")
    if db_data.get("olderthandays") is not None and (int(conf_data.get("olderthandays")) is None):
        raise Exception("Invalid olderthandays was found in request")
    if db_data.get("timeout") is not None and (int(conf_data.get("timeout")) is None or int(conf_data.get("timeout")) <= 0):
        raise Exception("Invalid timeout was found in request")
    if db_data.get("port") is not None and (int(conf_data.get("port")) is None or int(conf_data.get("port")) <= 0):
        raise Exception("Invalid port was found in request")
    if db_data.get("socketport") is not None and (int(conf_data.get("socketport")) is None or int(conf_data.get("socketport")) <= 0):
        raise Exception("Invalid socketport was found in request")
    if db_data.get("hrs") is not None and (int(conf_data.get("hrs")) is None or int(conf_data.get("hrs")) < 0):
        raise Exception("Invalid hrs was found in request")
    if db_data.get("min") is not None and (int(conf_data.get("min")) is None or int(conf_data.get("min")) < 0):
        raise Exception("Invalid min was found in request")
    if db_data.get("intervalGiven") is not None and (float(conf_data.get("intervalGiven")) is None or float(conf_data.get("intervalGiven")) <= float(0)):
        raise Exception("Invalid intervalGiven was found in request")
    if conf_data.get("upload_protocol") and conf_data.get("upload_protocol").lower() in ["filesystem"] and not conf_data.get("repo_path"):
        raise Exception("For upload protocol 'filesystem', 'repo_path' is mandatory ")
    return None
