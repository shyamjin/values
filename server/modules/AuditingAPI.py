from flask_restplus import Resource
from modules.apimodels.Restplus import api,header_parser
from flask import request
import json
from DBUtil import Auditing
from Services.AppInitServices import authService
from Services import Utils


auditdb = Auditing.Auditing()
auditingAPINs = api.namespace('auditing', description='Auditing Operations')

@auditingAPINs.route('/view/all', methods=['GET'])
class get_audit_all(Resource):
    @api.expect(header_parser, validate=True)
    @authService.authorized
    def get(self):
        """
        Get all auditing attributes
        """
        limit = int(request.args.get('perpage', "0"))
        page = int(request.args.get('page', "0"))
        user = request.args.get('user', None)
        api_type  = request.args.get('apitype',None)
        response_status_code = request.args.get('responsestatuscode', None)
        request_type = request.args.get('requesttype', None)
        filter={}
        if user:
            user=user.split(",")
            if "any" not in user:
                filter["user"]={}
                filter["user"]["$in"]=user
        if  api_type:
            api_type=api_type.split(",")
            if "any" not in api_type:
                filter["api_type"]={}
                filter["api_type"]["$in"]=api_type
        if  response_status_code:
            response_status_code=response_status_code.split(",")
            if "any" not in response_status_code:
                response_status_code= map(int, response_status_code)
                filter["response_status_code"]={}
                filter["response_status_code"]["$in"]=response_status_code
        if  request_type:
            request_type=request_type.split(",")
            if "any" not in request_type:
                filter["request_type"]={}
                filter["request_type"]["$in"]=request_type
        
        skip = page * limit
        return json.loads(Utils.JSONEncoder().encode({"result": "success",  "data": list(auditdb.get_all(skip,limit,filter)),
                    "message": "Auditing records were retrieved successfully"})), 200


@auditingAPINs.route('/view/id/<oid>', methods=['GET'])
@api.doc(params={'oid':'Object Id'})
class get_audit_by_id(Resource):
    @api.expect(header_parser, validate=True)
    @authService.authorized
    def get(self,oid):
        """
        Get all auditing attributes
        """
        audit_data=auditdb.get_audit_by_id(oid)
        return json.loads(Utils.JSONEncoder().encode({"result": "success",  "data": audit_data})), 200