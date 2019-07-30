from flask import Blueprint, request

from DBUtil import Tags
from Services import TeamService, TagHelperService,HelperServices
from Services.AppInitServices import authService
from settings import mongodb
from flask_restplus import Resource
from modules.apimodels import TagModel
from modules.apimodels.Restplus import api,header_parser
from modules.apimodels.GenericReponseModel import generic_response_model


tagAPI = Blueprint('TagAPI', __name__)
tagAPINs = api.namespace('tag', description='Tag Operations')

# get global db connection
db = mongodb
tagDB = Tags.Tags()
teamService = TeamService.TeamService()
 

@tagAPINs.route('/all', methods=['GET'])
class getalltag(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(TagModel.get_all_tags_response_model)
    @authService.authorized
    def get(self):
        return {"result": "success", "data": list(tagDB.get_tags())}, 200


@tagAPINs.route('/view/<id>', methods=['GET'])
@api.doc(params={'id':'Tag ID'})
class getTagbyID(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(TagModel.get_tag_by_id)
    @authService.authorized
    def get(self, id):
        return {"result": "success", "data": tagDB.get_tag_by_id(id)}, 200


@tagAPINs.route('/new', methods=['POST'])
class addNewTag(Resource):
    @api.expect(header_parser,TagModel.add_tag_input_model, validate=True)
    @api.marshal_with(TagModel.add_tag_response_model)
    @authService.authorized
    def post(self):
        newTag = request.get_json()
        if (newTag.get("name"))is None:
            raise Exception("Mandatory fields name to create a new Tag was not found.")
        if tagDB.get_tag_by_name(newTag.get("name")) is not None:
            raise Exception("Tag with name " + newTag.get("name") + " already exists")
        HelperServices.validate_name(newTag.get("name"),"tag name")
        tag_id = tagDB.add_tag(newTag)
        # RELOAD TEAM PERMISSIONS
        teamService.generate_details()
        return {"result": "success", "message": "The Tag is saved successfully", "data": {"id": tag_id}}, 200


@tagAPINs.route('/update', methods=['PUT'])
class update_tag(Resource):
    @api.expect(header_parser,TagModel.update_tag_input_model, validate=True)
    @api.marshal_with(generic_response_model)
    @authService.authorized
    def put(self):
        tag = request.get_json()        
        if (tag.get("name"))is None:
            raise Exception("Mandatory fields name to create a new Tag was not found.")
        if tagDB.get_tag_by_name(tag.get("name")) is not None:
            raise Exception("Tag with name " + tag.get("name") + " already exists")
        HelperServices.validate_name(tag.get("name"),"tag name")
        is_updated = tagDB.update_tag(tag)
        if is_updated == 1:
            # RELOAD TEAM PERMISSIONS
            teamService.generate_details()
            return {"result": "success", "message": "The Tag is updated successfully"}, 200
        else:
            raise Exception ("Tag was not updated")


@tagAPINs.route('/delete/<string:id>', methods=['DELETE'])
@api.doc(params={'id':'Tag Id'})
class deleteTag(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(TagModel.delete_tag_response_model)
    @authService.authorized
    def delete(self,id):
        TagHelperService.delete_tag(id)
        # RELOAD TEAM PERMISSIONS
        teamService.generate_details()
        return {"result": "success", "message": "Tag was deleted", "data": "1"}, 200
    