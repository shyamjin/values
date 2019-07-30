'''
Created on Mar 16, 2016

@author: PDINDA
'''



from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, wait
import logging
import os
from threading import Lock
import time
import traceback
import uuid
from autologging import logged
from DBUtil import Config, Sync, SyncRequest
from Services import  SyncServices, RemoteAuthenticationService, ConfigHelperService,\
    PushHelperService,PushTransferHelperService,SchedulerService
from Services.fabfile import runCommand
from settings import mongodb, export_full_path



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


@logged(logging.getLogger("PushServices"))
class PushServices(object):

    locker = Lock()
    # Init's Data

    def __init__(self):
        self.db = mongodb
        self.current_path = export_full_path
        if not os.path.exists(self.current_path):
            os.makedirs(self.current_path)
        if not os.access(os.path.dirname(self.current_path), os.W_OK):
            raise ValueError(
                "The directory does not have write access :" + self.current_path)
        self.remoteAuthenticationService = RemoteAuthenticationService.RemoteAuthenticationService()
        self.configdb = Config.Config(self.db)
        self.syncdb = Sync.Sync(self.db)
        self.syncRequestdb = SyncRequest.SyncRequest(self.db)
        self.syncService = SyncServices.SyncServices()
        self.remote_import_path = None
        self.count_of_files = 2  # Minimum Threads is 2
        self.allow_split = "true"  # Default split allowed
        self.config_id = 11
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()

    def load_configuration(self):
        ConfigHelperService.load_common_configuration(self)
        if self.result.get("remote_machine_import_path") is None:
            raise Exception(
                "remote_machine_import_path not found in config of PushServices")
        self.remote_import_path = self.result["remote_machine_import_path"]
        if self.result.get("count_of_files"):
            self.count_of_files = int(self.result["count_of_files"])
        if self.result.get("allow_split"):
            self.allow_split = str(self.result.get("allow_split")).lower()

    # This method runs in a given interval of  intervalGiven
    # if its already running then second instance will not get triggered
    # LOGIC
        # We are getting and active push request
        # If no request exists then skip job
        # validate data if all data exists
        # call authenticate def
    @ConfigHelperService.run
    def job_function(self):
        """Start of Push"""
        print ' started running at ' + time.ctime(time.time())
        self.load_configuration()
        machine_to_push_to = self.syncRequestdb.get_pending_sync_push()
        if len(machine_to_push_to) <= 0:
            print "No machine found to push to"            
        futures = []
        pool = ThreadPoolExecutor(2,__name__+".syncCall") # 2 threads for prod and non prod
        for rec in machine_to_push_to:
            futures.append(pool.submit(self.syncCall,rec))
        wait(futures)
        print ' ended running at ' + time.ctime(time.time())
        # YOU CANNOT EXPORT WHEN WE ARE PERFORMING A IMPORT.ALL METHODS SHOULD BE
    # LOCKED

    @synchronized(locker)
    def syncCall(self, rec):
        """Start processing a record"""
        try:
            self.load_configuration()
            self.syncRequestdb.update_deployment_request_status(
                str(rec["_id"]), "Started", "Push flow has started ")
            print "Trying to push to " + rec["host"]
            self.remoteAuthenticationService.authenticate(
                rec, self.pingMachine, rec)
            self.remoteAuthenticationService.authenticate(rec, self.push, rec)
            print "Am done pushing to " + rec["host"]
        except Exception as exception:  # catch *all* exceptions
            print 'failed to process push to :' + rec.get("host") + " with error :" + str(exception)
            traceback.print_exc()
            self.syncRequestdb.update_deployment_request_status(
                str(rec["_id"]), "Failed", "Error : " + str(exception))

    def pingMachine(self, rec, **kwargs):
        try:
            runCommand("hostname", False, **kwargs)
        except Exception as e:
            raise ValueError('ping machine failed with error : ' + str(e))

    # Prepare to push to machine
    def prepareRequest(self, rec):
        """Create zip file to be pushed"""
        self.syncRequestdb.update_deployment_request_status(
            str(rec["_id"]), "Preparing Started", "Preparing zip file")
        sync_id = str(uuid.uuid4())
        if not rec.get("filters_to_apply"):
            rec["filters_to_apply"] = {}
        rec["filters_to_apply"]["time_after"] = PushHelperService.decide_on_build_time(
            rec)  # INST IMP TO TAKE THE VALUE HERE
        # MARK BEFORE DOWNLOADING BUILDS
        rec["last_zip_cre_dt"] = datetime.now()
        
        file_created, toolName, toolNamesNotExported = self.syncService.createZipToExport({"file_path":self.current_path,"zip_file_name":sync_id,\
            "target_host":rec["host"],"sync_type":"push","external_artifacts":rec.get("external_artifacts")}, rec.get("filters_to_apply"))
       
        PushTransferHelperService.handle_input_for_push(file_created, self.allow_split,\
                                                 rec, toolName, toolNamesNotExported)
        self.syncRequestdb.update_deployment_request_status(str(
                rec["_id"]), "Preparing Completed", "Zip file" + str(os.path.basename(file_created)) + "was prepared to be pushed")
        return rec
        
    # Push zip file to target Account machine
    # Returns error is request fails
    # exports to path export_full_path of setting.py. Then takes zip file from this location and tries to push
    # Pushes to global path given in PushConfig .Or if folder_location exists
    # then pushes to this path
    def push(self, rec, **kwargs):
        """Created zip file to be pushed by this method"""
        # VALIDATE IF ALL FIELDS REQUIRED TO PULL A FILE ARE PRESENT
        PushHelperService.validatePushFile(rec)
        self.syncRequestdb.update_deployment_request_status(
            str(rec["_id"]), "Preparing File", "Creating a Zip file to push")
        sync_data = self.syncRequestdb.get_sync_request_by_id(rec["_id"])
        manual_invoke_ind = rec.get("manual_invoke_ind", False)
        if rec.get("manual_invoke_ind"):rec.pop("manual_invoke_ind")
        while(True):
            if not str(sync_data.get("copy_in_progress")).lower() == 'true' and PushTransferHelperService.check_if_lock_exists(rec, **kwargs):
                self.syncRequestdb.update_deployment_request_status(str(
                    rec["_id"]), "Pushing Aborted", "Lock:" + rec.get("zip_file_name") + ".lock was found.Retrying in 5 min's")
                print "Pushing Aborted Lock:" + rec.get("zip_file_name") + ".lock was found.Retrying in 5 min's"
                if manual_invoke_ind:
                    raise ValueError(
                        "Failed: " + "Lock:" + rec.get("zip_file_name") + ".lock was found.Cannot proceed")
                time.sleep(60 * 5)  # 5 min
            else:
                break
        if not sync_data.get("file_created") or not sync_data.get("zip_file_name") or not os.path.exists(os.path.normpath(sync_data.get("file_created"))) or \
                not str(sync_data.get("copy_in_progress")).lower() == 'true':
            PushHelperService.clear_old_data(rec, **kwargs)
            rec = self.prepareRequest(rec)
        self.syncRequestdb.update_deployment_request_status(str(
            rec["_id"]), "Pushing Started", "File" + str(os.path.basename(rec["file_created"])) + " is being pushed")
        PushTransferHelperService.start_push_to_remote(rec, **kwargs)        
        self.syncRequestdb.update_deployment_request_status(str(
            rec["_id"]), "Pushing Completed", "File" + str(os.path.basename(rec["file_created"])) + " is pushed")
        sync_data = self.syncRequestdb.get_sync_request_by_id(rec["_id"])
        if str(rec.get("trigger_ind")).lower() == "true":
            print "Push Service :trigger is True.Tyring to trigger sync process on targethost :" + rec["host"]
            PushHelperService.triggerRequest(rec)
        PushHelperService.notify(rec)
        print 'Push Service: ended running at ' + time.ctime(time.time())

    def schedule(self):
        """
        # Schedules the job
        # scheduler :Scheduler object
        # interval_given:Time interval for job to rerun"""
        global job
        self.load_configuration()
        job = self.schedulerService.schedule(job, self)
