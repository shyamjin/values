import os,json,uuid
from bson.json_util import dumps
from flask import Blueprint, jsonify, request
from werkzeug import secure_filename
from DBUtil import Versions, Build, Documents, DeploymentRequest, DeploymentFields, MediaFiles, ToolInstallation, Tool
from Services import FileUtils
from Services.AppInitServices import authService
from settings import mongodb, media_path, media_full_path


# blueprint declaration
versionAPI = Blueprint('versionAPI', __name__)

# get global db connection
db = mongodb


# collections
versionsDB = Versions.Versions(db)
buildDB = Build.Build()
documentsDB = Documents.Documents(db)
deploymentRequestDB = DeploymentRequest.DeploymentRequest(db)
deploymentFieldsDB = DeploymentFields.DeploymentFields(db)
mediaFilesDB = MediaFiles.MediaFiles(db)
toolInstallationDB = ToolInstallation.ToolInstallation(db)
tooldb = Tool.Tool(db)
# classes


@versionAPI.route('/tool/versions/uploadScreenshot', methods=['POST'])
@authService.authorized
def Upload_screenshots():
    uploaded = False
    ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp']
    version_id = request.form.get('version_id')
    if version_id is None:
        raise Exception("version_id not specified")
    if versionsDB.get_version(version_id, False) is None:
        raise Exception("Version not found in db")
    # check file NAMES
    for file in request.files:
        file = request.files[file]
        filename = ('.' in file.filename and
                    str(file.filename.rsplit('.', 1)[1]).lower() in ALLOWED_EXTENSIONS)
        if filename not in [True]:
            raise Exception("Invalid file name :" + str(file.filename))
    # This is the path to the upload directory
    data = {}
    data["parent_entity_id"] = version_id
    media_files = []
    uploaded_file = []
    # Get the name of the uploaded file
    for file in request.files:
        file = request.files[file]
        # Check if the file is one of the allowed types/extensions
        if file and filename:
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            file_extension = filename.split(".")[-1]
            # Redirect the user to the uploaded_file route, which
            # will basically show on the browser the uploaded file
            result1 = versionsDB.get_version(version_id, False)
            tool_id = result1["tool_id"]
            result2 = tooldb.get_tool_by_id(tool_id, False)
            toolname = '_'.join(result2["name"].split())
            uniqeid = str(uuid.uuid4())
            # Move the file form the temporal folder to
            # the upload folder we setup
            file_path = str(media_full_path + '/' + toolname +
                            "_" + uniqeid + '.' + file_extension)
            thumbnail_file_path = (str(
                media_full_path + '/' + toolname + "_" + uniqeid + '_thumbnail.' + file_extension))
            relative_thumbnail_file_path = str(
                media_path + '/' + toolname + "_" + uniqeid + '_thumbnail.' + file_extension)
            relative_file_path = str(
                media_path + '/' + toolname + "_" + uniqeid + '.' + file_extension)
            file.save(file_path)
            if not os.path.isfile(file_path):
                raise Exception(
                    "Failed to save screenshot to path :" + file_path)
            if None is FileUtils.thumbnail(file_path, thumbnail_file_path):
                relative_thumbnail_file_path = relative_file_path
            if not os.path.isfile(thumbnail_file_path):
                print "Failed to save screenshot thumbnail to path :" + thumbnail_file_path
            uploaded_file.append(file_path)
            filepath = file_path + '/log'
            if os.path.isfile(file_path):
                uploaded = True
                jsonEntry = {}
                jsonEntry["name"] = filename
                jsonEntry["content"] = " "
                jsonEntry["url"] = relative_file_path
                jsonEntry["thumbnail_url"] = relative_thumbnail_file_path
                jsonEntry["type"] = "image"
                jsonEntry["tooltip"] = "Tool Screenshot"
                media_files.append(jsonEntry)
            else:
                uploaded = False
                raise Exception('Unable to Save file in Target directory')
    if uploaded in [True]:
        data["media_files"] = media_files
        mediaEntry = mediaFilesDB.get_media_files(str(result1["_id"]))
        if mediaEntry:
            data["_id"] = {}
            data["_id"]["oid"] = str(mediaEntry["_id"])
            if mediaEntry.get("media_files"):
                if data.get("media_files"):
                    for rec in mediaEntry.get("media_files"):
                        data.get("media_files").append(rec)
            mediafileId = mediaFilesDB.update_media_files(data)
        else:
            mediafileId = mediaFilesDB.add_media_files(data)
        if mediafileId is None or mediafileId == 0:
            raise Exception('Unable to Add Media file in collection')
        else:
            return jsonify(json.loads(dumps({"result": "success", "message": "The Media Files was updated successfully and is readable"}))), 200
    else:
        if str(len(uploaded_file)) in ["0"]:
            raise Exception('No files were found in request')
        raise Exception('Unable to save images')
