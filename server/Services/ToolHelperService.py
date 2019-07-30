'''
Created on Dec 18, 2017

@author: pdinda
'''
import traceback
from datetime import datetime
from DBUtil import Config, Build,Versions,DeploymentUnitSet,DeploymentUnit,DeploymentUnitType,Tool,Tags,\
        ToolSet,Teams,DeploymentRequest,Machine
from settings import mongodb
from Services import HelperServices,TeamService
tagDB = Tags.Tags()
versionsDB = Versions.Versions(mongodb)
configdb = Config.Config(mongodb)
buildsDB = Build.Build()
deploymentunitsetdb = DeploymentUnitSet.DeploymentUnitSet()
deploymentunitdb = DeploymentUnit.DeploymentUnit()
deploymentUnitTypedb = DeploymentUnitType.DeploymentUnitType()
toolDB = Tool.Tool(mongodb)
teamService = TeamService.TeamService()
toolsetdb = ToolSet.ToolSet(mongodb)
teamsdb=Teams.Teams(mongodb)
deploymentrequestdb=DeploymentRequest.DeploymentRequest(mongodb)
machinedb=Machine.Machine(mongodb)
import RepositoryHelperService

def add_update_tool(tooldata, tool_id, logo_path, directory_to_import_from, full_logo_path):
    """Add Update a Tool"""
    # CHECK TOOL NAME
#     if tooldata.get("status"):
#         if (tool_id):
#             if(tooldata.get("status")=="3"):
#                 validate_tool(tool_id)
#                 
    if not tooldata.get("name"):
        raise ValueError("Invalid Tool Name")
    HelperServices.validate_name(tooldata.get("name"),"tool name")
    Tool = {}
    Tool["name"] = tooldata["name"]
    # CHECK TAG
    if not tooldata.get("tag"):
        Tool["tag"] = []
    else:
        Tool["tag"] = tagDB.get_tag_ids_from_given_ids_list(tooldata["tag"])

    if tooldata.get("support_details"):
        Tool["support_details"] = tooldata["support_details"]
    if tooldata.get("logo"):
        Tool["logo"] = tooldata["logo"]
    if tooldata.get("description"):
        Tool["description"] = tooldata["description"]
    if tooldata.get("tool_creation_source"):
        Tool["tool_creation_source"] = tooldata.get("tool_creation_source")
    if tooldata.get("allow_build_download"):
        Tool["allow_build_download"] = str(
            tooldata.get("allow_build_download"))
    else:
        Tool["allow_build_download"] = 'False'
    if tooldata.get("is_tool_cloneable"):
        Tool["is_tool_cloneable"] = str(
            tooldata.get("is_tool_cloneable"))
    if tooldata.get("artifacts_only"):
        Tool["artifacts_only"] = str(
            tooldata.get("artifacts_only"))
    
    Tool["status"]=tooldata.get("status","1")   

    Tool = HelperServices.add_update_logo(Tool, logo_path, full_logo_path, directory_to_import_from)
    # ADD UPDATE DATA
    if tool_id:
        Tool["_id"] = {}
        Tool["_id"]["oid"] = tool_id        
        result = toolDB.update_tool(Tool)
    else:        
        result = toolDB.add_tool(Tool)
    if result is None:
        raise Exception("Unable to create/update tool " + Tool["name"])
    else:
        # RELOAD TEAM PERMISSIONS
        teamService.generate_details()
    return str(result)

def validate_tool(tool_id):
    toolsets = toolsetdb.get_all_tool_set({"tool_set.tool_id": {"$in" : [str(tool_id)]}})
    present_in_toolset=[]
    for toolset in toolsets:
        if toolset.get("name") not in present_in_toolset:
            present_in_toolset.append(toolset.get("name")) 
    all_deployments=deploymentrequestdb.GetDeploymentRequestAll({"state_id": {"$in": [str(tool_id)]}})
    present_in_deployment=[]
    for dep in all_deployments:
        machine=machinedb.GetMachine(dep.get("machine_id"))
        if machine:
            if machine.get("machine_name") not in present_in_deployment:
                present_in_deployment.append(machine.get("machine_name")) 
    teams = teamsdb.get_teams_by_filter(str(tool_id))
    present_in_teams=[]
    for team in teams :
        if team.get("team_name") not in present_in_teams:
            present_in_teams.append(team.get("team_name"))
    err=""
    if len(present_in_toolset)>0: 
        err="The tool cannot be deleted as it is present in toolset: " + (','.join(map(str, present_in_toolset)))
    if len(present_in_deployment)>0:
        if len(err)>0: 
            err=err + " and has been deployed in machines: " + (','.join(map(str, present_in_deployment)))
        else:
            err="The tool cannot be delete as it has been deployed in machines: " + (','.join(map(str, present_in_deployment)))
    if len(present_in_teams)>0 :
        if len(err)>0: 
            err=err + " and is the part of teams: " +  (','.join(map(str, present_in_teams)))
        else:
            err="The tool cannot be deleted as it is the part of the teams : " + (','.join(map(str, present_in_teams)))
    if len(err)>0:
        raise ValueError (err)
    
def add_update_version(VersionsData, tool_id, version_id, allDetails=False):
    """Add Update a Version"""
    versionInsert = {}
    versionInsert['tool_id'] = tool_id
    if VersionsData.get("pre_requiests") is not None:
        versionInsert['pre_requiests'] = VersionsData['pre_requiests']
    if VersionsData.get("version_name") is not None:
        HelperServices.validate_name(VersionsData.get("version_name"),"version label")
        versionInsert['version_name'] = VersionsData['version_name']
    if VersionsData.get("version_date") is not None:
        try:
            versionInsert['version_date'] = datetime.strptime(
                (str(str(VersionsData['version_date']).split()[0])), "%Y-%m-%d")
        except Exception:  # catch *all* exceptions
            traceback.print_exc()
            raise Exception(
                "Failed while parsing version_date. Expected format is %Y-%m-%d %H:%M:%S.%f . Example 2016-07-15 13:01:09.758000")
    if VersionsData.get("version_number") is not None:
        HelperServices.validate_name(VersionsData.get("version_number"),"version number")
        versionInsert['version_number'] = VersionsData['version_number']
    if VersionsData.get("backward_compatible") is not None:
        versionInsert['backward_compatible'] = VersionsData['backward_compatible']
    if VersionsData.get("mps_certified") is not None:
        versionInsert['mps_certified'] = VersionsData['mps_certified']
    if VersionsData.get("release_notes") is not None:
        versionInsert['release_notes'] = VersionsData['release_notes']
    if VersionsData.get("gitlab_branch") is not None:
        versionInsert['gitlab_branch'] = VersionsData['gitlab_branch']
    if VersionsData.get("branch_tag") is not None:
        versionInsert['branch_tag'] = VersionsData['branch_tag']
    if VersionsData.get("dependent_tools") is not None:
        versionInsert['dependent_tools'] = VersionsData['dependent_tools']
    else:
        versionInsert['dependent_tools'] = []
    if VersionsData.get("deployer_to_use") is not None:
        versionInsert['deployer_to_use'] = VersionsData['deployer_to_use']
    if VersionsData.get("repository_to_use") is not None:
        if RepositoryHelperService.check_if_repo_exists_by_name(VersionsData.get("repository_to_use")):
            versionInsert['repository_to_use'] = VersionsData['repository_to_use']
        else:
            raise Exception(VersionsData.get("repository_to_use") + ": No such repository exists")
    if allDetails:  # WE DONT WANT TO UPDATE THESE FIELS WHILE USING SYNC ONLY WHEN EDIT TOOLS
        if VersionsData.get("jenkins_job") is not None:
            versionInsert['jenkins_job'] = VersionsData['jenkins_job']
        if VersionsData.get("gitlab_repo") is not None:
            versionInsert['gitlab_repo'] = VersionsData['gitlab_repo']
        if VersionsData.get("git_url") is not None:
            versionInsert['git_url'] = VersionsData['git_url']
    if version_id:
        versionInsert["_id"] = {}
        versionInsert["_id"]["oid"] = version_id
        versionInsert["status"] = VersionsData["status"]
        result = versionsDB.update_version(versionInsert)
    else:
        versionInsert["status"] = "1"
        result = versionsDB.add_version(versionInsert)
    if result is None:
        raise Exception("Unable to add new version")
    return str(result)


def validate_tool_data(tooldata=None):
    """Validate a ToolJson Data"""
    if not tooldata:
        raise Exception("tool_data is missing")
    if tooldata.get("operation") != "delete":
        if not tooldata.get("versions"):
            raise Exception("versions is missing from tool_data")
        for ver in tooldata.get("versions"):
            if ver.get("deployment_field"):
                if not ver.get("deployment_field").get("fields") or len(ver.get("deployment_field").get("fields")) < 1:
                    raise Exception("deployment_field has no fields")
            if ver.get("media_file"):
                if not ver.get("media_file").get("media_files") or len(ver.get("media_file").get("media_files")) < 1:
                    raise Exception("media_file has no media_files")
                for media in ver.get("media_file").get("media_files"):
                    if not media.get("url"):
                        raise Exception("media_files has no url")
            if ver.get("document"):
                if not ver.get("document").get("documents") or len(ver.get("document").get("documents")) < 1:
                    raise Exception("document has no documents")
    

def check_if_tool_data_is_valid(tooldata, localTool):
    """Check if tool data exists in database"""
    if localTool is None:
        raise Exception("No tool with name " +
                        tooldata["name"] + " was found in local DB")
    versions = tooldata.get("versions")
    if versions is None:
        raise Exception("versions is missing from tool_data")
    for record in versions:
        if record.get("version_name") is None:
            raise Exception("version_name is missing")
        if record.get("version_number") is None:
            raise Exception("version_number is missing")
        if record.get("operation").lower() in ["update", "delete"] and localTool is not None:
            localVersion = versionsDB.get_version_by_tool_id_name_and_number(
                str(localTool["_id"]), record["version_name"],
                record["version_number"])
            if localVersion is None:
                raise Exception("No Version exists with name: " +
                                record["version_name"] + " number: " +
                                record["version_number"] +
                                "in local DB to for tool "
                                + localTool["name"])
        if record.get("operation").lower() in ["insert"] and localTool is not None:
            localVersion = versionsDB.get_version_by_tool_id_name_and_number(
                str(localTool["_id"]), record["version_name"],
                record["version_number"])
            if localVersion is not None:
                if localVersion.get("status") != "0":
                    raise Exception("Version already exists with name: " +
                                    record["version_name"] +
                                    " number: " + record["version_number"]
                                    + "in local DB to for tool " + localTool["name"])
                    

def check_if_tool_exists(tooldata):
    """Check if tool data dependent data exists in database"""
    localTool = toolDB.get_tool_by_name(tooldata["name"])
    if localTool is not None:
        raise Exception("Tool already exists")
    versions = tooldata.get("versions")
    if versions is None:
        raise Exception("versions is missing from tool_data")
    for record in versions:
        if record.get("version_name") is None:
            raise Exception("version_name is missing")
        if record.get("version_number") is None:
            raise Exception("version_number is missing")
        if localTool:
            localVersion = versionsDB.get_version_by_tool_id_name_and_number(
                str(localTool["_id"]), record["version_name"], record["version_number"])
            if localVersion is not None:
                raise Exception("Version already exists with name: " +
                                record["version_name"] + " number: " +
                                record["version_number"] +
                                "in local DB for tool " + localTool["name"])
                
def get_dependend_tools(version, delete_ids=False):
    """Get DependendTools for version"""
    if version.get("dependent_tools") and len(version.get("dependent_tools")) > 0:
        dependent_tools = []
        for dTools in version.get("dependent_tools"):
            dependent_tool = toolDB.get_tool_by_id(dTools["tool_id"], False)
            if not dependent_tool or not dependent_tool.get("name"):
                raise ValueError("Dependent tool with _id:" +
                                 dTools["tool_id"] + " was not found in local db")
            else:
                dTools["tool_name"] = dependent_tool.get("name")
            dependent_version = versionsDB.get_version(
                dTools["version_id"], False)
            if not dependent_version or not dependent_version.get("version_name") or not dependent_version.get("version_number"):
                raise ValueError("Dependent version with _id:" +
                                 dTools["version_id"] + " was not found in local db")
            else:
                dTools["version_name"] = dependent_version.get("version_name")
                dTools["version_number"] = dependent_version.get(
                    "version_number")
            if delete_ids:
                if dTools.get("version_id"):
                    dTools.pop("version_id")
                if dTools.get("tool_id"):
                    dTools.pop("tool_id")
            dependent_tools.append(dTools)
        version["dependent_tools"] = dependent_tools
    return version


def set_dependend_tools(version, delete_ids=False):
    """Set DependendTools for version"""
    if version.get("dependent_tools") and len(version.get("dependent_tools")) > 0:
        dependent_tools = []
        for dTools in version.get("dependent_tools"):
            dependent_tool = toolDB.get_tool_by_name(dTools["tool_name"])
            if not dependent_tool or not dependent_tool.get("name"):
                raise ValueError("Dependent tool with name:" +
                                 dTools["tool_name"] + " was not found")
            else:
                dTools["tool_id"] = str(dependent_tool.get("_id"))
            dependent_version = versionsDB.get_version_by_tool_id_name_and_number(
                dTools["tool_id"], dTools["version_name"], dTools["version_number"])
            if not dependent_version or not dependent_version.get("version_name") or not dependent_version.get("version_number"):
                raise ValueError("Dependent version with tool_id:" + dTools["tool_id"] + " version_name:" +
                                 dTools["version_name"] + " version_number:" + dTools["version_number"] + " was not found")
            else:
                dTools["version_id"] = str(dependent_version.get("_id"))
            if delete_ids:
                if dTools.get("tool_name"):
                    dTools.pop("tool_name")
                if dTools.get("version_name"):
                    dTools.pop("version_name")
                if dTools.get("version_number"):
                    dTools.pop("version_number")
            dependent_tools.append(dTools)
        version["dependent_tools"] = dependent_tools
    return version



def get_ordered_tools(versions):
    """Calculate FinalOrderProcess of tool"""
    order_process = 0
    tool_names = []
    for version in versions:
        temp_order_process = 0
        temp_order_process, visitedToolVersionName = get_orderd_tools_inner(
            version, 0, [])
        if temp_order_process > order_process:
            order_process = temp_order_process
            tool_names = list(set(tool_names + visitedToolVersionName))
    return order_process, tool_names


def get_orderd_tools_inner(version_details, order_process, visitedToolVersionName=[]):
    """Calculate OrderProcess of tool"""
    version_details = get_dependend_tools(version_details, False)
    toolName = toolDB.get_tool_by_version(
        version_details["source_version_id"], False)["name"]
    if toolName in visitedToolVersionName:
        return order_process, visitedToolVersionName
    else:
        visitedToolVersionName.append(toolName)
    if version_details.get("dependent_tools") and len(version_details.get("dependent_tools")) > 0:
        for dependent_version in version_details.get("dependent_tools"):
            # print dependent_version
            dependent_version = versionsDB.get_version(
                dependent_version["version_id"], False)
            dependent_version["source_version_id"] = str(
                dependent_version["_id"])
            order_process, visitedToolVersionName = get_orderd_tools_inner(
                dependent_version, order_process + 1, visitedToolVersionName)
    return order_process, visitedToolVersionName


def verify_tool_set_data(toolsetData):
    """Verify ToolSetData"""
    if toolsetData.get("name"):
        HelperServices.validate_name(toolsetData.get("name"),"toolset name")
    if toolsetData.get("tool_set") and len(toolsetData.get("tool_set")) > 1:
        tool_set = []
        for tool_version in toolsetData.get("tool_set"):
            if not tool_version.get("version_id"):
                raise ValueError("version_id was not found in request")
            if not tool_version.get("tool_version"):
                raise ValueError("tool_version was not found in request")
            versionDetails = versionsDB.get_version(
                tool_version.get("version_id"), False)
            if not versionDetails:
                raise ValueError("Version with version_id:" +
                                 tool_version.get("version_id") + " was not found in database")
            if not versionDetails.get("tool_id"):
                raise ValueError("Version with version_id:" + tool_version.get(
                    "version_id") + " in database has missing tool_id")
            tool_set.append({"version_id": tool_version.get("version_id"), "tool_version": tool_version.get(
                "version_id"), "tool_id": versionDetails.get("tool_id")})
        toolsetData["tool_set"] = tool_set
    else:
        raise ValueError("Specify at least two tool versions in the ToolSet")
    # CHECK TAG
    if not toolsetData.get("tag"):
        toolsetData["tag"] = []
    else:
        toolsetData["tag"] = tagDB.get_tag_ids_from_given_ids_list(
            toolsetData["tag"])
    return toolsetData




def add_update_tool_set(toolSetData, tool_set_id=None, logo_path=None, logo_full_path=None):
    """Add ToolSetData"""
    toolSetData = verify_tool_set_data(toolSetData)
    if logo_path and logo_full_path:
        toolSetData = HelperServices.add_update_logo(toolSetData, logo_path, logo_full_path, None)
    if tool_set_id:
        toolSetData["_id"] = {}
        toolSetData["_id"]["oid"] = tool_set_id
        result = toolsetdb.update_tool_set(toolSetData)
    else:
        result = toolsetdb.add_new_tool_set(toolSetData)
    if result is None:
        raise Exception("Unable to create/update ToolSet ")
    else:
        # RELOAD TEAM PERMISSIONS
        teamService.generate_details()
    return str(result)


# ALSO USED FROM  /tool/delete/<string:tool_id>
def delete_tool(tool_id,validation_indicator = True):
    """Start Tool Deletion"""
    # MAINTAIN THE DELETED TOOLS
    deleted_tools = []
    deleted_version = []
    deleted_builds = []
    try:
        tool = toolDB.get_tool_by_id(tool_id, False)
        if not tool:
            validate_tool(tool_id)
        if validation_indicator == True :
            print ("Apply any validation here if required")
        tooldata = {}
        tooldata["_id"] = {}
        tooldata["_id"]["oid"] = str(tool_id)
        tooldata["status"] = "0"
        if str(tool.get("status")) <> "0":
            deltool = toolDB.update_tool(tooldata)
            if deltool in [None, 0]:
                raise Exception("Unable to delete tool " + str(tool_id))
            else:
                tooldata["status"] = tool.get("status")
                deleted_tools.append(tooldata)
        versions = versionsDB.get_all_tool_versions(str(tool_id), False)
        if versions:
            for version in versions:
                if str(version.get("status")) <> "0":
                    versiondata = {}
                    versiondata["_id"] = {}
                    versiondata["_id"]["oid"] = str(version.get("_id"))
                    versiondata["status"] = "0"
                    delversion = versionsDB.update_version(versiondata)
                    if delversion in [None, 0]:
                        raise Exception(
                            "Unable to delete version " + str(version.get("_id")))
                    else:
                        versiondata["status"] = version.get("status")
                        deleted_version.append(versiondata)
                builds = buildsDB.get_active_build(
                    str(version.get("_id")))
                if builds:
                    for build in builds:
                        if str(build.get("status")) <> "0":
                            Buildupdate = {}
                            Buildupdate["_id"] = {}
                            Buildupdate["_id"]["oid"] = str(
                                build.get("_id"))
                            Buildupdate["status"] = "0"
                            delbuild = buildsDB.update_build(
                                Buildupdate)
                            if delbuild in [None, 0]:
                                raise Exception(
                                    "Unable to delete build " + str(build.get("_id")))
                            else:
                                deleted_builds.append(Buildupdate)
        return {"result": "success", "message": "Tool was deleted"}
    except Exception as e_value:  # catch *all* exceptions
        for rec in deleted_tools:
            rec["status"] = "1"
            toolDB.update_tool(rec)
        for rec in deleted_version:
            rec["status"] = "1"
            versionsDB.update_version(rec)
        for rec in deleted_builds:
            rec["status"] = "1"
            buildsDB.update_build(rec)
        traceback.print_exc()
        return {"result": "failed", "message": str(e_value)}

def delete_tool_set(tool_set_id):
    toolset = toolsetdb.get_tool_set(tool_set_id)
    if toolset is None:
        raise ValueError ("No such ToolSet was found")
    teams = teamsdb.get_teams_by_filter([tool_set_id])
    present_in_teams=[]
    for team in teams :
        if team.get("team_name") not in present_in_teams:
            present_in_teams.append(team.get("team_name"))
    if len(present_in_teams)>0 :
        raise ValueError ("The toolset cannot be deleted as it is the part of the teams : " + (','.join(map(str, present_in_teams))) )
    isDeleted = toolsetdb.delete_tool_set(tool_set_id)
    return isDeleted