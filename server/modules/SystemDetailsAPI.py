'''
Created on Aug 10, 2016

@author: sjajula
'''

import json
from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from DBUtil import CloneRequest, SystemDetails
from Services.AppInitServices import authService
from settings import mongodb, current_path, logo_full_path, logo_path
from flask_restplus import Resource
from modules.apimodels import SystemDetailsModel
from modules.apimodels.Restplus import api,header_parser



# blueprint declaration
systemdetailsAPI = Blueprint('systemdetailsAPI', __name__)
#restplus delaration
systemdetailsAPINs = api.namespace('systemdetails', description='System Details Operations')

# get global db connection
db = mongodb


# collections
cloneRequestDB = CloneRequest.CloneRequest(db)
systemDetailsDB = SystemDetails.SystemDetails(db)
# classes


@systemdetailsAPI.route('/systemdetails/logoupload', methods=['POST'])
@authService.authorized
def upload_account_logo():
    # This is the path to the upload directory
    try:
        # Get the name of the uploaded file
        file = request.files['file']
        ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
        filename = None
        if file is not None:
            filename = ('.' in file.filename and
                        str(file.filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS)
        else:
            raise Exception(" File not found in request")
        if filename not in [True]:
            raise Exception("Invalid file .Please select file 'png', 'jpg', 'jpeg', 'gif'")
        # Check if the file is one of the allowed types/extensions
        file_path = str(logo_full_path + '/' + "Account_logo" +
                        "." + file.filename.rsplit('.', 1)[1])
        file.save(file_path)

        FilePath = {"account_logo": str(
            logo_path + '/' + "Account_logo" + "." + file.filename.rsplit('.', 1)[1])}
        SysDetails = systemDetailsDB.get_system_details_single()
        FilePath["_id"] = {"oid": str(SysDetails["_id"])}
        for key in FilePath.keys():
            if key not in ["_id"] and key not in FilePath.keys():
                FilePath[key] = SysDetails[key]
        systemDetailsDB.update_system_details(FilePath)
        return jsonify(json.loads(dumps({"result": "success", "message": "Account logo uploaded successfully"}))), 200
    finally:
        try:
            file.close()
        except Exception as e:
            print e

@systemdetailsAPINs.route('/get_logo', methods=['GET'])
class get_account_logo(Resource):
    @authService.unauthorized
    @api.marshal_with(SystemDetailsModel.get_logo_response_model)
    def get(self):
        sys_details = systemDetailsDB.get_system_details_single()
        return {"result": "success", "message": "Account logo path", "data": {"account_logo": sys_details.get("account_logo","")}}, 200
        
    
@systemdetailsAPI.route('/systemdetails/add', methods=['POST'])
@authService.authorized
def addDistributionCenterDistributionRequest():
    SystemDetails = request.get_json()
    if not SystemDetails:
        raise ValueError("No data in input")
    found = systemDetailsDB.get_system_details_single()
    if found is None:
        updated = systemDetailsDB.add_system_details(SystemDetails)
    else:
        SystemDetails["_id"] = {"oid": str(found["_id"])}
        for key in found.keys():
            if key not in ["_id"] and key not in SystemDetails.keys():
                SystemDetails[key] = found[key]
        updated = systemDetailsDB.update_system_details(SystemDetails)
    return jsonify(json.loads(dumps({"result": "success", "message": "System Details updated", "data": str(updated)}))), 200


@systemdetailsAPINs.route('/all', methods=['GET'])
class get_sys_detail(Resource):
    @authService.unauthorized
    @api.marshal_with(SystemDetailsModel.get_all_sysdet_response_model)
    def get(self):
        return {"result": "success", "data": systemDetailsDB.get_system_details_single()}, 200

