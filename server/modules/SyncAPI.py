from datetime import datetime
import os,json
import copy
from os.path import join
import shutil
import uuid
import math
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request, send_file
from werkzeug import secure_filename

from DBUtil import Sync, SyncRequest, Config, SavedExports, Users
from Services import SyncServices, FileUtils,PullServices, PushServices,SyncHelperService,Utils,CleanerServices
from Services.AppInitServices import authService
from settings import mongodb, import_full_path, export_full_path, export_path, relative_path, saved_export_full_path, \
    saved_export_path
from flask_restplus import Resource
from modules.apimodels.Restplus import api, header_parser
from modules.apimodels import SyncAPIModel
from modules.apimodels.GenericReponseModel import generic_response_model

# get global db connection
db = mongodb

# blueprint declaration
syncAPI = Blueprint('syncAPI', __name__)
# restPlus Declaration
syncAPINs = api.namespace('sync', description='Sync Operations',path="/sync")


# get global db connection
db = mongodb

# collection

syncDb = Sync.Sync(db)
userDb = Users.Users(db)
configDb = Config.Config(db)
cleanerServices = CleanerServices.CleanerServices(mongodb)


SavedExportsDb = SavedExports.SavedExports()
syncRequestDb = SyncRequest.SyncRequest(db)
syncService = SyncServices.SyncServices()
pullService = PullServices.PullServices()
pushService = PushServices.PushServices()

@syncAPINs.route('/savedexports', methods=['GET'])
class get_saved_exports(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(SyncAPIModel.get_saved_exports_response_model)
    @authService.authorized
    def get(self):
        return {"result": "success", "data": list(SavedExportsDb.get_exports())}, 200

# Route that will process the file upload


@syncAPI.route('/sync/import', methods=['POST']) 
@authService.authorized
def upload_manual_sync_file():
    file_path=None
    folder_path=None
    try:
        sync_id = None
        inserted_ids = []
        # Get the name of the uploaded file
        file = request.files['file']
        if file is None:
            raise ValueError("No file selected")
        filename = ('.' in file.filename and
                    file.filename.rsplit('.', 1)[1] in ['zip'])
        if filename not in [True]:
            raise Exception("Invalid file .Please select file of type 'zip'")
    # Check if the file is one of the allowed types/extensions
        if file and filename:
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            file_name_without_ext = filename.split(".")[0]
            import_path = str(import_full_path)
            temp_folder_path=str(import_full_path + '/' + file_name_without_ext)
            if os.path.isfile(temp_folder_path + "_done.zip") or os.path.exists(temp_folder_path):
                raise Exception("This file was already requested")
            folder_path = temp_folder_path
            file_path = str(import_full_path + '/' + filename)
            if os.path.isfile(file_path): os.remove(file_path)
            file.save(file_path)
            folder_path = os.path.normpath(
                FileUtils.unzipImportFile(file_path))
            toolJsonData = FileUtils.returnJsonFromFiles(
                folder_path, "data.json")
            SyncHelperService.validate_sync_data_from_json(toolJsonData)
            for rec in toolJsonData:
                # THIS IS USED IN CLEANER SERVICES
                rec["stored_folder_name"] = folder_path
                if request.form.get('callback_url'):rec["callback_url"]=request.form.get('callback_url')
                inserted_ids.append(syncDb.add_sync(rec))
                if not sync_id:
                    sync_id = rec.get("sync_id")
            FileUtils.renameFile(file_path, join(
                import_path, os.path.splitext(filename)[0] + "_done.zip")) 
            if request.form.get("skip_process_ind","false").lower()=="true":
                return jsonify(json.loads(dumps({"result": "success", "message":"File uploaded successfully.","data":sync_id}))), 200
            else:
                try:
                    syncService.job_function()
                except Exception as e:  # catch *all* exceptions
                    print str(e)
                sync_data=syncService.analyse_sync_details(sync_id,False)
                return jsonify(json.loads(dumps({"result": "success", "message": "File was uploaded successfully. " +
                                 sync_data.get("added") + " entities were processed.Success: " +
                                 sync_data.get("success_count")  + " Failed: " + sync_data.get("failed_count"),
                                 "data": sync_data.get("data")}))), 200
    except Exception as e:  # catch *all* exceptions
        if file_path is not None:
            if os.path.isfile(file_path):
                os.remove(file_path)
        if folder_path is not None:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                if os.path.isfile(folder_path + "_done.zip"):
                    os.remove(folder_path + "_done.zip")
        for ids in inserted_ids:
            syncDb.remove_sync(str(ids))
        raise e    
        

'''

Input Json :
{
    "target_host": "cgfdg",
    "filters_to_apply": {
        "type": "du",
        "time_after": "9999-11-02T18:30:00.000Z",
        "approval_status": "Any",
        "tags": ["any"],
        "package_state_name": ["sdfdsf","^T"]
    },
    "external_artifacts": true
}
'''
@syncAPI.route('/sync/manual/export', methods=['POST'])
@authService.authorized
@swag_from(relative_path + '/swgger/SyncAPI/manualExport.yml')
def export_manual_sync_file():
    file_created = None
    try:
        # CREATE TOOL DETAILS FILE
        data = request.get_json()
        sync_id = str(uuid.uuid4())
        if data.get("filters_to_apply"):
            if data.get("filters_to_apply").get("time_after"):
                data["filters_to_apply"]["time_after"] = datetime.strptime(
                    data["filters_to_apply"]["time_after"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
        print " Main : A manual export was requested for host :" + data.get("target_host") + " id :" + sync_id
        file_created, toolName, toolNamesNotExported = syncService.createZipToExport({"file_path":export_full_path,"zip_file_name":sync_id,\
                                                                                      "target_host":data.get("target_host"),"sync_type":"manual","external_artifacts":data.get("external_artifacts")},copy.deepcopy(data.get("filters_to_apply")))
        print " Main : A manual export was completed for host :" + data.get("target_host") + " id :" + sync_id
        filename = os.path.basename(file_created)
        shutil.copy(file_created, saved_export_full_path)
        user_id = authService.get_userid_by_auth_token()
        export_data = {"user": userDb.get_user_by_id(user_id, False)["user"], "export_date": datetime.now(), "no_of_exported": len(toolName), "no_of_not_exported": len(toolNamesNotExported), "export_size": str(float("{0:.2f}".format(os.path.getsize(
            file_created) / (1024 * 1024.0)))) + " MB", "file_name": filename, "exported": toolName, "not_exported": toolNamesNotExported, "file_path": saved_export_path + "/" + filename, "filters_to_apply": data.get("filters_to_apply"), "target_host": data.get("target_host")}
        SavedExportsDb.add_exports(export_data)
        SavedExportsDb.delete_extra_exports(saved_export_full_path)
        return jsonify(json.loads(dumps({"result": "success", "message": str(len(toolName)) + " entity were exported successfully", "data": {"file_path": str(export_path + "/" + filename), "tool_names": toolName, "tool_names_not_exported": toolNamesNotExported}}))), 200
        # return send_file(file_created, attachment_filename=filename,
        # as_attachment=True)
    except Exception as e:  # catch *all* exceptions
        if file_created:
            if os.path.isfile(file_created):
                os.remove(file_created)
        raise e


@syncAPI.route('/sync/pull/export', methods=['POST'])
@authService.authorized
@swag_from(relative_path + '/swgger/SyncAPI/pullExport.yml')
def export_pull_sync_file():
    file_created = None
    try:
        # CREATE TOOL DETAILS FILE
        data = request.get_json()
        print "Pull request was received from host :" + str(data.get("target_host"))
        sync_id = str(uuid.uuid4())
        
        file_created, toolName, toolNamesNotExported = syncService.createZipToExport({"file_path":export_full_path,"zip_file_name":sync_id,\
            "target_host":data.get("target_host"),"sync_type":"pull"}, data.get("filters_to_apply"))
        filename = os.path.basename(file_created)
        print "Pull request was completed completed for host :" + str(data.get("target_host"))
        return send_file(file_created, attachment_filename=filename, as_attachment=True)
    finally:
        if file_created:
            if os.path.isfile(file_created):
                os.remove(file_created)
    

@syncAPI.route('/sync/push/trigger/<string:targetHost>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/SyncAPI/getSyncTrigger.yml')
def run_manual_sync(targetHost):
    syncService.job_function()
    return jsonify(json.loads(dumps({"result": "success", "data": 1}))), 200


@syncAPI.route('/syncrequest/all', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/SyncAPI/getAllSyncRequest.yml')
def get_all_sync_requests():
    sync_list = syncRequestDb.get_all_sync_request()
    return jsonify(json.loads(dumps({"result": "success", "data": sync_list}))), 200

@syncAPI.route('/syncrequest/view/<string:id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/SyncAPI/getSyncRequestId.yml')
def get_sync_request_by_id(id):
    sync_list = syncRequestDb.get_sync_request_by_id(id)
    return jsonify(json.loads(dumps({"result": "success", "data": sync_list}))), 200

@syncAPI.route('/syncrequest/run/<string:sync_request_id>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/SyncAPI/runSyncRequestId.yml')
def run_sync_request_by_id(sync_request_id):
    validate_if_sync_is_running(sync_request_id)
    rec = syncRequestDb.get_sync_request_by_id(sync_request_id)
    rec["manual_invoke_ind"] = True
    if rec.get("sync_type").lower() in ["pull"]:
        pullService.syncCall(rec)
    elif rec.get("sync_type").lower() in ["push"]:
        pushService.syncCall(rec)        
    rec = syncRequestDb.get_sync_request_by_id(sync_request_id)
    return jsonify(json.loads(dumps({"result": "success", "message": "Request was completed - Status: " + str(rec.get("last_sync_status")) + " Message: " + str(rec.get("last_sync_message")), "data": rec}))), 200


@syncAPI.route('/syncrequest/update', methods=['PUT'])
@authService.authorized
def update_sync_request():
    sync_data = request.get_json()
    validate_if_sync_is_running(sync_data["_id"]["oid"])
    updated = syncRequestDb.update_sync_request(sync_data)
    return jsonify(json.loads(dumps({"result": "success", "message": "The SyncRequest was updated successfully", "data": updated}))), 200


@syncAPI.route('/syncrequest/delete/<string:sync_request_id>', methods=['DELETE'])
@authService.authorized
@swag_from(relative_path + '/swgger/SyncAPI/deleteSyncRequest.yml')
def delete_sync_request(sync_request_id):
    validate_if_sync_is_running(sync_request_id)
    isDeleted = syncRequestDb.remove_sync_request(sync_request_id)
    return jsonify(json.loads(dumps({"result": "success", "data": isDeleted, "message": "Sync request is deleted"}))), 200

@syncAPI.route('/sync/delete/<string:sync_id>', methods=['DELETE'])
@authService.authorized
def delete_sync(sync_id):
    recs = syncDb.get_sync_by_sync_id(sync_id)
    if recs:
        for rec in recs:
            if rec.get("stored_folder_name"):
                file_name = os.path.basename(rec.get("stored_folder_name"))
                break 
    syncDb.remove_sync_by_sync_id(sync_id)                       
    if os.path.exists(os.path.join(import_full_path, file_name)):
        cleanerServices.clean_old_data([import_full_path], file_name, -1)    
    return jsonify(json.loads(dumps({"result": "success", "message": "Sync is deleted"}))), 200
    
def validate_if_sync_is_running(sync_request_id):
    rec = syncRequestDb.get_sync_request_by_id(sync_request_id)
    if not rec:
        raise ValueError("No such sync request was found")
    if rec.get("sync_type").lower() in ["pull"]:
        db_data = configDb.getConfigByName("PullServices")
        if db_data.get("run_status") is not None and db_data.get("run_status").lower() in ["running"]:
            raise ValueError(
                "PullService is currently running.Please try again later")
    elif rec.get("sync_type").lower() in ["push"]:
        db_data = configDb.getConfigByName("PushServices")
        if db_data.get("run_status") is not None and db_data.get("run_status").lower() in ["running"]:
            raise ValueError(
                "PushService is currently running.Please try again later")
    else:
        raise ValueError("Invalid sync_type in request")

@syncAPI.route('/syncrequest/add', methods=['POST'])
@authService.authorized
def add_sync_request():
    NewSyncRequest = request.get_json()
    if NewSyncRequest.get("sync_type") is None:
        raise Exception("sync_type was not found in request")
    if NewSyncRequest.get("target_dpm_detail") is None:
        raise Exception("target_dpm_detail was not found in request")
    result = syncRequestDb.add_sync_request(NewSyncRequest)
    return jsonify(json.loads(dumps({"result": "success", "message": "New Sync request has been added successfully", "data": result}))), 200


@syncAPINs.route('/view/all', methods=['GET'])
class get_all_sync(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(SyncAPIModel.dep_view_all_response_model)
    @authService.authorized
    def get(self):
        limit = int(request.args.get('perpage', "30"))
        page = int(request.args.get('page', "0"))
        skip = page * limit
        syncs= syncDb.get_distinct_sync_id_by_status()
        if limit == 0:
            limit = len(list(syncs))
        c=1;
        sync_data=[]
        for sync in syncs:
            if c > skip and c <= skip+limit:
                sync_data.append(syncDb.get_sync_data_for_sync_all(sync))
            c=c+1
        return {"result": "success",  "data": {"data": list(sync_data), "page": page, "total": len(list(syncs)), "page_total": math.ceil((len(list(syncs))/float(limit)))}}, 200
 
           
@syncAPINs.route('/view/syncid/<sync_id>', methods=['GET'])
@api.doc(params={'sync_id':'Sync Id'})
class get_sync_by_sync_id(Resource):
    @api.expect(header_parser, validate=True)
    @authService.authorized
    def get(self,sync_id):
        filter_condition = {}
        limit = int(request.args.get('perpage', "30"))
        page = int(request.args.get('page', "0"))
        skip = page * limit
        if request.args.get('status', None):
            status_list = request.args.get("status").split(",")
            filter_condition["status"] = {"$in" : status_list}
        if request.args.get('operation', None):
            operation_list = request.args.get("operation").split(",")
            filter_condition["operation"] = {"$in" : operation_list}
        filter_condition["sync_id"] = sync_id
        sync_data = syncDb.get_sync_by_filter(filter_condition, skip, limit)            
        new=0
        retry=0
        compared=0
        success=0
        failed=0
        skipped=0
        sync_data.rewind() 
        total_data=syncDb.get_sync_by_sync_id(sync_id)    
        total= len(list(total_data))
        if total==0:
            raise Exception ("No sync request found with the sync id provided: " + sync_id)
        total_data.rewind()
        for sync in total_data:
            if sync.get("status").lower() == "new":
                new+=1
            elif sync.get("status").lower() == "retry":
                retry+=1
            elif sync.get("status").lower() == "compared":
                compared+=1
            elif sync.get("status").lower() == "success":
                success+=1
            elif sync.get("status").lower() == "failed":
                failed+=1  
            elif sync.get("status").lower() == "skipped":
                skipped+=1  
        if limit == 0:
            limit = total
        status="success"
        if failed >0:
            status = "failed" 
        elif  new+retry+compared >0:
            status = "running"        
        return json.loads(Utils.JSONEncoder().encode({"result": "success",  "data": {"data": list(sync_data),"new": new,"retry": retry,"compared": compared,"success": success, "failed": failed,"skipped":skipped, "total": total,"status": status, "page": page, "page_total": math.ceil((total/float(limit)))}})), 200

@syncAPINs.route('/retry', methods=['PUT'])
class retry_sync(Resource):
    @api.expect(header_parser,SyncAPIModel.retry_sync_input_model,validate=True)
    @api.marshal_with(generic_response_model)
    @authService.authorized
    def put(self):
        data = request.json
        return {"result": "success", "message": str(SyncHelperService.retry_sync(data.get("_id"),data.get("sync_id")))+" request updated successfully" }, 200
