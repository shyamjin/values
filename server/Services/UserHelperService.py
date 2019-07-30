'''
Created on Jan 5, 2018

@author: vijasing
'''
from DBUtil import Teams, Machine, Users, Role, UserFavoriteMachine
from settings import mongodb
from Services.AppInitServices import authService
from flask import jsonify

teamsdb=Teams.Teams(mongodb)
machinedb=Machine.Machine(mongodb)
userdb=Users.Users(mongodb)
roledb=Role.Role(mongodb)
machineFavDb = UserFavoriteMachine.UserFavoriteMachine(mongodb)


def delete_user(uid):
    """Start User Deletion"""
    user_id = authService.get_userid_by_auth_token()
    if user_id is None:
        return jsonify({"result": "failed", "message": "Token verification failed"}), 404
    loggedInUser = userdb.get_user_by_id(user_id, False)
    UserToDelete = userdb.get_user_by_id(uid, False)
    loggedInUserRole = roledb.get_role_by_id(loggedInUser["roleid"], True)
    if loggedInUserRole["name"].lower() == "superadmin":
        pass
    else:
        newUserRole = roledb.get_role_by_id(
            UserToDelete.get("roleid"), False)
        if newUserRole["name"].lower() == "superadmin":
            raise ValueError("Only SuperAdmin can remove a SuperAdmin")
        else:
            pass
        
    all_machines=machinedb.GetMachines({"permitted_users": {"$in" : [str(uid)]}}) 
    present_in_machine_permissions=[]
    for mach in all_machines:
        if mach.get("machine_name") not in present_in_machine_permissions:
            present_in_machine_permissions.append(mach.get("machine_name")) 
    all_teams = teamsdb.get_teams_by_filter(str(uid))
    present_in_teams=[]
    for rec in all_teams :
        if rec.get("team_name") not in present_in_teams:
            present_in_teams.append(rec.get("team_name"))
    err=""
    if len(present_in_machine_permissions)>0: 
        err="The user cannot be deleted as it is in the machine permissions: " + (','.join(map(str, present_in_machine_permissions)))
    if len(present_in_teams)>0 :
        if len(err)>0: 
            err=err + " and is the part of teams: " +  (','.join(map(str, present_in_teams)))
        else:
            err="The user cannot be deleted as it is the part of the teams : " + (','.join(map(str, present_in_teams)))
    if len(err)>0:
        raise ValueError (err)
    userfavmc = machineFavDb.get_user_favorite_machine_by_user_id(
        uid, False)
    if userfavmc is not None:
        for record in userfavmc:
            machineFavDb.delete_user_favorite_machine(record["_id"])
    if teamsdb.get_team_by_user(uid) is not None:
        teams = teamsdb.get_team_by_user(uid)
        for team in teams:
            teamsdb.remove_user_from_team(team["_id"], uid)
    if machinedb.get_machine_by_permitted_user(uid) is not None:
        machines = machinedb.get_machine_by_permitted_user(uid)
        for machine in machines:
            machinedb.RemoveUserPermissionToMachine(machine["_id"], uid)
    return (userdb.delete_user(uid))
             
   