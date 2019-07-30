'''
Created on Mar 16, 2016

@author: PDINDA
'''
import copy
from datetime import datetime
import logging
from os import listdir
import os
from os.path import isfile, join
import shutil
from threading import Lock
import time
import traceback

from autologging import logged

from DBUtil import Config, DistributionSync, Tool, Versions
from Services import Mailer, FileUtils, HelperServices, ToolHelperService
from Services import SchedulerService, ConfigHelperService,SyncHelperService
from settings import mongodb, current_path, \
    distribution_center_import_full_path, \
    distribution_center_export_full_path, \
    distribution_center_import_path, logo_path, logo_full_path, \
    media_path, media_full_path



job = None


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


@logged(logging.getLogger("DistributionSyncServices"))
class DistributionSyncServices(object):

    zipFileCreatorLock = Lock()
    # Init's Data

    def __init__(self):
        """Initializing Variable """
        self.db = mongodb
        self.distributionSync = DistributionSync.DistributionSync(self.db)
        self.toolDB = Tool.Tool(self.db)
        self.versionsDB = Versions.Versions(self.db)
        self.mailer = Mailer.Mailer()
        self.static_folder_path = current_path
        self.current_import_path = distribution_center_import_full_path
        self.current_import_small_path = distribution_center_import_path
        if self.current_import_path in [None, ""]:
            raise ValueError("Import path was not provided")
        if not os.path.exists(self.current_import_path):
            os.makedirs(self.current_import_path)
        if not os.access(os.path.dirname(self.current_import_path), os.W_OK):
            raise ValueError(
                "The directory does not have write access :" + self.current_import_path)
        self.current_export_path = distribution_center_export_full_path
        if self.current_export_path in [None, ""]:
            raise ValueError("Export path was not provided")
        if not os.path.exists(self.current_export_path):
            os.makedirs(self.current_export_path)
        if not os.access(os.path.dirname(self.current_export_path), os.W_OK):
            raise ValueError(
                "The directory does not have write access :" + self.current_export_path)
        self.configdb = Config.Config(self.db)
        self.logo_path = logo_path
        self.full_logo_path = logo_full_path
        self.media_files_path = media_path
        self.full_media_files_path = media_full_path
        self.config_id = 13
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()

    def load_configuration(self):
        ConfigHelperService.load_common_configuration(self)

    # This method runs in a given interval of  intervalGiven
    # if its already running then second instance will not get triggered
    # LOGIC
        # We are checking if we have any pending zip files to process (Only if listner is true)
        # For pending sync data perform compare and process them
    @ConfigHelperService.run
    def job_function(self):
        """Start of DistributionSyncServices"""
        print ' started running at ' + time.ctime(time.time())
        print ' job_function: Will check if files are pending to process '
        self.load_configuration()
        self.checkPendingImports()
        self.compare()
        print ' ended running at ' + time.ctime(time.time())
    # Check if we have pending Imports
    # If found validate them and add to sync collection

    def checkPendingImports(self):
        """Checking Pending Import """
        try:
            onlyfiles = [f for f in listdir(self.current_import_path) if isfile(join(
                self.current_import_path, f)) if "DPM_tools_manifest" in str(f) and not str(f).endswith("_done.zip")]
            if onlyfiles is not None:
                if len(onlyfiles) <= 0:
                    print "No pending zip files to process"
                    return
            for selected_file in onlyfiles:
                try:
                    file_path = join(self.current_import_path, selected_file)
                    file_name = os.path.basename(file_path)
                    file_name_without_ext = os.path.splitext(file_name)[0]
                    print " Processing file :" + file_path
                    if os.path.isfile(join(self.current_import_path, file_name_without_ext) + '_done.zip'):
                        print join(self.current_import_path, file_name_without_ext) \
                            + '_done.zip' + ' was found. Deleting it'
                        os.remove(join(self.current_import_path,
                                       file_name_without_ext) + '_done.zip')
                    if os.path.exists(join(self.current_import_path, file_name_without_ext)):
                        print join(self.current_import_path, file_name_without_ext) \
                            + ' was found. Deleting it'
                        shutil.rmtree(
                            join(self.current_import_path, file_name_without_ext))
                    print 'checkPendingImports : Am processing ' \
                        + file_path
                    folder_path = \
                        os.path.normpath(FileUtils.unzipImportFile(file_path))
                    toolJsonData = FileUtils.returnJsonFromFiles(
                        folder_path, 'data.json')
                    SyncHelperService.validate_sync_data_from_json(
                        toolJsonData, False)
                    generalJsonData = FileUtils.returnJsonFromFiles(
                        folder_path, "generalData.json")
                    if generalJsonData is None:
                        raise ValueError(
                            "generalData.json was not found inside the zip file")
                    self.distributionSync.CancelAllDistributions()
                    for rec in toolJsonData:
                        rec = self.updatePaths(
                            join(self.current_import_small_path, os.path.basename(folder_path)), rec)
                        # THIS IS USED IN CLEANER SERVICES
                        rec["stored_folder_name"] = folder_path
                        idd = self.distributionSync.AddDistribution(rec)
                        print " New tool " + rec.get("tool_data").get("name") + " was added in Sync with _id :" + str(idd)
                    try:
                        self.add_notify(
                            self.result.get("distribution_list"))
                    except Exception as e_value:  # catch *all* exceptions
                        print 'Email will not be sent due to error :' \
                            + str(e_value)
                    FileUtils.renameFile(file_path, join(
                        self.current_import_path, os.path.splitext(file_name)[0] + "_done.zip"))
                    print 'checkPendingImports: Am done processing ' \
                        + join(self.current_import_path, os.path.splitext(file_name)[0]
                               + '_done.zip')
                except Exception as e_value:  # catch *all* exceptions
                    print 'checkPendingImports: File :' \
                        + str(file_path) + \
                        ' was skipped due to error ' + str(e_value)
                    FileUtils.renameFile(file_path, join(self.current_import_path, os.path.splitext(
                        file_name)[0] + "_failed_as_" + str(e_value).replace(" ", "_") + "_done.zip"))
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            print 'checkPendingImports: Error while unzipping pending files :' + str(e_value)

    def add_notify(self, distribution_list=None):
        """Send Notify Email Once DistributionSyncServices Done """
        try:
            if str(distribution_list).strip() in ["None", None, ""]:
                print "notify:Email will not be send as distribution_list is not found"
                return
            recs = self.distributionSync.GetNewDistribution()
            total_no_of_records = recs.count()
            tools_added = ""
            for rec in recs:
                if rec is not None:
                    if rec.get("tool_data"):
                        if rec.get("tool_data").get("name"):
                            tools_added = tools_added + \
                                str(rec.get("tool_data").get("name")) + " <br>"
            self.mailer.send_html_notification(distribution_list, None, None, 11,
                                               {"name": "User", "total_no_of_records": total_no_of_records, "tool_name": str(tools_added)})
        except Exception as e_value:  # catch *all* exceptions
            print 'HelperServices :Error :notify:' + str(e_value)
            traceback.print_exc()
            print "HelperServices:Notification failed.User will not be notified for DistributionSyncServices"

    def notifyCompared(self, distribution_list=None):
        """Send Notify Email Once DistributionSyncServices Compared Done """
        try:
            if str(distribution_list).strip() in ["None", None, ""]:
                print "notify:Email will not be send as distribution_list is not found"
                return
            recs = self.distributionSync.GetComparedAndSuccessDistribution()
            total_no_of_records = 0
            total_no_of_records_new = 0
            total_no_of_records_updated = 0
            total_no_of_records_failed = 0
            total_no_of_records_success = 0
            for rec in recs:
                total_no_of_records = total_no_of_records + 1
                if rec.get("status").lower() in ["compared"] and rec.get("operation").lower() in ["insert"]:
                    total_no_of_records_new = total_no_of_records_new + 1
                elif rec.get("status").lower() in ["compared"] and rec.get("operation").lower() in ["update"]:
                    total_no_of_records_updated = total_no_of_records_updated + 1
                elif rec.get("status").lower() in ["failed"]:
                    total_no_of_records_failed = total_no_of_records_failed + 1
                elif rec.get("status").lower() in ["success"]:
                    total_no_of_records_success = total_no_of_records_success + 1
            self.mailer.send_html_notification(distribution_list, None, None, 12,
                                               {"name": "User", "total_no_of_records": total_no_of_records, "total_no_of_records_new": str(total_no_of_records_new), "total_no_of_records_updated": str(total_no_of_records_updated), "total_no_of_records_failed": str(total_no_of_records_failed), "total_no_of_records_success": str(total_no_of_records_success)})
        except Exception as e_value:  # catch *all* exceptions
            print 'HelperServices :Error :notify:' + str(e_value)
            traceback.print_exc()

    def updatePaths(self, folder_path, rec):
        """Update path For Logo and Thumbnail"""
        folder_logo_path = os.path.normpath(join(folder_path, 'logos'))
        folder_media_path = join(folder_path, 'mediaFiles')
        if rec.get("tool_data"):
            tool_data = rec.get("tool_data")
            if tool_data.get("logo"):
                if "default" in tool_data.get("logo"):
                    tool_data["logo"] = os.path.normpath(
                        join(self.logo_path, os.path.basename(tool_data.get("logo"))))
                else:
                    tool_data["logo"] = os.path.normpath(
                        join(folder_logo_path, os.path.basename(tool_data.get("logo"))))
            if tool_data.get("thumbnail_logo"):
                if "default" in tool_data.get("thumbnail_logo"):
                    tool_data["thumbnail_logo"] = os.path.normpath(
                        join(self.logo_path, os.path.basename(tool_data.get("thumbnail_logo"))))
                else:
                    tool_data["thumbnail_logo"] = os.path.normpath(
                        join(folder_logo_path, os.path.basename(tool_data.get("thumbnail_logo"))))
            if tool_data.get("versions"):
                versions = tool_data.get("versions")
                updated_versions = []
                for ver in versions:
                    media_files = []
                    if ver.get("media_file") and ver.get("media_file").get("media_files"):
                        for media in ver.get("media_file").get("media_files"):
                            if media.get("url"):
                                media["url"] = os.path.normpath(
                                    join(folder_media_path, os.path.basename(media.get("url"))))
                            if media.get("thumbnail_url"):
                                media["thumbnail_url"] = os.path.normpath(
                                    join(folder_media_path, os.path.basename(media.get("thumbnail_url"))))
                            if media.get("full_url"):
                                media["full_url"] = os.path.normpath(
                                    join(folder_media_path, os.path.basename(media.get("full_url"))))
                            media_files.append(media)
                        ver["media_file"]["media_files"] = media_files
                    updated_versions.append(ver)
                tool_data["versions"] = updated_versions
                rec["tool_data"] = tool_data
        return rec

    def compare(self):
        """Comparing sync data"""
        try:
            print "compare: comparing sync data"
            tools = self.distributionSync.GetNewDistribution()
            if tools and tools.count() > 0:
                for tool in tools:
                    tool["changed_object"] = []
                    try:
                        modified = 0
                        tool_id = {}
                        tool_id["oid"] = str(tool["_id"])
                        tool["_id"] = tool_id
                        distributedTool = tool.get("tool_data")
                        # VALIDATE THE TOOL DETAILS
                        ToolHelperService.validate_tool_data(distributedTool)
                        tool_name = distributedTool["name"]
                        ltooldata = self.toolDB.get_tool_by_name(tool_name)
                        if ltooldata is None:
                            print "compare: tool " + tool_name + " was not found in local DB."
                            tool["operation"] = "insert"
                            tool["status"] = "compared"
                            tool["updated_time"] = datetime.now()
                            distributedTool["operation"] = "insert"
                            modified = 1
                            tool["tool_data"] = distributedTool
                            # updated=1
                            updated = self.distributionSync.UpdateDistribution(
                                tool)
                            if updated:
                                print "compare:This tool will be created while processing"
                            else:
                                print "compare: Unable to trigger tool creation while processing"
                            continue
                        else:
                            print "compare: tool " + tool_name + " was found in local DB."
                            sub = SyncHelperService.compare_tool_data(
                                copy.deepcopy(distributedTool), copy.deepcopy(ltooldata))
                            if sub:
                                print "compare:tool_data of tool " + tool_name + " is required to be updated as the tool data has changed."
                                distributedTool["operation"] = "update"
                                tool["operation"] = "update"
                                toolchange = {}
                                toolchange["tool"] = str(sub)
                                tool["changed_object"].append(toolchange)
                                modified = 1
                            else:
                                print "compare: tool_data of tool " + tool_name + " is not required to be updated.As tool data has not changed"
                                distributedTool["operation"] = ""
                                modified = 0
                            syncversions = []
                            for version in distributedTool["versions"]:
                                localversion, isActive = list(self.versionsDB.get_version_detail_and_status(
                                    str(ltooldata["_id"]), version["version_number"], version["version_name"], True))
                                if localversion:
                                    ToolHelperService.get_dependend_tools(
                                        localversion, True)
                                    if isActive:
                                        sub = SyncHelperService.compare_version_data(
                                            copy.deepcopy(version), copy.deepcopy(localversion))
                                        if sub:
                                            print "compare:versions of  tool " + tool_name + " is required to be updated as the version has changed."
                                            version["operation"] = "update"
                                            modified = 1
                                            versionchange = {}
                                            versionchange["version"] = str(sub)
                                            tool["changed_object"].append(
                                                versionchange)
                                            # version["version_id"]= str(localversion["_id"])
                                        else:
                                            print "compare:versions of tool " + tool_name + " is not required to be updated.As versions has not changed"
                                            version["operation"] = ""
                                    else:
                                        version["operation"] = "update"
                                        modified = 1
                                        versionchange = {}
                                        versionchange["version"] = str(
                                            "Version is not active")
                                        tool["changed_object"].append(
                                            versionchange)
                                else:
                                    version["operation"] = "insert"
                                    modified = 1
                                    versionchange = {}
                                    versionchange["version"] = str(
                                        "Version was not found")
                                    tool["changed_object"].append(
                                        versionchange)
                                syncversions.append(version)
                            tool["status"] = "compared"
                            tool["updated_time"] = datetime.now()
                            distributedTool["versions"] = syncversions
                        tool["tool_data"] = distributedTool
                        if modified == 1 and tool["operation"] == "":
                            tool["operation"] = "update"
                        elif modified == 0:
                            tool["operation"] = ""
                            tool["status"] = "success"
                            tool["status_message"] = "No difference was found while comparing"
                        updated = self.distributionSync.UpdateDistribution(
                            tool)
                    except Exception as e_value:  # catch *all* exceptions
                        print 'DistributionSyncServices-Compare :' + str(e_value)
                        traceback.print_exc()
                        self.distributionSync.UpdateDistributionStatus(
                            str(tool["_id"]["oid"]), "failed", "Comparing failed with error :" + str(e_value))
                # SEND EMAIL ONLY IF WE HAVE NEW TOOLS
                try:
                    self.notifyCompared(self.result.get("distribution_list"))
                except Exception as e_value:  # catch *all* exceptions
                    print 'compare : An email will not be sent due to error :' + str(e_value)
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            print 'DistributionSyncServices-Compare :' + str(e_value)

    def schedule(self):
        """
        # Schedules the job
        # scheduler :Scheduler object
        # interval_given:Time interval for job to rerun"""
        global job
        self.load_configuration()
        job = self.schedulerService.schedule(job, self)
