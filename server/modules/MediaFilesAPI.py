import json
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from bson.json_util import dumps
from DBUtil import MediaFiles, Versions
from Services.AppInitServices import authService
from settings import mongodb, relative_path
from flask_restplus import Resource
from modules.apimodels import MediaFilesModel
from modules.apimodels.Restplus import api,header_parser
from modules.apimodels.GenericReponseModel import generic_response_model


# blueprint declaration
mediafilesAPI = Blueprint('mediafilesAPI', __name__)
#restplus delaration
mediafilesAPINs = api.namespace('mediafiles', description='Media Files Operations')




# get global db connection
db = mongodb
# collections
mediaFilesDB = MediaFiles.MediaFiles(db)
versionsDB = Versions.Versions(db)

# classes

@mediafilesAPINs.route('/update', methods=['PUT'])
class UpdateMediaFile(Resource):
    @api.expect(header_parser,MediaFilesModel.update_media_files,validate=True)
    @api.marshal_with(generic_response_model)
    @authService.authorized
    def put(self):
        data = request.get_json()
        backup_of_mediafiles = []
        # PERFORM VALIDATION
        for rec in data.get("data"):
            # CHECK IF parent_entity_id exists
            if not rec.get('_id'):
                raise Exception("_id not found in request:")
            # CHECK IF version exists with parent_entity_id
            if not rec.get('media_files') or len(rec.get('media_files')) < 1 or type(rec.get('media_files')) is not list:
                raise Exception("media_files not found or invalid media_files found in request")                                
            # CHECK IF media file exists with _id
            media_file_data = mediaFilesDB.get_media_file_by_id(
                str(rec.get('_id').get("oid")))
            if not media_file_data:
                raise Exception("MediaFiles with _id:" + rec.get('_id').get("oid") + " does not exists in database")
            else:
                media_file_data["_id"] = {"oid": str(media_file_data["_id"])}
                backup_of_mediafiles.append(media_file_data)
        # PERFORM UPDATES
        for rec in data.get("data"):
            updated = mediaFilesDB.update_media_files(rec)  # Missing Method
            if updated != 1:
                for recOfBackup in backup_of_mediafiles:
                    mediaFilesDB.update_media_files(recOfBackup)                
        return {"result": "success", "message": "The Mediafiles were updated successfully"}, 200

@mediafilesAPI.route('/mediafiles/delete/<string:id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/MediaFilesAPI/DeleteMediaFile.yml')
def DeleteMediaFile(id):
    isDeleted = mediaFilesDB.delete_media_file(id)  # Missing Method
    if isDeleted == 1:
        return jsonify(json.loads(dumps({"result": "success", "message": "The media file was deleted successfully"}))), 200
    else:
        raise Exception("The media file is not found")
    