import json
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify

from DBUtil import Permissions, PermissionGroup
from Services.AppInitServices import authService
from settings import mongodb, relative_path


# blueprint declaration
permissionAPI = Blueprint('permissionAPI', __name__)

# get global db connection
db = mongodb

# collections
permissiondb = Permissions.Permissions(db)
groupPermissiondb = PermissionGroup.PermissionGroup(db)


@permissionAPI.route('/grouppermissions/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/PermissionAPI/getAllGroupPermissions.yml')
def getAllGroupPermissions():
    per_list = groupPermissiondb.get_all_group_permission(True)
    return jsonify(json.loads(dumps({"result": "success", "data": per_list}))), 200
