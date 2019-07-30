from flask import request
from DBUtil import ProposedTools
from Services.AppInitServices import authService
from settings import mongodb
from flask_restplus import Resource
from modules.apimodels.Restplus import api, header_parser
from Services import ProposedToolsHelper
from modules.apimodels import ProposedToolsModel


# get global db connection
db = mongodb
proposedToolsAPINs = api.namespace('proposedtool', description='Proposed Tools Operations',path="/proposed/tool")
proposedToolsDB=ProposedTools.ProposedTools()



@proposedToolsAPINs.route('/new', methods=['POST'])
class CreatePT(Resource):
    @api.expect(ProposedToolsModel.pt_create_request, validate=True)
    @authService.unauthorized
    @api.marshal_with(ProposedToolsModel.pt_create_response)
    def post(self):
        """
        Create new PT definition
        """
        pt_create_request_details = request.get_json()
        proposed_data=ProposedToolsHelper.create_request(pt_create_request_details)
        pt_id = proposedToolsDB.add(proposed_data)
        ProposedToolsHelper.email_tool_proposed(pt_create_request_details)
        ProposedToolsHelper.email_approval_req(pt_create_request_details)
        return {"result": "success", "message": "Request Received.We will contact you soon! ", "data"\
                : {"_id": pt_id}}, 200

@proposedToolsAPINs.route('/approve', methods=['POST'])
class ApprovePT(Resource):
    @api.expect(header_parser,ProposedToolsModel.pt_approve_request, validate=True)
    @api.marshal_with(ProposedToolsModel.pt_create_response)
    @authService.authorized
    def post(self):
        """
        Approve new PT definition
        """
        pt_create_request_details = proposedToolsDB.get_by_id(request.json.get("_id"))
        request.json.update(pt_create_request_details)
        return ProposedToolsHelper.approve_tool(request)


@proposedToolsAPINs.route('/view/all', methods=['GET'])
class GetAll(Resource):   
    @api.expect(header_parser, validate=True)
    @api.marshal_with(ProposedToolsModel.pt_get_all_response)
    @authService.authorized
    def get(self):
        """
        Get all PT
        """
        return {"result": "success", "message": "PTs were retrieved successfully", "data": list(proposedToolsDB.get_all())}, 200


@proposedToolsAPINs.route('/view/<id>', methods=['GET'])
@api.doc(params={'id':'PT ID'})
class RetrievePTById(Resource): 
    @api.expect(header_parser, validate=True)
    @api.marshal_with(ProposedToolsModel.retrieve_pt_by_id_response)
    @authService.authorized  
    def get(self, id):
        """
        Retrieve PT by ID
        """
        pt = proposedToolsDB.get_by_id(id)
        return {"result": "success", "message": "PT was retrieved successfully", "data": pt}, 200
    
@proposedToolsAPINs.route('/delete/<id>', methods=['DELETE'])
@api.doc(params={'id':'PT ID'})
class DeletePTById(Resource): 
    @api.expect(header_parser, validate=True)
    @api.marshal_with(ProposedToolsModel.reject_pt_by_id_response)
    @authService.authorized  
    def delete(self, id):
        """
        delete PT by ID
        """
        pt_create_request_details = proposedToolsDB.get_by_id(id)
        proposedToolsDB.delete(id)
        ProposedToolsHelper.email_rejeted(pt_create_request_details)
        return {"result": "success", "message": "PT was rejected"}, 200    