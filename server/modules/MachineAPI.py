import csv
import os
import re
import traceback
from jsondiff import diff
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from werkzeug import secure_filename

from DBUtil import MachineType, UserFavoriteMachine, Machine, Users, Accounts, Tool,\
Versions, ToolsOnMachine, MachineGroups, Tags, Role, ToolInstallation, DeploymentUnit,\
 DistributionMachine, Teams, DeploymentRequest,Build
from Services import fabfile, PasswordHelper, RemoteAuthenticationService, TeamService,\
    MachineHelperService, HelperServices
from Services.AppInitServices import authService
from settings import mongodb, import_full_path, key, relative_path
from flask_restplus import Resource
from modules.apimodels import MachineModel
from modules.apimodels.Restplus import api,header_parser
import json
from modules.apimodels.GenericReponseModel import dynamic_response_model
# blueprint declaration
machineAPI = Blueprint('machineAPI', __name__)
# restplus declaration
machineAPINs = api.namespace('machine', description='Machine Groups Operations')
# get global db connection

#Collections
db = mongodb
tagDB = Tags.Tags()
machineTypeDb = MachineType.MachineType(db)
machineFavDb = UserFavoriteMachine.UserFavoriteMachine(db)
toolInstallationDB = ToolInstallation.ToolInstallation(db)
machineDB = Machine.Machine(db)
userdb = Users.Users(db)
accountDB = Accounts.Accounts()
tooldb = Tool.Tool(db)
versionsDB = Versions.Versions(db)
toolsonmachinedb = ToolsOnMachine.ToolsOnMachine(db)
remoteAuthenticationService = RemoteAuthenticationService.RemoteAuthenticationService()
machinegroupDB = MachineGroups.MachineGroups(db)
roleDb = Role.Role(db)
deploymentUnitDb = DeploymentUnit.DeploymentUnit()
teamService = TeamService.TeamService()
distributionMachinetDB = DistributionMachine.DistributionMachine(db)
teamsDb = Teams.Teams(db)
deploymentRequestDb = DeploymentRequest.DeploymentRequest(db)
buildDB = Build.Build()
passHelper = PasswordHelper.PasswordHelper(key)


# MachineType - **********************************************************
@machineAPI.route('/machine/type/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineAPI/getAllMachineTypes.yml')
def get_all_machine_types():
    type_list = machineTypeDb.get_all_machine_type()
    return jsonify(json.loads(dumps({"result": "success", "data": type_list}))), 200


@machineAPI.route('/machine/fav/user/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineAPI/getUserFavoriteMachineByUserId.yml')
def get_user_fav_by_user_id(id):
    type_list = machineFavDb.get_user_favorite_machine_by_user_id(id, True)
    return jsonify(json.loads(dumps({"result": "success", "data": type_list}))), 200


@machineAPI.route('/machine/fav/machine/<string:machineId>/user/<string:userId>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineAPI/getUserFavoriteMachineByMachineIdAndUserId.yml')
def get_user_fav_by_user_id_and_machine_id(machineId, userId):
    type_list = machineFavDb.get_user_favorite_machine_by_machine_id_and_user_id(
        machineId, userId)
    return jsonify(json.loads(dumps({"result": "success", "data": type_list}))), 200

@machineAPINs.route('/fav/new', methods=['POST'])
class add_user_fav_machine(Resource):
    @api.expect(header_parser,MachineModel.fav_machine_input_model,validate=True)
    @api.marshal_with(MachineModel.fav_machine_response_model)
    @authService.authorized 
    def post(self):
        data = request.get_json()
        if (data.get("machine_id") and data.get("user_id"))is None:
            raise Exception("Mandatory field type to create a new Machine Fav machine_id,user_id was not found.")
        if machineDB.GetMachine(data.get("machine_id")) is None:
            raise Exception("Invalid machine_id.Machine not found")
        if userdb.get_user_by_id(data.get("user_id"), False) is None:
            raise Exception("Invalid user_id.User not found")
        if machineFavDb.get_user_favorite_machine_by_machine_id_and_user_id(
                data.get("machine_id"), data.get("user_id")):
            raise ValueError(
                "This machine is already present in your favourite list")
        result = machineFavDb.add_user_favorite_machine(data)
        return {"result": "success", "message": "Machine was added to your favourite list", "data": {"_id": str(result)}}, 200



@machineAPI.route('/machine/fav/delete/<string:id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineAPI/deleteUserFavoriteMachine.yml')
def delete_user_fav_machine(id):
    return jsonify(json.loads(dumps({"result": "success", "message": "Machine was removed from your favourite list", "data": machineFavDb.delete_user_favorite_machine(id)}))), 200


@machineAPINs.route('/new', methods=['POST'])
class add_machine(Resource):
    @api.expect(header_parser,MachineModel.machine_input_model,validate=True)
    @api.marshal_with(MachineModel.machine_response_model)
    @authService.authorized 
    def post(self):
        machine_details = request.get_json()
        machine_id = MachineHelperService.add_update_machine(machine_details, None)
        return {"result": "success", "message": "The machine is added successfully", "data": {"id": machine_id}}, 200


@machineAPINs.route('/test', methods=['POST'])
class test_machine_connectivity(Resource):
    @api.expect(header_parser,MachineModel.machine_input_model,validate=True)
    @api.marshal_with(MachineModel.ping_machine_response_model)
    @authService.authorized 
    def post(self):
        machineDetails = request.get_json()
        if (machineDetails.get("username") and machineDetails.get("ip") and machineDetails.get("password") and machineDetails.get("host")) is None:
            raise Exception ("Mandatory fields username,ip,host,port,password not found.")
        remoteAuthenticationService.authenticate(
            machineDetails, fabfile.PingMachine, machineDetails)
        return {"result": "success", "message": "The machine is verified with host :" + machineDetails["host"]}, 200


@machineAPI.route('/machine/view/<string:env_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineAPI/GetMachine.yml')
def get_machine_details_by_id(env_id):
    machine = machineDB.GetMachine(env_id)
    if not machine : raise Exception("Machine was not found")
    return jsonify(json.loads(dumps({"result": "success", "data": MachineHelperService.get_machine_details(machine)}))), 200
    

@machineAPI.route('/machine/view/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineAPI/GetMachines.yml')
def get_all_machines():
    limit = int(request.args.get('perpage', "30"))
    page = int(request.args.get('page', "0"))
    skip = page * limit
    tags_filter = request.args.get('tags', None)
    if not tags_filter or "any" in tags_filter:
        tags_filter = None
    else:
        tags_filter = tags_filter.split(",")
    machine_type_filter = request.args.get('machine_type', None)
    if not machine_type_filter or "any" in machine_type_filter:
        machine_type_filter = None
    else:
        machine_type_filter = machine_type_filter.split(",")
    machine_name_filter = request.args.get('machine_name', None)
    if machine_name_filter : machine_name_filter = machine_name_filter.split(",")  
    host_filter = request.args.get('host', "")
    machine_id_filter = request.args.get('machine_id_list', None)
    if not machine_id_filter or "any" in machine_id_filter:
        machine_id_filter = None
    else:
        machine_id_filter = machine_id_filter.split(",")
    id_list = teamService.get_user_permissions(authService.get_userid_by_auth_token())[
        "machine_id_list"]  # TOOL SET IDS
    machines = list(machineDB.GetMachines({"_id": {"$in": id_list},\
                                           "host": {"$regex": str(host_filter), "$options": "i"}},skip,limit))
    total_machines = list(machineDB.GetMachines({"_id": {"$in": id_list}}))
    user_id = authService.get_userid_by_auth_token()
    keys_to_keep= ["username","machine_name","host","status","_id","machine_type","flexible_attributes"]
    final_list_of_machines=[]
    for index,machine in enumerate(machines):
        #FILTER BY TAGS
        if(HelperServices.filter_handler(machine, tags_filter,tagDB.get_tag_names_from_given_ids_list(machine.get("tag",[])),"tag")):
            continue
        if machine_type_filter and machineTypeDb.get_machine_type_by_id(machine.get("machine_type")).get("type") not in machine_type_filter:
            continue
        if machine_name_filter:
            if len([f for f in machine_name_filter if re.compile(f.lower(), re.IGNORECASE).match(machine.get("machine_name").lower())]) == 0:
                continue
        if machine_id_filter:
            if len([f for f in machine_id_filter if f in str(machine.get("_id"))]) == 0:
                continue    
        machines[index] = machineDB.decrypt(machine)  # DECRYPT PASSWORDS
        for key in  machines[index].keys():
            if key not in keys_to_keep: machine.pop(key)
        fav_machine = machineFavDb.get_user_favorite_machine_by_machine_id_and_user_id(str(machines[index].get("_id")), user_id)
        if machines[index].get("machine_type"):
            machine_type = machineTypeDb.get_machine_type_by_id(
                machines[index]["machine_type"])
            if machines[index]:
                machines[index]["machine_type"] = machine_type["type"]
        final_list_of_machines.append(machine)        
    return jsonify(json.loads(dumps({"result": "success", "data": {"data": final_list_of_machines, "page": page, "total": len(total_machines), "page_total": len(final_list_of_machines)}}))), 200


@machineAPINs.route('/update', methods=['PUT'])
class update_machine(Resource):
    @api.expect(header_parser,MachineModel.machine_update_input_model,validate=True)
    @api.marshal_with(MachineModel.machine_update_response_model)
    @authService.authorized 
    def put(self):
        machine_details = request.get_json()
        if machine_details.get("_id"):
            if type(machine_details.get("_id")) is not dict:
                raise Exception("The type of _id is invalid")
            if not machine_details.get("_id").get("oid"):
                raise Exception ("oid was not found in _id")
        else:
            raise Exception ("_id was not found in input request ")
        result = MachineHelperService.add_update_machine(machine_details, machine_details["_id"]["oid"])
        return {"result": "success", "message": "Machine updated successfully", "data": result}, 200        

@machineAPI.route('/machine/remove/<string:machine_id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/MachineAPI/DeleteMachine.yml')
def delete_machine(machine_id):
    isDeleted=MachineHelperService.delete_machine(machine_id)
    if isDeleted == "1":
        return jsonify(json.loads(dumps({"result": "success", "message": "The machine was deleted"}))), 200
    else:
        raise Exception("Machine was not deleted")


@machineAPI.route('/machine/import', methods=['POST'])
@authService.authorized
def uploads_machines_using_csv():
    # This is the path to the upload directory
    try:
        # Get the name of the uploaded file
        file = request.files['file']
        if file is None:
            raise ValueError("No file selected")
        filename = ('.' in file.filename and
                    file.filename.rsplit('.', 1)[1] in ['csv'])
        if filename not in [True]:
            raise Exception("Invalid file .Please select file of type 'csv'")
        # Check if the file is one of the allowed types/extensions
        if file and filename:
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            file_path = str(import_full_path + '/' + filename)
            file.save(file_path)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as f:
                    reader = csv.reader(f)
                    index = 0
                    status = 0
                    variable = []
                    fieldnames = ("username","password","account_name","ip","host","machine_type","port","shell_type","reload_command" ,"machine_name","tags", "tunneling")
                    reader = csv.DictReader( f)
                    for idx, row in enumerate(reader):
                        try:                                
                            for item in fieldnames:
                                if item not in row.keys():
                                    raise Exception(" Field "+ item +" was not found." )      
                                if item == "account_name": 
                                    if row.get("account_name"): 
                                        account = accountDB.get_account_by_name(str(row.get("account_name")))
                                        if account:
                                            row["account_id"]=str(account["_id"])
                                            row.pop("account_name")
                                        else :
                                            raise Exception("No such account exists with name " + str(row.get("account_name")))
                                if item == "machine_type": 
                                    if row.get("machine_type"): 
                                        machint_type = machineTypeDb.get_machine_type_by_name(str(row.get("machine_type")))
                                        if machint_type:
                                            row["machine_type"]=str(machint_type["_id"])
                                        else :
                                            raise Exception("No such machine_type exists with name " + str(row.get("machine_type")))
                                        
                                if item == "port": 
                                    try:
                                        int(row.get("port"))
                                    except Exception as e:  # catch *all* exceptions
                                        raise Exception ("Invalid value for Machine port was defined") 
                                if item == "tags": 
                                    if row.get("tags"): 
                                        row["tag"] = row["tags"].split("||")
                                        row.pop("tags")
                                    else :
                                        row["tag"]=[]
                                if (item == "tunneling" ) :                                
                                    if  len(row.get("tunneling",[])) >0  :
                                        row["tunneling"] = row.get("tunneling").split("|||")
                                        count = 0
                                        row["steps_to_auth"] = []
                                        for idx1, rec in enumerate(row["tunneling"]):
                                            count+=1
                                            
                                            tunnel_rec = rec.split("||")
                                            
                                            if len(tunnel_rec)<> 5:
                                                raise Exception(" Field "+ item +" record " + str(idx1 + 1) +" was not found." )     
                                            else:
                                                if str(tunnel_rec[0]).lower() not in ["ssh", "telnet"]:
                                                    raise Exception ("Invalid value for Tunneling type")
                                                try:
                                                    int(tunnel_rec[2])
                                                except Exception as e:  # catch *all* exceptions
                                                    raise Exception ("Invalid value for Tunneling port")
                                                    
                                                row["steps_to_auth"].append({
                                                                   "type" :str(tunnel_rec[0]),
                                                                   "host" :str(tunnel_rec[1]),
                                                                   "port" :int(tunnel_rec[2]),
                                                                   "username" :str(tunnel_rec[3]),
                                                                   "password" :str(tunnel_rec[4]),
                                                                   "order" : count
                                                                   } ) 
                                    else:
                                        row["steps_to_auth"]=[]                    
                                    
                            #POP NWANTED VALUES
                            for key in ["tunneling","tags","account_name"] :
                                if key in row.keys():
                                    row.pop(key)   
                            #ADD ADDITONAL PARAMETERS
                            row["auth_type"]="password"                 
                            MachineHelperService.add_update_machine(row, None)
                            variable.append("Row no: " + str(idx + 2)+ " Machine was added ")                    
                        except Exception as e:  # catch *all* exceptions
                            variable.append("Row no: " + str(idx + 2)+" "+ str(e))
                              
                # RELOAD TEAM PERMISSIONS
                teamService.generate_details()
                return jsonify(json.loads(dumps({"result": "success", "message": "File has been uploaded", "data": variable}))), 200
            else:
                raise Exception("Unable to upload file")
    finally:
        try:
            f.close()
            os.remove(file_path)
        except Exception as e:
            print e
            
@machineAPINs.route('/bulk/load', methods=['POST'])
class MachineGroupBulkUpload(Resource):
    @api.expect(header_parser,MachineModel.machine_bulk_input_model,validate=True)
    @api.marshal_with(MachineModel.machine_bulk_response_model)
    @authService.authorized            
    def post(self):
        """
        Creates or updates requested MAchineGroups.
        """
        bulk_machine_response = []
        machine_details = request.get_json()
        if type(machine_details.get("data")) is list and len(machine_details.get("data")) > 0: 
            for machine in machine_details.get("data"):
                rec = {"_id":"","username":machine.get("username"),\
                       "host":machine.get("host"),"machine_name":machine.get("machine_name"),"result":"success","message":"machine was created"}
                try:
                    keys_to_validate=["username","host"]
                    for key in keys_to_validate:
                        if not machine.get(key): raise Exception ("mandatory key: "+ key+" is missing in machine details")
                    if machine.get("_id"):
                        if type(machine.get("_id")) is not dict:
                            raise Exception ("invalid type was found for key: _id")
                        if not machine.get("_id").get("oid"):
                            raise Exception ("oid was not found in _id")
                        rec["_id"]=machine["_id"]["oid"]
                        existing_machine=machineDB.GetMachine(rec["_id"])
                        result = MachineHelperService.add_update_machine(machine, str(machine["_id"]["oid"]))
                        if str(result) == "1":
                            if existing_machine.get("_id"):
                                existing_machine.pop("_id")
                            if  machine.get("_id"):
                                machine.pop("_id")   
                            sub = diff(existing_machine, machine)    
                            if sub:
                                rec["message"]="machine was updated"
                            else:
                                rec["message"]="no changes found"    
                        elif str(result) == "0":
                            rec["message"]="no changes found"                        
                    elif machineDB.get_machine_by_user_and_host(machine.get("username"),machine.get("host")) :
                        existing_machine = machineDB.get_machine_by_user_and_host(machine.get("username"),machine.get("host"))
                        rec["_id"]=str(existing_machine.get("_id"))
                        result = MachineHelperService.add_update_machine(machine, str(existing_machine["_id"]))
                        if str(result) == "1":
                            if existing_machine.get("_id"):
                                existing_machine.pop("_id")
                            if  machine.get("_id"):
                                machine.pop("_id")   
                            sub = diff(existing_machine, machine)    
                            if sub:
                                rec["message"]="machine was updated"
                            else:
                                rec["message"]="no changes found"    
                        elif str(result) == "0":
                            rec["message"]="no changes found"
                    else:
                        rec["_id"] = MachineHelperService.add_update_machine(machine, None)
                except Exception as e:  # catch *all* exceptions
                    rec["result"]="failed"
                    rec["message"]=str(e)
                    traceback.print_exc()
                if rec.get("result")=="success" and not rec.get("machine_name"):
                    existing_machine=machineDB.GetMachine(rec["_id"])
                    rec["machine_name"] = existing_machine["machine_name"]       
                bulk_machine_response.append(rec)          
        else:
            raise Exception("expected input type is list with atleast one record") 
        return {"result": "success", "message": "machines has been uploaded","data":bulk_machine_response}, 200

@machineAPI.route('/machine/view/deployment/history/entity/<string:entity>/<string:env_id>', methods=['GET'])
@authService.authorized
def get_deployment_history(entity, env_id):
    data = {}
    machine_ids_from_host = MachineHelperService.get_machine_ids_from_host(env_id)
    history = deploymentRequestDb.GetDeploymentRequestAll(
        {"machine_id": {"$in": machine_ids_from_host}, "status": re.compile("done", re.IGNORECASE)})
    tools = []
    dus = []
    for dep_history in history:
        dep = {}
        dep["update_date"] = dep_history.get("update_date")
        dep["build_number"] = dep_history.get("build_number")
        dep["requested_by"] = dep_history.get("requested_by")
        dep["request_type"] = dep_history.get("request_type")
        if versionsDB.get_version(dep_history.get("parent_entity_id"), False):
            version_details = versionsDB.get_version(
                dep_history.get("parent_entity_id"), False)
            if version_details:
                dep["version"] = str(version_details.get(
                    "version_name")) + " " + str(version_details.get("version_number"))
                tool_details = tooldb.get_tool_by_id(
                    version_details.get("tool_id"), False)
                if tool_details:
                    dep["name"] = tool_details.get("name")
            tools.append(dep)
        elif deploymentUnitDb.GetDeploymentUnitById(dep_history.get("parent_entity_id"), False):
            du_details = deploymentUnitDb.GetDeploymentUnitById(
                dep_history.get("parent_entity_id"), False)
            if du_details:
                dep["name"] = du_details.get("name")
            dus.append(dep)

    tool1 = []
    du1 = []
    dep1 = {}
    names = []
    if len(tools) >0:
        for tool in tools:
            if tool.get("name") not in names:
                names.append(tool.get("name"))
        for name in names:
            dep1 = {"name": name, "deployments": []}
            for tool in tools:
                if tool.get("name") == name:
                    tool.pop("name")
                    dep1["deployments"].append(tool)
            tool1.append(dep1)
        if entity == 'tool':
            data["history"] = {"tools": tool1}
    elif len(dus) > 0:
        for du in dus:
            if du.get("name") not in names:
                names.append(du.get("name"))
        for name in names:
            dep1 = {"name": name, "deployments": []}
            for du in dus:
                if du.get("name") == name:
                    du.pop("name")
                    dep1["deployments"].append(du)
            du1.append(dep1)
        if entity == 'du':
            data["history"] = {"dus": du1}
    return jsonify(json.loads(dumps({"result": "success", "data": data}))), 200
 
@machineAPINs.route('/search/tag/<string:tag>', methods=['GET'])
class get_machine_by_tag(Resource):
    @api.param('showDetails', 'valid values are true/false.Default is false')
    @api.expect(header_parser, validate=True)
    @api.marshal_with(dynamic_response_model)
    @authService.authorized 
    def get(self,tag):
        show_all_details = str(request.args.get('showDetails', 'false')).lower()
        machine_list = machineDB.get_machine_by_tag(tag)
        final_machine_list=[]
        if show_all_details.lower() == "true":
            for machine in machine_list:
                final_machine_list.append(MachineHelperService.get_machine_details(machine))
        else:
            final_machine_list= list(machine_list)
        return {"result": "success",  "data": final_machine_list}, 200

@machineAPINs.route('/search/name/<string:name>', methods=['GET'])
class get_machine_by_name(Resource):
    @api.param('showDetails', 'valid values are true/false.Default is false')
    @api.expect(header_parser, validate=True)
    @api.marshal_with(dynamic_response_model)
    @authService.authorized 
    def get(self,name):
        show_all_details = str(request.args.get('showDetails', 'false')).lower()
        machine_list = machineDB.GetMachinebyName(name)
        final_machine_list=[]
        if show_all_details.lower() == "true":
            for machine in machine_list:
                final_machine_list.append(MachineHelperService.get_machine_details(machine))
        else:
            final_machine_list= list(machine_list)
        return {"result": "success",  "data": final_machine_list}, 200
