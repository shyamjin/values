'''
Created on Dec 18, 2017

@author: pdinda
'''

import copy,re
from pymongo.cursor import Cursor
from datetime import datetime
import os
import shutil
import traceback
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_EXCEPTION
from jsondiff import diff
from DBUtil import Versions, Tool, Build, Sync, \
     SystemDetails, Tags, \
    DeploymentUnitSet, DeploymentUnit, DeploymentUnitType, \
    PreRequisites,State,Config,SyncRequest,FlexibleAttributes,ExitPointPlugins,Repository,\
    DeploymentUnitApprovalStatus
from Services import CleanerServices, FileUtils,BuildHelperService,\
    ToolHelperService, DuHelperService, StateHelperService
from settings import mongodb, import_full_path, current_path


from fabfile import runCommand
from StateHelperService import check_state_mandate_fields

versionsDB = Versions.Versions(mongodb)
toolDB = Tool.Tool(mongodb)
configdb = Config.Config(mongodb)
syncDb = Sync.Sync(mongodb)
buildsDB = Build.Build()
systemDetailsDb = SystemDetails.SystemDetails(mongodb)
systemDetail = systemDetailsDb.get_system_details_single()
deploymentunitsetdb = DeploymentUnitSet.DeploymentUnitSet()
deploymentunitdb = DeploymentUnit.DeploymentUnit()
deploymentUnitTypedb = DeploymentUnitType.DeploymentUnitType()
tagsDB = Tags.Tags()
preRequisitesDB = PreRequisites.PreRequisites(mongodb)
cleanerServices = CleanerServices.CleanerServices(mongodb)
statedb=State.State(mongodb)
buildDB = Build.Build()
syncRequestDb = SyncRequest.SyncRequest(mongodb)
flexAttrDB = FlexibleAttributes.FlexibleAttributes()
exitPointPlugins=ExitPointPlugins.ExitPointPlugins()
repositoryDb=Repository.Repository()
deploymentUnitApprovalStatusDB = DeploymentUnitApprovalStatus.DeploymentUnitApprovalStatus()


def delete_version_and_related_builds(version_id):
    """Remove a version and dependent builds"""
    version = {}
    version["status"] = "0"
    version["_id"] = {}
    version["_id"]["oid"] = version_id
    delversion = versionsDB.update_version(version)
    if delversion is None:
        raise Exception("Unable to delete version" + version.get("_id"))
    else:
        deletedBuilds = []
        builds = {}
        builds = buildsDB.get_active_build(version_id)
        if builds:
            for build in builds:
                builddata = {}
                builddata["_id"] = {}
                builddata["_id"]["oid"] = str(build.get("_id"))
                builddata["status"] = "0"
                delbuild = buildsDB.update_build(builddata)
                if delbuild in [None, 0]:
                    version["status"] = "1"
                    for rec in deletedBuilds:
                        buildsDB.update_build(rec)
                        versionsDB.update_version(version)
                    raise Exception(
                        "Unable to delete build" + version.get("_id"))
                else:
                    builddata["status"] = "1"
                    deletedBuilds.append(builddata)


def handle_filter_for_sync(filters_to_apply, data):
    # Filter by Tag
    if filters_to_apply:
        tags_filter = filters_to_apply.get("tags", [])
        if len(tags_filter) > 0:
            if data.get("tag") and "any" not in tags_filter:
                if tags_filter and len(tags_filter) > 0 and len(list(set(tags_filter) & set(data["tag"]))) < 1:
                    raise Exception(
                        "Does not adhere to applied filters of tag")
            else:
                if tags_filter and len(tags_filter) > 0 and "any" not in tags_filter:
                    raise Exception(
                        "Does not adhere to applied filters of tag")
    # DEFAULT BEHAVIOUR
    if data and data.get("is_tool_cloneable","true") == "false":
            raise Exception(
                "Does not adhere to applied filters as tool is not allowed to be cloned or exported")


def handle_states_filters_for_sync(filters_to_apply, state):
    # Filters by Approval status
    if filters_to_apply:        
        # Filter by approval status
        filter_approval_status = filters_to_apply.get("approval_status")
        if filter_approval_status not in ["None","",None]:
            if filter_approval_status.lower() != "any":
                if state.get("type") == "dusetstate":
                    if filter_approval_status != state.get("approval_status"):
                        raise Exception(
                            "Does not adhere to applied filters of state approval status")
                if state.get("type") == "dustate":
                    if not check_state_part_of_duset_for_approval_status(state.get("_id"),filter_approval_status):
                        if filter_approval_status != state.get("approval_status"):
                            raise Exception(
                               "Does not adhere to applied filters of state approval status")
        
        #filter by du_package_state_name
        filter_package_state_name = filters_to_apply.get("package_state_name")
        if filter_package_state_name:
            filter_package_state_name =  [re.compile(state_name, re.IGNORECASE) for state_name in filter_package_state_name.split(",")]
            if state.get("type") == "dusetstate":
                if not len(statedb.get_state_all(False, None, None, 0, 0, {"_id": {"$in": [state.get("_id")]},"name": {"$in": filter_package_state_name}})) > 0:
                    raise Exception(
                                    "Does not adhere to applied filters of package state name")
            if state.get("type") == "dustate":
                if check_state_part_of_duset_for_package_state_name(state.get("_id"),filter_package_state_name):
                        raise Exception(
                           "Does not adhere to applied filters of package state name")                    


def check_state_part_of_duset_for_approval_status(state_id, filter_approval_status):
    dusetstates = statedb.get_state_all(False, None, None, 0, 0, {"states": {"$in": [str(state_id)]}})
    if len(dusetstates) > 0:
        for dusetstate in dusetstates:
            if dusetstate.get("approval_status") == filter_approval_status:
                return True
    return False


def check_state_part_of_duset_for_package_state_name(state_id, filter_package_state_name):
    dusetstates = statedb.get_state_all(False, None, None, 0, 0, {"states": {"$in": [str(state_id)]},"name": {"$in": filter_package_state_name}})
    if len(dusetstates) > 0:        
        return False
    return True


def download_logo_files(tool_data, static_folder_path, logo_file_path):
    """Download LogoFiles Files"""
    if tool_data.get("logo"):
        if os.path.exists(static_folder_path + '/' + tool_data["logo"]):
            shutil.copy(static_folder_path + '/' +
                        tool_data["logo"], logo_file_path)
        else:
            raise ValueError(
                "Logo : " + os.path.basename(tool_data["logo"]) + " does not exists")

    if tool_data.get("thumbnail_logo"):
        if os.path.exists(static_folder_path + '/' + tool_data["thumbnail_logo"]):
            shutil.copy(static_folder_path + '/' +
                        tool_data["thumbnail_logo"], logo_file_path)
        else:
            raise ValueError(
                "Logo Thumbnail : " + os.path.basename(tool_data["thumbnail_logo"]) + " does not exists")


def export_du_sets_for_new_sync(targetHost, sync_id,
                                logo_file_path, error_prefix, media_file_path, AddBuilds,
                                download_build_after=None, filters_to_apply=None):
    # CREATE TOOLS DETAILS FILE
    exported_du_sets_data = []
    exported_du_sets_names = []
    not_exported_du_set_names = []
    not_exported_du_set_names_and_reason = []
    du_sets, not_exported_du_set_names, not_exported_du_set_names_and_reason = deploymentunitsetdb.get_du_sets_to_sync()
    for du_set in du_sets:
        try:
            handle_filter_for_sync(filters_to_apply, du_set.get("duset_data"))
            if sync_id:
                du_set["sync_id"] = sync_id
            # GET ORDER PROCESS OF DU
            du_set["process_order"] = int(0)
            # HANDLE LOGO
            download_logo_files(
                du_set["duset_data"], current_path, logo_file_path)
            # GET BUILD
            exported_du_sets_data.append(du_set)
            exported_du_sets_names.append(du_set["duset_data"].get("name"))
        except Exception as e_value:  # catch *all* exceptions

            traceback.print_exc()

            not_exported_du_set_names_and_reason.append(du_set["duset_data"].get(
                "name") + " skipped :" + str(e_value))
            not_exported_du_set_names.append(du_set["duset_data"].get(
                "name"))
    return exported_du_sets_data, exported_du_sets_names, not_exported_du_set_names, not_exported_du_set_names_and_reason


def export_dus_for_new_sync(targetHost, sync_id,
                            logo_file_path, error_prefix, media_file_path, AddBuilds, \
                            artifact_path, download_build_after=None, filters_to_apply=None, external_artifacts=None):
    # CREATE TOOLS DETAILS FILE
    dus = deploymentunitdb.get_dus_to_sync()
    exported_dus_data = []
    exported_dus_names = []
    not_exported_dus_names = []
    not_exported_du_names_and_reason = []
    for du in dus:
        try:
            handle_filter_for_sync(filters_to_apply, du.get("du_data"))
            if sync_id:
                du["sync_id"] = sync_id
            # GET ORDER PROCESS OF DU
            du["process_order"] = int(0)
            # HANDLE LOGO
            download_logo_files(
                du["du_data"], current_path, logo_file_path)
            # GET BUILD
            if AddBuilds and du["du_data"].get("build"):
                futures = []
                pool = ThreadPoolExecutor(1,__name__+".export_dus_for_new_sync")
                for build in du["du_data"].get("build"):
                    futures.append(pool.submit(
                        BuildHelperService.download_build_files, copy.deepcopy(build),du["source_du_id"], \
                        os.path.join(artifact_path,du["du_data"]["repository_to_use"]), download_build_after, external_artifacts))
                wait(futures, return_when=FIRST_EXCEPTION)
                exceptions_list = []
                for future in futures:
                    if future.exception():
                        exceptions_list.append(str(future.exception()))
                if len(exceptions_list):
                    raise Exception(','.join(exceptions_list))
            exported_dus_data.append(du)
            exported_dus_names.append(du["du_data"].get("name"))
        except Exception as e_value:  # catch *all* exceptions

            traceback.print_exc()

            not_exported_du_names_and_reason.append(du["du_data"].get(
                "name") + " skipped :" + str(e_value))
            not_exported_dus_names.append(du["du_data"].get(
                "name"))
    return exported_dus_data, exported_dus_names, not_exported_dus_names, not_exported_du_names_and_reason


def export_states_for_new_sync( targetHost, sync_id,filters_to_apply=None):
    # CREATE TOOLS DETAILS FILE
    exported_states_data = []
    exported_states_names = []
    not_exported_states_names = []
    not_exported_states_names_and_reason = []
    states = statedb.get_state_all()
    for state in states:
        state_name=state.get("name")
        try:
            handle_states_filters_for_sync(filters_to_apply, state)
            state=statedb.get_state_data_for_sync(state)
            if sync_id:
                state["sync_id"] = sync_id
            # GET ORDER PROCESS OF DU
            check_state_mandate_fields(state.get("state_data"))                 
            if(state.get("state_data").get("states")):
                state["process_order"] = set_process_order(state.get("state_data").get("states"))
            else:
                state["process_order"] = int(0)
            StateHelperService.convert_parent_ids_to_name(state.get("state_data"))
            exported_states_data.append(state)
            exported_states_names.append(state["state_data"].get("name"))
        except Exception as e_value:  # catch *all* exceptions
            
            traceback.print_exc()
            
            not_exported_states_names_and_reason.append(state_name + " skipped :" + str(e_value))
            not_exported_states_names.append(state_name)
    return exported_states_data, exported_states_names, not_exported_states_names, not_exported_states_names_and_reason


def set_process_order1(state,processorder=1):  
    if statedb.get_state_by_id(state).get("states") :
        processorder=set_process_order(statedb.get_state_by_id(state).get("states"), processorder+1)
    return(processorder)


def set_process_order(states,processorder=1):
    processorderList=[]
    for state in states:
        processorderList.append(set_process_order1(state,processorder))
    return(max(processorderList))


def download_media_files(version, error_prefix, static_folder_path, media_file_path):
    """Download MediaFiles Files"""
    # GET MEDIAFILES
    media_file = version.get("media_file")
    if media_file is not None:
        for media in media_file.get("media_files"):
            # COPY URL
            if media.get("url"):
                print error_prefix + "Copying file :" + media["url"]
                if os.path.exists(static_folder_path + '/' + media["url"]):
                    shutil.copy(static_folder_path + '/' +
                                media["url"], media_file_path)
                else:
                    raise ValueError(
                        "MediaFile : " + os.path.basename(media["url"]) + " does not exists")
                print error_prefix + "Copying file completed for :" + media["url"]
            # COPY THUMBNAIL URL
            if media.get("thumbnail_url"):
                print error_prefix + "Copying file :" + media["thumbnail_url"]
                if os.path.exists(static_folder_path + '/' + media["thumbnail_url"]):
                    shutil.copy(static_folder_path + '/' +
                                media["thumbnail_url"], media_file_path)
                else:
                    raise ValueError(
                        "MediaFile Thumbnail : " + os.path.basename(media["thumbnail_url"]) + " does not exists")
                print error_prefix + "Copying file completed for :" + media["thumbnail_url"]


def export_tools_for_new_sync( targetHost, sync_id,
                              logo_file_path, error_prefix, media_file_path, AddBuilds,\
                               artifact_path, download_build_after=None, filters_to_apply=None,external_artifacts=None):
    # CREATE TOOLS DETAILS FILE
    tools_with_active_versions, tools_with_inactive_versions = toolDB.get_tool_details_to_sync()
    exported_tools_data = []
    exported_tools_names = []
    not_exported_tools_names = []
    not_exported_tool_names_and_reason = []
    for rec in tools_with_inactive_versions:
        not_exported_tool_names_and_reason.append(
            rec + " with error :No active version found")
        not_exported_tools_names.append(rec)
    for tool in tools_with_active_versions:
        try:
            if handle_filter_for_sync(filters_to_apply, tool.get("tool_data")):
                continue
            if sync_id:
                tool["sync_id"] = sync_id
            # HANDLE LO
            download_logo_files(
                tool["tool_data"], current_path, logo_file_path)

            versions = tool["tool_data"].get("versions")

            # GET ORDER PROCESS OF TOOL
            process_order, toolNames = ToolHelperService.get_ordered_tools(versions)
            tool["process_order"] = int(process_order)

            # WE GET EVERYTHING SEPERATELY AS IT SAVES TIME
            for version in versions:
                # GET DEPLOYMENT TOOLS
                version = ToolHelperService.get_dependend_tools(
                    version, True)
            for version in versions:
                # GET MEDIAFILES
                download_media_files(
                    version, error_prefix, current_path, media_file_path)
            for version in versions:  # GET BUILD AT LAST AS THEY ARE HUGE
                # GET BUILD
                if AddBuilds and version.get("build"):
                    futures = []
                    pool = ThreadPoolExecutor(1,__name__+".export_tools_for_new_sync")
                    for build in version.get("build"):
                        futures.append(pool.submit(
                            BuildHelperService.download_build_files, \
                            copy.deepcopy(build),version["source_version_id"],os.path.join(artifact_path,version["repository_to_use"]), download_build_after,external_artifacts))
                    wait(futures, return_when=FIRST_EXCEPTION)
                    exceptions_list = []
                    for future in futures:
                        if future.exception():
                            exceptions_list.append(str(future.exception()))
                    if len(exceptions_list):
                        raise Exception(','.join(exceptions_list))
            exported_tools_data.append(tool)
            exported_tools_names.append(tool["tool_data"].get("name"))
        except Exception as e_value:  # catch *all* exceptions
            
            traceback.print_exc()
            
            not_exported_tool_names_and_reason.append(tool["tool_data"].get(
                "name") + " skipped :" + str(e_value))
            not_exported_tools_names.append(tool["tool_data"].get(
                "name"))
    return exported_tools_data, exported_tools_names, not_exported_tools_names, not_exported_tool_names_and_reason

def new_sync(file_path, targetHost, general_file,
             artifact_path, media_file_path, logo_file_path,
             general_file_details, tags_file_details, prerequisites_file_details,plugins_path,fa_file_details,er_file_details,repository_file_details,\
             state_status_file_details):

    if not systemDetail:
        raise Exception("systemDeatils not found")
    if not systemDetail.get("hostname"):
        raise Exception("hostname not found in systemDeatils")
    if not systemDetail.get("port"):
        raise Exception("port not found in systemDeatils")

    keys_to_pop=["_id","created_time","updated_time"]
    # CREATE TAGS DETAILS FILE
    tags_file = []
    tags_in_db = tagsDB.get_tags()
    if tags_in_db:
        for tag in tags_in_db:
            for rec in keys_to_pop:
                if rec in tag.keys():
                    tag.pop(rec)
            tags_file.append(tag)
    # CREATE FA DETAILS FILE
    fa_file = []
    fa_in_db = flexAttrDB.get_all()
    if fa_in_db:
        for fa in fa_in_db:
            for rec in keys_to_pop:
                if rec in fa.keys():
                    fa.pop(rec)            
            fa_file.append(fa)        
    # CREATE PreRequisites DETAILS FILE
    prerequisites_file = []
    prerequisites_in_db = preRequisitesDB.get_all_pre_requisites()
    if prerequisites_in_db:
        for prerequisite in prerequisites_in_db:
            for rec in keys_to_pop:
                if rec in prerequisite.keys():
                    prerequisite.pop(rec)
            prerequisites_file.append(prerequisite)
    
    
    # CREATE State Status DETAILS FILE
    state_status_file = []
    state_status_in_db = deploymentUnitApprovalStatusDB.GetAllDeploymentUnitApprovalStatus()
    if state_status_in_db:
        for rep in state_status_in_db:
            for rec in keys_to_pop:
                if rec in rep.keys():
                    rep.pop(rec)
            state_status_file.append(rep)  
            
    # CREATE Repository DETAILS FILE
    repositories_file = []
    repositories_in_db = repositoryDb.get_all()
    if repositories_in_db:
        for rep in repositories_in_db:
            for rec in keys_to_pop:
                if rec in rep.keys():
                    rep.pop(rec)
            repositories_file.append(rep)        

    # CREATE external_plugins DETAILS FILE
    external_plugins_file = []
    external_plugins_in_db = exitPointPlugins.get_all()
    if external_plugins_in_db:
        for external_plugins in external_plugins_in_db:
            for rec in keys_to_pop:
                if rec in external_plugins.keys():
                    external_plugins.pop(rec)
            external_plugins_file.append(external_plugins)

    FileUtils.mkdirs([file_path, artifact_path, media_file_path, logo_file_path,plugins_path], True)
    FileUtils.jsontoFile(general_file_details, general_file)
    FileUtils.jsontoFile(tags_file_details, tags_file)
    FileUtils.jsontoFile(fa_file_details, fa_file)
    FileUtils.jsontoFile(prerequisites_file_details, prerequisites_file)
    FileUtils.jsontoFile(er_file_details, external_plugins_file)
    FileUtils.jsontoFile(repository_file_details,repositories_file)
    FileUtils.jsontoFile(state_status_file_details,state_status_file)


def clean_processed_sync(sync_id):
    try:
        recs = syncDb.get_sync_by_sync_id(sync_id)
        if recs:
            for rec in recs:
                if rec.get("stored_folder_name"):
                    file_name = os.path.basename(rec.get("stored_folder_name"))
                if str(rec["status"]).lower() not in ["success", "skipped"]:
                    return
        if os.path.exists(os.path.join(import_full_path, file_name)):
            cleanerServices.clean_old_data([import_full_path], file_name, -1)
    except Exception as e:  # catch *all* exceptions
        print 'HelperServices :clean:' + str(e)
        traceback.print_exc()


def validate_sync_data_from_json(toolJsonData, validateSyncId=True):
    """Validate a ToolJson"""
    if toolJsonData is None:
        raise ValueError("toolData was not found.This is a corrupt file")
    for rec in toolJsonData:
        if rec.get("sync_id") is not None:
            existstingRecords = syncDb.get_sync_by_sync_id(rec.get("sync_id"))
            if existstingRecords is not None and existstingRecords.count() > 0:
                raise ValueError(
                    "This Sync already exists in database.Please select a new file")
        elif validateSyncId:
            raise ValueError(
                "sync_id not found in toolData.json.This is a corrupt file")
        if rec.get("tool_data"):  # Checking if json is formatted
            tool = rec.get("tool_data")
            if tool.get("name") is not None:
                if tool.get("versions") is not None:
                    for ver in tool.get("versions"):
                        if datetime.strptime((str(str(ver['version_date']).split()[0])), "%Y-%m-%d"):
                            print ""
                        if ver.get("version_name") is None:
                            raise ValueError(
                                "version_name not found in versions.This is a corrupt file")
                        if ver.get("version_number") is None:
                            raise ValueError(
                                "version_number not found in versions.This is a corrupt file")
                else:
                    raise ValueError(
                        "versions not found in tool_data.This is a corrupt file")
            else:
                raise ValueError(
                    "name not found in tool_data.This is a corrupt file")
        elif rec.get("du_data"):  # Checking if json is formatted
            du = rec.get("du_data")
            if not du.get("name"):
                raise ValueError(
                    "name not found in du_data.This is a corrupt file")
        elif rec.get("duset_data"):  # Checking if json is formatted
            duset_data = rec.get("duset_data")
            if not duset_data.get("name"):
                raise ValueError(
                    "name not found in duset_data.This is a corrupt file")
            if not duset_data.get("du_set") and len(duset_data.get("du_set",[])) < 1:
                raise ValueError(
                    "du_set not found in duset_data.This is a corrupt file")    
        elif rec.get("state_data"):  # Checking if json is formatted
            state_data = rec.get("state_data")
            if not state_data.get("name"):
                raise ValueError(
                    "name not found in state_data.This is a corrupt file")
            if not state_data.get("parent_entity_id"):
                raise ValueError(
                    "parent_entity_id not found in state_data.This is a corrupt file")   
            if not state_data.get("build_id") and len(state_data.get("states",[]))<1:
                raise ValueError(
                    "build_id/states not found in state_data.This is a corrupt file")                 
        else:
            raise ValueError(
                "This is a corrupt file as neither tool_data/du_data/duset_data/state_data was found")


def get_sync_id_and_type(record):
    """GEt Sync Id and Type from record"""
    if record.get("sync_id"):
        sync_id = record.get("sync_id")
    if record.get("type"):
        sync_type = record.get("type")
    if not sync_id or not sync_type:
        raise ValueError("sync_id or type was not found in record")
    if (str(sync_type.strip()).lower() not in ["pull", "push", "manual"]):
        raise ValueError("Sync type :" + type.strip() + " is invalid")
    return sync_id, str(sync_type.strip()).lower()


def compare_tools_for_sync():
    """Compare data for sync"""
    sync_id = sync_type = None
    try:
        print "HelperServices : compare :Checking if there is pending data to Process. If found Compare will be skipped"
        pending_process_list = syncDb.get_pending_sync_to_process()
        if pending_process_list:
            print "HelperServices : compare : There are active records to be Processed. New records will not be compared."
            return

        print "HelperServices:compare: comparing sync data"
        tools = list(syncDb.get_pending_sync_to_compare())
        not_exported_List = {"tools": []}
        if tools and copy.deepcopy(tools) > 0:
            for tool in tools:
                if "tool_data" not in tool.keys():
                    continue
                tool["changed_object"] = []
                tool["operation"] = ""
                try:
                    sync_id, sync_type = get_sync_id_and_type(tool)
                    modified = 0
                    tool["_id"] = {"oid": str(tool["_id"])}
                    synctool = tool.get("tool_data")
                    # VALIDATE THE TOOL DETAILS
                    ToolHelperService.validate_tool_data(synctool)
                    tool_name = synctool["name"]
                    ltooldata = toolDB.get_tool_by_name(tool_name)

                    if ltooldata is None:
                        print "HelperServices:compare: tool " + tool_name + " was not found in local DB."
                        tool["operation"] = "insert"
                        tool["status"] = "compared"
                        tool["status_message"] = ""
                        tool["updated_time"] = datetime.now()
                        synctool["operation"] = "insert"
                        modified = 1
                        tool["tool_data"] = synctool
                        updated = syncDb.update_sync(tool)
                        if updated:
                            print "HelperServices:compare:This tool will be created while processing"
                        else:
                            print "HelperServices:compare: Unable to trigger tool creation while processing"
                        continue
                    else:
                        print "HelperServices:compare: tool " + tool_name + " was found in local DB."
                        sub = compare_tool_data(copy.deepcopy(
                            synctool), copy.deepcopy(ltooldata))
                        if sub:
                            print "HelperServices:compare:tool_data of tool " \
                                + tool_name + " is required to be updated as the tool data has changed."
                            synctool["operation"] = "update"
                            tool["operation"] = "update"
                            toolchange = {}
                            toolchange["tool"] = str(sub)
                            tool["changed_object"].append(toolchange)
                            modified = 1
                        else:
                            print "HelperServices:compare: tool_data of tool " \
                                + tool_name + " is not required to be updated.As tool data has not changed"
                            synctool["operation"] = ""
                            modified = 0

                        activeversionids = []
                        syncversions = []
                        for version in synctool["versions"]:
                            localversion, isActive = list(versionsDB.get_version_detail_and_status(
                                str(ltooldata["_id"]), version["version_number"], version["version_name"], True))
                            if localversion:
                                ToolHelperService.get_dependend_tools(localversion, True)
                                activeversionids.append(
                                    str(localversion["_id"]))
                                if isActive:
                                    sub = compare_version_data(copy.deepcopy(
                                        version), copy.deepcopy(localversion))
                                    if sub:
                                        print "HelperServices:compare:versions of  tool " + \
                                            tool_name + " is required to be updated as the version has changed."
                                        version["operation"] = "update"
                                        modified = 1
                                        versionchange = {}
                                        versionchange["version"] = str(sub)
                                        tool["changed_object"].append(
                                            versionchange)
                                        # version["version_id"]= str(localversion["_id"])
                                    else:
                                        print "HelperServices:compare:versions of tool " + \
                                            tool_name + " is not required to be updated.As versions has not changed"
                                        version["operation"] = ""
                                else:
                                    version["operation"] = "update"
                                    modified = 1
                                    versionchange = {}
                                    versionchange["version"] = str(
                                        "Version is not active")
                                    tool["changed_object"].append(
                                        versionchange)

                                if version["operation"] in [None, "", "update"]:
                                    any_change = []
                                    copyldocument = {}
                                    copydocument = {}
                                    copybuild = {}
                                    copylbuild = {}
                                    copymediafile = {}
                                    copylmediafile = {}
                                    copydeployfields = {}
                                    copyldeployfields = {}
                                    # DocumentCompare
                                    if "document" in version.keys():
                                        if version["document"] and "documents" in version["document"].keys():
                                            copydocument = copy.deepcopy(
                                                version["document"]["documents"])
                                    if "document" in localversion.keys():
                                        if localversion["document"] and "documents" in localversion["document"].keys():
                                            copyldocument = copy.deepcopy(
                                                localversion["document"]["documents"])
                                    any_change.append(
                                        diff(copydocument, copyldocument))
                                    # BuildCompare
                                    if "build" in version.keys():
                                        if version["build"] is not None and len(version["build"]) > 0:
                                            copybuild = copy.deepcopy(
                                                version["build"])
                                            builds = []
                                            for build in copybuild:
                                                build = toolDB.trim_data_for_sync(
                                                    build)
                                                if build.get("build_date"):
                                                    build["build_date"] = str(
                                                        build["build_date"]).split(".")[0]
                                                if build.get("file_path"): build.pop("file_path")
                                                builds.append(build)
                                    if "build" in localversion.keys():
                                        if localversion["build"] is not None and localversion["build"].count() > 0:
                                            copylbuild = copy.deepcopy(
                                                localversion["build"])
                                            lbuilds = []
                                            for build in localversion["build"]:
                                                build = toolDB.trim_data_for_sync(
                                                    build)
                                                if build.get("build_date"):
                                                    build["build_date"] = str(
                                                        build["build_date"]).split(".")[0]
                                                if build.get("file_path"): build.pop("file_path")
                                                lbuilds.append(build)
                                            copylbuild = lbuilds
                                    any_change.append(
                                        diff(copybuild, copylbuild))
                                    # MediaFileCompare
                                    if "media_file" in version.keys():
                                        if version["media_file"] and "media_files" in version["media_file"].keys():
                                            copymediafile = copy.deepcopy(
                                                version["media_file"]["media_files"])
                                    if "media_file" in localversion.keys():
                                        if localversion["media_file"] and "media_files" in localversion["media_file"].keys():
                                            copylmediafile = copy.deepcopy(
                                                localversion["media_file"]["media_files"])
                                    any_change.append(
                                        diff(copymediafile, copylmediafile))
                                    # DeploymentFieldsCompare
                                    if "deployment_field" in version.keys():
                                        if version["deployment_field"] and "fields" in version["deployment_field"].keys():
                                            copydeployfields = copy.deepcopy(
                                                version["deployment_field"]["fields"])
                                    if "deployment_field" in localversion.keys():
                                        if localversion["deployment_field"] and "fields" in localversion["deployment_field"].keys():
                                            copyldeployfields = copy.deepcopy(
                                                localversion["deployment_field"]["fields"])
                                    any_change.append(
                                        diff(copydeployfields, copyldeployfields))
                                    # IterChanges
                                    changes = iter(any_change)
                                    element = next(changes)
                                    if element:
                                        version["operation"] = "update"
                                        modified = 1
                                        versionchange = {}
                                        versionchange["document"] = str(
                                            element)
                                        tool["changed_object"].append(
                                            versionchange)
                                        print "document are changed"
                                    element = next(changes)
                                    if element:
                                        version["operation"] = "update"
                                        modified = 1
                                        versionchange = {}
                                        versionchange["build"] = str(element)
                                        tool["changed_object"].append(
                                            versionchange)
                                        print "build are changed"
                                    element = next(changes)
                                    if element:
                                        version["operation"] = "update"
                                        modified = 1
                                        versionchange = {}
                                        versionchange["media_file"] = str(
                                            element)
                                        tool["changed_object"].append(
                                            versionchange)
                                        print "media file is changed"
                                    element = next(changes)
                                    if element:
                                        version["operation"] = "update"
                                        modified = 1
                                        versionchange = {}
                                        versionchange["deployment_field"] = str(
                                            element)
                                        tool["changed_object"].append(
                                            versionchange)
                                        print "deployment fields are changed"
                            else:
                                version["operation"] = "insert"
                                modified = 1
                                versionchange = {}
                                versionchange["version"] = str(
                                    "Version was not found")
                                tool["changed_object"].append(versionchange)
                            syncversions.append(version)
                        tool["status"] = "compared"
                        tool["updated_time"] = datetime.now()
                        allactiveversions = []
                        allactiveversions = versionsDB.get_sync_versions_by_tool_id(
                            str(ltooldata["_id"]), False)
                        for activeversion in allactiveversions:
                            if str(activeversion["_id"]) not in activeversionids:
                                activeversion["operation"] = "delete"
                                modified = 1
                                syncversions.append(activeversion)
                        synctool["versions"] = syncversions

                    tool["tool_data"] = synctool
                    if modified == 1 and tool["operation"] == "":
                        tool["operation"] = "update"
                    elif modified == 0:
                        tool["operation"] = ""
                        tool["status"] = "success"
                        tool["status_message"] = "No difference was found while comparing"
                    updated = syncDb.update_sync(tool)
                except Exception as e:  # catch *all* exceptions
                    print 'SyncServices-Compare :' + str(e)
                    traceback.print_exc()
                    syncDb.update_sync_status(
                        str(tool["_id"]["oid"]), "failed", "Comparing failed with error :" + str(e))

        # CHECK IF THERE ARE ANY ACTIVE TOOLS WHICH ARE NOT FOUND IN SYNC
        # COLLECTON FOR THE GIVEN SYNC ID
        # Check if sync_id (active sync request) was found to compare
        if sync_id and sync_type:
            print "HelperServices:compare: Load not exported list from sync data"
            not_exported_List = get_not_exorted_list(tools)
            print "HelperServices : compare : Checking if system has tools to delete from local."
            allactivetools = toolDB.get_tools_all(['active'])
            for activetool in allactivetools:
                recs = syncDb.get_sync_by_sync_id_and_name(
                    sync_id, "tool_data.name", str(activetool["name"]))
                if recs is None or recs.count() <= 0:
                    if not_exported_List.get("tools") and str(activetool["name"]) in not_exported_List["tools"]:
                        skiptool = {}
                        skipactivetool = toolDB.get_tool_by_id(
                            str(activetool["_id"]), False)
                        skipactivetool["operation"] = "skip"
                        skiptool["operation"] = "skip"
                        skiptool["tool_data"] = skipactivetool
                        skiptool["status"] = "skipped"
                        skiptool["status_message"] = "Skipped as tool was not exported at source"
                        skiptool["sync_id"] = sync_id
                        skiptool["source_host"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        skiptool["target"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        skiptool["type"] = sync_type
                        updated = syncDb.add_sync(skiptool)
                        if updated:
                            print "HelperServices:compare: tool " + activetool["name"] + \
                                " will be skipped from local."
                    else:
                        delete_tool = {}
                        delactivetool = toolDB.get_tool_by_id(
                            str(activetool["_id"]), False)
                        delactivetool["operation"] = "delete"
                        delete_tool["operation"] = "delete"
                        delete_tool["tool_data"] = delactivetool
                        delete_tool["status"] = "compared"
                        delete_tool["sync_id"] = sync_id
                        delete_tool["source_host"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        delete_tool["target"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        delete_tool["type"] = sync_type
                        updated = syncDb.add_sync(delete_tool)
                        if updated:
                            print "HelperServices:compare: tool " + activetool["name"] + \
                                " will be removed from local."
    except Exception as e:  # catch *all* exceptions
        traceback.print_exc()
        print 'SyncServices-Compare :' + str(e)

def compare_dus_for_sync():
    """Compare data for sync"""
    sync_id = sync_type = None
    try:
        print "HelperServices : compare :Checking if there is pending data to Process. If found Compare will be skipped"
        pending_process_list = syncDb.get_pending_sync_to_process()
        if pending_process_list:
            print "HelperServices : compare : There are active records to be Processed. New records will not be compared."
            return

        print "HelperServices:compare: comparing sync data"
        dus = list(syncDb.get_pending_sync_to_compare())
        if dus and list(dus) > 0:
            for du in dus:
                if "du_data" not in du.keys():
                    continue
                du["changed_object"] = []
                du["operation"] = ""
                try:
                    sync_id, sync_type = get_sync_id_and_type(du)
                    modified = 0
                    du["_id"] = {"oid": str(du["_id"])}
                    sync_du = du.get("du_data")
                    # VALIDATE THE DU DETAILS
                    DuHelperService.validate_du_data(sync_du)
                    du_name = sync_du["name"]
                    ldudata = deploymentunitdb.GetDeploymentUnitByName(
                        du_name, True)

                    if ldudata is None:
                        print "HelperServices:compare: du " + du_name + " was not found in local DB."
                        du["operation"] = "insert"
                        du["status"] = "compared"
                        du["status_message"] = ""
                        du["updated_time"] = datetime.now()
                        du["operation"] = "insert"
                        modified = 1
                        du["du_data"] = sync_du
                        updated = syncDb.update_sync(du)
                        if updated:
                            print "HelperServices:compare:This du will be created while processing"
                        else:
                            print "HelperServices:compare: Unable to trigger tool creation while processing"
                        continue
                    else:
                        print "HelperServices:compare: du " + du_name + " was found in local DB."
                        sub = compare_du_data(copy.deepcopy(
                            sync_du), copy.deepcopy(ldudata))
                        if sub:
                            print "HelperServices:compare:du_data of tool " \
                                + du_name + " is required to be updated as the tool data has changed."
                            sync_du["operation"] = "update"
                            du["operation"] = "update"
                            duchange = {}
                            duchange["du"] = str(sub)
                            du["changed_object"].append(duchange)
                            modified = 1
                        else:
                            print "HelperServices:compare: du_data of du " \
                                + du_name + " is not required to be updated.As tool data has not changed"
                            sync_du["operation"] = ""
                            modified = 0
                            any_change = []
                            copybuild = {}
                            copylbuild = {}
                            copydeployfields = {}
                            copyldeployfields = {}
                            build_not_to_compare_list = []
                            # BuildCompare
                            if "build" in sync_du.keys():
                                if sync_du["build"] is not None and len(sync_du["build"]) > 0:
                                    copybuild = copy.deepcopy(
                                        sync_du["build"])
                                    for build in copybuild:
                                        # List of all build which should not be compared
                                        if str(build.get("to_process","true")).lower() == "false" : build_not_to_compare_list.append(build.get("build_number"))
                                        if build.get("to_process"):build.pop("to_process")
                                        if build.get("to_process_reason"):build.pop("to_process_reason")
                                        build = deploymentunitdb.trim_data_for_sync(
                                            build)
                                        if build.get("build_date"):
                                            build["build_date"] = str(
                                                build["build_date"]).split(".")[0]
                                        if build.get("file_path"):build.pop("file_path")                                    
                            if "build" in ldudata.keys():
                                if ldudata.get("build") and ldudata["build"].count() > 0:
                                    copylbuild = copy.deepcopy(
                                        ldudata["build"])
                                    if type(copylbuild) == Cursor : copylbuild = list(copylbuild)
                                    for build in copylbuild:
                                        build = deploymentunitdb.trim_data_for_sync(
                                            build)
                                        if build.get("build_date"):
                                            build["build_date"] = str(
                                                build["build_date"]).split(".")[0]
                                        if build.get("file_path"): build.pop("file_path")
                                        
                            # Use case when we dont want to process builds from source,but we have missing build in target
                            # There will be mismatch as source builds were not added to the target machine before, but now we are comparing
                            #To fix this we need to remove the build from both places which are marked as not to process and then compare them
                            for build in copy.deepcopy(copybuild) :
                                if build.get("build_number") in build_not_to_compare_list: copybuild.remove(build)
                            for build in copy.deepcopy(copylbuild) :
                                if build.get("build_number") in build_not_to_compare_list: copylbuild.remove(build)
                                                                                
                            any_change.append(
                                diff(copybuild, copylbuild))
                            # DeploymentFieldsCompare
                            if "deployment_field" in sync_du.keys():
                                if sync_du["deployment_field"] and "fields" in sync_du["deployment_field"].keys():
                                    copydeployfields = copy.deepcopy(
                                        sync_du["deployment_field"]["fields"])
                            if "deployment_field" in ldudata.keys():
                                if ldudata["deployment_field"] and "fields" in ldudata["deployment_field"].keys():
                                    copyldeployfields = copy.deepcopy(
                                        ldudata["deployment_field"]["fields"])
                            any_change.append(
                                diff(copydeployfields, copyldeployfields))
                            # IterChanges
                            changes = iter(any_change)
                            element = next(changes)
                            if element:
                                sync_du["operation"] = "update"
                                modified = 1
                                du["changed_object"].append(
                                    {"build": str(element)})
                                print "build are changed"
                            element = next(changes)
                            if element:
                                sync_du["operation"] = "update"
                                modified = 1
                                du["changed_object"].append(
                                    {"deployment_field": str(element)})
                                print "deployment fields are changed"
                        du["status"] = "compared"
                        du["updated_time"] = datetime.now()
                    du["du_data"] = sync_du
                    if modified == 1 and du["operation"] == "":
                        du["operation"] = "update"
                    elif modified == 0:
                        du["operation"] = ""
                        du["status"] = "success"
                        du["status_message"] = "No difference was found while comparing"
                    updated = syncDb.update_sync(du)
                except Exception as e:  # catch *all* exceptions
                    print 'SyncServices-Compare :' + str(e)
                    traceback.print_exc()
                    syncDb.update_sync_status(
                        str(du["_id"]["oid"]), "failed", "Comparing failed with error :" + str(e))

        # CHECK IF THERE ARE ANY ACTIVE DUS WHICH ARE NOT FOUND IN SYNC
        # COLLECTON FOR THE GIVEN SYNC ID
        # Check if sync_id (active sync request) was found to compare
        if sync_id and sync_type:
            print "HelperServices:compare: Load not exported list from sync data"
            not_exported_List = get_not_exorted_list(dus)
            print "HelperServices : compare : Checking if system has dus to delete from local."
            allactivedus = deploymentunitdb.GetAllDeploymentUnits(['active'])
            for activedu in allactivedus:
                recs = syncDb.get_sync_by_sync_id_and_name(
                    sync_id, "du_data.name", str(activedu["name"]))
                if recs is None or recs.count() <= 0:
                    if not_exported_List.get("dus") and str(activedu["name"]) in not_exported_List["dus"]:
                        skipdu = {}
                        skipactivedu = deploymentunitdb.GetDeploymentUnitById(
                            str(activedu["_id"]), False)
                        skipactivedu["operation"] = "skip"
                        skipdu["operation"] = "skip"
                        skipdu["tool_data"] = skipactivedu
                        skipdu["status"] = "skipped"
                        skipdu["status_message"] = "Skipped as du was not exported at source"
                        skipdu["sync_id"] = sync_id
                        skipdu["source_host"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        skipdu["target"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        skipdu["type"] = sync_type
                        updated = syncDb.add_sync(skipdu)
                        if updated:
                            print "HelperServices:compare: du " + activedu["name"] + \
                                " will be skipped from local."
                    else:
                        deletedu = {}
                        delactivedu = deploymentunitdb.GetDeploymentUnitById(
                            str(activedu["_id"]), False)
                        delactivedu["operation"] = "delete"
                        deletedu["operation"] = "delete"
                        deletedu["du_data"] = delactivedu
                        deletedu["status"] = "compared"
                        deletedu["sync_id"] = sync_id
                        deletedu["source_host"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        deletedu["target"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        deletedu["type"] = sync_type
                        updated = syncDb.add_sync(deletedu)
                        if updated:
                            print "HelperServices:compare: du " + activedu["name"] + \
                                " will be removed from local."
    except Exception as e:  # catch *all* exceptions
        traceback.print_exc()
        print 'SyncServices-Compare :' + str(e)

def get_not_exorted_list(data_list):
    if data_list and len(data_list) > 0:
        for data in data_list:
            directory_to_import_from = get_source_dir(data)
            if os.path.exists(os.path.join(directory_to_import_from, "notExportedList.json")):
                return FileUtils.returnJsonFromFiles(
                    directory_to_import_from, "notExportedList.json")
                
                
def compare_duset_for_sync():
    """Compare data for sync"""
    sync_id = sync_type = None
    try:
        print "HelperServices : compare :Checking if there is pending data to Process. If found Compare will be skipped"
        pending_process_list = syncDb.get_pending_sync_to_process()
        if pending_process_list:
            print "HelperServices : compare : There are active records to be Processed. New records will not be compared."
            return

        print "HelperServices:compare: comparing sync data"
        dusets = list(syncDb.get_pending_sync_to_compare())
        if dusets and len(dusets) > 0:
            for duset in dusets:
                if "duset_data" not in duset.keys():
                    continue
                duset["changed_object"] = []
                try:
                    sync_id, sync_type = get_sync_id_and_type(duset)
                    modified = 0
                    duset["_id"] = {"oid": str(duset["_id"])}
                    sync_duset = duset.get("duset_data")
                    # VALIDATE THE DUSET DETAILS
                    DuHelperService.validate_duset_data(sync_duset)
                    duset_name = sync_duset["name"]
                    ldusetdata = deploymentunitsetdb.GetDeploymentUnitSetByName(duset_name, False)
                    if ldusetdata is None:
                        print "HelperServices:compare: duset " + duset_name + " was not found in local DB."
                        duset["operation"] = "insert"
                        duset["status"] = "compared"
                        duset["status_message"] = ""
                        duset["updated_time"] = datetime.now()
                        modified = 1
                        duset["duset_data"] = sync_duset
                        updated = syncDb.update_sync(duset)
                        if updated:
                            print "HelperServices:compare:This duset will be created while processing"
                        else:
                            print "HelperServices:compare: Unable to trigger duset creation while processing"
                        continue
                    else:
                        print "HelperServices:compare: duset " + duset_name + " was found in local DB."
                        # CHANGE FORMAT AS SOURCE FOR SYNC COMPARISION
                        deploymentunitsetdb.parse_du_set_data_for_sync(ldusetdata)
                        sub = compare_duset_data(copy.deepcopy(
                            sync_duset), copy.deepcopy(ldusetdata))
                        if sub:
                            print "HelperServices:compare:du_data of tool " \
                                + duset_name + " is required to be updated as the tool data has changed."
                            duset["operation"] = "update"
                            dusetchange = {}
                            dusetchange["duset"] = str(sub)
                            duset["changed_object"].append(dusetchange)
                            modified = 1
                        else:
                            print "HelperServices:compare: duset_data of duset " \
                                + duset_name + " is not required to be updated.As duset data has not changed"
                            modified = 0                           
                        duset["status"] = "compared"
                        duset["updated_time"] = datetime.now()
                    duset["duset_data"] = sync_duset
                    if modified == 1 and duset["operation"] == "":
                        duset["operation"] = "update"
                    elif modified == 0:
                        duset["operation"] = ""
                        duset["status"] = "success"
                        duset["status_message"] = "No difference was found while comparing"
                    updated = syncDb.update_sync(duset)
                except Exception as e:  # catch *all* exceptions
                    print 'SyncServices-Compare :' + str(e)
                    traceback.print_exc()
                    syncDb.update_sync_status(
                        str(duset["_id"]["oid"]), "failed", "Comparing failed with error :" + str(e))

        # CHECK IF THERE ARE ANY ACTIVE DUS WHICH ARE NOT FOUND IN SYNC
        # COLLECTON FOR THE GIVEN SYNC ID
        # Check if sync_id (active sync request) was found to compare
        if sync_id and sync_type:
            print "HelperServices:compare: Load not exported list from sync data"
            not_exported_List = get_not_exorted_list(dusets)
            print "HelperServices : compare : Checking if system has dusset to delete from local."
            allactivedusets = deploymentunitsetdb.GetAllDeploymentUnitSet()
            for activeduset in allactivedusets:
                recs = syncDb.get_sync_by_sync_id_and_name(
                    sync_id, "duset_data.name", str(activeduset["name"]))
                if recs is None or recs.count() <= 0:
                    if not_exported_List.get("duset") and str(activeduset["name"]) in not_exported_List["duset"]:
                        skipduset = {}
                        skipactiveduset = deploymentunitsetdb.GetDeploymentUnitSetById(str(activeduset["_id"]), False)
                        skipduset["operation"] = "skip"
                        skipduset["duset_data"] = skipactiveduset
                        skipduset["status"] = "skipped"
                        skipduset["status_message"] = "Skipped as duset was not exported at source"
                        skipduset["sync_id"] = sync_id
                        skipduset["source_host"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        skipduset["target"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        skipduset["type"] = sync_type
                        updated = syncDb.add_sync(skipduset)
                        if updated:
                            print "HelperServices:compare: duset " + activeduset["name"] + \
                                " will be skipped from local."
                    else:
                        deleteduset = {}
                        delactiveduset = deploymentunitsetdb.GetDeploymentUnitSetById(
                            str(activeduset["_id"]), False)
                        deleteduset["operation"] = "delete"
                        deleteduset["duset_data"] = delactiveduset
                        deleteduset["status"] = "compared"
                        deleteduset["sync_id"] = sync_id
                        deleteduset["source_host"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        deleteduset["target"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        deleteduset["type"] = sync_type
                        updated = syncDb.add_sync(deleteduset)
                        if updated:
                            print "HelperServices:compare: duset " + activeduset["name"] + \
                                " will be removed from local."
    except Exception as e:  # catch *all* exceptions
        traceback.print_exc()
        print 'SyncServices-Compare :' + str(e)

def compare_states_for_sync():
    """Compare data for sync"""
    sync_id = sync_type = None
    try:
        print "HelperServices : compare :Checking if there is pending data to Process. If found Compare will be skipped"
        pending_process_list = syncDb.get_pending_sync_to_process()
        if pending_process_list:
            print "HelperServices : compare : There are active records to be Processed. New records will not be compared."
            return

        print "HelperServices:compare: comparing sync data"
        states = list(syncDb.get_pending_sync_to_compare())
        if states and len(states) > 0:
            for state in copy.deepcopy(states):
                if "state_data" not in state.keys():
                    continue
                state["changed_object"] = []
                try:
                    sync_id, sync_type = get_sync_id_and_type(state)
                    modified = 0
                    state["_id"] = {"oid": str(state["_id"])}
                    sync_state = state.get("state_data")
                    # VALIDATE THE DUSET DETAILS
                    StateHelperService.check_state_mandate_fields(sync_state)
                    state_name = sync_state["name"]
                    state_details=StateHelperService.convert_parent_names_to_ids(copy.deepcopy(sync_state)) 
                    lstatedata=statedb.get_state_by_parent_entity_id_name(state_name, state_details.get("parent_entity_id"), False)
                    lstatedata = statedb.add_state_details_for_sync(lstatedata)
                    if lstatedata is None:
                        print "HelperServices:compare: state " + state_name + " was not found in local DB."
                        state["operation"] = "insert"
                        state["status"] = "compared"
                        state["status_message"] = ""
                        state["updated_time"] = datetime.now()
                        modified = 1
                        state["state_data"] = sync_state
                        updated = syncDb.update_sync(state)
                        if updated:
                            print "HelperServices:compare:This state will be created while processing"
                        else:
                            print "HelperServices:compare: Unable to trigger state creation while processing"
                        continue
                    else:
                        print "HelperServices:compare: state " + state_name + " was found in local DB."
                        # CHANGE FORMAT AS SOURCE FOR SYNC COMPARISION
                        StateHelperService.convert_parent_ids_to_name(lstatedata)
                        if lstatedata.get("build"):
                            lstatedata["build_id"]=lstatedata.get("build").get("build_number")
                        sub = compare_state_data(copy.deepcopy(
                            sync_state), copy.deepcopy(lstatedata))
                        if sub:
                            print "HelperServices:compare:state of tool " \
                                + state_name + " is required to be updated as the tool data has changed."
                            state["operation"] = "update"
                            statechange = {}
                            statechange["state"] = str(sub)
                            state["changed_object"].append(statechange)
                            modified = 1
                        else:
                            modified = 0
                            any_change = []
                            copydeployfields = {}
                            copyldeployfields = {}
                            # DeploymentFieldsCompare
                            if "deployment_field" in sync_state.keys():
                                if sync_state["deployment_field"] and "fields" in sync_state["deployment_field"].keys():
                                    copydeployfields = copy.deepcopy(
                                        sync_state["deployment_field"]["fields"])
                            if "deployment_field" in lstatedata.keys():
                                if lstatedata["deployment_field"] and "fields" in lstatedata["deployment_field"].keys():
                                    copyldeployfields = copy.deepcopy(
                                        lstatedata["deployment_field"]["fields"])
                            any_change.append(
                                diff(copydeployfields, copyldeployfields))
                            # IterChanges
                            changes = iter(any_change)
                            element = next(changes)
                            if element:
                                sync_state["operation"] = "update"
                                modified = 1
                                state["changed_object"].append(
                                    {"deployment_field": str(element)})
                                print "deployment fields are changed"
                        state["status"] = "compared"
                        state["updated_time"] = datetime.now()
                    state["state_data"] = sync_state
                    if modified == 1 and state["operation"] == "":
                        state["operation"] = "update"
                    elif modified == 0:
                        state["operation"] = ""
                        state["status"] = "success"
                        state["status_message"] = "No difference was found while comparing"
                    updated = syncDb.update_sync(state)
                except Exception as e:  # catch *all* exceptions
                    print 'SyncServices-Compare :' + str(e)
                    traceback.print_exc()
                    syncDb.update_sync_status(
                        str(state["_id"]["oid"]), "failed", "Comparing failed with error :" + str(e))

        # CHECK IF THERE ARE ANY ACTIVE DUS WHICH ARE NOT FOUND IN SYNC
        # COLLECTON FOR THE GIVEN SYNC ID
        # Check if sync_id (active sync request) was found to compare
        if sync_id and sync_type:
            print "HelperServices:compare: Load not exported list from sync data"
            not_exported_List = get_not_exorted_list(states)
            print "HelperServices : compare : Checking if system has state to delete from local."
            allactivestates = statedb.get_state_all()
            for activestate in allactivestates:
                recs = syncDb.get_sync_by_sync_id_and_name(
                    sync_id, "state_data.name", str(activestate["name"]))
                if recs is None or recs.count() <= 0:
                    if not_exported_List.get("states") and str(activestate["name"]) in not_exported_List["states"]:
                        skipstate = {}
                        skipactivestate = statedb.get_state_by_id(str(activestate["_id"]), False)
                        skipstate["operation"] = "skip"
                        skipstate["state_data"] = skipactivestate
                        skipstate["status"] = "skipped"
                        skipstate["status_message"] = "Skipped as state was not exported at source"
                        skipstate["sync_id"] = sync_id
                        skipstate["source_host"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        skipstate["target"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        skipstate["type"] = sync_type
                        updated = syncDb.add_sync(skipstate)
                        if updated:
                            print "HelperServices:compare: state " + activestate["name"] + \
                                " will be skipped from local."
                    else:
                        deletestate = {}
                        delactiveduset =  statedb.get_state_by_id(str(activestate["_id"]), False)
                        deletestate["operation"] = "delete"
                        deletestate["state_data"] = delactiveduset
                        deletestate["status"] = "compared"
                        deletestate["sync_id"] = sync_id
                        deletestate["source_host"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        deletestate["target"] = systemDetail.get(
                            "hostname")  # THIS RECORD IS CREATED INTERNALLY
                        deletestate["type"] = sync_type
                        updated = syncDb.add_sync(deletestate)
                        if updated:
                            print "HelperServices:compare: state " + activestate["name"] + \
                                " will be removed from local."
    except Exception as e:  # catch *all* exceptions
        traceback.print_exc()
        print 'SyncServices-Compare :' + str(e)


def compare_duset_data(copyduset, copylduset):
    """Compare a duset data"""    
    keys_to_pop=["_id","operation","state"]
    for key in keys_to_pop:
        if copyduset.has_key(key):
            copyduset.pop(key)
        if copylduset.has_key(key):
            copylduset.pop(key)
    if "source_duset_id" in copyduset.keys():
        copyduset.pop("source_duset_id")
    if "source_duset_id" in copylduset.keys():
        copylduset.pop("source_duset_id")
    if "logo" in copyduset.keys():
        copyduset["logo"] = os.path.basename(copyduset.get("logo"))
    if "logo" in copylduset.keys():
        copylduset["logo"] = os.path.basename(copylduset.get("logo"))
    if "thumbnail_logo" in copyduset.keys():
        copyduset["thumbnail_logo"] = os.path.basename(
            copyduset.get("thumbnail_logo"))
    if "thumbnail_logo" in copylduset.keys():
        copylduset["thumbnail_logo"] = os.path.basename(
            copylduset.get("thumbnail_logo"))
    if "name" in copyduset.keys():
        copyduset["name"] = str(copyduset["name"]).lower()
    if "name" in copylduset.keys():
        copylduset["name"] = str(copylduset["name"]).lower()

    sub = diff(copyduset, copylduset)
    print "Difference in duset_data :" + str(sub)
    return sub

def compare_state_data(copystate, copylstate):
    """Compare a duset data"""    
    keys_to_pop=["_id","operation","deployment_field","build"]
    for key in keys_to_pop:
        if copystate.has_key(key):
            copystate.pop(key)
        if copylstate.has_key(key):
            copylstate.pop(key)
    if "name" in copystate.keys():
        copystate["name"] = str(copystate["name"]).lower()
    if "name" in copylstate.keys():
        copylstate["name"] = str(copylstate["name"]).lower()
    sub = diff(copystate, copylstate)
    print "Difference in state_data :" + str(sub)
    return sub

def compare_version_data(copyversion, copylversion):
    """Compare a version data"""
    keys_to_pop=["_id","tool_id","operation","document","build","media_file","deployment_field",\
                 "jenkins_job","gitlab_repo","git_url","gitlab_branch","source_version_id"]
    for key in keys_to_pop:
        if copyversion.has_key(key):
            copyversion.pop(key)
        if copylversion.has_key(key):
            copylversion.pop(key)
    if "version_date" in copyversion.keys():
        copyversion["version_date"] = str(datetime.strptime(
            (str(str(copyversion['version_date']).split()[0])), "%Y-%m-%d"))
    if "version_date" in copylversion.keys():
        copylversion["version_date"] = str(datetime.strptime(
            (str(str(copylversion['version_date']).split()[0])), "%Y-%m-%d"))
    if "pre_requiests" in copyversion.keys():
        if copyversion.get("pre_requiests") is None or len(copyversion.get("pre_requiests")) < 1:
            copyversion.pop("pre_requiests")
    if "pre_requiests" in copylversion.keys():
        if copylversion.get("pre_requiests") is None or len(copylversion.get("pre_requiests")) < 1:
            copylversion.pop("pre_requiests")

    if "mps_certified" in copyversion.keys():
        if copyversion.get("mps_certified") is None or len(copyversion.get("mps_certified")) < 1:
            copyversion.pop("mps_certified")
    if "mps_certified" in copylversion.keys():
        if copylversion.get("mps_certified") is None or len(copylversion.get("mps_certified")) < 1:
            copylversion.pop("mps_certified")

    if "version_name" in copylversion.keys():
        copylversion["version_name"] = str(
            copylversion["version_name"]).lower()
    if "version_name" in copyversion.keys():
        copyversion["version_name"] = str(copyversion["version_name"]).lower()
    sub = diff(copyversion, copylversion)
    print "Difference in version :" + str(sub)
    return sub

def compare_du_data(copydu, copyldu):
    """Compare a du data"""
    keys_to_pop=["_id","operation","state","source_du_id",\
                 "included_in","build","deployment_field"]
    for key in keys_to_pop:
        if copydu.has_key(key):
            copydu.pop(key)
        if copyldu.has_key(key):
            copyldu.pop(key)        
    if "logo" in copydu.keys():
        copydu["logo"] = os.path.basename(copydu.get("logo"))
    if "logo" in copyldu.keys():
        copyldu["logo"] = os.path.basename(copyldu.get("logo"))

    if "thumbnail_logo" in copydu.keys():
        copydu["thumbnail_logo"] = os.path.basename(
            copydu.get("thumbnail_logo"))
    if "thumbnail_logo" in copyldu.keys():
        copyldu["thumbnail_logo"] = os.path.basename(
            copyldu.get("thumbnail_logo"))
    if "name" in copydu.keys():
        copydu["name"] = str(copydu["name"]).lower()
    if "name" in copyldu.keys():
        copyldu["name"] = str(copyldu["name"]).lower()

    sub = diff(copydu, copyldu)
    print "Difference in du_data :" + str(sub)
    return sub

def compare_tool_data(copytool, copyltool):
    """Compare a tool data"""
    keys_to_pop=["_id","operation","versions","source_tool_id"]
    for key in keys_to_pop:
        if copytool.has_key(key):
            copytool.pop(key)
        if copyltool.has_key(key):
            copyltool.pop(key)        
    if "logo" in copytool.keys():
        copytool["logo"] = os.path.basename(copytool.get("logo"))
    if "logo" in copyltool.keys():
        copyltool["logo"] = os.path.basename(copyltool.get("logo"))

    if "thumbnail_logo" in copytool.keys():
        copytool["thumbnail_logo"] = os.path.basename(
            copytool.get("thumbnail_logo"))
    if "thumbnail_logo" in copyltool.keys():
        copyltool["thumbnail_logo"] = os.path.basename(
            copyltool.get("thumbnail_logo"))

    if "tool_creation_source" in copytool.keys():
        if copytool.get("tool_creation_source") is None or len(copytool.get("tool_creation_source")) < 1:
            copytool.pop("tool_creation_source")
    if "tool_creation_source" in copyltool.keys():
        if copyltool.get("tool_creation_source") is None or len(copyltool.get("tool_creation_source")) < 1:
            copyltool.pop("tool_creation_source")

    if "name" in copytool.keys():
        copytool["name"] = str(copytool["name"]).lower()
    if "name" in copyltool.keys():
        copyltool["name"] = str(copyltool["name"]).lower()

    sub = diff(copytool, copyltool)
    print "Difference in tool_data :" + str(sub)
    return sub




def create_lock(rec, lock_directory, lock_name, lock_data="", **kwargs):
    result = runCommand("cd {}; echo ".format(
        lock_directory) + lock_data + " | tee " + lock_name, True, None, **kwargs)
    if not result or result.return_code != 0:
        raise Exception(" unable to create lock with unknown error")
    else:
        print "lock file created..."


def remove_lock(rec, lock_directory, lock_name, **kwargs):
    if lock_name in str(runCommand('cd {}; find . -name '.format(lock_directory) + lock_name), True, None, **kwargs).lower():
        result = runCommand("cd {}; rm -f ".format(lock_directory) + lock_name)
        if result.return_code != 0:
            raise Exception(" unable to remove lock with unknown error")
        else:
            print "lock file removed..."
    else:
        raise Exception(lock_name + " was not found at: " + lock_directory)


def read_lock(rec, lock_directory, lock_name, **kwargs):
    try:
        if lock_name in str(runCommand('cd {}; find . -name '.format(lock_directory) + lock_name, True, None, **kwargs)).lower():
            return True
        else:
            return False
    except Exception as exp:  # catch *all* exceptions
        traceback.print_exc()
        raise Exception(
            "Unable to check if .lock file exists.Error: " + str(exp))


def get_source_dir(record):
    """Checking Import Folder and Write Access"""
    directory_to_import_from = record.get("stored_folder_name")
    if directory_to_import_from:
        if not os.path.exists(directory_to_import_from):
            raise ValueError(
                " Import Folder does not exists :" + directory_to_import_from)
        if not os.access(os.path.dirname(directory_to_import_from), os.W_OK):
            raise ValueError(
                "The directory does not have write access :" + directory_to_import_from)
        return directory_to_import_from
    else:
        if record.get("operation").lower() in ["insert", "update"]:
            raise ValueError("stored_folder_name was not found")


def get_distribution_list_and_status(config):
    """Get distribution list for sync"""
    full_sync_flag = None
    distribution_list = None
    if config.get("full_sync_flag") is None:
        raise Exception("full_sync_flag was not found")
    else:
        full_sync_flag = config.get("full_sync_flag").lower()                    
    if config.get("distribution_list") is None:
            raise Exception("distribution_list was not found")
    else:
        distribution_list = config.get(
                "distribution_list").lower()
    return full_sync_flag, distribution_list

def notify(sync_id, distribution_list, mailer):
    """Email User"""
    try:
        if str(distribution_list).strip() in ["None", None, ""]:
            print "HelperServices :notify:Email will not be send as distribution_list is not found"
            return
        recs = syncDb.get_sync_by_sync_id(sync_id)
        if recs:
            total_no_of_records = recs.count()
            total_no_of_records_success = 0
            total_no_of_records_failed = 0
            failed_issues = ""
            for rec in recs:
                if rec["status"].lower() == "success":
                    total_no_of_records_success = total_no_of_records_success + 1
                else:
                    total_no_of_records_failed = total_no_of_records_failed + 1
                    failed_issues = failed_issues + " " + \
                        str(rec["_id"]) + " : " + str(rec.get("status_message")) + " \n"
            mailer.send_html_notification(distribution_list, None, None, 6,
                                          {"name": "User",
                                           "total_no_of_records": total_no_of_records,
                                           "total_no_of_records_success": total_no_of_records_success,
                                           "total_no_of_records_failed": total_no_of_records_failed,
                                           "failed_issues": str(failed_issues)})
        else:
            print "HelperServices :notify: Email's will not be sent as no records with sync_id :" + sync_id + " were found"
    except Exception as e:  # catch *all* exceptions
        print 'HelperServices :notify:' + str(e)
        traceback.print_exc()
        print "HelperServices :notify:Notification failed. User will not be notified for sync_id :" + sync_id


def add_notify(sync_id, distribution_list, mailer):
    """Email User about a new sync request"""
    try:
        if str(distribution_list).strip() in ["None", None, ""]:
            print "HelperServices :notify:Email will not be send as distribution_list is not found"
            return
        recs = syncDb.get_sync_by_sync_id(sync_id)
        total_no_of_records = recs.count()
        tools_added = ""
        for rec in recs:
            if rec is not None:
                if rec.get("tool_data"):
                    if rec.get("tool_data").get("name"):
                        tools_added = tools_added + \
                            str(rec.get("tool_data").get("name")) + " <br>"
        mailer.send_html_notification(distribution_list, None, None, 7,
                                      {"name": "User", "sync_id": sync_id,
                                       "total_no_of_records": total_no_of_records,
                                       "tool_name": str(tools_added)})
    except Exception as e:  # catch *all* exceptions
        print 'HelperServices :Error :notify:' + str(e)
        traceback.print_exc()
        print "HelperServices :notify:Notification failed. User will not be notified for sync_id :" + sync_id
        
def handle_additional_data_while_processing_sync(directory_to_import_from,plugin_full_path):
    #HANDLE PREREQUSIT 
    if os.path.exists(os.path.join(directory_to_import_from, "preRequisitesData.json")):
        preRequisitesDB.delete_all_pre_requisites()    
        preRequisitesJsonData = FileUtils.returnJsonFromFiles(
            directory_to_import_from, "preRequisitesData.json")
        if preRequisitesJsonData and len(preRequisitesJsonData) > 0:
            for req in preRequisitesJsonData:
                preRequisitesDB.add_pre_requisites(
                    req)
      
    #HANDLE EXTERNAL PLUGINS    
    plugins_dir=directory_to_import_from+"/plugins"
    if os.path.exists(plugins_dir):
        files_and_dirs=os.listdir(plugins_dir)                    
        for rec in files_and_dirs:
            src=os.path.join(plugins_dir,rec)
            if os.path.isfile(src):
                if os.path.exists(os.path.join(plugin_full_path,rec)):
                    os.remove(os.path.join(plugin_full_path,rec))
                shutil.copy(src, os.path.join(plugin_full_path,rec))
            else:    
                for file_to_copy in os.listdir(src):
                    if os.path.exists(os.path.join(plugin_full_path,rec,file_to_copy)):
                        os.remove(os.path.join(plugin_full_path,rec,file_to_copy))
                    if not os.path.exists(os.path.join(plugin_full_path,rec)):
                        os.mkdir(os.path.join(plugin_full_path,rec))
                    shutil.copy(os.path.join(src,file_to_copy), os.path.join(plugin_full_path,rec,file_to_copy))
    
    #HANDLE EXTERNAL PLUGINGS DB
    if os.path.exists(os.path.join(directory_to_import_from, "erData.json")):
        er_data = FileUtils.returnJsonFromFiles(
            directory_to_import_from, "erData.json")
        if er_data and len(er_data) > 0:
            for er in er_data:
                if not exitPointPlugins.get_by_plugin_name(er.get("plugin_name")):
                    exitPointPlugins.add(er)     
                
    #HANDLE STATE STATUS  DB
    if os.path.exists(os.path.join(directory_to_import_from, "ssData.json")):
        ss_data = FileUtils.returnJsonFromFiles(
            directory_to_import_from, "ssData.json")
        if ss_data and len(ss_data) > 0:
            for ss in ss_data:
                if not deploymentUnitApprovalStatusDB.GetDeploymentUnitApprovalStatusByName(ss.get("name")):
                    deploymentUnitApprovalStatusDB.AddDeploymentUnitApprovalStatus(ss)
    
    #HANDLE REPOSITORY DB
    if os.path.exists(os.path.join(directory_to_import_from, "reData.json")):
        re_data = FileUtils.returnJsonFromFiles(
            directory_to_import_from, "reData.json")
        if re_data and len(re_data) > 0:
            for re in re_data:
                if not repositoryDb.get_repository_by_name(re.get("name"), False):
                    repositoryDb.add(re)
                    
    #HANDLE FLEXIBLE ATTRIBUTE    
    if os.path.exists(os.path.join(directory_to_import_from, "faData.json")):
        flexAttrDB.delete_all()
        fa_data = FileUtils.returnJsonFromFiles(
            directory_to_import_from, "faData.json")
        if fa_data and len(fa_data) > 0:
            for fa in fa_data:
                flexAttrDB.add(fa)
    
def retry_sync(_id,sync_id):
    modified_count=0;
    if _id and not sync_id:
        sync = syncDb.get_sync_by_id(_id)
        if sync is None:
            raise Exception ("no sync request found with object_id : " + _id)
        if sync.get("status").lower() != "failed":
            raise Exception("only failed requests can be retried")
        sync["status"]="retry"
        sync["callback_status"]="retry"
        sync["callback_status_reason"]="Requested to retry"
        sync["status_message"]="Requested to retry"
        oid=str(sync.get("_id"))
        sync["_id"]={"oid":oid}
        modified_count=syncDb.update_sync(sync)
    elif sync_id and not _id :
        syncs = syncDb.get_sync_by_sync_id(sync_id)
        if len(list(syncs))==0:
            raise Exception ("no sync request found with sync_id : " + sync_id)
        syncs.rewind()
        for sync in syncs:
            if sync.get("status").lower() == "failed":
                sync["status"]="retry"
                sync["status_message"]="Requested to retry"
                sync["callback_status"]="retry"
                sync["callback_status_reason"]="Requested to retry"
                oid=str(sync.get("_id"))
                sync["_id"]={"oid":oid}
                syncDb.update_sync(sync)
                modified_count+=1
        if modified_count == 0:
            raise Exception ("only failed requests can be retried")
    else:
        raise Exception("You can either retry complete sync or a particular sync request at time")

    return modified_count
