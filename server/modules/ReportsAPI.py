import traceback

from bson.json_util import dumps
from flask import Blueprint, jsonify

from DBUtil import Users, SystemDetails, Reports
from Services.AppInitServices import authService
from settings import mongodb
from flask_restplus import Resource
from modules.apimodels.Restplus import api, header_parser
from modules.apimodels import GenericReponseModel,ReportsModel


# blueprint declaration
reportAPI = Blueprint('reportAPI', __name__)
reportAPINs = api.namespace('reports', description='Reports Operations')

# get global db connection
db = mongodb
reportsDB = Reports.Reports()
userDB = Users.Users(db)
systemDetailsDB = SystemDetails.SystemDetails(db)


@reportAPINs.route('/all', methods=['GET'])
class getallreports(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(ReportsModel.get_all_reports_response_model)
    @authService.authorized
    def get(self):
        """fetch all reports in DPM
            ---
            tags:
             - Reports
            parameters:
            - name: Token
              in: header
              description: API key
              required: false
              type: string
              format: string
    
            responses:
              200:
                description: A list of Reports
                examples:
                  result: "success"
                  message: null
              404:
                description: exception in fetching reports
                examples:
                  result: "failed"
                  message: "Throws an exception"
            """
        return {"result": "success", "data": list(reportsDB.GetReports())}, 200