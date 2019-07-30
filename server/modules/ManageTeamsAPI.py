import json
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request

from DBUtil import Users, Teams, Tags, Machine, Tool, DeploymentUnit, MachineGroups, ToolSet, DeploymentUnitSet
from Services import TeamService,HelperServices
from Services.AppInitServices import authService
from settings import mongodb, relative_path
from flask_restplus import Resource
from modules.apimodels import ManageTeamsModel
from modules.apimodels.Restplus import api,header_parser
from modules.apimodels.GenericReponseModel import generic_post_response_model,generic_response_model


# blueprint declaration
manageTeamsAPI = Blueprint('ManageTeamsAPI', __name__)
#restplus delaration
manageTeamsAPINs = api.namespace('teams', description='Teams Operations')

# get global db connection
db = mongodb

# collections
userDB = Users.Users(db)
teamDB = Teams.Teams(db)
tagDB = Tags.Tags()
machineDB = Machine.Machine(db)
machinegroupsDB = MachineGroups.MachineGroups(db)
toolDB = Tool.Tool(mongodb)
toolsetdb = ToolSet.ToolSet(db)
deploymentUnitDB = DeploymentUnit.DeploymentUnit()
deploymentUnitSetDB = DeploymentUnitSet.DeploymentUnitSet()
teamService = TeamService.TeamService()


@manageTeamsAPINs.route('/add', methods=['POST'])
class AddTeam(Resource):
    @api.expect(header_parser,ManageTeamsModel.add_teams_input_model,validate=True)
    @api.marshal_with(generic_post_response_model)
    @authService.authorized
    def post(self):
        teamDetails = request.get_json()
        if (teamDetails.get("team_name") and teamDetails.get("users_id_list") and teamDetails.get("distribution_list")) is None:
            raise Exception("Mandatory fields to create a new team was not found.")
        if teamDB.get_team_by_name(teamDetails.get("team_name")):
            raise Exception("Team with name " + teamDetails.get("team_name") + " already exists")
        HelperServices.validate_name(teamDetails.get("team_name"),"team name")
        if not teamDetails.get("users_id_list"):
            teamDetails["users_id_list"] = []
        if not teamDetails.get("tag_id_list"):
            teamDetails["tag_id_list"] = []
        if not teamDetails.get("machine_id_list"):
            teamDetails["machine_id_list"] = []
        if not teamDetails.get("machine_group_id_list"):
            teamDetails["machine_group_id_list"] = []
        if not teamDetails.get("parent_entity_id_tool_list"):
            teamDetails["parent_entity_id_tool_list"] = []
        if not teamDetails.get("parent_entity_id_du_list"):
            teamDetails["parent_entity_id_du_list"] = []
        if not teamDetails.get("parent_entity_tool_set_id_list"):
            teamDetails["parent_entity_tool_set_id_list"] = []
        if not teamDetails.get("parent_entity_du_set_id_list"):
            teamDetails["parent_entity_du_set_id_list"] = []
        if not teamDetails.get("parent_entity_tag_list"):
            teamDetails["parent_entity_tag_list"] = []
        if not teamDetails.get("parent_entity_set_tag_list"):
            teamDetails["parent_entity_set_tag_list"] = []
        new_team_id = teamDB.add_team(teamDetails)
        teamService.generate_details()
        return {"result": "success", "message": "The team is created successfully", "data": {"id": new_team_id}}, 200

@manageTeamsAPI.route('/teams/view', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ManageTeamsAPI/GetTeams.yml')
def GetTeams():
    return jsonify(json.loads(dumps({"result": "success", "data": teamDB.get_all_teams()}))), 200


@manageTeamsAPI.route('/teams/view/<string:team_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/ManageTeamsAPI/GetTeam.yml')
def GetTeam(team_id):
    # @author ---> stuti
    # This will return list of names not mongoIDS for each entity in team document
    team = teamDB.get_team(team_id)
    if team is None:
        raise ValueError("No such Team with _id: " +
                         team_id + " was not found")
    team["tool_list"] = []
    team["du_list"] = []
    team["toolset_list"] = []
    team["duset_list"] = []

    if team.get("tag_id_list"):
        team["tag_id_list"] = tagDB.get_tag_names_from_given_ids_list(
            team["tag_id_list"])
    if team.get("parent_entity_tag_list"):
        team["parent_entity_tag_list"] = tagDB.get_tag_names_from_given_ids_list(
            team["parent_entity_tag_list"])
    if team.get("parent_entity_set_tag_list"):
        team["parent_entity_set_tag_list"] = tagDB.get_tag_names_from_given_ids_list(
            team["parent_entity_set_tag_list"])

    if team.get("parent_entity_id_tool_list") and len(team.get("parent_entity_id_tool_list")) > 0:
        for parent_entity_id in team.get("parent_entity_id_tool_list"):
            if str(parent_entity_id).lower() == "all":
                team["tool_list"].append("all")
            else:
                team["tool_list"].append(toolDB.get_tool_by_id(
                    parent_entity_id, False)["name"])

    if team.get("parent_entity_id_du_list") and len(team.get("parent_entity_id_du_list")) > 0:
        for parent_entity_id in team.get("parent_entity_id_du_list"):
            if str(parent_entity_id).lower() == "all":
                team["du_list"].append("all")
            else:
                team["du_list"].append(deploymentUnitDB.GetDeploymentUnitById(
                    parent_entity_id, False)["name"])

    if team.get("parent_entity_tool_set_id_list") and len(team.get("parent_entity_tool_set_id_list")) > 0:
        for parent_entity_set_id in team.get("parent_entity_tool_set_id_list"):
            if str(parent_entity_set_id).lower() == "all":
                team["toolset_list"].append("all")
            else:
                team["toolset_list"].append(
                    toolsetdb.get_tool_set(parent_entity_set_id)["name"])

    if team.get("parent_entity_du_set_id_list") and len(team.get("parent_entity_du_set_id_list")) > 0:
        for parent_entity_set_id in team.get("parent_entity_du_set_id_list"):
            if str(parent_entity_set_id).lower() == "all":
                team["duset_list"].append("all")
            else:
                team["duset_list"].append(deploymentUnitSetDB.GetDeploymentUnitSetById(
                    parent_entity_set_id, False)["name"])

    if team.get("machine_id_list") and len(team.get("machine_id_list")) > 0:
        for index, machine_id in enumerate(team.get("machine_id_list")):
            if str(machine_id).lower() == "all":
                team["machine_id_list"][index] = ("all")
            elif machineDB.GetMachine(machine_id) and len(machineDB.GetMachine(machine_id)) > 0:
                team["machine_id_list"][index] = machineDB.GetMachine(machine_id)[
                    "machine_name"]

    if team.get("machine_group_id_list") and len(team.get("machine_group_id_list")) > 0:
        for index, machine_group_id in enumerate(team.get("machine_group_id_list")):
            if str(machine_group_id).lower() == "all":
                team["machine_group_id_list"][index] = ("all")
            elif machinegroupsDB.get_machine_groups(machine_group_id) and len(machinegroupsDB.get_machine_groups(machine_group_id)) > 0:
                team["machine_group_id_list"][index] = machinegroupsDB.get_machine_groups(
                    machine_group_id)["group_name"]

    if team.get("users_id_list") and len(team.get("users_id_list")) > 0:
        for index, user_id in enumerate(team.get("users_id_list")):
            if str(user_id).lower() == "all":
                team["users_id_list"][index] = ("all")
            elif userDB.get_user_by_id(user_id, False) and len(userDB.get_user_by_id(user_id, False)) > 0:
                team["users_id_list"][index] = userDB.get_user_by_id(user_id, False)[
                    "user"]

    return jsonify(json.loads(dumps({"result": "success", "data": team}))), 200


@manageTeamsAPINs.route('/update', methods=['PUT'])
class UpdateTeam(Resource):
    @api.expect(header_parser,ManageTeamsModel.update_teams_input_model,validate=True)
    @api.marshal_with(generic_response_model)
    @authService.authorized
    def put(self):
        teamDetails = request.get_json()
        if teamDetails.get("team_name"):
            HelperServices.validate_name(teamDetails.get("team_name"),"team name")
        updated_team = teamDB.update_team(teamDetails)     
        teamService.generate_details()
        return {"result": "success", "message": "Team Group updated successfully"}, 200        


@manageTeamsAPI.route('/teams/delete/<string:team_id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/ManageTeamsAPI/DeleteTeam.yml')
def DeleteTeam(team_id):
    teamService.generate_details()
    return jsonify(json.loads(dumps({"result": "success", "message": "The team was deleted successfully"}))), 200

