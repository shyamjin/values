'''
Created on Jan 5, 2018

@author: vijasing
'''

from DBUtil import Teams,Machine,DeploymentRequest,DeploymentUnitSet,DeploymentUnit,MachineGroups,\
DistributionMachine,DeploymentRequestGroup,CloneRequest,ToolsOnMachine,UserFavoriteMachine,MachineType,\
Accounts,Tags,Users, Tool, Versions, Build
from settings import mongodb
from Services import HelperServices, TeamService, FlexibleAttributesHelper, EnvironmentVariablesHelper,Utils,AccountHelperService

teamsdb=Teams.Teams(mongodb)
machinedb=Machine.Machine(mongodb)
deploymentrequestdb=DeploymentRequest.DeploymentRequest(mongodb)
deploymentrequestgroupdb=DeploymentRequestGroup.DeploymentRequestGroup(mongodb)
deploymentunitsetdb = DeploymentUnitSet.DeploymentUnitSet()
deploymentunitdb = DeploymentUnit.DeploymentUnit()
machinegroupdb=MachineGroups.MachineGroups(mongodb)
distributionmachinetdb=DistributionMachine.DistributionMachine(mongodb)
clonerequestdb=CloneRequest.CloneRequest(mongodb)
toolsonmachinedb=ToolsOnMachine.ToolsOnMachine(mongodb)
machineFavDb=UserFavoriteMachine.UserFavoriteMachine(mongodb)
machineTypeDb = MachineType.MachineType(mongodb)
accountDB = Accounts.Accounts()
machineDB = Machine.Machine(mongodb)
tagDB = Tags.Tags()
teamsDb = Teams.Teams(mongodb)
teamService = TeamService.TeamService()
machinegroupDB = MachineGroups.MachineGroups(mongodb)
userdb = Users.Users(mongodb)
distributionMachinetDB = DistributionMachine.DistributionMachine(mongodb)
tooldb = Tool.Tool(mongodb)
versionsDB = Versions.Versions(mongodb)
buildDB = Build.Build()

def delete_machine(machine_id):
    """Start Machine Deletion"""
 
    if machinedb.GetMachine(machine_id) is None:
        raise ValueError("Machine does not exists")
    machinegroups=machinegroupdb.get_all_machine_groups({"machine_id_list": {"$in" : [str(machine_id)]}})
    present_in_machinegroups=[]
    for machinegroup in machinegroups:
        if machinegroup.get("group_name") not in present_in_machinegroups:
            present_in_machinegroups.append(machinegroup.get("group_name")) 
    deployments = deploymentrequestdb.GetDeploymentRequestAll({"machine_id": {"$in" : [str(machine_id)]}})
    present_in_deployments=[]
    for deployment in deployments :
        deploymentrequestgroups=deploymentrequestgroupdb.get_all_group_deployment_request_by_condition({"details.deployment_id": {"$in" : [str(deployment.get("_id"))]}})
        for deploymentrequestgroup in deploymentrequestgroups:
            if deploymentrequestgroup.get("name") not in present_in_deployments:
                present_in_deployments.append(deploymentrequestgroup.get("name"))
    teams = teamsdb.get_teams_by_filter(str(machine_id))
    present_in_teams=[]
    for team in teams :
        if team.get("team_name") not in present_in_teams:
            present_in_teams.append(team.get("team_name"))
    distributionmachines = distributionmachinetdb.GetDistributionMachineRequestByMachineId(machine_id)
    present_in_distributionmachines=[]
    if distributionmachines:
        present_in_distributionmachines.append(distributionmachines.get("machine_id"))
    clonerequests = clonerequestdb.GetCloneRequestsByMachineId(machine_id)
    present_in_clonerequest=[]
    for clonerequest in clonerequests:
        if clonerequest.get("_id") not in present_in_clonerequest:
            present_in_clonerequest.append(clonerequest.get("_id"))    
    err=""
    if len(present_in_machinegroups)>0: 
        err="The Machine cannot be deleted as it is present in Machine Groups: " + (','.join(map(str, present_in_machinegroups)))
    if len(present_in_deployments)>0:
        if len(err)>0: 
            err=err + " and is present in Deployment Groups: " + (','.join(map(str, present_in_deployments)))
        else:
            err="The Machine cannot be deleted as it is present in Deployment Groups: " + (','.join(map(str, present_in_deployments)))
    if len(present_in_teams)>0 :
        if len(err)>0: 
            err=err + " and is the part of teams: " +  (','.join(map(str, present_in_teams)))
        else:
            err="The Machine cannot be deleted as it is the part of the teams : " + (','.join(map(str, present_in_teams)))        
    if len(present_in_distributionmachines)>0:
        if len(err)>0: 
            err=err + " and has a distribution machine "
        else:
            err="The Machine cannot be delete as it has a distribution machine "
    if len(present_in_clonerequest)>0:
        if len(err)>0: 
            err=err + " and is present in clone requests: " + (','.join(map(str, present_in_clonerequest)))
        else:
            err="The Machine cannot be delete as it is present in clone requests:  " + (','.join(map(str, present_in_clonerequest)))        
    
    if len(err)>0:
        raise ValueError (err)
    toolsonmachinedb.delete_tools_by_machine_id(machine_id)
    machineFavDb.delete_tools_by_machine_id(machine_id)
    distributionmachinetdb.delete_tools_by_machine_id(machine_id)
    isDeleted = machinedb.DeleteDocument(machine_id)
    machinegroupdb.remove_machine_from_all_groups(machine_id)
    teamsdb.remove_machine_from_all_teams(machine_id)
    return (isDeleted)


def validate_machine_type(machine_type):
    result=None
    if Utils.is_valid_obj_id(machine_type):
        result=machineTypeDb.get_machine_type_by_id(machine_type)
    else:
        result=machineTypeDb.get_machine_type_by_name(machine_type)       
    if result is None:
        raise Exception("Machine Type provided is invalid")
    return str(result.get("_id"))

def validate_machine_details(machine_details):
    keys_to_validate=["username","account_id","ip","host","password",\
                          "machine_type","auth_type"]
    for key in keys_to_validate:
        if not machine_details.get(key): raise Exception ("mandatory key: "+ key+" is missing in machine details")
    machine_details["machine_type"] = validate_machine_type(machine_details.get("machine_type"))
    machine_details["account_id"] = AccountHelperService.validate_account_id(machine_details.get("account_id"))
    if not machine_details.get("machine_name"):
        machine_details["machine_name"] = str(machine_details.get(
        "username")) + '@' + str(machine_details.get('host'))
    HelperServices.validate_name(machine_details.get("machine_name"),"machine name")
    if machine_details.get("tag"):
        machine_details["tag"] = tagDB.get_tag_ids_from_given_ids_list(
            machine_details.get("tag"))
    if machine_details.get('permitted_users') :
        for record in machine_details["permitted_users"]:
            if str(record).lower() <> "all":
                if userdb.get_user_by_id(record, False) is None:
                    raise Exception(" user id: " + str(record) + " don't exist")
    if machine_details.get('permitted_teams') :
        for team in machine_details["permitted_teams"]:
            if teamsDb.get_team(team) is None:
                raise Exception("team id: " + str(team) + "don't exist")
    if machine_details.get('included_in') :
        for include in machine_details["included_in"]:
            if machinegroupDB.get_machine_groups(include) is None:
                raise Exception("machine group: " + str(include) + "don't exist")
    if machine_details.get("flexible_attributes"):
        FlexibleAttributesHelper.validate_entity_value("Machine", machine_details.get("flexible_attributes"))
    if machine_details.get("environment_variables"):
        EnvironmentVariablesHelper.validate_env_vars(machine_details.get("environment_variables"))
    
    
def add_missing_attr(machine_details,is_new_machine=True):
    input_as_array=["permitted_users","steps_to_auth","tag"]
    input_as_string=["reload_command","shell_type"]
    input_as_int=["port"]
    if is_new_machine:
        for rec in input_as_array: 
            if rec not in machine_details.keys() or machine_details.get(rec) is None : machine_details[rec]=[]
        for rec in input_as_string: 
            if rec not in machine_details.keys() or machine_details.get(rec) is None : machine_details[rec]=""
        for rec in input_as_int: 
            if rec not in machine_details.keys() or machine_details.get(rec) is None : machine_details[rec]=22       
    else:
        for rec in input_as_array: 
            if rec in machine_details.keys() and machine_details.get(rec) is None : machine_details[rec]=[]
        for rec in input_as_string: 
            if rec in machine_details.keys() and  machine_details.get(rec) is None : machine_details[rec]=""
        for rec in input_as_int: 
            if rec in machine_details.keys() and  machine_details.get(rec) is None : machine_details[rec]=22
           
                  
def add_update_machine(machine_details,machine_id=None):
    
    #VALIDATE AND EXTRACT DATA
    validate_machine_details(machine_details)
    permitted_teams = machine_details.get("permitted_teams")
    if permitted_teams is not None:
        machine_details.pop("permitted_teams")
    included_in = machine_details.get("included_in")
    if included_in is not None:
        machine_details.pop("included_in")    
    
    #EXISTING MACHINE
    if machine_id:
        add_missing_attr(machine_details,False)
        if not machineDB.GetMachine(machine_id):
            raise Exception("No such machine was found with _id: "+machine_id)
        duplicate_machine = machineDB.is_machine_duplicate(machine_details.get(
            "username"), machine_details.get("host"), machine_details.get("machine_name"), "update", machine_id)
        if duplicate_machine:
            raise ValueError("Failed as duplicate machine was found with name: "+duplicate_machine)
        machinegroupDB.remove_machine_from_all_groups(machine_id)
        teamsDb.remove_machine_from_all_teams(machine_id)
        if permitted_teams is not None:
                for team in permitted_teams:
                    teamsDb.add_machine_to_team(team, machine_id)
        if included_in is not None:
            for machineGroup in included_in:
                machinegroupDB.add_to_machine_groups(
                    machineGroup, machine_id)
        # RENAME HOSTNAME IN TOOLSONMACHINE
        toolsonmachinedb.update_hostname(machine_id, machine_details.get("host"))
        # RENAME HOSTNAME IN DISTRIBUTIONMACHINE
        distributionMachinetDB.update_hostname(
            machine_id, machine_details.get("host"))
        machine_details["_id"] = {}
        machine_details["_id"]["oid"] = machine_id
        machine_id = machineDB.UpdateMachine(machine_details)
    else:           
        #NEW MACHINE
        duplicate_machine=machineDB.is_machine_duplicate(machine_details.get(
            "username"), machine_details.get("host"), machine_details.get("machine_name"), "new")
        if not duplicate_machine:
            try:
                add_missing_attr(machine_details,True)
                machine_id = machineDB.AddMachine(machine_details)
                if permitted_teams is not None:
                    for team in permitted_teams:
                        teamsDb.add_machine_to_team(team, machine_id)
                if included_in is not None:
                    for machineGroup in included_in:
                        machinegroupDB.add_to_machine_groups(
                            machineGroup, machine_id)
            except Exception as e:  # catch *all* exceptions
                if  machine_id:                       
                    machineDB.DeleteDocument(machine_id)
                    machinegroupDB.remove_machine_from_all_groups(machine_id)
                    teamsDb.remove_machine_from_all_teams(machine_id)  
                raise e                 
        else:
            raise ValueError("Failed as duplicate machine was found with name: "+duplicate_machine)
    teamService.generate_details()
    return machine_id

def get_deployed_tool_details(machine_id):
    data = {}
    tool_list = []
    du_list = []
    # IF a tool/du is not present in ToolsOnMachine but present in
    # DeploymentRequest.It will not be considired
    for dep_on_machine in toolsonmachinedb.get_tools_on_machine_by_machine_id(machine_id):
        # GET CHECKSUM OF BUILD DEPLOYED
        if dep_on_machine.get("build_id"):
            build_details = buildDB.get_build_by_id(dep_on_machine.get("build_id"), False)
            if build_details:
                dep_on_machine["checksum"] = build_details.get("additional_info", {}).get("checksum")
        # GET CHECKSUM OF BUILD DEPLOYED
        if dep_on_machine.get("deployment_request_id"):
            dep_group_details = deploymentrequestgroupdb.get_grp_depreq_by_inner_depreq_ids(
                dep_on_machine.get("deployment_request_id"))
            if dep_group_details:
                dep_on_machine["dep_group_details"] = {"_id": str(dep_group_details.get("_id")), \
                                                       "name": dep_group_details.get("name")}

        tool_data = tooldb.get_tool_by_version(
            dep_on_machine["parent_entity_id"], False)
        if tool_data:
            tool_data["version"] = versionsDB.get_version(
                dep_on_machine["parent_entity_id"], False)  # This will required to get tool_id
            latestVersionForThisTool = tooldb.get_tool_by_id(
                tool_data["version"]["tool_id"], True)
            if latestVersionForThisTool is not None:
                result = latestVersionForThisTool.get("version")
                if not intern(str(tool_data["version"].get("version_number"))) is intern(
                        str(result.get("version_number"))):
                    tool_data["new_version_exists"] = "true"
                else:
                    tool_data["new_version_exists"] = "false"
                tool_data["latest_version_number"] = result.get(
                    "version_number")
                tool_data["latest_version_name"] = result.get(
                    "version_name")
            tool_data["all_availabe_versions"] = versionsDB.get_tool_with_all_version_name_and_number(
                tool_data["version"]["tool_id"], True, True)
            # WE WANT TO ADD TOOLS MACHINE DETAILS ALSO
            for key in ["_id", "status"]:
                if key in dep_on_machine.keys(): dep_on_machine.pop(key)
            tool_data.update(dep_on_machine)
            tool_list.append(tool_data)

    data["tool_list"] = tool_list

    return data

def get_deployed_du_details(machine_id):
    data = {}
    tool_list = []
    du_list = []
    # IF a tool/du is not present in ToolsOnMachine but present in
    # DeploymentRequest.It will not be considired
    for dep_on_machine in toolsonmachinedb.get_tools_on_machine_by_machine_id(machine_id):
        # GET CHECKSUM OF BUILD DEPLOYED
        if dep_on_machine.get("build_id"):
            build_details = buildDB.get_build_by_id(dep_on_machine.get("build_id"), False)
            if build_details:
                dep_on_machine["checksum"] = build_details.get("additional_info", {}).get("checksum")
        # GET CHECKSUM OF BUILD DEPLOYED
        if dep_on_machine.get("deployment_request_id"):
            dep_group_details = deploymentrequestgroupdb.get_grp_depreq_by_inner_depreq_ids(
                dep_on_machine.get("deployment_request_id"))
            if dep_group_details:
                dep_on_machine["dep_group_details"] = {"_id": str(dep_group_details.get("_id")), \
                                                       "name": dep_group_details.get("name")}

        du_data = deploymentunitdb.GetDeploymentUnitById(
            dep_on_machine["parent_entity_id"], True)
        if du_data:
            # # for GUI to check if revert can be done or not ##
            if du_data.get('build'):
                all_build_data = list(du_data.get('build'))
                latest_build = all_build_data[0].get('build_number')
                oldest_build = all_build_data[-1].get('build_number')
                du_data["new_build_exists"] = "true" if int(
                    latest_build) > int(dep_on_machine.get('build_no')) else "false"
                du_data["old_build_exists"] = "true" if int(
                    oldest_build) < int(dep_on_machine.get('build_no')) else "false"
                du_data.pop('build')
                du_data["all_available_builds"] = all_build_data
            ###pop useless data ###
            for key in ["deployment_field", "included_in", "pre_requiests", "gitlab_repo",
                        "gitlab_branch", "tag", "jenkins_job", "approval_list", "state"]:
                if key in du_data.keys(): du_data.pop(key)
            for key in ["_id", "status"]:
                if key in dep_on_machine.keys(): dep_on_machine.pop(key)
            du_data.update(dep_on_machine)
            du_list.append(du_data)

    data["du_list"] = du_list

    return data

def get_machine_ids_from_host(machine_id):
    # IF a tool/du is not present in ToolsOnMachine but present in
    # DeploymentRequest.It will not be considired
    machine_ids_from_host = []  # We will use this list for creating history
    for dep_on_machine in toolsonmachinedb.get_tools_on_machine_by_machine_id(machine_id):
        # GET CHECKSUM OF BUILD DEPLOYED
        if dep_on_machine.get("build_id"):
            build_details = buildDB.get_build_by_id(dep_on_machine.get("build_id"), False)
            if build_details:
                dep_on_machine["checksum"] = build_details.get("additional_info", {}).get("checksum")
        # GET CHECKSUM OF BUILD DEPLOYED
        if dep_on_machine.get("deployment_request_id"):
            dep_group_details = deploymentrequestgroupdb.get_grp_depreq_by_inner_depreq_ids(
                dep_on_machine.get("deployment_request_id"))
            if dep_group_details:
                dep_on_machine["dep_group_details"] = {"_id": str(dep_group_details.get("_id")), \
                                                       "name": dep_group_details.get("name")}
        if dep_on_machine.get("machine_id"):
            machine_ids_from_host.append(
                str(dep_on_machine.get("machine_id")))
    return machine_ids_from_host

def get_machine_details(machine):
    env_id=str(machine.get("_id"))
    if machine.get("tag"):
        machine["tag"] = tagDB.get_tag_names_from_given_ids_list(machine["tag"])
    tool_deployment_data = get_deployed_tool_details(env_id)
    du_deployment_data = get_deployed_du_details(env_id)
    machine["deploymentunits"] = du_deployment_data["du_list"]
    # If tools goes empty means no data in ToolsInMachine
    machine["Tools"] = tool_deployment_data["tool_list"]
    permitted_users = machine.get("permitted_users")
    permitted_users_arr = []
    if permitted_users is not None:
        for rec in permitted_users:
            if rec not in ["All", "all"]:
                user = userdb.get_user_by_id(str(rec), False)
                if user is None:
                    raise Exception("User with _id :" +
                                    str(rec) + " was not found")
                user["password"] = ""
                permitted_users_arr.append(user)
            else:
                permitted_users_arr.append(rec)
    machine["permitted_users"] = permitted_users_arr
    groups_for_machine = machinegroupDB.get_machine_group_by_machine(
        str(env_id))
    included_in = []
    for group in groups_for_machine:
        included_in.append(str(group["_id"]))
    machine["included_in"] = included_in

    teams_for_machine = teamsDb.get_teams_by_machine(str(env_id))
    permitted_teams = []
    for team in teams_for_machine:
        permitted_teams.append(str(team["_id"]))
    machine["permitted_teams"] = permitted_teams
    return machine
    
