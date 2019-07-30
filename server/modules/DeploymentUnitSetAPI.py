import os,json,random,re,string,traceback
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from jsondiff import diff
from werkzeug import secure_filename

from DBUtil import DeploymentUnit, DeploymentUnitSet, Users, SystemDetails,State,Build,DeploymentUnitType
from Services import FileUtils, HelperServices, TeamService, DuHelperService
from Services.AppInitServices import authService
from settings import mongodb, relative_path, logo_path, logo_full_path
from flask_restplus import Resource
from modules.apimodels import DeploymentUnitSetModel
from modules.apimodels.Restplus import api,header_parser
from modules.apimodels.GenericReponseModel import generic_post_response_model,generic_response_model

# blueprint declaration
deploymentUnitSetAPI = Blueprint('deploymentUnitSetAPI', __name__)

deploymentUnitSetAPINs = api.namespace('deploymentunitset', description='Deployment Unit Set Operations')
# get global db connection
db = mongodb
deploymentUnitSetDB = DeploymentUnitSet.DeploymentUnitSet()
userDB = Users.Users(db)
systemDetailsDB = SystemDetails.SystemDetails(db)
teamService = TeamService.TeamService()
deploymentUnitDB = DeploymentUnit.DeploymentUnit()
stateDB = State.State(db)

@deploymentUnitSetAPI.route('/deploymentunitset/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitSetAPI/getAllDeploymentUnitSets.yml')
def getAllDeploymentUnitSets():
    
    limit = int(request.args.get('perpage', '30'))
    page = int(request.args.get('page', "0"))
    skip = page * limit
    tags_filter = []
    duName_filter = []
    approval_status_filter = []
    name_filter=None
    if request.args.get('tags', None):
        tags_filter = request.args.get('tags', None).split(",")
    if request.args.get('duname', None):
        duName_filter = request.args.get('duname', None).split(",")
    if request.args.get('approval_status', None):
        approval_status_filter = request.args.get('approval_status', None).split(",")           
    id_list = teamService.get_user_permissions(authService.get_userid_by_auth_token())[
    "parent_entity_set_id_list"]
    if request.args.get('name', None):
        name_filter = request.args.get('name', None)
    filter_required={"_id": {"$in": id_list}}
    if name_filter:
        filter_required.update({"name": re.compile(name_filter, re.IGNORECASE)})        
    deploymentUnitSets = deploymentUnitSetDB.GetAllDeploymentUnitSet(
        False, filter_required, skip, limit)
    # total_count=len(id_list)
    total_count = len(list(deploymentUnitSetDB.GetAllDeploymentUnitSet(
        False, {"_id": {"$in": id_list}})))
    ###########GROUP by DeploymentUnitType#############################
    finalData = []
    if len(tags_filter)>0 or len(approval_status_filter)>0 or len(duName_filter) > 0:
        for dus in deploymentUnitSets:
            #FILTER BY TAGS
            if len(tags_filter)>0:
                if(HelperServices.filter_handler(dus, tags_filter,dus.get("tag",[]),"tag")):
                    continue
            #Filter by state approval status
            if len(approval_status_filter)>0:
                approval_sts_of_states=[]
                for state in stateDB.get_state_by_parent_entity_id(str(dus["_id"]), True):
                    if state.get("approval_status"):
                        approval_sts_of_states.append(state.get("approval_status"))
                if(HelperServices.filter_handler({"approval_status":True},\
                                                                  approval_status_filter,approval_sts_of_states , "approval_status")):
                    continue
            if len(duName_filter) > 0:
                du_list = []
                for eachTool in dus.get("du_set"):
                    if eachTool.get("du_id"):
                        du_list.append(eachTool["du_id"])
    
                if du_list and "any" not in duName_filter:
                    if duName_filter and len(duName_filter) > 0 and len(list(set(duName_filter) & set(du_list))) < 1:
                        continue
    
            finalData.append(dus)
        return jsonify(json.loads(dumps({"result": "success", "data": {"data": finalData, "page": page, "total": total_count, "page_total": len(finalData)}}))), 200
    else:
        return jsonify(json.loads(dumps({"result": "success", "data": {"data": list(deploymentUnitSets), "page": page, "total": total_count, "page_total": len(deploymentUnitSets)}}))), 200
@deploymentUnitSetAPI.route('/deploymentunitset/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitSetAPI/getDeploymentUnitSetbyID.yml')
def getDeploymentUnitSetbyID(id):
    data=deploymentUnitSetDB.GetDeploymentUnitSetById(id, False, False)
    return jsonify(json.loads(dumps({"result": "success", "data":data }))), 200

@deploymentUnitSetAPI.route('/deploymentunitset/view/getbuilds/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitSetAPI/getDeploymentUnitSetbyID.yml')
def getDeploymentUnitSetbyIDGetBuild(id):
    data=deploymentUnitSetDB.GetDeploymentUnitSetBuildsById(id)
    return jsonify(json.loads(dumps({"result": "success", "data":data }))), 200


@deploymentUnitSetAPI.route('/deploymentunitset/view/states/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitSetAPI/getDeploymentUnitSetbyID.yml')
def getDeploymentUnitSetbyIDGetStates(id):
    data=deploymentUnitSetDB.GetDeploymentUnitSetStatesById(id)    
    return jsonify(json.loads(dumps({"result": "success", "data":data }))), 200



def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


@deploymentUnitSetAPINs.route('/new', methods=['POST'])
class DeploymentUnitSetNew(Resource):
    @api.expect(header_parser,DeploymentUnitSetModel.duset_input_model,validate=True)
    @api.marshal_with(generic_post_response_model)
    @authService.authorized
    def post(self):
            newDeploymentUnitSet = request.get_json()
            if deploymentUnitSetDB.GetDeploymentUnitSetByName(newDeploymentUnitSet.get("name"), False) is not None:
                raise Exception("Deployment Set with name " + newDeploymentUnitSet.get("name") + " already exists")
            newDeploymentUnitSet["id"] = id_generator()  # ADD UNIQUE ID
            deployment_unit_set_id = DuHelperService.add_update_du_set(
                newDeploymentUnitSet, None, logo_path, logo_full_path)
            return {"result": "success", "message": "The DeploymentUnit Set is added successfully", "data": {"_id": deployment_unit_set_id }}, 200


@deploymentUnitSetAPINs.route('/update', methods=['PUT'])
class updateNewDeploymentUnitSet(Resource):
    @api.expect(header_parser,DeploymentUnitSetModel.duset_input_model_for_update,validate=True)
    @api.marshal_with(generic_response_model)
    @authService.authorized
    def put(self):
        deploymentUnitSet = request.get_json()
        if deploymentUnitSet.get("_id"):
            if type(deploymentUnitSet.get("_id")) is not dict:
                raise Exception("The type of _id is invalid")
            if not deploymentUnitSet.get("_id").get("oid"):
                raise Exception ("oid was not found in _id")
        else:
            raise Exception ("_id was not found in input request ")
        DuHelperService.add_update_du_set(
            deploymentUnitSet, deploymentUnitSet["_id"]["oid"], logo_path, logo_full_path)
        return {"result": "success", "message": "The DeploymentUnit Set is updated successfully"}, 200        

@deploymentUnitSetAPI.route('/deploymentunitset/delete/<string:id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitSetAPI/deleteDeploymentUnitSet.yml')
def deleteDeploymentUnitSet(id):
    isDeleted = DuHelperService.delete_du_set(id)
    return jsonify(json.loads(dumps({"result": "success", "message": "DeploymentUnit Set was deleted", "data": isDeleted}))), 200


@deploymentUnitSetAPI.route('/deploymentunitset/upload/logo', methods=['POST'])
@authService.authorized
def uploadLogoFile():
    # This is the path to the upload directory
    duset_name = ""
    # These are the extension that we are accepting to be uploaded
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']

    re.compile("active", re.IGNORECASE)
# Get the name of the uploaded file
    file = request.files.get('logo')
    duset_id = request.form.get('duset_id')
    if duset_id is None:
        raise Exception("duset_id not found in request")
    if deploymentUnitSetDB.GetDeploymentUnitSetById(duset_id, False) is None:
        raise Exception("No such DU SET exists")
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
        result1 = deploymentUnitSetDB.GetDeploymentUnitSetById(
            duset_id, False)
        duset_name = '_'.join(result1["name"].split())
        file_path = str(logo_full_path + '/' + duset_name +
                        '_' + duset_id + '.' + file_extension)
        thumbnail_file_path = (str(
            logo_full_path + '/' + duset_name + '_' + duset_id + '_thumbnail.' + file_extension))
        current_logo_file = str(
            logo_path + '/' + duset_name + '_' + duset_id + '.' + file_extension)
        current_thumbnail_file = str(
            logo_path + '/' + duset_name + '_' + duset_id + '_thumbnail.' + file_extension)
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
            #                 updated=tooldb.add_tool_logo(current_logo_file,current_thumbnail_file,duset_id)
            updated = deploymentUnitSetDB.add_du_set_logo(
                current_logo_file, current_thumbnail_file, duset_id)
        else:
            sub = diff(db_logo_file, current_logo_file)
            if sub:
                print "Du Set API:compare: logo " + db_logo_file + " is required to be updated as the logo data has changed."
                # updated=tooldb.add_tool_logo(current_logo_file,current_thumbnail_file,duset_id)
                updated = deploymentUnitSetDB.add_du_set_logo(
                    current_logo_file, current_thumbnail_file, duset_id)
        return jsonify(json.loads(dumps({"result": "success", "message": "File and Deployment Unit Set was updated successfully and is readable"}))), 200
        

@deploymentUnitSetAPINs.route('/bulk/load', methods=['POST'])
class DeploymentUnitSetBulkLoad(Resource):
    @api.expect(header_parser,DeploymentUnitSetModel.duset_bulk_input_model,validate=True)
    @api.marshal_with(DeploymentUnitSetModel.duset_bulk_response_model)
    @authService.authorized
    def post(self):
        """
        Creates or updates requested DU set.
        """
        bulk_du_set_response = []
        du_set_details = request.get_json()
        if type(du_set_details.get("data")) is list and len(du_set_details.get("data")) > 0:
            for set in du_set_details.get("data"):
                rec = {"_id":"","name": set.get("name"), "result":"success", "message":"DU set was created"}
                try:
                    keys_to_validate_in_set = ["name", "du_set"]
#                     keys_to_validate_in_du_details = ["du_id", "dependent", "order"]
                    for key in keys_to_validate_in_set:
                        if not set.get(key): raise Exception ("mandatory key: "+ key+" is missing in du set details")                    
                    if set.get("_id"):
                        if type(set.get("_id")) is not dict:
                            raise Exception ("invalid type was found for key: _id")
                        if not set.get("_id").get("oid"):
                            raise Exception ("oid was not found in _id")
                        rec["_id"] = set["_id"]["oid"]
                        result = DuHelperService.add_update_du_set(set, str(rec["_id"]), logo_path, None, logo_full_path)                             
                        if result == "1":
                                rec["message"] = "DU Set was updated"
                        else:
                            rec["message"] = "no changes found"
                    elif deploymentUnitSetDB.GetDeploymentUnitSetByName(set.get("name")) :
                        existing_du_set = deploymentUnitSetDB.GetDeploymentUnitSetByName(set.get("name"))
                        rec["_id"] = str(existing_du_set.get("_id"))
                        result = DuHelperService.add_update_du_set(set, str(rec["_id"]), logo_path, None, logo_full_path)
                        if result == "1":
                                rec["message"] = "DU Set was updated"
                        else:
                            rec["message"] = "no changes found"
                    else:
                        rec["_id"] = DuHelperService.add_update_du_set(set, None, logo_path, None, logo_full_path)
                except Exception as e:  # catch *all* exceptions
                    rec["result"]="failed"
                    rec["message"]=str(e)
                    traceback.print_exc()
                bulk_du_set_response.append(rec)          
        else:
            raise Exception("expected input type is list with atleast one record") 
        return {"result": "success", "message": "DU Set's has been processed for uploading","data":bulk_du_set_response}, 200