import json
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from DBUtil import Role, PermissionGroup, Users
from Services.AppInitServices import authService
from settings import mongodb, relative_path
from modules.apimodels.Restplus import api, header_parser
from flask_restplus import Resource
from modules.apimodels import RolesModel
from modules.apimodels.GenericReponseModel import generic_response_model

# blueprint declaration
roleAPI = Blueprint('roleAPI', __name__)
roleAPINs = api.namespace('roles', description='Roles Operations',path="/role")
# get global db connection
db = mongodb
roledb = Role.Role(db)
groupPermissiondb = PermissionGroup.PermissionGroup(db)
userdb = Users.Users(db)


@roleAPI.route('/role/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/RoleAPI/getAllRoles.yml')
def getAllRoles():
    role_list = roledb.get_all_roles()
    return jsonify(json.loads(dumps({"result": "success", "data": role_list}))), 200


@roleAPINs.route('/list/update', methods=['PUT'])
class UpdateRoleFromList(Resource):
    @api.expect(RolesModel.update_model,header_parser, validate=True)
    @api.marshal_with(generic_response_model)
    @authService.authorized
    def put(self):
        role_data_list = request.get_json()
        # PERFORM VALIDATIONS
        for role_data in role_data_list.get("roles"):
            if not roledb.get_role_by_id(role_data.get("role_id"), False):
                raise ValueError(
                    "No such role found with _id:" + role_data.get("role_id"))
            if role_data.get("permissiongroup"):
                for rec in role_data.get("permissiongroup"):
                    if not groupPermissiondb.get_group_permission_by_id(rec, False):
                        raise ValueError(
                            "GroupPermission id :" + rec + " from permissiongroup array was not found.")
        # UPDATE DATA
        for role_data in role_data_list.get("roles"):
            role_data["_id"] = {"oid": role_data.get("role_id")}
            role_data.pop("role_id")
            roledb.update_role(role_data)
        return {"result": "success", "message": "Role was updated"}, 200
