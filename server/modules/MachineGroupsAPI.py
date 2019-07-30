import traceback,re,json
from bson.json_util import dumps
from flasgger import swag_from, validate
from flask import Blueprint, jsonify, request

from DBUtil import Machine, Users, MachineGroups, Tags,DeploymentRequestGroup,DeploymentRequest,State,Config
from Services import TeamService,MachineGroupHelperService, HelperServices
from Services.AppInitServices import authService
from settings import mongodb, relative_path
from flask_restplus import Resource
from modules.apimodels import MachineGroupsModel
from modules.apimodels.Restplus import api,header_parser

# blueprint declaration
machineGroupsAPI = Blueprint('MachineGroupsAPI', __name__)
# restplus declaration
machineGroupsAPINs = api.namespace('machinegroups', description='Machine Groups Operations')
# collections
machineDB = Machine.Machine(mongodb)
tagDB = Tags.Tags()
userdb = Users.Users(mongodb)
machinegroupsDB = MachineGroups.MachineGroups(mongodb)
teamService = TeamService.TeamService()
deploymentRequestGroupDB = DeploymentRequestGroup.DeploymentRequestGroup(mongodb)
deploymentRequestDb = DeploymentRequest.DeploymentRequest(mongodb)
stateDb=State.State(mongodb)
configDb=Config.Config(mongodb)

@machineGroupsAPI.route('/machinegroups/add', methods=['POST'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineGroupsAPI/AddMachineGroups.yml')
def AddMachineGroups():
    
    machine_group_details = request.get_json()
    validate(machine_group_details, 'MachineGroup', relative_path +
             '/swgger/MachineGroupsAPI/AddMachineGroups.yml')
    existing_machine_group_detail = machinegroupsDB.machine_groups_by_name(machine_group_details.get("group_name"))
    if existing_machine_group_detail:
        raise Exception("duplicate machinegroup was found with same Group Name")
    machine_group_id = MachineGroupHelperService.add_update_machinegroups(machine_group_details, None)
    return jsonify(json.loads(dumps({"result": "success", "message": "The machine groups is saved successfully", "data": {"id": machine_group_id}}))), 200


@machineGroupsAPI.route('/machinegroups/view', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineGroupsAPI/GetMachineGroups.yml')
def GetMachineGroups():
    limit = int(request.args.get('perpage', "30"))
    page = int(request.args.get('page', "0"))
    skip = page * limit
    machine_group_name_filter = request.args.get('machine_group_name', None)
    machine_id_filter = request.args.get('machine_id_list', None)
    if not machine_id_filter or "any" in machine_id_filter:
        machine_id_filter = None
    else:
        machine_id_filter = machine_id_filter.split(",")
    if machine_group_name_filter: machine_group_name_filter = machine_group_name_filter.split(",")                            
    id_list = teamService.get_user_permissions(
        authService.get_userid_by_auth_token())["machine_group_id_list"]
    final_machine_group_list=[]
    for machine_group in machinegroupsDB.get_all_machine_groups({"_id": {"$in": id_list}}):
        if(HelperServices.filter_handler(machine_group, machine_id_filter,\
                                machine_group.get("machine_id_list",[]),"machine_id_list")):
            continue
        if machine_group_name_filter:
            if len([f for f in machine_group_name_filter if re.compile(f.lower(), re.IGNORECASE).match(machine_group.get("group_name").lower())]) == 0:
                continue
        final_machine_group_list.append(machine_group)
    total_machine_groups=list(machinegroupsDB.get_all_machine_groups({"_id": {"$in": id_list}}))
    return jsonify(json.loads(dumps({"result": "success", "data":{"data": final_machine_group_list, "page": page,\
                    "total": len(total_machine_groups), "page_total": len(final_machine_group_list)} }))), 200
    
def add_deployment_group_details(data):
    data["dep_group_details"]=[]    
    for grp in  deploymentRequestGroupDB.get_all_group_deployment_request_by_condition({"machine_group_id": str(data.get("_id"))},int(configDb.getConfigByName("MachineGroup").get("deployment_details_count_to_display"))):   
        rec = {"_id":str(grp.get("_id")),"name":grp.get("name"),"status":grp.get("status"),"requested_by":grp.get("requested_by"),\
                 "request_type":grp.get("request_type"),"deployment_type":grp.get("deployment_type"),"create_date":grp.get("create_date"),
                 "package_state_name":"NA"}
        if grp.get("package_state_id",None):
            state_package = stateDb.get_state_by_id(grp.get("package_state_id"), False)
            if state_package :
                rec["package_state_name"] = state_package.get("name",None)                 
        data["dep_group_details"].append(rec)
    return data    

@machineGroupsAPI.route('/machinegroups/view/<string:env_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineGroupsAPI/GetMachineGroup.yml')
def GetMachineGroup(env_id):
    group = machinegroupsDB.get_machine_groups(env_id)
    if not group: raise Exception("Group was not found")
    if request.args.get('deploymentgroupdetails', "true")=="true":
        group= add_deployment_group_details(group)
    return jsonify(json.loads(dumps({"result": "success", "data":group}))), 200

@machineGroupsAPI.route('/machinegroups/view/name/<string:group_name>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineGroupsAPI/GetMachineGroupByName.yml')
def GetMachineGroupByName(group_name):

    group = machinegroupsDB.machine_groups_by_name(group_name)
    if not group: raise Exception("Group was not found")
    return jsonify(json.loads(dumps({"result": "success", "data": group}))), 200

@machineGroupsAPI.route('/machinegroups/update', methods=['PUT'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineGroupsAPI/UpdateMachineGroups.yml')
def UpdateMachineGroups():
    machine_group_details = request.get_json()
    validate(machine_group_details, 'MachineGroup', relative_path +
             '/swgger/MachineGroupsAPI/UpdateMachineGroups.yml')
    if machine_group_details.get("_id"):
        if type(machine_group_details.get("_id")) is not dict:
            raise Exception("The type of _id is invalid")
        if not machine_group_details.get("_id").get("oid"):
            raise Exception ("oid was not found in _id")
    else:
        raise Exception ("_id was not found in input request ")  
    MachineGroupHelperService.add_update_machinegroups(machine_group_details, machine_group_details["_id"]["oid"])
    return jsonify(json.loads(dumps({"result": "success", "message": "Machinegroup updated successfully"}))), 200        


@machineGroupsAPI.route('/machinegroups/delete/<string:id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineGroupsAPI/DeleteMachineGroups.yml')
def DeleteMachineGroups(id):
    isDeleted = machinegroupsDB.delete_machine_groups(id)  # Missing Method
    return jsonify(json.loads(dumps({"result": "success", "message": "The Group was deleted successfully"}))), 200
    
@machineGroupsAPINs.route('/bulk/load', methods=['POST'])
class MachineGroupBulkUpload(Resource):
    @api.expect(header_parser,MachineGroupsModel.machinegroup_bulk_input_model,validate=True)
    @api.marshal_with(MachineGroupsModel.machinegroup_bulk_response_model)
    @authService.authorized
    def post(self):
        """
        Creates or updates requested MAchineGroups.
        """
        bulk_machine_groups_response =[]
        machine_group_details = request.get_json()
        if type(machine_group_details.get("data"))  is list and len(machine_group_details.get("data")) > 0:
            for machine_groups in machine_group_details.get("data"):
                rec = {"_id":"","group_name":machine_groups.get("group_name"),"result":"success","message":"machinegroup was created"}
                try:
                    if machine_groups.get("_id"):
                        if type(machine_groups.get("_id")) is not dict:
                            raise Exception ("invalid type was found for key: _id")
                        if not machine_groups.get("_id").get("oid"):
                            raise Exception ("oid was not found in _id")
                        rec["_id"]=str(machine_groups["_id"]["oid"])
                        result = MachineGroupHelperService.add_update_machinegroups(machine_groups, rec["_id"])
                        if str(result) == "1":   
                            rec["message"]="machinegroup was updated"
                        elif str(result) == "0":
                            rec["message"]="no changes found"
                    elif machinegroupsDB.machine_groups_by_name(machine_groups.get("group_name")):
                        existing_machine_groups = machinegroupsDB.machine_groups_by_name(machine_groups.get("group_name"))
                        rec["_id"]=str(existing_machine_groups.get("_id"))
                        result = MachineGroupHelperService.add_update_machinegroups(machine_groups, rec["_id"])
                        if str(result) == "1":
                            rec["message"]="machinegroup was updated"
                        elif str(result) == "0":
                            rec["message"]="no changes found"
                    else:
                        rec["_id"] = MachineGroupHelperService.add_update_machinegroups(machine_groups, None)
                except Exception as e:  # catch *all* exceptions
                    rec["result"]="failed"
                    rec["message"]=str(e)
                    traceback.print_exc() 
                bulk_machine_groups_response.append(rec)                 
        else:
            raise Exception("expected input type is list with atleast one record") 
        return {"result": "success", "message": "machinegroups has been uploaded","data":bulk_machine_groups_response}, 200         