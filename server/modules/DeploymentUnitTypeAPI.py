import json
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify
from Services.AppInitServices import authService
from DBUtil import DeploymentUnitType, Users, SystemDetails
from settings import mongodb, relative_path


# blueprint declaration
deploymentUnitTypeAPI = Blueprint('deploymentUnitTypeAPI', __name__)

# get global db connection
db = mongodb
deploymentUnitTypeDB = DeploymentUnitType.DeploymentUnitType()
userDB = Users.Users(db)
systemDetailsDB = SystemDetails.SystemDetails(db)


@deploymentUnitTypeAPI.route('/deploymentunittype/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/DeploymentUnitTypeAPI/getallDeploymentUnitType.yml')
def getallDeploymentUnitType():
    return jsonify(json.loads(dumps({"result": "success", "data": deploymentUnitTypeDB.GetDeploymentUnitType()}))), 200
