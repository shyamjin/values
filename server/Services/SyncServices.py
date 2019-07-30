'''
Created on Mar 16, 2016

@author: PDINDA
'''
import logging
from os import listdir
import os
from os.path import join
import shutil
import subprocess
from threading import Lock
import time
import traceback
import copy
import requests
from autologging import logged
import json

from DBUtil import Config, Versions, Tool, DeploymentFields, Build,\
Machine, Sync, SyncRequest, Documents, MediaFiles, SystemDetails, Tags, PreRequisites, DeploymentUnit,DeploymentUnitSet,State,FlexibleAttributes
import FileUtils
from Services import Mailer, HelperServices,SyncHelperService,SchedulerService, ConfigHelperService,BuildHelperService,\
    DuHelperService,ToolHelperService, StateHelperService
from settings import mongodb, import_full_path, export_full_path, logo_path, logo_full_path, media_path, media_full_path, \
    plugin_full_path, plugin_directories_to_be_copied
from datetime import datetime
from Services.SyncInputDataHelper import SyncInputDataHelper



job = None
locker = Lock()


def synchronized(lock):
    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap


@logged(logging.getLogger("SyncServices"))
class SyncServices(object):

    # Init's Data
    def __init__(self):
        self.db = mongodb
        self.current_import_path = import_full_path
        if self.current_import_path in [None, ""]:
            raise ValueError("Import path was not provided")
        if not os.path.exists(self.current_import_path):
            os.makedirs(self.current_import_path)
        if not os.access(os.path.dirname(self.current_import_path), os.W_OK):
            raise ValueError(
                "The directory does not have write access :" + self.current_import_path)
        self.current_export_path = export_full_path
        if self.current_export_path in [None, ""]:
            raise ValueError("Export path was not provided")
        if not os.path.exists(self.current_export_path):
            os.makedirs(self.current_export_path)
        if not os.access(os.path.dirname(self.current_export_path), os.W_OK):
            raise ValueError(
                "The directory does not have write access :" + self.current_export_path)
        self.configdb = Config.Config(self.db)
        self.versionsDB = Versions.Versions(self.db)
        self.toolDB = Tool.Tool(self.db)
        self.deploymentFieldsDB = DeploymentFields.DeploymentFields(self.db)
        self.machineDB = Machine.Machine(self.db)
        self.syncDb = Sync.Sync(self.db)
        self.mailer = Mailer.Mailer()
        self.syncRequestDb = SyncRequest.SyncRequest(self.db)
        self.buildsDB = Build.Build()
        self.documentsDB = Documents.Documents(self.db)
        self.toolDB = Tool.Tool(self.db)
        self.deploymentunitDB = DeploymentUnit.DeploymentUnit()
        self.deploymentunitsetDB = DeploymentUnitSet.DeploymentUnitSet()
        self.mediaFilesDB = MediaFiles.MediaFiles(self.db)
        self.tagsDB = Tags.Tags()
        self.preRequisitesDB = PreRequisites.PreRequisites(self.db)
        self.logo_path = logo_path
        self.full_logo_path = logo_full_path
        self.media_files_path = media_path
        self.full_media_files_path = media_full_path
        self.systemDetailsDb = SystemDetails.SystemDetails(self.db)
        self.systemDetail = self.systemDetailsDb.get_system_details_single()
        self.statedb =  State.State(self.db)
        if not self.systemDetail:
            raise Exception("systemDeatils not found")
        self.config_id = 9
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()
        self.flexAttrDB = FlexibleAttributes.FlexibleAttributes()

    def load_configuration(self):
        ConfigHelperService.load_common_configuration(self)

    # This method runs in a given interval of  intervalGiven
    # if its already running then second instance will not get triggered
    # LOGIC
        # We are checking if we have any pending zip files to process (Only if listner is true)
        # For pending sync data perform compare and process them
    # YOU CANNOT IMPORT WHEN WE ARE PERFORMING A EXPORT.ALL METHODS SHOULD BE
    # LOCKED
    @ConfigHelperService.run
    @synchronized(locker)
    def job_function(self):
        """Start of SyncServices"""
        print 'started running at ' + time.ctime(time.time())
        print 'job_function:Will check if files are pending to process '
        self.load_configuration()
        SyncInputDataHelper().run_service() # CHECK IF NEW DATA IS AVAILABLE TO LOAD
        while self.syncDb.get_pending_sync_to_compare() is not None\
         or self.syncDb.get_pending_sync_to_process() is not None:
            try:
                SyncHelperService.compare_tools_for_sync()
                SyncHelperService.compare_dus_for_sync() # DU SHOULD ALWAYS SYNC FIRST
                SyncHelperService.compare_duset_for_sync()
                SyncHelperService.compare_states_for_sync() # DU/DUSET SHOULD ALWAYS SYNC FIRST
                self.process_additional_data()
                self.process_bulk_upload()
                self.process_sync()
            except Exception as e:
                raise e
            finally:
                self.callbackUrl()
        self.cleanSync()
        print 'ended running at ' + time.ctime(time.time())
   
    def cleanSync(self):
        print 'cleanSync:started'
        sync_ids = []
        for rec in self.syncDb.sync_all():
            if rec.get("status") <> None and str(rec.get("status")).lower() in ["success", "skipped"]:
                if str(rec["sync_id"]) not in sync_ids:
                    sync_ids.append(str(rec["sync_id"]))
        # Clean
        for sync_id in sync_ids:
            SyncHelperService.clean_processed_sync(sync_id)
        print 'cleanSync:ended'

    # Perform Process
    def process_additional_data(self):
        """Start of Processing process_additional_data"""
        # Gets all record for minimum sync_id sorted by _id and created_time
        pending_sync_list = self.syncDb.get_pending_sync_to_process()
        if pending_sync_list and pending_sync_list.count() > 0 :
            for record in pending_sync_list:
                print " process: Processing _id :" + str(record["_id"])
                try:
                    if not self.syncDb.get_sync_by_id(str(record["_id"])).get("processed_additional_data",False):
                        directory_to_import_from = SyncHelperService.get_source_dir(record)
                        if directory_to_import_from:
                            SyncHelperService.handle_additional_data_while_processing_sync(directory_to_import_from, plugin_full_path)
                            self.syncDb.update_add_processed_by_sync_id(record["sync_id"])
                except Exception as e_value:  # catch *all* exceptions
                    traceback.print_exc()
                    self.syncDb.update_sync_status(
                        str(record["_id"]), "failed", "Processing additional data failed with error" +str(e_value))
    
        # Perform Process
    def process_bulk_upload(self):
        pass
            
    # Perform Process
    def process_sync(self):
        """Start of Processing"""
        sync_id = sync_type = directory_to_import_from = None
        # Gets all record for minimum sync_id sorted by _id and created_time
        pending_sync_list = self.syncDb.get_pending_sync_to_process()
        if pending_sync_list:
            print 'No of Pending Sync List to process:' + str(pending_sync_list.count())
        else:
            print 'process:No of Pending Sync List to process:' + str(0) + ". Existing.."
            return
        for record in pending_sync_list:
            print " process: Processing _id :" + str(record["_id"])
            try:
                sync_id, sync_type = SyncHelperService.get_sync_id_and_type(record)
                directory_to_import_from = SyncHelperService.get_source_dir(record)
                distribution_list = None
                self.handle_extra_validations(record)
                print 'Process: Working on sync_id :' + sync_id + " _id :" + str(record["_id"])
                full_sync_flag, distribution_list = SyncHelperService.get_distribution_list_and_status(
                    self.result)  # Distribution_list can be empty # full_sync_flag is mandatory
                self.handle_operation(record, full_sync_flag, directory_to_import_from)
                print 'Process: Done on sync_id :' + sync_id + " _id :" + str(record["_id"])
            except Exception as e_value:  # catch *all* exceptions
                traceback.print_exc()
                self.syncDb.update_sync_status(
                    str(record["_id"]), "failed", str(e_value))
        # Notify Users
        SyncHelperService.notify(sync_id, distribution_list, self.mailer)

    def handle_extra_validations(self,record): 
        # VALIDATE THE TOOL DETAILS
        if record.get("tool_data"):
            ToolHelperService.validate_tool_data(
                record.get("tool_data"))
            # Update tool Dependency
            tooldata = record.get("tool_data")
            if tooldata and tooldata.get("versions"):
                versions_list = []
                versions = tooldata.get("versions")
                if versions and len(versions) > 0:
                    for VersionsData in versions:
                        versions_list.append(
                            ToolHelperService.set_dependend_tools(VersionsData, True))
                    record["tool_data"]["versions"] = versions_list
        elif record.get("du_data"):
            DuHelperService.validate_du_data(record.get("du_data"))
        elif record.get("duset_data"):
            DuHelperService.validate_duset_data(record.get("duset_data"))    
        elif record.get("state_data"):
            StateHelperService.check_state_mandate_fields(record.get("state_data"))
        else:    
            raise Exception(
                    "Validations:Conditions to process were not found")     
        
    def handle_insert_operation(self,record,full_sync_flag,directory_to_import_from):
        if record.get("tool_data"):
            return self.addtool(
                record, full_sync_flag.lower(), directory_to_import_from)
        if record.get("du_data"):
            return self.adddu(
                record, full_sync_flag.lower(), directory_to_import_from)
        elif record.get("duset_data"):
            return self.add_update_du_set(record, full_sync_flag, directory_to_import_from)
        elif record.get("state_data"):
            return self.add_update_state(record, full_sync_flag, directory_to_import_from)
        raise Exception(
                "Processing:Conditions to process were not found")    
        
    def handle_update_operation(self,record,full_sync_flag,directory_to_import_from):
        if record.get("tool_data"):
            return self.updatetool(
                record, full_sync_flag.lower(), directory_to_import_from)
        if record.get("du_data"):
            return self.updatedu(
                record, full_sync_flag.lower(), directory_to_import_from)
        elif record.get("duset_data"):
            return self.add_update_du_set(record, full_sync_flag, directory_to_import_from)
        elif record.get("state_data"):
            return self.add_update_state(record, full_sync_flag, directory_to_import_from)
        raise Exception(
                "Processing:Conditions to process were not found")  
          
    def handle_delete_operation(self,record,full_sync_flag,directory_to_import_from):
        if full_sync_flag.lower() == "true":
            if record.get("tool_data"):
                return ToolHelperService.delete_tool(record.get("tool_data").get("_id"),False)
            if record.get("du_data"):
                return DuHelperService.delete_du(record.get("du_data").get("_id"),False)
            elif record.get("duset_data"):
                return DuHelperService.delete_du_set(record.get("duset_data").get("_id"),False)
            elif record.get("state_data"):
                return StateHelperService.delete_state(record.get("state_data").get("_id"),False)
        elif full_sync_flag.lower() == "false":
            return {"result":"success","message":"Skipping as full_sync_flag is not true"}
        raise Exception(
                "Processing:Conditions to process were not found")    
    
    def handle_operation(self,record,full_sync_flag,directory_to_import_from):
        result={"result":"failed","message":"Conditions to process were not found"}        
        if record.get("operation").lower() == "insert":
            result=self.handle_insert_operation(record, full_sync_flag, directory_to_import_from)
        elif record.get("operation").lower() == "update":
            result=self.handle_update_operation(record, full_sync_flag, directory_to_import_from)
        elif record.get("operation").lower() == "delete":    
            result=self.handle_delete_operation(record, full_sync_flag, directory_to_import_from)
        else:
            raise Exception(
                "Processing:Conditions to process were not found.Skipping")
        self.syncDb.update_sync_status(
            str(record["_id"]), result.get("result"), result.get("message"))
        
    def addtool(self, tool, full_sync_flag="false", directory_to_import_from=None):
        """Start Tool Addition"""
        # MAINTAINING ARRAY TO MEMORISE INSERTED IDS
        inserted_tools_list = []
        inserted_build_list = []
        inserted_versions_list = []
        inserted_deployment_fields_list = []
        inserted_media_files_list = []
        inserted_documents_list = []
        tooldata = tool.get("tool_data")
        ToolHelperService.check_if_tool_exists(tooldata)
        try:
            tooldata = tool.get("tool_data")
            tool_inserted = ToolHelperService.add_update_tool(tool.get(
                "tool_data"), None, self.logo_path, directory_to_import_from, self.full_logo_path)
            inserted_tools_list.append(tool_inserted)
            versions = tooldata.get("versions")
            if versions is None:
                raise Exception("versions is missing from tool_data")
            for VersionsData in versions:
                Versionresult = ToolHelperService.add_update_version(
                    VersionsData, tool_inserted, None, False)
                inserted_versions_list.append(Versionresult)
                # preparing version data
                # preparing DeploymentFields data
                if VersionsData.get("deployment_field") is not None and len(VersionsData.get("deployment_field")) > 0:
                    inserted_deployment_fields_list.append(HelperServices.add_update_deployment_fields(
                        VersionsData.get("deployment_field")["fields"], Versionresult))
                if VersionsData.get('media_file') is not None \
                        and len(VersionsData.get('media_file')) > 0:
                    inserted_media_files_list.append(HelperServices.add_update_media_files(VersionsData.get('media_file'
                                                                                                         )['media_files'], Versionresult, directory_to_import_from, self.full_media_files_path, self.media_files_path))
                # preparing Document data
                if VersionsData.get("document") is not None and len(VersionsData.get("document")) > 0:
                    inserted_documents_list.append(HelperServices.add_update_documents(
                        VersionsData.get("document")["documents"], Versionresult))
                # preparing Build data
                if VersionsData.get("build") is not None and len(VersionsData.get("build")):
                    for build in VersionsData.get("build"):
                        inserted_build_list.append(BuildHelperService.add_update_build(
                            build, Versionresult, join(directory_to_import_from,os.path.join("artifacts",VersionsData["repository_to_use"]))))
            return {"result": "success", "message": tooldata["name"]+" was inserted"}
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            for rec in inserted_deployment_fields_list:
                self.deploymentFieldsDB.DeleteDeploymentFields(rec)
            for rec in inserted_media_files_list:
                self.mediaFilesDB.delete_media_file(rec)
            for rec in inserted_documents_list:
                self.documentsDB.DeleteDocuments(rec)
            for rec in inserted_versions_list:
                self.versionsDB.delete_version(rec)
            for rec in inserted_tools_list:
                self.toolDB.delete_tool(rec)
            for rec in inserted_build_list:
                self.buildsDB.delete_build(rec)
            return {"result": "failed", "message": str(e_value)}

    def adddu(self, du, full_sync_flag="false", directory_to_import_from=None):
        """Start Tool Addition"""
        # MAINTAINING ARRAY TO MEMORISE INSERTED IDS
        inserted_du_list = []
        inserted_build_list = []
        inserted_deployment_fields_list = []
        dudata = du.get("du_data")
        deployment_field = dudata.get("deployment_field")
        builds = dudata.get("build")
        DuHelperService.check_if_du_exists(dudata)
        try:
            du_inserted = DuHelperService.add_update_du(
                dudata, None, self.logo_path, directory_to_import_from, self.full_logo_path,False)
            inserted_du_list.append(du_inserted)
            if deployment_field is not None and len(deployment_field) > 0:
                inserted_deployment_fields_list.append(HelperServices.add_update_deployment_fields(
                    deployment_field["fields"], du_inserted))
            # preparing Build data
            if builds is not None and len(builds) > 0:
                for build in builds:
                    if build.get("to_process","true").lower()=="true":
                        inserted_build_list.append(BuildHelperService.add_update_build(
                            build, du_inserted, join(directory_to_import_from, os.path.join("artifacts",dudata["repository_to_use"]))))
            return {"result": "success", "message": dudata["name"]+" was inserted"}
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            for rec in inserted_deployment_fields_list:
                self.deploymentFieldsDB.DeleteDeploymentFields(rec)
            for rec in inserted_du_list:
                self.deploymentunitDB.DeleteDeploymentUnit(rec)
            for rec in inserted_build_list:
                self.buildsDB.delete_build(rec)
            return {"result": "failed", "message": str(e_value)}

    def add_update_state(self, state, full_sync_flag="false", directory_to_import_from=None):
        """Start State Addition/Update"""
        deployment_fields_data=None
        try:
            state_data=state.get("state_data")
            StateHelperService.convert_parent_names_to_ids(state_data,True)
            # IF DU STATE
            if state_data.get("build_id"):
                build=self.buildsDB.get_build_by_number(state_data.get("parent_entity_id"), state_data.get("build_id"), False)
                if build:
                    state_data["build_id"]=str(build.get("_id"))
                else:
                    raise Exception ("Build with number: "+str(state_data.get("build_id"))\
                                     +" and parent_entity_id: "+str(state_data.get("parent_entity_id")) +" was not found in DB")
            
            if state_data.get("deployment_field"):deployment_fields_data=state_data.get("deployment_field")
            # IF DU PACKAGE STATE
            if state_data.get("states"):
                StateHelperService.convert_parent_to_states(state_data) 
            existing_state=self.statedb.get_state_by_parent_entity_id_name(state_data.get("name"),\
                                                         state_data.get("parent_entity_id"), False)
            if existing_state:
                StateHelperService.add_update_state(state_data, str(existing_state.get("_id")))
                state_id=str(existing_state.get("_id"))
            else:
                state_id=str(StateHelperService.add_update_state(state_data,None))    
            if deployment_fields_data:
                HelperServices.add_update_deployment_fields(deployment_fields_data.get("fields"), state_id)        
            return {"result": "success", "message": state_data["name"] +" was handled"}
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            return {"result": "failed", "message": str(e_value)}  

    def updatetool(self, tool, full_sync_flag="false", directory_to_import_from=None):
        """Start Tool Update """
        tooldata = tool.get("tool_data")
        localTool = self.toolDB.get_tool_by_name(tooldata["name"])
        ToolHelperService.check_if_tool_data_is_valid(tooldata, localTool)
        tool_id = str(localTool.get("_id"))
        try:
            if tooldata.get("operation").lower() == "update":
                ToolHelperService.add_update_tool(
                    tooldata, tool_id, self.logo_path, directory_to_import_from, self.full_logo_path)
            versions = tooldata.get("versions")
            for record in versions:
                if record.get("operation") not in ["delete", "update", "insert"]:
                    continue
                VersionsData = record
                localVersion = self.versionsDB.get_version_by_tool_id_name_and_number(
                    tool_id, VersionsData["version_name"], VersionsData["version_number"])
                if localVersion:
                    version_id = str(localVersion["_id"])
                if record.get("operation").lower() == "delete" and full_sync_flag == "true":
                    SyncHelperService.delete_version_and_related_builds(version_id)
                else:
                    # HANDLE VERSION
                    # WE SEE THAT THE VERSION HAS TO BE BE UPDATED OR INSERTED

                    # IF ITS A EXISTING VERSION WE WILL ALREADY HAVE VERSION_ID
                    if record.get("operation").lower() == "update":
                        ToolHelperService.add_update_version(
                            VersionsData, tool_id, version_id, False)
                    # IF ITS A NEW VERSION
                    if record.get("operation").lower() == "insert":
                        version_id = ToolHelperService.add_update_version(
                            VersionsData, tool_id, None, False)
            
                    # HANLDE BUILD
                    if VersionsData.get('build') is not None and len(VersionsData.get('build')) > 0:
                        builds_handled = []  # WE need to deactivate all other builds
                        for build in VersionsData.get('build'):
                            BuildHelperService.add_update_build(
                                build, version_id, join(directory_to_import_from, os.path.join("artifacts",VersionsData["repository_to_use"])))
                            builds_handled.append(build["build_number"])
                        # SUPPOSE THE ACCOUNT SENDS 2 BUILDS THAT ARE  ACTIVE THEY WILL BE HANDLED
                        # BUT ALL OTHER BUILDS SHOULD BE MADE INACTIVE IN LOCAL
                        for build in self.buildsDB.get_all_builds(version_id):
                            if build["build_number"] not in builds_handled:
                                build_id = build.get("_id")
                                build["_id"] = {}
                                build["_id"]["oid"] = str(build_id)
                                build["status"] = "0"
                                self.buildsDB.update_build(build)

                    # HANLDE DOCUMENT
                    if VersionsData.get('document') is not None \
                            and len(VersionsData.get('document')) > 0:
                        HelperServices.add_update_documents(
                            VersionsData['document']['documents'], version_id)
            
                    # HANLDE DEPLOYMENT FIELDS
                    if VersionsData.get('deployment_field') is not None \
                            and len(VersionsData.get('deployment_field')) > 0:
                        HelperServices.add_update_deployment_fields(
                            VersionsData['deployment_field']['fields'], version_id)

                    # HANLDE MEDIA FILES
                    if VersionsData.get('media_file') is not None \
                            and len(VersionsData.get('media_file')) > 0:
                        HelperServices.add_update_media_files(VersionsData['media_file']['media_files'], version_id,
                                                           directory_to_import_from,
                                                           self.full_media_files_path,
                                                           self.media_files_path)
            return {"result": "success", "message": tooldata["name"]+" was updated"}
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            return {"result": "failed", "message": str(e_value)}

    def updatedu(self, du, full_sync_flag="false", directory_to_import_from=None):
        """Start Tool Update """
        dudata = du.get("du_data")
        builds = dudata.get('build')
        deployment_field = dudata.get('deployment_field')
        localDu = self.deploymentunitDB.GetDeploymentUnitByName(dudata["name"])
        du_id = str(localDu.get("_id"))
        try:
            if dudata.get("operation").lower() == "update":
                DuHelperService.add_update_du(
                    dudata, du_id, self.logo_path, directory_to_import_from, self.full_logo_path,False)
                # HANLDE BUILD
                if builds is not None and len(builds) > 0:
                    builds_handled = []  # WE need to deactivate all other builds
                    builds_not_to_process = []
                    for build in builds:
                        if build.get("to_process","true").lower()=="true":
                            if build.get("to_process"):build.pop("to_process")
                            if build.get("to_process_reason"):build.pop("to_process_reason")
                            BuildHelperService.add_update_build(
                                build, du_id, join(directory_to_import_from, os.path.join("artifacts",dudata["repository_to_use"])))
                            builds_handled.append(build["build_number"])
                        else:
                            builds_not_to_process.append(build["build_number"])
                    # SUPPOSE THE ACCOUNT SENDS 2 BUILDS THAT ARE  ACTIVE THEY WILL BE HANDLED
                    # BUT ALL OTHER BUILDS SHOULD BE MADE INACTIVE IN LOCAL
                    for build in self.buildsDB.get_all_builds(du_id):
                        if build["build_number"] not in builds_handled and build["build_number"] not in  builds_not_to_process:
                            build_id = build.get("_id")
                            build["_id"] = {}
                            build["_id"]["oid"] = str(build_id)
                            build["status"] = "0"
                            self.buildsDB.update_build(build)

                # HANLDE DEPLOYMENT FIELDS
                if deployment_field is not None \
                        and len(deployment_field) > 0:
                    HelperServices.add_update_deployment_fields(
                        deployment_field['fields'], du_id)
            return {"result": "success", "message": dudata["name"]+" was updated"}
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            return {"result": "failed", "message": str(e_value)}
    
    def add_update_du_set(self, du_set, full_sync_flag="false", directory_to_import_from=None):
        """Start DUSET Update/Add"""
        try:
            du_set_data=du_set.get("duset_data")
            if du_set_data.get("du_set"):
                du_set_det =[]
                for record in du_set_data.get("du_set"):
                    du=self.deploymentunitDB.GetDeploymentUnitByName(str(record.get("du_id")))
                    if du:
                        record["du_id"] = str(du.get("_id"))
                    else:
                        raise Exception ("No such DU found with name: "+str(record.get("du_id")))    
                    du_set_det.append(record)
            
            local_du_set = self.deploymentunitsetDB.GetDeploymentUnitSetByName(du_set_data.get("name"))
            if local_du_set:
                #directory_to_import_from not required as DUSET has default logo only 
                DuHelperService.add_update_du_set(du_set_data, str(local_du_set.get("_id")), self.logo_path, self.full_logo_path,directory_to_import_from)
            else:
                #directory_to_import_from not required as DUSET has default logo only 
                DuHelperService.add_update_du_set(du_set_data, None, self.logo_path, self.full_logo_path,directory_to_import_from)    
            return {"result": "success", "message": du_set_data["name"]+" was handled"}
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            return {"result": "failed", "message": str(e_value)}
        
    def schedule(self):
        """
        # Schedules the job
        # scheduler :Scheduler object
        # interval_given:Time interval for job to rerun"""
        global job
        self.load_configuration()
        job = self.schedulerService.schedule(job, self)

    # YOU CANNOT EXPORT WHEN WE ARE PERFORMING A IMPORT.ALL METHODS SHOULD BE
    # LOCKED
    @synchronized(locker)
    def createZipToExport(self,export_details,filters_to_apply=None):
        """Start Creating Zip File To Export"""
        # CONSTANTS
        file_path=export_details.get("file_path")
        zip_file_name=export_details.get("zip_file_name")
        target_host=export_details.get("target_host","Multiple")
        sync_type=export_details.get("sync_type","")
        download_artifacts=export_details.get("download_artifacts",True)
        get_tools=export_details.get("get_tools",True)
        get_dus=export_details.get("get_dus",True)  
        get_du_sets=export_details.get("get_du_sets",True) 
        get_states=export_details.get("get_states",True)      
        download_build_created_after_date = None
        external_artifacts = str(export_details.get("external_artifacts")).lower() =="true"
        if filters_to_apply:
            if str(filters_to_apply.get("type")).lower() in ["tool"]:
                get_dus = False
                get_du_sets = False
                get_states = False
            if str(filters_to_apply.get("type")).lower() in ["du"]:
                get_tools = False
            if filters_to_apply.get("time_after"):
                download_build_created_after_date = str(
                    filters_to_apply.get("time_after"))
                filters_to_apply.pop("time_after")
        error_prefix = "[" + sync_type + \
            "][TargetHost:" + target_host + "][sync_id:" + str(zip_file_name) + "]: "
        file_path = file_path + "/" + \
            str(zip_file_name) + '_' + str(sync_type)
        artifact_path = file_path + "/artifacts"
        media_file_path = file_path + "/mediaFiles"
        logo_file_path = file_path + "/logos"
        plugins_path = file_path + "/plugins"
        general_file_details = file_path + '/generalData.json'
        systemDetail = self.systemDetailsDb.get_system_details_single()
        tags_file_details = file_path + '/tagsData.json'
        fa_file_details = file_path + '/faData.json'
        er_file_details = file_path + '/erData.json'
        repository_file_details = file_path + '/reData.json'
        state_status_file_details = file_path + '/ssData.json'
        prerequisites_file_details = file_path + '/preRequisitesData.json'
        data_file = file_path + '/data.json'
        not_exported_list_reason = file_path + '/notExportedListReason.json'
        exported_list = file_path + '/exportedList.json'
        not_exported_list = file_path + '/notExportedList.json'
        tool_data = []
        tool_names = []
        not_exported_tool_names = []
        not_exported_tool_names_and_reason = []
        du_data = []
        du_names = []
        not_exported_du_names = []
        not_exported_du_names_and_reason = []
        du_sets_names = []
        du_sets_data = []
        not_exported_du_sets_names = []
        not_exported_du_sets_names_and_reason = []
        states_data = []
        states_names = []
        not_exported_states_names = []
        not_exported_states_names_and_reason = []
        try:
            general_file = {"date": str(datetime.now()),
                            "source_host": systemDetail.get("hostname"),
                            "source_port": systemDetail.get("port"),
                            "source_dpm_version": systemDetail.get("dpm_version"), 
                            "target": target_host ,
                            "sync_id" : zip_file_name,
                            "filters_applied":filters_to_apply,
                            "extract_builds_after_date":str(download_build_created_after_date)}
            
            SyncHelperService.new_sync(file_path, target_host,general_file,
                                    artifact_path, media_file_path, logo_file_path,
                                    general_file_details, tags_file_details, prerequisites_file_details,\
                                    plugins_path,fa_file_details,er_file_details,repository_file_details,state_status_file_details)
            
            #COPY PLUGINS
            self.handle_plugins_copy(plugins_path)
            
            
            if get_tools:
                tool_data, tool_names, not_exported_tool_names, not_exported_tool_names_and_reason = SyncHelperService.export_tools_for_new_sync(target_host, zip_file_name,
                                                                                                                                              logo_file_path, error_prefix, media_file_path, download_artifacts, artifact_path, download_build_created_after_date, filters_to_apply,external_artifacts)
            if get_dus:
                du_data, du_names, not_exported_du_names, not_exported_du_names_and_reason = SyncHelperService.export_dus_for_new_sync(target_host, zip_file_name,
                                                                                                                                    logo_file_path, error_prefix, media_file_path, download_artifacts, artifact_path, download_build_created_after_date, filters_to_apply,external_artifacts)
            if get_du_sets:
                du_sets_data, du_sets_names, not_exported_du_sets_names, not_exported_du_sets_names_and_reason = SyncHelperService.export_du_sets_for_new_sync(target_host, zip_file_name,
                                                                                                                                    logo_file_path, error_prefix, media_file_path, download_artifacts,download_build_created_after_date, filters_to_apply)
            if get_states:
                states_data, states_names, not_exported_states_names, not_exported_states_names_and_reason = SyncHelperService.export_states_for_new_sync(target_host, zip_file_name,
                                                                                                                         filters_to_apply)
                          
            if filters_to_apply.get("approval_status","any").lower() != "any" or filters_to_apply.get("package_state_name","")!="":
                self.filter_data(states_data,du_data,du_sets_data,du_names,du_sets_names,not_exported_du_names,not_exported_du_names_and_reason,not_exported_du_sets_names,not_exported_du_sets_names_and_reason)
                                           
            data=self.add_general_details(tool_data + du_data + du_sets_data + states_data,general_file,sync_type)
            
            if len(data) > 0:
                FileUtils.jsontoFile(data_file,data)
                FileUtils.jsontoFile(
                    exported_list, {"tools": tool_names, "dus": du_names , "duset" :du_sets_names , "states" :  states_names})
                FileUtils.jsontoFile(not_exported_list, {
                                     "tools": not_exported_tool_names, "dus": not_exported_du_names , "duset" :not_exported_du_sets_names ,  "states" :not_exported_states_names })
                FileUtils.jsontoFile(not_exported_list_reason,{"tools": not_exported_tool_names_and_reason, "dus": not_exported_du_names_and_reason , "duset" :not_exported_du_sets_names_and_reason , "states" :  not_exported_states_names_and_reason} )
                FileUtils.createZipFile(file_path, file_path)
                return file_path + ".zip", tool_names + du_names+du_sets_names+states_names, \
                    not_exported_tool_names_and_reason + not_exported_du_names_and_reason + not_exported_du_sets_names_and_reason + not_exported_states_names_and_reason
            else:
                raise Exception("Could not export any entities")
        except Exception as e_value:  # catch *all* exceptions
            print 'SyncServices Error :' + error_prefix + str(e_value)
            traceback.print_exc()
            raise ValueError(str(e_value))
        finally:
            try:
                if os.path.exists(file_path):
                    shutil.rmtree(file_path, ignore_errors=True)
            except Exception as e_value:  # catch *all* exceptions
                pass
    
    def filter_data(self,states_data,du_data,du_sets_data,du_names,du_sets_names,not_exported_du_names,not_exported_du_names_and_reason,not_exported_du_sets_names,not_exported_du_sets_names_and_reason):
        du_to_keep=[]
        du_package_to_keep=[]
        build_json={}        
        # filter all du and du packages
        for state in states_data:
            if state.get("state_data").get("type") == "dustate":
                du_to_keep.append(state.get("state_data").get("parent_entity_id"))
                if build_json.get(state.get("state_data").get("parent_entity_id")) is None : build_json[state.get("state_data").get("parent_entity_id")]=[]
                build_json[state.get("state_data").get("parent_entity_id")].append(state.get("state_data").get("build_id")) # These are the build we want to process in target machine
            elif state.get("state_data").get("type") == "dusetstate":
                du_package_to_keep.append(state.get("state_data").get("parent_entity_id")) 
        
        # filter all du packages
        temp_copy=copy.deepcopy(du_sets_data)
        for du_set in temp_copy:
            if du_set.get("duset_data").get("name") not in du_package_to_keep:
                not_exported_du_sets_names.append(du_set.get("duset_data").get("name"))
                not_exported_du_sets_names_and_reason.append(du_set.get("duset_data").get("name") + " with error : Does not adhere to applied filters of package state name or approval status")
                du_sets_data.remove(du_set)
                du_sets_names.remove(du_set.get("duset_data").get("name"))
            else:
                # we also need to include all the du's that are part of included du packages
                for du in du_set.get("duset_data",{}).get("du_set",[]):
                    if du.get("du_id") and du.get("du_id") not in du_to_keep : 
                        du_to_keep.append(du["du_id"])                       
                
        # filter all du        
        for c,du in enumerate(du_data):
            if du.get("du_data").get("name") not in du_to_keep:
                not_exported_du_names.append(du.get("du_data").get("name"))
                not_exported_du_names_and_reason.append(du.get("du_data").get("name") + " with error : Does not adhere to applied filters of package state name or approval status.Please check if we have a state for this DU part of the filtered state package ")
                du_data[c] = None
                du_names.remove(du.get("du_data").get("name"))
            else:
                if du_data[c] and du_data[c].get("du_data").get("build"):
                    for build in du_data[c].get("du_data").get("build"):
                        if not build_json.get(du_data[c].get("du_data").get("name")) or  build.get("build_number") not in build_json.get(du_data[c].get("du_data").get("name")):
                            build["to_process"]="false"
                            build["to_process_reason"]="build does not adhere to applied filters of package state name or approval status."                  
        
        # Remove all none values
        for du in copy.deepcopy(du_data):
            if not du:
                du_data.remove(du)
                       
    def add_general_details(self,data,general_file,requested_by):
        
        general_file["operation"] = ""
        general_file["source_created_time"] = str(datetime.now())
        general_file["created_by"] = requested_by
        general_file["type"] = requested_by
        final_data=[]
        for record in data:
            record.update(general_file)
            final_data.append(record)
        return final_data
        
    def str_to_bool(self, s):
        """# Converter Function"""
        if s.lower() == 'true':
            return True
        elif s.lower() == 'false':
            return False
        
    def handle_plugins_copy(self,plugins_path):
        for direc in plugin_directories_to_be_copied:
            source_path=os.path.join(plugin_full_path,direc)
            source = os.listdir(source_path)            
            for files in source:
                destination = os.path.join(plugins_path,direc,files)
                if "__init__" not in files and not files.endswith(".pyc"):
                    if not os.path.exists(os.path.dirname(destination)):
                        os.mkdir(os.path.dirname(destination))
                    shutil.copy(source_path+"/"+files,destination)                   
            
    def callbackUrl(self):
        # CALLBACK URL
        sync_ids=self.syncDb.get_distinct_sync_id_pending_callback()
        for sync_id in sync_ids:
            callback_url=None
            callback_status_reason=""
            callback_status="success"
            try:
                sync_config = self.configdb.getConfigByName("SyncServices")
                if sync_config.get("enable_callback","false")=="false":
                    self.syncDb.update_callback_status_by_sync_id(sync_id,"skipped","Callback is disabled in global configuration")
                    return                
                sync_data=self.analyse_sync_details(sync_id)
                callback_url=sync_data.get("callback_url")
                callback_json = {"sync_id": sync_id, "total_count":sync_data.get("total_count"),"success_count":sync_data.get("success_count"),"failed_count":sync_data.get("failed_count"),\
                                 "data": sync_data.get("data")}
                response = requests.post(callback_url, json=json.dumps(callback_json), timeout=int(sync_config.get("callback_timeout",30)), verify=False)
                response.raise_for_status()
            except Exception as e:  # catch *all* exceptions
                callback_status="failed"
                callback_status_reason = str(e)
            finally:
                self.syncDb.update_callback_status_by_sync_id(sync_id, callback_status, callback_status_reason)
                
    def analyse_sync_details(self,sync_id,background_run=True):
        added = []
        success_count = 0
        failed_count = 0
        details = self.syncDb.get_sync_by_sync_id(sync_id)
        if details and details.count() > 0:
            for rec in details:
                callback_url=rec.get("callback_url")
                if not rec.get("callback_url") and background_run:
                    raise Exception ("callback_url not provided")
                if str(rec.get("status")).lower() == "success":
                    success_count = success_count + 1
                elif str(rec.get("status")).lower() == "failed":
                    fialed_count = failed_count + 1
                if rec.get("tool_data"):
                    added.append("Tool: " + str(rec.get("tool_data").get("name")) + " Status: " + str(
                        rec.get("status")).upper() + " (" + str(rec.get("status_message")) + ")")
                elif rec.get("du_data"):
                    added.append("Du: " + str(rec.get("du_data").get("name")) + " Status: " + str(
                        rec.get("status")).upper() + " (" + str(rec.get("status_message")) + ")")
                elif rec.get("duset_data"):
                    added.append("Du Package: " + str(rec.get("duset_data").get("name")) + " Status: " + str(
                        rec.get("status")).upper() + " (" + str(rec.get("status_message")) + ")")
                elif rec.get("state_data"):
                    added.append("State: " + str(rec.get("state_data").get("name")) + " Status: " + str(
                        rec.get("status")).upper() + " (" + str(rec.get("status_message")) + ")")            
        return {"total_count":len(list(details)) ,"added" : str(len(added)), "success_count": str(success_count) , "failed_count" : str(failed_count), "data": added , "callback_url":callback_url}