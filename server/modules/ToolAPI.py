import json
import os
import re
import traceback
from flasgger import swag_from, validate, ValidationError
from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from jsondiff import diff
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from werkzeug import secure_filename

from DBUtil import Tool, Versions, DeploymentFields, MediaFiles, Documents, Users, SystemDetails, Tags, ToolsOnMachine, DeploymentRequest, ToolSet, Machine,Build
from Services import FileUtils, HelperServices, ToolHelperService
from Services import TeamService
from Services.AppInitServices import authService
from settings import dpm_url_prefix
from settings import mongodb, logo_path, logo_full_path, media_path, media_full_path,relative_path
from flask_restplus import Resource
from modules.apimodels import ToolModel
from modules.apimodels.Restplus import api,header_parser
from modules.apimodels.GenericReponseModel import generic_post_response_model
from flask_cors.decorator import cross_origin


# blueprint declaration
toolAPI = Blueprint('toolAPI', __name__)
#restplus delaration
toolAPINs = api.namespace('tool', description='Tool Operations')



# get global db connection
db = mongodb

# collection
tooldb = Tool.Tool(db)
toolsetdb = ToolSet.ToolSet(db)
versionsDB = Versions.Versions(db)
deploymentFieldsDB = DeploymentFields.DeploymentFields(db)
mediaFilesDB = MediaFiles.MediaFiles(db)
machineDB = Machine.Machine(db)
documentsDB = Documents.Documents(db)
toolsonmachinedb = ToolsOnMachine.ToolsOnMachine(db)
deploymentRequestDB = DeploymentRequest.DeploymentRequest(db)
userdb = Users.Users(db)
systemDetailsDb = SystemDetails.SystemDetails(db)
tagDB = Tags.Tags()
teamService = TeamService.TeamService()
buildDB = Build.Build()


@toolAPI.route('/tool/all/', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ToolAPI/getAllTools.yml')
def getAllTools():  # NO NEED TO PASS DEPENDEDT TOOLS HERE
    
    id_list = teamService.get_user_permissions(authService.get_userid_by_auth_token())[
        "parent_entity_id_list"]  # TOOL SET IDS
    # total_count=len(id_list)
    tool_list = []
    status_filter = []
    tags_filter = []
    toolSet_filter = []
    toolName_filter = []
    if request.args.get('status', None):
        status_filter = request.args.get('status', None).split(",")
        if "any" in status_filter:
            status_filter = None
    if request.args.get('tags', None):
        tags_filter = request.args.get('tags', None).split(",")
    if request.args.get('toolset', None):
        toolSet_filter = request.args.get('toolset', None).split(",")
    if request.args.get('toolname', None):
        toolName_filter = request.args.get('toolname', None)
    limit = int(request.args.get('perpage', "30"))
    page = int(request.args.get('page', "0"))
    skip = page * limit
    if toolName_filter:
        tools = list(tooldb.get_tools_all(status_filter, {"$and": [{"_id": {"$in": id_list}}, {
                     "name": {"$regex": str(toolName_filter), "$options": "i"}}]}, 0, 0))
    else:
        tools = list(tooldb.get_tools_all(status_filter, {
                     "_id": {"$in": id_list}}, skip, limit))
    total_count_of_tool_in_db = len(list(tooldb.get_tools_all(
        status_filter, {"_id": {"$in": id_list}})))
#         if not tools or len(tools) < 1:
#             raise Exception("No tools were found")
    for record in tools:
        if(HelperServices.filter_handler(record, tags_filter,tagDB.get_tag_names_from_given_ids_list(record.get("tag",[])),"tag")):
            continue
#             if len(toolName_filter) > 0:
#                 if  "any" not in toolName_filter and  not record["name"] in toolName_filter:
#                     continue

        tool_id = record["_id"]
        included_in_tool_set = []
        included_in_tool_set_names = []
        for toolSetdata in toolsetdb.get_tool_set_by_condition("tool_set.tool_id", tool_id):
            included_in_tool_set.append({"toolset_id": str(
                toolSetdata["_id"]), "toolset_name": str(toolSetdata.get("name"))})
            included_in_tool_set_names.append(str(toolSetdata.get("name")))
        if "any" not in toolSet_filter:
            if toolSet_filter and len(toolSet_filter) > 0 and len(list(set(toolSet_filter) & set(included_in_tool_set_names))) < 1:
                continue
        record["included_in"] = included_in_tool_set
        Versions = versionsDB.get_all_tool_versions(str(tool_id), True)
        if not Versions:
            raise Exception("No version was found for tool_id :" + record["name"])
        versionlist = []
        for version in Versions:
            data = {}
            data["version_id"] = str(version["_id"])
            data["version_name"] = version["version_name"]
            data["version_number"] = version["version_number"]
            # Latest BUILD NUMBER and BUILD TYPE
            latest_build_details=buildDB.get_last_active_build(data["version_id"])
            if latest_build_details:
                data["latest_build_number"] = latest_build_details.get(
                    "build_number")
                data["latest_build_id"] = str(latest_build_details.get("_id"))
            versionlist.append(data)
        record["versions"] = versionlist
        tool_list.append(record)
    return jsonify(json.loads(dumps({"result": "success", "data": {"data": tool_list, "page": page, "total": total_count_of_tool_in_db, "page_total": len(tool_list)}}))), 200


@toolAPI.route('/tool/view/<string:tool_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ToolAPI/getToolID.yml')
@cross_origin()
def getToolID(tool_id):
    tool = tooldb.get_tool_by_id(tool_id, True)
    if not tool:
        raise Exception("No such tool was found")
    if not tool.get("version"):
        raise Exception("No version was found for this tool")
    tool["version"] = ToolHelperService.get_dependend_tools(
        tool.get("version"), False)
    tool["all_versions"] = versionsDB.get_tool_with_all_version_name_and_number(
        tool_id, True, False)
    if tool.get("all_versions") and len(tool.get("all_versions")) > 0:
        all_versions = []
        for version in tool["all_versions"]:
            version = ToolHelperService.get_dependend_tools(version, False)
            included_in_tool_set = []
            for toolSetdata in toolsetdb.get_tool_set_by_condition("tool_set.version_id", str(version["_id"])):
                included_in_tool_set.append({"toolset_id": str(
                    toolSetdata["_id"]), "toolset_name": str(toolSetdata.get("name"))})
            version["included_in"] = included_in_tool_set
            deployed_on_machines = []
            for toolsOnMachinesdata in toolsonmachinedb.get_tools_on_machine_by_machine_by_condition("parent_entity_id", str(version["_id"])):
                machine = machine_name = None
                machine = machineDB.GetMachine(
                    str(toolsOnMachinesdata["machine_id"]))
                if machine:
                    machine_name = machine.get("machine_name")
                deployed_on_machines.append({"machine_id": str(
                    toolsOnMachinesdata["machine_id"]), "machine_name": str(machine_name)})
            version["deployed_on"] = deployed_on_machines
            all_versions.append(version)
        tool["all_versions"] = all_versions
    return jsonify(json.loads(dumps({"result": "success", "data": tool}))), 200


@toolAPI.route('/tool/view/version/<string:version_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ToolAPI/getToolByVersion.yml')
def getToolByVersion(version_id):
    tool = tooldb.get_tool_by_version(version_id, False)
    if not tool:
        raise Exception("No tool was found ")
    tool["version"] = versionsDB.get_version(version_id, True)
    if not tool.get("version"):
        raise Exception("No such version was found for this tool")
    tool["version"] = ToolHelperService.get_dependend_tools(
        tool.get("version"), False)
    return jsonify(json.loads(dumps({"result": "success", "data": tool}))), 200

# Fix for Issue 478 by Surendra


@toolAPI.route('/tool/view/version/<string:version_id>/prevversion/<string:prev_version_id>/machine/<string:machine_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ToolAPI/getToolByVersionAndMachine.yml')
# Duplicate Of /tool/view/version/<string:version_id>
def getToolByVersionAndMachine(version_id, prev_version_id, machine_id):
    tool = tooldb.get_tool_by_version(version_id, False)
    if not tool:
        raise Exception("No tool is found")
    tool["version"] = versionsDB.get_version(version_id, True)
    if not tool.get("version"):
        raise Exception("No such version is found")
    tool["version"] = ToolHelperService.get_dependend_tools(
        tool.get("version"), False)
    deployement_req = toolsonmachinedb.get_tools_on_machine_by_machine_id_and_parent_entity_id(
        machine_id, prev_version_id)
    if deployement_req and len(deployement_req) > 0 and deployement_req.get("deployment_request_id"):
        prev_tool_deployment = deploymentRequestDB.GetDeploymentRequest(
            deployement_req.get("deployment_request_id"))
        if prev_tool_deployment and len(prev_tool_deployment) > 0 and prev_tool_deployment.get("tool_deployment_value"):
            prev_tool_deployment_value = prev_tool_deployment.get(
                "tool_deployment_value")
            if prev_tool_deployment_value and len(prev_tool_deployment_value) > 0:
                tool_deployement_field = tool["version"]["deployment_field"]
                # tool_deployement_field=tool_deployement_version["deployment_field"]
                if tool_deployement_field and prev_tool_deployment_value and len(tool_deployement_field) > 0 and len(prev_tool_deployment_value) > 0and tool_deployement_field.get("fields") and len(tool_deployement_field.get("fields")) > 0:
                    new_deployment_field = []
                    for rec in tool_deployement_field.get("fields"):
                        if"input_name" in rec.keys():
                            for rec_prev in prev_tool_deployment_value:
                                if "input_name" in rec_prev.keys() and rec.get("input_name") == rec_prev.get("input_name"):
                                    rec["prev_input_value"] = rec_prev["input_value"]
                                    new_deployment_field.append(rec)

                    tool["version"]["deployment_field"]["fields"] = new_deployment_field
    return jsonify(json.loads(dumps({"result": "success", "data": tool}))), 200


# PLEASE NOTE def checkIfToolExistsInMaster is using this method.Please
# change accordingly
@toolAPI.route('/tool/exists/name/<string:name>', methods=['GET'])
@swag_from(relative_path + '/swgger/ToolAPI/getIfToolExistsByName.yml')
@authService.unauthorized
def getIfToolExistsByName(name):  # OPEN TO ALL.NO NEED TO AUTH
    tool = tooldb.get_tool_by_name(name, True)
    if not tool:
        return jsonify(json.loads(dumps({"result": "success", "message": "false"}))), 200
    if not tool.get("version"):
        raise Exception("No version was found for this tool")
    tool["all_versions"] = versionsDB.get_tool_with_all_version_name_and_number(
        str(tool["_id"]), True, False)
    return jsonify(json.loads(dumps({"result": "success", "message": "true", "data": tool}))), 200


@toolAPI.route('/tool/search/tag/<string:tag>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ToolAPI/getToolByTag.yml')
def getToolByTag(tag):
    tool_list = tooldb.get_tool_by_tag(tag)
    return jsonify(json.loads(dumps({"result": "success", "data": tool_list}))), 200


def checkIfToolExistsInMaster(host, port, tool_name):
    trigger_url = dpm_url_prefix + host + ":" + port + "/tool/exists/name/" + tool_name
    trigger_headers = {'Content-Type': 'application/json'}
    print "Trying to call :" + trigger_url
    response = requests.get(
        trigger_url, headers=trigger_headers, timeout=600, verify=False)
    if response.status_code == 200:
        result = json.loads(response.content)
        message = str(result.get("message"))
        # Tool was not found # WE ARE GOOD TO CONTINUE
        if message.lower() in ["false"]:
            return
        else:
            raise Exception("Tool with name:" + tool_name + " already exists in master")
    else:
        msg = str(response.status_code) + ' ' + response.reason + '. ' + \
            str(response._content).translate(None, '{"}') + '. ' + trigger_url
        raise Exception(str(msg))

########THIS API IS GETTING CALLED FROM proposed/tool/approve ####
########THIS API IS GETTING CALLED FROM clonerequest ####
@toolAPI.route('/tool/add', methods=['POST'])
@authService.authorized
@swag_from(relative_path + '/swgger/ToolAPI/add_tool.yml')
def add_tool():
    Toolresult = None
    DeploymentFieldsresult = None
    MediaFilesresult = None
    DocumentFieldsresult = None
    Versionresult = None
    try:
        data = request.json
        validate(data, 'Tools', relative_path +
                 '/swgger/ToolAPI/add_tool.yml')
        systemDetail = systemDetailsDb.get_system_details_single()
        user_id = authService.get_userid_by_auth_token()
        if user_id is None:
            raise Exception("Token verification failed")
        # WE NEED THIS AS THIS CHECK SHOULD BE DISABLES IN CASE OF CLONE
        if 'verify_tool' not in request.headers:
            verify_tool = 'true'
        else:
            verify_tool = request.headers["verify_tool"]
        tool_creation_source = userdb.get_user_by_id(user_id, False)
        if tool_creation_source is None:
            raise Exception("User found in token")
        if systemDetail.get("dpm_type") in ["dpm_account"]:
            if str(verify_tool).lower() == "true" and not systemDetail.get("master_host") or not systemDetail.get("master_port"):
                raise Exception("System Details master_host,master_port have not been setup properly.Please correct the same")
        tool_creation_source["source_host"] = systemDetail.get("hostname")
        tool_creation_source["source_dpm_type"] = systemDetail.get("dpm_type")
        keys = tool_creation_source.keys()
        for key in keys:
            if key not in  ["account","employeeid","source_host","user","email","source_dpm_type"]:
                tool_creation_source.pop(key)
        ToolData = request.get_json()
        VersionsData = ToolData.get("version")
        if tooldb.get_tool_by_name(ToolData.get("name")):
            raise Exception("Tool with name " + ToolData.get("name") + " already exists")
        
        if (ToolData.get("name") and ToolData.get("description") and ToolData.get("support_details")) is None:
            raise Exception("Mandatory tool fields name , description ,support details to create a new tool was not found.")
        else:
            # CHECK IF TOOL EXISTS IN MASTER
            if str(verify_tool).lower() == "true" and systemDetail.get("dpm_type") in ["dpm_account"]:
                checkIfToolExistsInMaster(systemDetail.get(
                    "master_host"), systemDetail.get("master_port"), ToolData.get("name"))
            if(VersionsData.get("version_number") and VersionsData.get("version_name")) is None:
                raise Exception("Mandatory version fields version_number,version_name to create a new tool was not found.")
            else:
                # preparing tool data
                if not ToolData.get("tool_creation_source"):
                    ToolData["tool_creation_source"] = tool_creation_source
                else:
                    keys = ToolData.get("tool_creation_source").keys();
                    for key in keys:
                        if key not in  ["account","employeeid","source_host","user","email","source_dpm_type"]:
                            ToolData["tool_creation_source"].pop(key) 
                Toolresult = ToolHelperService.add_update_tool(
                    ToolData, None, logo_path, None, logo_full_path)
                # preparing Version data
                Versionresult = ToolHelperService.add_update_version(
                    VersionsData, Toolresult, None, True)
                # preparing DeploymentFields data
                if VersionsData.get("deployment_field") is not None:
                    DocumentFieldsresult = HelperServices.add_update_deployment_fields(
                        VersionsData.get("deployment_field")["fields"], Versionresult)
                # preparing MediaFiles data
                if VersionsData.get("media_file") is not None:
                    MediaFilesresult = HelperServices.add_update_media_files(VersionsData.get(
                        "media_file")["media_files"], Versionresult, None, media_full_path, media_path)
                # preparing Document data
                if VersionsData.get("document") is not None:
                    DocumentFieldsresult = HelperServices.add_update_documents(
                        VersionsData.get("document")["documents"], Versionresult)
                return jsonify(json.loads(dumps({"result": "success", "message": "Tool with it's version and deployment fields created successfully", "data": {"_id": Toolresult,
                                                                                                                                              "version_id": Versionresult}}))), 200
            
    except Exception as e:  # catch *all* exceptions
        if Toolresult is not None:
            tooldb.delete_tool(Toolresult)
        if DeploymentFieldsresult is not None:
            deploymentFieldsDB.DeleteDeploymentFields(DeploymentFieldsresult)
        if MediaFilesresult is not None:
            mediaFilesDB.delete_media_file(MediaFilesresult)
        if DocumentFieldsresult is not None:
            documentsDB.DeleteDocuments(DocumentFieldsresult)
        if Versionresult is not None:
            versionsDB.delete_version(Versionresult)
        if type(e) in [ConnectionError, ReadTimeout]:
            raise Exception("Unable to connect master:" + systemDetail.get("master_host") + ":" + systemDetail.get("master_port"))
        raise e

@toolAPINs.route('/update', methods=['PUT'])
class updateTool(Resource):
    @authService.authorized
    @api.expect(header_parser,ToolModel.update_tool_input_model,validate=True)
    @api.marshal_with(ToolModel.update_tool_response_model)
    def put(self):
        data = request.json
        Toolresult = None
        versions_added = []
        tool_prevdata = None
        # prev_version_data=None
        tool_id = None
        Tool = request.get_json()
        if Tool.get("_id"):
            if Tool.get("_id").get("oid"):
                tool_id = Tool["_id"]["oid"]
            else:
                raise Exception(
                    "Found _id but oid is missing for tool details ")
        else:
            if Tool.get("name"):
                localTool = tooldb.get_tool_by_name(
                    str(Tool.get("name")), False)
                if localTool is not None:
                    tool_id = str(localTool.get("_id"))
        if not tool_id:
            raise Exception("Unable to find tool id ")
        tool_prevdata = tooldb.get_tool_by_id(tool_id, True)
        if tool_prevdata:
            Toolresult = ToolHelperService.add_update_tool(
                Tool, tool_id, logo_path, None, logo_full_path)
            if Toolresult is not None:
                # prev_version_data=versionsDB.get_sync_versions_by_tool_id(tool_id, True)
                versions = None
                if Tool["version"]:
                    versions = Tool["version"]
                if versions is [None, ""]:
                    raise Exception("versions is missing from tool_data")
                for version in versions:
                    version_id = None
                    if version.get("_id"):
                        if version.get("_id").get("oid"):
                            version_id = version["_id"]["oid"]
                        else:
                            raise Exception(
                                "Found _id but oid is missing for version details")
                    else:
                        print "A new version is expected"
                        if version.get("version_name") and version.get("version_number"):
                            localVersion = versionsDB.get_version_by_tool_id_name_and_number(
                                tool_id, version["version_name"], version["version_number"])
                            if localVersion is not None:
                                version_id = str(localVersion.get("_id"))

                    if version_id:
                        # UPDATE THE VERSION
                        ToolHelperService.add_update_version(
                            version, tool_id, version_id, True)
                    else:
                        # ADD NEW VERSION
                        version_id = ToolHelperService.add_update_version(
                            version, tool_id, None, True)
                        versions_added.append(version_id)
                    if version.get("deployment_field"):
                        HelperServices.add_update_deployment_fields(
                            version["deployment_field"]["fields"], version_id)
                    if version.get("document"):
                        HelperServices.add_update_documents(
                            version["document"]["documents"], version_id)
                    # preparing MediaFiles data
                    if version.get("media_file") is not None:
                        HelperServices.add_update_media_files(version.get(
                            "media_file")["media_files"], version_id, None, media_full_path, media_path)
                if Toolresult is not None:
                    return {"result": "success", "message": "Tool was updated successfully", "data": {"version_inserted": versions_added}}, 200
                else:
                    raise Exception("Tool was not updated correctly please check again")
            else:
                raise Exception("Tool was not updated")
        else:
            raise ("No tool found with _id :" + Tool["_id"]["oid"])

@toolAPI.route('/tool/upload/logo', methods=['POST'])
@authService.authorized
def Upload_logoFile():
    # This is the path to the upload directory
    # These are the extension that we are accepting to be uploaded
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']

    re.compile("active", re.IGNORECASE)
# Get the name of the uploaded file
    file = request.files.get('logo')
    tool_id = request.form.get('tool_id')
    if tool_id is None:
        raise Exception("tool_id not found in request")
    if tooldb.get_tool_by_id(tool_id, False) is None:
        raise Exception("No such tool exists")
    filename = None
    if file is not None:
        filename = ('.' in file.filename and
                    str(file.filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS)
    else:
        raise Exception(" File not found in request")
    if filename not in [True]:
        raise Exception("Invalid file .Please select file 'png', 'jpg', 'jpeg', 'gif'")

# Check if the file is one of the allowed types/extensions
    if file and filename:
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        file_extension = filename.split(".")[-1]
        result1 = tooldb.get_tool_by_id(tool_id, False)
        tool_name = '_'.join(result1["name"].split())
        file_path = str(logo_full_path + '/' + tool_name +
                        '_' + tool_id + '.' + file_extension)
        thumbnail_file_path = (str(
            logo_full_path + '/' + tool_name + '_' + tool_id + '_thumbnail.' + file_extension))
        current_logo_file = str(
            logo_path + '/' + tool_name + '_' + tool_id + '.' + file_extension)
        current_thumbnail_file = str(
            logo_path + '/' + tool_name + '_' + tool_id + '_thumbnail.' + file_extension)
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
            #                 updated=tooldb.add_tool_logo(current_logo_file,current_thumbnail_file,tool_id)
            updated = tooldb.add_tool_logo(
                current_logo_file, current_thumbnail_file, tool_id)
        else:
            sub = diff(db_logo_file, current_logo_file)
            if sub:
                print "ToolAPI:compare: logo " + db_logo_file + " is required to be updated as the logo data has changed."
                # updated=tooldb.add_tool_logo(current_logo_file,current_thumbnail_file,tool_id)
                updated = tooldb.add_tool_logo(
                    current_logo_file, current_thumbnail_file, tool_id)
        return jsonify(json.loads(dumps({"result": "success", "message": "File and Tool was updated successfully and is readable"}))), 200
    