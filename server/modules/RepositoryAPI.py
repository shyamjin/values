from DBUtil import Repository
from settings import mongodb
from flask import request,jsonify
from flask_restplus import Resource
from modules.apimodels.Restplus import api,header_parser
from Services import RepositoryHelperService, HelperServices
from modules.apimodels import RepositoryAPIModel
from Services.AppInitServices import authService
from bson.json_util import dumps
import json
RepositoryAPINs = api.namespace('repository', description='Repository Operations',path="/repository")

# get global db connection
db = mongodb

# collection
Repositorydb = Repository.Repository()

@RepositoryAPINs.route('/add', methods=['POST'])
class add_repository(Resource):
    @api.expect(header_parser,RepositoryAPIModel.repo_create_request,validate=True)
    @api.marshal_with(RepositoryAPIModel.repo_create_response)
    @authService.authorized
    def post(self):
        repo_data = request.get_json()
        repo_id = RepositoryHelperService.add_repo(repo_data)
        return {"result": "success", "message": "Repository was created successfully", "data": {"_id": repo_id }}, 200
        

@RepositoryAPINs.route('/update', methods=['PUT'])
class update_repository(Resource):
    @api.expect(header_parser,RepositoryAPIModel.repo_update_request,validate=True)
    @api.marshal_with(RepositoryAPIModel.repo_update_response)
    @authService.authorized
    def put(self):
        repo_data = request.get_json()
        update_count = RepositoryHelperService.update_repo(repo_data)
        return {"result": "success", "message": "Repository was updated successfully", "data": update_count}, 200

@RepositoryAPINs.route('/delete/<object_id>', methods=['DELETE'])
@api.doc(params={'object_id':'Repo object_id'})
class delete_repository(Resource):
    @api.expect(header_parser,validate=True)
    @api.marshal_with(RepositoryAPIModel.generic_response_model)
    @authService.authorized
    def delete(self,object_id):
        RepositoryHelperService.delete_repo(object_id)
        return {"result": "success", "message": "Repository was deleted successfully"}, 200
        
@RepositoryAPINs.route('/view/all', methods=['GET'])
class all_repository(Resource):
    @api.expect(header_parser,validate=True)
    #@api.marshal_with(RepositoryAPIModel.repo_get_all_response)
    @authService.authorized
    def get(self):
        return json.loads(dumps({"result": "success",  "data": list(Repositorydb.get_all())})), 200
   
#CALLED BY CLONE
@RepositoryAPINs.route('/view/name/<name>', methods=['GET'])
@api.doc(params={'name':'Repo Name'})
class repository_by_name(Resource):
    @api.expect(header_parser,validate=True)
    @authService.authorized
    def get(self,name):
        data = Repositorydb.get_repository_by_name(name,True)
        if data:
            return json.loads(dumps({"result": "success",  "data": data})), 200
        else:
            raise Exception("No repository found with name : "+ name )
    
@RepositoryAPINs.route('/view/<object_id>', methods=['GET'])
@api.doc(params={'object_id':'Repo object_id'})
class repository_by_id(Resource):
    @api.expect(header_parser,validate=True)
    @authService.authorized
    def get(self,object_id):
        data=Repositorydb.get_repository_by_id(object_id,True)
        if data:
            return json.loads(dumps({"result": "success","data": Repositorydb.get_repository_by_id(object_id,True)})), 200
        else:
            raise Exception("No repository found with id : "+ object_id )
    
    
# Using repository_by_name
@RepositoryAPINs.route('/view/byparententity/<parent_entity_id>', methods=['GET'])
@api.doc(params={'parent_entity_id':'Tool Version/Du Id'})
class repository_by_parent_entity(Resource):
    @api.expect(header_parser,validate=True)
    @authService.authorized
    def get(self,parent_entity_id):
        return repository_by_name().get(HelperServices.get_details_of_parent_entity_id(parent_entity_id).get("repository_to_use"))
        
