'''
Created on Nov 2, 2016

@author: SJAJULA
'''

import os,json,re
from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from jsondiff import diff
from werkzeug import secure_filename

from DBUtil import Tool, Versions, ToolSet, Tags,Build
from Services import HelperServices, TeamService, FileUtils, ToolHelperService
from Services.AppInitServices import authService
from settings import mongodb, logo_path, logo_full_path,relative_path
from flasgger import swag_from
from flask_restplus import Resource
from modules.apimodels import ToolSetModel
from modules.apimodels.Restplus import api,header_parser
from modules.apimodels.GenericReponseModel import generic_post_response_model,generic_response_model


# blueprint declaration
toolSetAPI = Blueprint('toolSetAPI', __name__)
#restplus delaration
toolSetAPINs = api.namespace('toolset', description='ToolSet Operations')

# blueprint declaration
toolSetAPI = Blueprint('toolSetAPI', __name__)

# get global db connection
db = mongodb

# collection
toolsetdb = ToolSet.ToolSet(db)
tooldb = Tool.Tool(db)
versionsDB = Versions.Versions(db)
teamService = TeamService.TeamService()
tagDB = Tags.Tags()
buildDB = Build.Build()


@toolSetAPI.route('/toolset/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ToolSetAPI/getAllToolSets.yml')
def getAllToolSets():
    limit = int(request.args.get('perpage', '30'))
    page = int(request.args.get('page', "0"))
    skip = page * limit
    finalData = []
    tags_filter = []
    toolName_filter = []    
    name_filter=None    
    if request.args.get('tags', None):
        tags_filter = request.args.get('tags', None).split(",")
    if request.args.get('toolname', None):
        toolName_filter = request.args.get('toolname', None).split(",")
    id_list = teamService.get_user_permissions(authService.get_userid_by_auth_token())[
        "parent_entity_set_id_list"]  # TOOL SET IDS
    if request.args.get('name', None):
        name_filter = request.args.get('name', None)
    filter_required={"_id": {"$in": id_list}}
    if name_filter:
        filter_required.update({"name": {"$regex": str(name_filter), "$options": "i"}})
    total_count = len(
        list(toolsetdb.get_all_tool_set({"_id": {"$in": id_list}})))
    if name_filter:
        skip = limit = 0
    toolsets = toolsetdb.get_all_tool_set(filter_required, skip, limit)
    for record in toolsets:
        if(HelperServices.filter_handler(record, tags_filter,record.get("tag",[]),"tag")):
            continue
        if len(toolName_filter) > 0:
            tool_list = []
            for eachTool in record.get("tool_set"):
                if eachTool.get("tool_id"):
                    tool_list.append(str(eachTool["tool_id"]))

            if tool_list and "any" not in toolName_filter:
                if toolName_filter and len(toolName_filter) > 0 and len(list(set(toolName_filter) & set(tool_list))) < 1:
                    continue

        finalData.append(record)
    return jsonify(json.loads(dumps({"result": "success", "data": {"data": finalData, "page": page, "total": total_count, "page_total": len(finalData)}}))), 200


@toolSetAPI.route('/toolset/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ToolSetAPI/getToolSets.yml')
def getToolSets(id):
    tool_set = toolsetdb.get_tool_set(id)
    if not tool_set :
        raise ValueError("No such ToolSet was found")
    if tool_set.get("tool_set"):
        for idx, item in enumerate(tool_set.get("tool_set")):
            tool_data= tooldb.get_tool_by_id(item.get("tool_id"), False)
            if tool_data:
                tool_set["tool_set"][idx]["tool_name"]=tool_data.get("name")
            # Latest BUILD NUMBER and BUILD TYPE
            latest_build_details=buildDB.get_last_active_build(str(item.get("version_id")))
            if latest_build_details:
                tool_set["tool_set"][idx]["build_number"] = latest_build_details.get(
                        "build_number")
                tool_set["tool_set"][idx]["build_id"] = str(latest_build_details.get(
                        "_id"))
    return jsonify(json.loads(dumps({"result": "success", "data": tool_set}))), 200

@toolSetAPINs.route('/update', methods=['PUT'])
class updateToolSet(Resource):
    @api.expect(header_parser,ToolSetModel.update_toolset_input_model,validate=True)
    @api.marshal_with(generic_response_model)
    @authService.authorized
    def put(self):
        toolsetData = request.get_json()
        tool_set_id = toolsetData["_id"]["oid"]
        tools = toolsetdb.get_tool_set(tool_set_id)
        if not tools:
            raise Exception("No such ToolSet was found")
        ToolHelperService.add_update_tool_set(
            toolsetData, tool_set_id, logo_path, logo_full_path)
        return {"result": "success", "message": "ToolSet was updated successfully"}, 200



@toolSetAPI.route('/toolset/delete/<string:id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/ToolSetAPI/deleteToolSet.yml')
def deleteToolSet(id):
    isDeleted = ToolHelperService.delete_tool_set(id)
    return jsonify(json.loads(dumps({"result": "success", "message": "ToolSet was deleted", "data": isDeleted}))), 200

@toolSetAPINs.route('/add', methods=['POST'])
class AddToolSet(Resource):
    @api.expect(header_parser,ToolSetModel.add_toolset_input_model,validate=True)
    @api.marshal_with(generic_post_response_model)
    @authService.authorized
    def post(self):
        toolsetData = request.get_json()
        if not toolsetData.get("name"):
            raise ValueError("ToolSet Name is mandatory")
        if toolsetdb.get_tool_set_by_group_name(toolsetData.get("name")):
            raise ValueError("ToolSet with this name already exists")
        toolset_id = ToolHelperService.add_update_tool_set(
            toolsetData, None, logo_path, logo_full_path)
        return {"result": "success", "data":{"_id": toolset_id }, "message": "ToolSet was created successfully"}, 200


@toolSetAPI.route('/toolset/upload/logo', methods=['POST'])
@authService.authorized
def Upload_logoFile():
    # This is the path to the upload directory
    toolset_name = ""
    # These are the extension that we are accepting to be uploaded
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']

    re.compile("active", re.IGNORECASE)
# Get the name of the uploaded file
    file = request.files.get('logo')

    toolset_id = request.form.get('toolset_id')
    if toolset_id is None:
        raise Exception("toolset_id not found in request")
    if toolsetdb.get_tool_set(toolset_id) is None:
        raise Exception("No such tool set exists")
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
        result1 = toolsetdb.get_tool_set(toolset_id)
        toolsetname = '_'.join(result1["name"].split())
        file_path = str(logo_full_path + '/' + toolsetname +
                        '_' + toolset_id + '.' + file_extension)
        thumbnail_file_path = (str(
            logo_full_path + '/' + toolsetname + '_' + toolset_id + '_thumbnail.' + file_extension))
        current_logo_file = str(
            logo_path + '/' + toolsetname + '_' + toolset_id + '.' + file_extension)
        current_thumbnail_file = str(
            logo_path + '/' + toolsetname + '_' + toolset_id + '_thumbnail.' + file_extension)
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
            #                 updated=tooldb.AddToolSetLogo(current_logo_file,current_thumbnail_file,toolset_id)
            updated = toolsetdb.add_tool_set_logo(
                current_logo_file, current_thumbnail_file, toolset_id)
        else:
            sub = diff(db_logo_file, current_logo_file)
            if sub:
                print "ToolSetAPI:compare: logo " + db_logo_file + " is required to be updated as the logo data has changed."
                # updated=toolsetdb.AddToolSetLogo(current_logo_file,current_thumbnail_file,toolset_id)
                updated = toolsetdb.add_tool_set_logo(
                    current_logo_file, current_thumbnail_file, toolset_id)
        return jsonify(json.loads(dumps({"result": "success", "message": "File and Toolset was updated successfully and is readable"}))), 200
