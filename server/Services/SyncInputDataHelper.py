'''
Created on Mar 16, 2016

@author: PDINDA
'''
import logging
from os import listdir
import os
from os.path import isfile, join, isdir
import shutil
import subprocess
from threading import Lock
import time
import traceback
from autologging import logged
from DBUtil import Sync 
import FileUtils
from Services import SyncHelperService,ConfigHelperService,Mailer
from settings import mongodb, import_full_path, export_full_path

mailer = Mailer.Mailer()

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


@logged(logging.getLogger(__name__))
class SyncInputDataHelper(object):

    # Init's Data
    def __init__(self):
        self.db = mongodb
        self.current_import_path = import_full_path
        self.current_export_path = export_full_path
        self.config_id = 9
        self.syncDb = Sync.Sync(self.db)
        
    def load_configuration(self):
        ConfigHelperService.load_common_configuration(self)
            
    @synchronized(locker)
    def run_service(self):       
        self.load_configuration() 
        self.meargezipfile()
        self.checkPendingImports()
        self.renameInvalidFiles()
        print 'ended running at ' + time.ctime(time.time())

    def meargezipfile(self):
        try:
            onlydirectory = [f for f in listdir(self.current_import_path) if\
                             isdir(join(self.current_import_path, f)) if (str(str(f).lower()).endswith("_push")
                                                                                                                          or str(str(f).lower()).endswith("_manual") or str(str(f).lower()).endswith("_pull"))]
            # SORT FILES BY CREATE DATE
            onlydirectory.sort(key=lambda fn: os.path.getmtime(
                os.path.join(self.current_import_path, fn)))
            if onlydirectory is not None:
                if len(onlydirectory) <= 0:
                    print " meargezipfile: No pending directory to process"
                    return
            for directory in onlydirectory:
                dir_path = join(self.current_import_path, directory)
                if "wip" in str(listdir(dir_path)).lower() or "zip" not in str(listdir(dir_path)).lower():
                    continue
                try:
                    source_file_to_merge = os.path.normpath(os.path.join(dir_path, directory + '.zip*'))
                    target_merged_file = os.path.normpath(os.path.join(self.current_import_path, directory + '.zip'))
                    print " meargezipfile: Trying to merge files in dir: "+source_file_to_merge+" to: "+target_merged_file
                    print 'cat ' + source_file_to_merge + ' > ' + target_merged_file
                    print subprocess.check_output('cat ' + source_file_to_merge + ' > ' + target_merged_file, shell=True, stderr=subprocess.STDOUT)
                    print "Trying to remove dir:" + dir_path
                    shutil.rmtree(dir_path)
                    try:
                        print "Trying to remove lock file:" + dir_path + ".lock"
                        if os.path.isfile(dir_path + ".lock"):
                            os.remove(dir_path + ".lock")
                        if os.path.isfile(dir_path + ".zip.lock"):
                            os.remove(dir_path + ".zip.lock")
                    except Exception:
                        pass
                except Exception as e_value:  # catch *all* exceptions
                    traceback.print_exc()
                    print "Trying to rename dir:" + dir_path + " to " + dir_path + "_failed_" + str(e_value)
                    os.rename(dir_path, dir_path +
                              "_failed_" + str(e_value))
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            print 'checkPendingImports:Error in unzipping pending files:' + str(e_value)

    def renameInvalidFiles(self):
        """Rename Invalid Files"""
        try:
            onlyfiles = [f for f in listdir(self.current_import_path) if isfile(
                join(self.current_import_path, f)) if not "done" in str(f).lower() if not str(f).lower().endswith(".lock") if not str(f).lower().endswith(".wip")]
            if onlyfiles is not None:
                if len(onlyfiles) <= 0:
                    print " renameInvalidFiles: No invalid  files to rename"
                    return
            for file_rename in onlyfiles:
                file_path = join(self.current_import_path, file_rename)
                file_name = os.path.basename(file_path)
                FileUtils.renameFile(file_path, join(self.current_import_path, os.path.splitext(
                    file_name)[0] + "_failed_as_invalid_file" + "_done" + os.path.splitext(file_name)[1]))
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            print 'renameInvalidFiles: Error while processing pending files :' + str(e_value)
    # Check if we have pending Imports
    # If found validate them and add to sync collection

    def checkPendingImports(self):
        """Checking Pending Imports"""
        try:
            onlyfiles = [f for f in listdir(self.current_import_path) if isfile(join(self.current_import_path, f)) if str(
                str(f).lower()).endswith("zip") if not str(str(f).lower()).endswith("done.zip")]
            # SORT FILES BY CREATE DATE
            onlyfiles.sort(key=lambda fn: os.path.getmtime(
                os.path.join(self.current_import_path, fn)))
            if onlyfiles is not None:
                if len(onlyfiles) <= 0:
                    print " checkPendingImports: No pending zip files to process"
                    return
            for file in onlyfiles:
                file_path = join(self.current_import_path, file)
                file_name = os.path.basename(file_path)
                file_name_without_ext = os.path.splitext(file_name)[0]
                try:
                    print " checkPendingImports: Processing file :" + file_path
                    if os.path.isfile(join(self.current_import_path, file_name_without_ext) + "_done.zip"):
                        print join(self.current_import_path, file_name_without_ext) + "_done.zip" + " was found. Deleting it"
                        os.remove(join(self.current_import_path,
                                       file_name_without_ext) + "_done.zip")
                    if os.path.exists(join(self.current_import_path, file_name_without_ext)):
                        print join(self.current_import_path, file_name_without_ext) + " was found. Deleting it"
                        shutil.rmtree(
                            join(self.current_import_path, file_name_without_ext))
                    print "checkPendingImports : Am processing " + file_path
                    folder_path = os.path.normpath(
                        FileUtils.unzipImportFile(file_path))
                    self.add_records_to_sync(folder_path) # PROCESS DATA
                    try:
                        print "Trying to remove lock file:" + folder_path + ".lock"
                        if os.path.isfile(folder_path + ".lock"):
                            os.remove(folder_path + ".lock")
                        if os.path.isfile(folder_path + ".zip.lock"):
                            os.remove(folder_path + ".zip.lock")
                    except Exception:
                        pass
                    FileUtils.renameFile(file_path, join(
                        self.current_import_path, os.path.splitext(folder_path)[0] + "_done.zip"))
                    print "checkPendingImports: Am done processing " + join(self.current_import_path, os.path.splitext(folder_path)[0] + "_done.zip")
                except Exception as e_value:  # catch *all* exceptions
                    print 'checkPendingImports: File :' + str(file_path) + " was skipped due to error " + str(e_value)
                    new_name = os.path.normpath(join(os.path.dirname(
                        file_path), file_name_without_ext)) + "_failed_as_" + str(e_value).replace(" ", "_") + "_done.zip"
                    FileUtils.renameFile(file_path, new_name)
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            print 'checkPendingImports:Error in unzipping pending files:' + str(e_value)
    
    
    def add_records_to_sync(self,folder_path):
        toolJsonData = FileUtils.returnJsonFromFiles(
                        folder_path, "data.json")
        SyncHelperService.validate_sync_data_from_json(toolJsonData)
        sync_id = None
        type = None
        for rec in toolJsonData:
            sync_id = rec.get("sync_id")
            type = rec.get("type").lower()
            if rec is not None:
                # THIS IS USED IN CLEANER SERVICES
                rec["stored_folder_name"] = folder_path
                idd = self.syncDb.add_sync(rec)
                print " New record was added in Sync with _id :" + str(idd) + " and type :" + rec.get("type") + " and sync_id :" + rec.get("sync_id")
            else:
                raise ValueError(
                    " No data found for :") + folder_path
        try:
            # Distribution_list can be empty # full_sync_flag is
            # mandatory
            full_sync_flag, distribution_list = SyncHelperService.get_distribution_list_and_status(
                self.result)
            SyncHelperService.add_notify(
                sync_id, distribution_list, mailer)
        except Exception as e_value:  # catch *all* exceptions
            print 'checkPendingImports: An email will not be sent due to error :' + str(e_value)         