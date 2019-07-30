'''
Created on Jan 5, 2018

@author: vijasing
'''
import TeamService
from DBUtil import Teams,Machine,Users,Role,DeploymentRequest,DeploymentUnitSet,DeploymentUnit,MachineGroups,Tool,ToolSet,Tags
from settings import mongodb
from bson.objectid import ObjectId
teamsdb=Teams.Teams(mongodb)
machinedb=Machine.Machine(mongodb)
userdb=Users.Users(mongodb)
roledb=Role.Role(mongodb)
teamService = TeamService.TeamService()
deploymentrequestdb=DeploymentRequest.DeploymentRequest(mongodb)
deploymentunitsetdb = DeploymentUnitSet.DeploymentUnitSet()
deploymentunitdb = DeploymentUnit.DeploymentUnit()
machinegroupdb=MachineGroups.MachineGroups(mongodb)
toolsetdb=ToolSet.ToolSet(mongodb)
tooldb=Tool.Tool(mongodb)
tagdb=Tags.Tags()

def delete_tag(uid):
    """Start Tag Deletion"""
    if ObjectId(uid) in teamService.get_active_tags():
        raise Exception("This tag cannot be removed as it is in use")
    
    dus = deploymentunitdb.GetAllDeploymentUnits(None,None, False, {"tag": {"$in" : [str(uid)]}})
    present_in_du=[]
    for du in dus:
        if du.get("name") not in present_in_du:
            present_in_du.append(du.get("name")) 
    dusets = deploymentunitsetdb.GetAllDeploymentUnitSet(False, {"tag": {"$in" : [str(uid)]}})
    present_in_duset=[]
    for duset in dusets:
        if duset.get("name") not in present_in_duset:
            present_in_duset.append(duset.get("name")) 
    machines=machinedb.GetMachines({"tag": {"$in" : [str(uid)]}}) 
    present_in_machines=[]
    for machine in machines:
        if machine.get("machine_name") not in present_in_machines:
            present_in_machines.append(machine.get("machine_name")) 
    machinegroups=machinegroupdb.get_all_machine_groups({"tag": {"$in" : [str(uid)]}})
    present_in_machinegroups=[]
    for machinegroup in machinegroups:
        if machinegroup.get("group_name") not in present_in_machinegroups:
            present_in_machinegroups.append(machinegroup.get("group_name")) 
    teams = teamsdb.get_teams_by_filter(str(uid))
    present_in_teams=[]
    for team in teams :
        if team.get("team_name") not in present_in_teams:
            present_in_teams.append(team.get("team_name"))
    tools = tooldb.get_tools_all(None,{"tag": {"$in" : [str(uid)]}})
    present_in_tool=[]
    for tool in tools:
        if tool.get("name") not in present_in_tool:
            present_in_tool.append(tool.get("name")) 
    toolsets = toolsetdb.get_all_tool_set({"tag": {"$in" : [str(uid)]}})
    present_in_toolset=[]
    for toolset in toolsets:
        if toolset.get("name") not in present_in_toolset:
            present_in_toolset.append(toolset.get("name")) 
    
    err=""
    if len(present_in_du)>0: 
        err="The Tag cannot be deleted as it is present in Du: " + (','.join(map(str, present_in_du)))
    if len(present_in_duset)>0:
        if len(err)>0: 
            err=err + " and is present in Du Package: " + (','.join(map(str, present_in_duset)))
        else:
            err="The Tag cannot be delete as it is present in Du Package: " + (','.join(map(str, present_in_duset)))
    if len(present_in_machines)>0:
        if len(err)>0: 
            err=err + " and is present in machine: " + (','.join(map(str, present_in_machines)))
        else:
            err="The Tag cannot be delete as it is present in machine: " + (','.join(map(str, present_in_machines)))  
    if len(present_in_machinegroups)>0:
        if len(err)>0: 
            err=err + " and is present in machine groups: " + (','.join(map(str, present_in_machinegroups)))
        else:
            err="The Tag cannot be delete as it is present in machine groups: " + (','.join(map(str, present_in_machinegroups)))        
    if len(present_in_teams)>0 :
        if len(err)>0: 
            err=err + " and is the part of teams: " +  (','.join(map(str, present_in_teams)))
        else:
            err="The Tag cannot be deleted as it is the part of the teams : " + (','.join(map(str, present_in_teams)))
    if len(present_in_tool)>0:
        if len(err)>0: 
            err=err + " and is present in tools: " + (','.join(map(str, present_in_tool)))
        else:
            err="The Tag cannot be delete as it is present in tools: " + (','.join(map(str, present_in_tool)))  
    if len(present_in_toolset)>0:
        if len(err)>0: 
            err=err + " and is present in Tool Sets: " + (','.join(map(str, present_in_toolset)))
        else:
            err="The Tag cannot be delete as it is present in Tool Sets: " + (','.join(map(str, present_in_toolset)))        
    if len(err)>0:
        raise ValueError (err)  
    return (tagdb.delete_tag(uid))
             
   