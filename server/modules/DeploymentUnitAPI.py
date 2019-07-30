import os
import re
import traceback
import json

from bson.json_util import dumps
from flasgger import swag_from, ValidationError
from flask import Blueprint, jsonify, request
from jsondiff import diff
from werkzeug import secure_filename

from DBUtil import DeploymentUnit, Tags, Build, DeploymentUnitApprovalStatus, \
DeploymentUnitSet, DeploymentFields, ToolsOnMachine, DeploymentRequest,State,DeploymentUnitType
from Services import FileUtils, HelperServices, TeamService,DuHelperService
from Services.AppInitServices import authService
from settings import mongodb, relative_path, logo_path, logo_full_path
from flask_restplus import Resource
from modules.apimodels import DeploymentUnitModel
from modules.apimodels.Restplus import api,header_parser
from modules.apimodels.GenericReponseModel import generic_post_response_model


# blueprint declaration
deploymentUnitAPI = Blueprint('deploymentUnitAPI', __name__)
#restplus delaration
deploymentUnitAPINs = api.namespace('deploymentunit', description='Deployment Unit Operations')

# get global db connection
db = mongodb
deploymentUnitDB = DeploymentUnit.DeploymentUnit()
tagDB = Tags.Tags()
buildDB = Build.Build()
deploymentUnitApprovalStatusDB = DeploymentUnitApprovalStatus.DeploymentUnitApprovalStatus()
deploymentUnitSetDB = DeploymentUnitSet.DeploymentUnitSet()
deploymentFieldsDB = DeploymentFields.DeploymentFields(db)
teamService = TeamService.TeamService()
toolsonmachinedb = ToolsOnMachine.ToolsOnMachine(db)
deploymentRequestDB = DeploymentRequest.DeploymentRequest(db)
stateDB = State.State(db)
deploymentUnitTypeDB = DeploymentUnitType.DeploymentUnitType()

@deploymentUnitAPI.route('/deploymentunit/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitAPI/getAllDeploymentUnits.yml')
def getAllDeploymentUnits():
    
    id_list = teamService.get_user_permissions(authService.get_userid_by_auth_token())[
        "parent_entity_id_list"]  # TOOL SET IDS
    # total_count=len(id_list)
    status_filter = request.args.get('status', None)
    tags_filter = []
    duSet_filter = []
    duName_filter = []
    approval_status_filter = []
    deployment_unit_type_filter = []
    total_count_of_du_in_page=0
    limit = int(request.args.get('perpage', "30"))
    page = int(request.args.get('page', "0"))
    skip = page * limit
    if request.args.get('tags', None):tags_filter = request.args.get('tags').split(",")
    if request.args.get('duset', None):duSet_filter = request.args.get('duset', None).split(",")
    if not status_filter: status_filter = ['1']
    elif not status_filter or "any" in status_filter:status_filter = None
    else:status_filter = status_filter.split(",")
    if request.args.get('type', None):deployment_unit_type_filter = request.args.get('type', None)
    if not deployment_unit_type_filter or "any" in deployment_unit_type_filter:deployment_unit_type_filter = None
    else:deployment_unit_type_filter = deployment_unit_type_filter.split(",")
    if request.args.get('approval_status', None):approval_status_filter = request.args.get('approval_status', None).split(",")           
    if request.args.get('duname', None):duName_filter = request.args.get('duname', None)
    if duName_filter:
        deploymentUnits = deploymentUnitDB.GetAllDeploymentUnits(status_filter,deployment_unit_type_filter,False, {
                            "$and": [{"_id": {"$in": id_list}}, {"name": re.compile(duName_filter, re.IGNORECASE)}]}, 0, 0, True)
    else:
        deploymentUnits = deploymentUnitDB.GetAllDeploymentUnits(status_filter,deployment_unit_type_filter,False,
                            {"_id": {"$in": id_list}}, skip, limit, True)
    total_count_of_du_in_db = len(list(deploymentUnitDB.GetAllDeploymentUnits(
        status_filter,None,False, {"_id": {"$in": id_list}})))

    ###########GROUP by DeploymentUnitType#############################
    duJsonObj = {}
    du_list = []

    for du in deploymentUnits:
        #FILTER BY TAGS
        if(HelperServices.filter_handler(du, tags_filter,du.get("tag",[]),"tag")):
            continue    
        #Filter by state approval status
        if approval_status_filter:
            approval_sts_of_states=[]
            for state in stateDB.get_state_by_parent_entity_id(str(du["_id"]), True):
                if state.get("approval_status"):
                    approval_sts_of_states.append(state.get("approval_status"))
            if(HelperServices.filter_handler({"approval_status":True},\
                                                              approval_status_filter,approval_sts_of_states,"approval_status")):
                continue    
        if duSet_filter:    
            included_in_du_set_names = []
            for duSetdata in deploymentUnitSetDB.GetDeploymentUnitSetByCondition("du_set.du_id", du["_id"]):
                if duSetdata.get("_id") or duSetdata("name") is not None:
                    included_in_du_set_names.append(str(duSetdata.get("name")))
            if "any" not in duSet_filter:
                if duSet_filter and len(duSet_filter) > 0 and len(list(set(duSet_filter) & set(included_in_du_set_names))) < 1:
                    continue
        # Latest BUILD NUMBER and BUILD TYPE
        latest_build_details=buildDB.get_last_active_build(str(du["_id"]))
        if latest_build_details:
            du["build_number"] = latest_build_details.get(
                    "build_number")
            du["build_id"] = str(latest_build_details.get(
                    "_id"))
        # ADD GROUPS HERE
        if du.get("type") in duJsonObj.keys():
            duJsonObj[du.get("type")].append(du)
        else:
            duJsonObj[du.get("type")] = []
            duJsonObj[du.get("type")].append(du)
        total_count_of_du_in_page+=1   
    for keytype in duJsonObj.keys():
        dutype = {}
        dutype["type"] = keytype
        dutype["data"] = duJsonObj.get(keytype)
        du_list.append(dutype)                
    return jsonify(json.loads(dumps({"result": "success", "data":\
                                      {"data": du_list, "page": page, "total": total_count_of_du_in_db, "page_total": total_count_of_du_in_page}}))), 200



@deploymentUnitAPI.route('/deploymentunit/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitAPI/getDeploymentUnitbyID.yml')
def getDeploymentUnitbyID(id):
    deploymentUnits = deploymentUnitDB.GetDeploymentUnitById(id, True)
    return jsonify(json.loads(dumps({"result": "success", "data": deploymentUnits}))), 200


@deploymentUnitAPI.route('/deploymentunit/view/<string:parent_entity_id>/machine/<string:machine_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitAPI/getDeploymentUnitbyMachineId.yml')
def getDeploymentUnitbyMachineId(parent_entity_id, machine_id):
    deploymentUnit = deploymentUnitDB.GetDeploymentUnitById(
        parent_entity_id, False)
    if not deploymentUnit:
        raise Exception("No tool is found")
    du_on_machine_data = toolsonmachinedb.get_tools_on_machine_by_machine_id_and_parent_entity_id(
        machine_id, parent_entity_id)
    if du_on_machine_data and len(du_on_machine_data) > 0 and du_on_machine_data.get("deployment_request_id"):
        deployement_req = deploymentRequestDB.GetDeploymentRequest(
            du_on_machine_data.get("deployment_request_id"))
        if deployement_req and len(deployement_req) > 0 and deployement_req.get("tool_deployment_value"):
            previous_deployment_value = deployement_req.get(
                "tool_deployment_value")
            if previous_deployment_value and len(previous_deployment_value) > 0:
                du_deployement_field = deploymentFieldsDB.GetDeploymentFields(
                    parent_entity_id)
                deploymentUnit["deployment_field"] = du_deployement_field
                new_deployment_field = []
                for rec in du_deployement_field.get("fields"):
                    if"input_name" in rec.keys():
                        for rec_prev in previous_deployment_value:
                            if "input_name" in rec_prev.keys() and rec.get("input_name") == rec_prev.get("input_name"):
                                rec["prev_input_value"] = rec_prev["input_value"]
                                new_deployment_field.append(rec)
                deploymentUnit["deployment_field"]["fields"] = new_deployment_field

    return jsonify(json.loads(dumps({"result": "success", "data": deploymentUnit}))), 200


@deploymentUnitAPI.route('/deploymentunit/search/name/<string:name>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitAPI/getDeploymentUnitbyName.yml')
def getDeploymentUnitbyName(name):
    get_details = request.headers.get("details","true") == "true"
    deploymentUnits = deploymentUnitDB.GetDeploymentUnitByName(name, get_details)
    return jsonify(json.loads(dumps({"result": "success", "data": deploymentUnits}))), 200


@deploymentUnitAPI.route('/deploymentunit/search/tag/<string:tag>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitAPI/getDeploymentUnitbyTag.yml')
def getDeploymentUnitbyTag(tag):
    show_all_details = str(request.args.get('showDetails', 'false')).lower()
    if show_all_details.lower() == "true":
        deploymentUnits = deploymentUnitDB.GetDeploymentUnitByTag(tag, True)
    else:    
        deploymentUnits = deploymentUnitDB.GetDeploymentUnitByTag(tag, False)
    return jsonify(json.loads(dumps({"result": "success", "data": deploymentUnits}))), 200


@deploymentUnitAPINs.route('/new', methods=['POST'])
class DeploymentUnitAdd(Resource):
    @api.expect(header_parser,DeploymentUnitModel.du_input_model,validate=True)
    @api.marshal_with(generic_post_response_model)
    @authService.authorized
    def post(self):
        deploymentUnitData = request.get_json()
        if deploymentUnitDB.GetDeploymentUnitByName(deploymentUnitData.get("name")) is not None:
            raise Exception("DeploymentUnit with name " + deploymentUnitData.get("name") + " already exists")
        du_id = DuHelperService.add_update_du(
            deploymentUnitData, None, logo_path, None, logo_full_path)
        return {"result": "success", "message": "DeploymentUnit was created successfully", "data": {"_id": du_id }}, 200


@deploymentUnitAPINs.route('/update', methods=['PUT'])
class DeploymentUnitUpdate(Resource):
    @api.expect(header_parser,DeploymentUnitModel.du_update_input_model, validate=True)
    @api.marshal_with(generic_post_response_model)
    @authService.authorized
    def put(self):
        deploymentUnitData = request.get_json()
        if deploymentUnitData.get("_id"):
            if type(deploymentUnitData.get("_id")) is not dict:
                raise Exception("The type of _id is invalid")
            if not deploymentUnitData.get("_id").get("oid"):
                raise Exception("oid was not found in _id")
        else:
            raise Exception("_id was not found in input request ")
        DuHelperService.add_update_du(
            deploymentUnitData, deploymentUnitData["_id"]["oid"], logo_path, None, logo_full_path)
        return {"result": "success", "message": "The deploymentUnit is updated successfully", "data": {"_id": str(deploymentUnitData.get("_id").get("oid"))}}, 200
        

@deploymentUnitAPI.route('/deploymentunit/delete/<string:id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitAPI/deleteDeploymentUnit.yml')
def deleteDeploymentUnit(id):
    result=DuHelperService.delete_du(id)
    if result.get("result") == "failed":
        raise Exception(result)
    else:
        return jsonify(result), 200


@deploymentUnitAPI.route('/deploymentunit/upload/logo', methods=['POST'])
@authService.authorized
def uploadLogoFile():
    # This is the path to the upload directory
    du_name = ""
    # These are the extension that we are accepting to be uploaded
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']

    re.compile("active", re.IGNORECASE)
# Get the name of the uploaded file
    file = request.files.get('logo')
    du_id = request.form.get('du_id')
    if du_id is None:
        raise Exception("du_id not found in request")
    if deploymentUnitDB.GetDeploymentUnitById(du_id, False) is None:
        raise Exception("No such Deployment Unit exists")
    filename = None
    if file is not None:
        filename = ('.' in file.filename and
                    str(file.filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS)
    else:
        raise Exception("File not found in request.")
    if filename not in [True]:
        raise Exception("Invalid file .Please select file 'png', 'jpg', 'jpeg', 'gif'")

# Check if the file is one of the allowed types/extensions
    if file and filename:
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        file_extension = filename.split(".")[-1]
        result1 = deploymentUnitDB.GetDeploymentUnitById(du_id, False)
        du_name = '_'.join(result1["name"].split())
        file_path = str(logo_full_path + '/' + du_name +
                        '_' + du_id + '.' + file_extension)
        thumbnail_file_path = (str(
            logo_full_path + '/' + du_name + '_' + du_id + '_thumbnail.' + file_extension))
        current_logo_file = str(
            logo_path + '/' + du_name + '_' + du_id + '.' + file_extension)
        current_thumbnail_file = str(
            logo_path + '/' + du_name + '_' + du_id + '_thumbnail.' + file_extension)
        db_logo_file = result1.get("logo")
        # db_thumbnail_file=result1.get("thumbnail_logo")
        file.save(file_path)
        if not os.path.isfile(file_path):
            raise Exception("Failed to save logo to path :" + file_path)
        if FileUtils.thumbnail(file_path, thumbnail_file_path) is None:
            current_thumbnail_file = current_logo_file
        if not os.path.isfile(thumbnail_file_path):
            current_thumbnail_file = current_logo_file

        if db_logo_file is None:
            #                 updated=tooldb.add_tool_logo(current_logo_file,current_thumbnail_file,du_id)
            updated = deploymentUnitDB.add_du_logo(
                current_logo_file, current_thumbnail_file, du_id)
        else:
            sub = diff(db_logo_file, current_logo_file)
            if sub:
                print "DuAPI:compare: logo " + db_logo_file + " is required to be updated as the logo data has changed."
                # updated=tooldb.add_tool_logo(current_logo_file,current_thumbnail_file,du_id)
                updated = deploymentUnitDB.add_du_logo(
                    current_logo_file, current_thumbnail_file, du_id)
        return jsonify(json.loads(dumps({"result": "success", "message": "File and Deployment Unit was updated successfully and is readable"}))), 200
        


@deploymentUnitAPINs.route('/bulk/load', methods=['POST'])
class DeploymentUnitBulkLoad(Resource):
    @api.expect(header_parser,DeploymentUnitModel.du_bulk_input_model,validate=True)
    @api.marshal_with(DeploymentUnitModel.du_bulk_response_model)
    @authService.authorized
    def post(self):
        """
        Creates or updates requested DUs.
        """
        bulk_du_response = []
        du_details = request.get_json()
        if type(du_details.get("data")) is list and len(du_details.get("data")) > 0:
            for du in du_details.get("data"):
                rec = {"_id":"","name": du.get("name"), "result":"success", "message":"DU was created"}
                try:
                    keys_to_validate = ["name"]
                    for key in keys_to_validate:
                        if not du.get(key): raise Exception ("mandatory key: "+ key+" is missing in du details")
                    if du.get("_id"):
                        if type(du.get("_id")) is not dict:
                            raise Exception ("invalid type was found for key: _id")
                        if not du.get("_id").get("oid"):
                            raise Exception ("oid was not found in _id")
                        rec["_id"] = du["_id"]["oid"]
                        result = DuHelperService.add_update_du(du, str(rec["_id"]), logo_path, None, logo_full_path)                             
                        if result == "1":
                                rec["message"] = "DU was updated"
                        else:
                            rec["message"] = "no changes found"
                    elif deploymentUnitDB.GetDeploymentUnitByName(du.get("name")) :
                        existing_du = deploymentUnitDB.GetDeploymentUnitByName(du.get("name"))
                        rec["_id"] = str(existing_du.get("_id"))
                        result = DuHelperService.add_update_du(du, str(rec["_id"]), logo_path, None, logo_full_path)
                        if result == "1":
                                rec["message"] = "DU was updated"
                        else:
                            rec["message"] = "no changes found"
                    else:
                        rec["_id"] = DuHelperService.add_update_du(du, None, logo_path, None, logo_full_path)
                except Exception as e:  # catch *all* exceptions
                    rec["result"]="failed"
                    rec["message"]=str(e)
                    traceback.print_exc()
                bulk_du_response.append(rec)          
        else:
            raise Exception("expected input type is list with atleast one record") 
        return {"result": "success", "message": "DU's has been processed for uploading","data":bulk_du_response}, 200