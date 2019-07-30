'''
Created on Mar 16, 2016

@author: PDINDA
'''

'''
###Scope###

###Limitations###

###Assumptions###


####Possible Inputs###

# 1)PULL A URL FILE
{
    "_id" : ObjectId("58257ced7fe7b94388f4f08a"),
    "status" : "active",
    "sync_type" : "Pull",
    "full_sync_flag" : "true",
    "target_dpm_detail" : {
        "dpm_username" : "VwHsY39bx8WpzJ5bKq23Kn4ybtVLR3agJre6iQgf8MZ0TfJJ2OHvOz/LPLmn7dGy",
        "dpm_host" : "dgfg",
        "dpm_token" : "dfgf",
        "dpm_port" : "534",
        "dpm_password" : "xJJzKdnkqcHlrOucdB4hu8CnxVddF+bD9ObZrykUKDY/Hw+jnzi1HkThqeRXydlI"
    },
    "distribution_list" : "dfgf@sd.com",
    "notification_type" : "always"
}


# 2)PULL A FILE
{
    "_id" : ObjectId("58245f697fe7b92e7c11e1eb"),
    "status" : "active",
    "sync_type" : "Pull",
    "pull_type" : "file",
    "remote_source_location" : "/home/valuepack/dpm/static/DPMDataUpdates/imports/",
    "full_sync_flag" : "false",
    "target_dpm_detail" : {
        "dpm_username" : "eQj0fV+HGlT+szgVnJNPSibH+yaqXDp6oKuEA4dH6tKInC6TJvzfgUXPZFocq/Wx",
        "dpm_host" : "asds",
        "dpm_password" : "6SnVxXHfJLQrITQzU1U71MUZjithh5Trq4JPiqjONv3V7TXi8INYA0S3TuvFgeNh"
    },
    "distribution_list" : "pdinda@amdocs.com",
    "notification_type" : "always",
}

'''


import cgi
from datetime import datetime
import json
import logging
import os
import errno
import subprocess
from threading import Lock
import time
import traceback
from urllib2 import Request, urlopen

from autologging import logged
from concurrent.futures import ThreadPoolExecutor, wait
import requests
from requests.exceptions import ConnectionError, ReadTimeout

from DBUtil import Config, Sync, SyncRequest, SystemDetails
from Services import Mailer, SyncServices, RemoteAuthenticationService, ConfigHelperService
from Services import SchedulerService
from Services.fabfile import copyFromRemote, runCommand
from settings import mongodb, import_full_path, dpm_url_prefix


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


@logged(logging.getLogger("PullServices"))
class PullServices(object):

    locker = Lock()
    # Init's Data

    def __init__(self):
        self.db = mongodb
        self.current_import_path = import_full_path
        if not os.path.exists(self.current_import_path):
            os.makedirs(self.current_import_path)
        if not os.access(self.current_import_path, os.W_OK):
            raise ValueError(
                "The directory does not have write access :" + self.current_import_path)
        self.configdb = Config.Config(self.db)
        self.syncdb = Sync.Sync(self.db)
        self.syncRequestdb = SyncRequest.SyncRequest(self.db)
        self.mailer = Mailer.Mailer()
        self.syncService = SyncServices.SyncServices()
        self.systemDetailsDb = SystemDetails.SystemDetails(self.db)
        self.systemDetail = self.systemDetailsDb.get_system_details_single()
        self.remoteAuthenticationService = RemoteAuthenticationService.RemoteAuthenticationService()
        if not self.systemDetail:
            raise Exception("systemDeatils not found")
        if not self.systemDetail.get("hostname"):
            raise Exception("hostname not found in systemDeatils")
        self.host_name = self.systemDetail.get("hostname")
        self.post_url = "/sync/pull/export"
        self.config_id = 10
        self.count_of_files = 2  # Minimum Threads is 2
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()

    def load_configuration(self):
        ConfigHelperService.load_common_configuration(self)
        if self.result.get("count_of_files"):
            self.count_of_files = int(self.result["count_of_files"])

    # This method runs in a given interval of  intervalGiven
    # if its already running then second instance will not get triggered
    @ConfigHelperService.run
    def job_function(self):
        """Start of Push"""
        print ' started running at ' + time.ctime(time.time())
        self.load_configuration()
        machine_to_pull_from = self.syncRequestdb.get_pending_sync_pull()
        if len(machine_to_pull_from) <= 0:
            print "No machine found to pull from"
            return
        for rec in machine_to_pull_from:
            try:
                self.syncCall(rec)
            finally:
                if rec.get("notification_type") is not None and rec.get("distribution_list") is not None:
                    if rec.get("notification_type").lower() == "always":  self.notify(rec)
                    elif rec.get("notification_type").lower() == "only if fails":
                        if str(self.syncRequestdb.get_sync_request_by_id(str(rec["_id"]))\
                               ["last_sync_status"]).lower().contains("failed"):
                            self.notify(rec)
        print ' ended running at ' + time.ctime(time.time())

    # YOU CANNOT EXPORT WHEN WE ARE PERFORMING A IMPORT.ALL METHODS SHOULD BE
    # LOCKED
    @synchronized(locker)
    def syncCall(self, rec):
        """Start processing a record"""
        try:
            print "Am trying to pull ....."
            self.load_configuration()
            self.syncRequestdb.update_deployment_request_status(
                str(rec["_id"]), "Started", "Pull flow has started ")
            self.pull(rec)
            print "Am done pulling ....."
            try:
                print "Am trying to process received file ....."
                self.syncService.job_function()
            except Exception as e:  # catch *all* exceptions
                print str(e)
        except Exception as e:  # catch *all* exceptions
            print 'failed to process pull with error :' + str(e)
            traceback.print_exc()
            self.syncRequestdb.update_deployment_request_status(
                str(rec["_id"]), "Failed", "Error : " + str(e))

    # Notify users about the request
    def notify(self, rec):
        """Email user for a record"""
        try:
            if str(rec.get("pull_type")).lower() in ["url"]:
                # WHEN TYPE IS URL WE HAVE DPM_HOST
                host = rec["target_dpm_detail"]["dpm_host"]
            elif str(rec.get("pull_type")).lower() in ["file"]:
                host = rec.get("host")  # WHEN TYPE IS URL WE HAVE HOST
            self.mailer.send_html_notification(rec.get("distribution_list"), None, None, 4,
                                               {"name": "User", "host": host, "status": self.syncRequestdb.get_sync_request_by_id(str(rec["_id"]))["last_sync_status"], "last_sync_message": self.syncRequestdb.get_sync_request_by_id(str(rec["_id"]))["last_sync_message"]})
            print "Users have been notified :" + rec.get("distribution_list")
            # self.syncRequestdb.update_deployment_request_status(str(rec["_id"]), "Notification Completed", "File was pulled and request to notify users was added." )
        except Exception:
            traceback.print_exc()
            print '#################### THIS ERROR IS FROM NOTIFICATION CODE ###################'
            print "File was pushed but notification failed for :" + rec.get("distribution_list")

    # Pull zip file from target DPM machine
    # Returns error is request fails
    # Time out if response is not received
    # saves to location set for import_full_path of settings.py
    def pull(self, rec):
        """Determine pull type"""
        if rec.get("pull_type") is None:
            raise ValueError("pull_type was not found in request")
        if str(rec.get("pull_type")).lower() in ["url"]:
            self.pullByUrl(rec)
        elif str(rec.get("pull_type")).lower() in ["file"]:
            self.remoteAuthenticationService.authenticate(
                rec, self.pingMachine, rec)
            self.remoteAuthenticationService.authenticate(
                rec, self.pullByFile, rec)
        else:
            raise ValueError("pull_type given is invalid")
        self.update_sync_time(rec)

    def pingMachine(self, rec, **kwargs):
        try:
            runCommand("hostname", False, **kwargs)
        except Exception as e:
            raise ValueError('ping machine failed with error : ' + str(e))

    def decide_on_build_time(self, rec):
        if str(rec.get("incremental_pull_ind")).lower() == "true":
            if not rec.get("last_success_pull_date"):
                return str(None)
            else:
                return str(rec.get("last_success_pull_date")).split(".")[0]
        else:
            return str(None)

    # Pull zip file from target DPM machine
    # Returns error is request fails
    # Time out if response is not received
    # saves to location set for import_full_path of settings.py
    def pullByUrl(self, rec):
        """Pull by type URL"""
        # VALIDATE IF ALL FIELDS REQUIRED TO PULL A URL ARE PRESENT
        self.validatePullByUrlEntry(rec)
        # START PULLING
        self.syncRequestdb.update_deployment_request_status(
            str(rec["_id"]), "Pulling Started", "Authenticating to dpm")
        payload = {"user": rec["target_dpm_detail"].get("dpm_username"), "password": rec["target_dpm_detail"].get("dpm_password")}
        url = dpm_url_prefix + rec["target_dpm_detail"]["dpm_host"] + \
            ":" + str(rec["target_dpm_detail"]["dpm_port"]) + '/user/auth'
        headers = {'Content-Type': 'application/json'}
        print "*** authenticate to account DPM"
        print "Trying to authnticate :" + url
        try:
            response = requests.post(url, data=json.dumps(
                payload), headers=headers, timeout=int(self.result["timeout"]), verify=False)
        except Exception as e:
            if type(e) in [ConnectionError, ReadTimeout]:
                raise Exception(
                    "Unable to connect:" + rec["target_dpm_detail"]["dpm_host"] + ":" + rec["target_dpm_detail"]["dpm_port"])
            else:
                raise e
        result = json.loads(response.content)
        token = str(result["data"]["Token"])
        url = dpm_url_prefix + rec["target_dpm_detail"]["dpm_host"] + \
            ":" + str(rec["target_dpm_detail"]["dpm_port"]) + self.post_url
        filters_to_apply = {}
        if rec.get("filters_to_apply"):
            filters_to_apply = rec["filters_to_apply"]
        filters_to_apply["time_after"] = self.decide_on_build_time(rec)
        data = json.dumps({'target_host': str(self.host_name),
                           'filters_to_apply': filters_to_apply})
        req = Request(url, data)
        req.add_header('Content-Type', 'application/json')
        req.add_header('dpm_token', rec["target_dpm_detail"]["dpm_token"])
        req.add_header(
            'dpm_username', rec["target_dpm_detail"]["dpm_username"])
        req.add_header(
            'dpm_password', rec["target_dpm_detail"]["dpm_password"])
        req.add_header('Token', token)
        try:
            self.syncRequestdb.update_deployment_request_status(
                str(rec["_id"]), "Pulling Started", "Trying to Pull from " + url)
            print "Trying to Pull zip file from :" + url
            f = urlopen(req, timeout=int(self.result["timeout"]))
            _, params = cgi.parse_header(
                f.headers.get('Content-Disposition', ''))
            if f.getcode() <> 200:
                raise Exception("Response from target was:" + str(f.getcode()))
            if params.get('filename'):
                filename = params['filename']
            else:
                raise Exception("Filename was not found in header")
        except Exception as e:  # catch *all* exceptions
            raise ValueError("Failed while trying to connect to " +
                             rec["target_dpm_detail"]["dpm_host"] + " with error :" + str(e))
        # SAVE RECEIVED FILE
        with open(self.current_import_path + '/' + filename, "wb") as local_file:
            local_file.write(f.read())
        rec["file_created"] = str(self.current_import_path + '/' + filename)
        if not os.path.isfile(rec["file_created"]):
            raise ValueError(
                "File :" + rec["file_created"] + " was not created after pull")
        self.syncRequestdb.update_deployment_request_status(str(
            rec["_id"]), "Pulling Completed", "File" + str(os.path.basename(rec["file_created"])) + " was pulled successfully")
        print "Pull request was completed from " + url

    def update_sync_time(self, rec):
        self.syncRequestdb.update_sync_request(
            {"_id": {"oid": str(rec["_id"])}, "last_success_pull_date": datetime.now()})

    def fetch_locks(self, rec, **kwargs):
        file_created = []
        remote_source_location = rec.get("remote_source_location")
        result = runCommand("find {}".format(
            remote_source_location), True, None, **kwargs)
        if result and result.return_code == 0:
            result = None
            result = runCommand(
                "cd {}; ls -tar |grep .lock".format(remote_source_location), True, None, **kwargs)
            if not result or result.return_code != 0:
                raise Exception(" unable to find locks with unknown error")
            else:
                for line in result.stdout.split():
                    try:
                        self.handle_lock(rec, line, **kwargs)
                        file_created.append(
                            "Status: Success File: " + remote_source_location + "/" + line)
                        print "Status: Success File: " + remote_source_location + "/" + line
                    except Exception as exp:
                        print "Unable to process lock:" + line + " Error:" + str(exp)
                        file_created.append(
                            "Status: Failed File: " + remote_source_location + "/" + line + " Error:" + str(exp))
        else:
            raise Exception("Unable to access Path: " + remote_source_location)
        return file_created

    def handle_lock(self, rec, lock_name, **kwargs):
        remote_source_location = rec.get("remote_source_location")
        result = None
        result = runCommand("cd {}; cat ".format(
            remote_source_location) + lock_name, True, None, **kwargs)
        if not result:
            raise Exception(" unable to read lock " + lock_name +
                            " reason is unknown.Please check logs")
        if result.return_code != 0:
            raise Exception(" unable to read lock  with unknown error")
        else:
            data = result.stdout.split(",")
            try:
                if len(data) <> 2:
                    raise ValueError()
                no_of_files_required = int(data[0])
            except Exception:
                raise ValueError("The lock file: " + lock_name + " is invalid")
            self.syncRequestdb.update_deployment_request_status(str(
                rec["_id"]), "Pulling Started", "Trying to pull: " + remote_source_location + "/" + str(lock_name.split(".lock")[0]))
            if no_of_files_required > 1:
                self.handle_dir(rec, lock_name.split(".lock")[
                                0], no_of_files_required, **kwargs)
            else:
                self.handle_file(rec, lock_name.split(".lock")[
                                 0], no_of_files_required, **kwargs)
            self.syncRequestdb.update_deployment_request_status(str(
                rec["_id"]), "Pulling Started", "Pulled: " + remote_source_location + "/" + str(lock_name.split(".lock")[0]))

    def handle_file(self, rec, file_name, no_of_files_required, **kwargs):
        file_to_copy = self.get_md5sum_checksum(
            rec, file_name, False, **kwargs)
        current_import_file = self.current_import_path + \
            "/" + file_to_copy[0].split()[1]
        remote_source_file = rec.get(
            "remote_source_location") + "/" + file_to_copy[0].split()[1]
        self.copy_file_to_remote(rec, remote_source_file,
                           file_to_copy[0].split()[0], current_import_file)
        if "wip" not in current_import_file and self.verify_md5sum_in_local(file_to_copy[0].split()[0], current_import_file):
            runCommand("rm -f " + remote_source_file +
                       ".lock", False, None, **kwargs)

    def do_copy(self, rec, remote_full_path, source_md5, file_to_be_copied_full_path, **kwargs):
        try:
            result = runCommand("find {}".format(
                remote_full_path), True, None, **kwargs)
            if result and result.return_code == 0:
                if "wip" not in file_to_be_copied_full_path.lower() and not self.verify_md5sum_in_local(source_md5, file_to_be_copied_full_path, **kwargs):
                    copyFromRemote(
                        remote_full_path, file_to_be_copied_full_path + ".wip", **kwargs)
                    if os.path.exists(file_to_be_copied_full_path):
                        os.remove(file_to_be_copied_full_path)
                    os.rename(file_to_be_copied_full_path +
                              ".wip", file_to_be_copied_full_path)
            else:
                raise ValueError(
                    "File:" + remote_full_path + " does not exists")
        except Exception as exp:
            try:
                if os.path.exists(file_to_be_copied_full_path + ".wip"):
                    os.remove(file_to_be_copied_full_path + ".wip")
                if os.path.exists(file_to_be_copied_full_path):
                    os.remove(file_to_be_copied_full_path)
            except Exception:
                pass
            raise exp

    def copy_file_to_remote(self, rec, remote_full_path, source_md5, file_to_be_copied_full_path):
        self.remoteAuthenticationService.authenticate(
            rec, self.do_copy, rec, remote_full_path, source_md5, file_to_be_copied_full_path)

    def handle_dir(self, rec, dir_name, no_of_files_required, **kwargs):
        remote_source_location = rec.get(
            "remote_source_location") + "/" + dir_name
        current_import_path = self.current_import_path + "/" + dir_name
        result = runCommand("find {}".format(
            remote_source_location), True, None, **kwargs)
        if result and result.return_code == 0:
            data = self.get_md5sum_checksum(rec, dir_name, True, **kwargs)
            if len(data) == 0:
                raise ValueError(
                    "No files found in: " + remote_source_location + " with name not having .wip")
            else:
                self.mkdir_p(current_import_path)
                futures = []
                pool = ThreadPoolExecutor(int(self.count_of_files),__name__+".handle_dir")
                self.write_wip(current_import_path, no_of_files_required, str(len(data)), str(
                    len([f for f in os.listdir(current_import_path) if str(f).lower() <> "wip"])))
                for file_to_copy in data:
                    futures.append(pool.submit(self.copy_file_to_remote, rec, remote_source_location + "/" + file_to_copy.split()[
                                   1], file_to_copy.split()[0], current_import_path + "/" + file_to_copy.split()[1]))
                wait(futures)
                exceptions_list = []
                for future in futures:
                    if future.exception():
                        exceptions_list.append(str(future.exception()))
                if len(exceptions_list):
                    raise Exception(','.join(exceptions_list))
                self.write_wip(current_import_path, no_of_files_required, str(len(data)), str(
                    len([f for f in os.listdir(current_import_path) if str(f).lower() <> "wip"])))
                self.validate_if_everthing_was_copied(rec, dir_name, len(data), no_of_files_required, len(
                    [f for f in os.listdir(current_import_path) if "wip" not in str(f).lower()]), **kwargs)
        else:
            raise Exception(
                "Path:" + remote_source_location + " does not exists")

    def start_thread(self, rec, folder_to_push_to):
        futures = []
        pool = ThreadPoolExecutor(int(self.count_of_files),__name__+".start_thread")
        for f in rec.get("file_list").keys():
            if rec.get("file_list").get(f)["file_status"] in ["new", "processing"]:
                futures.append(pool.submit(self.start_push, rec, f, rec.get("file_list").get(
                    f)["file_name"], rec.get("file_list").get(f)["file_path"], folder_to_push_to))

    def write_wip(self, current_import_path, no_of_files_required, no_of_files_in_remote, no_of_files_in_local):
        with open(current_import_path + "/wip", "w") as file:
            file.write("Last locked by pull at " + str(datetime.now()) + "  required_file_count: " + str(no_of_files_required) +
                       " remote_file_count: " + str(no_of_files_in_remote) + " local_file_count: " + str(no_of_files_in_local))

    def validate_if_everthing_was_copied(self, rec, dir_name, no_of_files_in_remote, no_of_files_required, no_of_files_in_local, **kwargs):
        remote_source_location = rec.get(
            "remote_source_location") + "/" + dir_name
        current_import_path = self.current_import_path + "/" + dir_name
        if no_of_files_in_remote <> no_of_files_required or no_of_files_in_local <> no_of_files_required:
            self.write_wip(current_import_path, no_of_files_required,
                           no_of_files_in_remote, no_of_files_in_local)
        else:
            os.remove(current_import_path + "/wip")
            runCommand("rm -f " + remote_source_location +
                       ".lock", False, None, **kwargs)

    def verify_md5sum_in_local(self, md5_value_source, file_full_path, **kwargs):
        try:
            result = subprocess.check_output(
                "md5sum " + file_full_path, shell=True).split()[0]
            if str(md5_value_source).strip() == str(result).strip().replace("\\", ""):
                return True
        except Exception:
            return False

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def get_md5sum_checksum(self, rec, name, is_dir_ind=False, **kwargs):
        remote_source_location = rec.get("remote_source_location")
        if is_dir_ind:
            remote_source_location = remote_source_location + "/" + name
        result = None
        if is_dir_ind:
            result = runCommand("cd {}; ls * -1 | sort |md5sum * | grep -v .wip".format(
                remote_source_location), True, None, **kwargs)
        else:
            result = runCommand("cd {}; md5sum ".format(
                remote_source_location) + name, True, None, **kwargs)
        if not result:
            raise Exception("Path: " + remote_source_location +
                            " seems to be invalid/empty")
        if result.return_code != 0:
            raise Exception(" unable to md5sum on :" + name + "  with unknown error")
        else:
            return [x for x in result.stdout.split('\n') if x]

    # Pull zip file from target DPM machine
    # Returns error is request fails
    # saves to location set for import_full_path of settings.py
    def pullByFile(self, rec, **kwargs):
        """Pull by type FILE"""
        # VALIDATE IF ALL FIELDS REQUIRED TO PULL A FILE ARE PRESENT
        self.validatePullByFileEntry(rec)
        remote_source_location = rec.get("remote_source_location")
        # START PULLING
        print "Trying to Pull zip file from :" + remote_source_location + " of host :" + rec.get("host")
        self.syncRequestdb.update_deployment_request_status(str(
            rec["_id"]), "Pulling Started", "Trying to Pull from " + remote_source_location)
        file_created = self.fetch_locks(rec, **kwargs)
        rec["file_created"] = str(file_created)
        self.syncRequestdb.update_deployment_request_status(str(
            rec["_id"]), "Pulling Completed", "Files" + str(rec["file_created"]))
        print "Pull request was completed from " + remote_source_location

    def validatePullByFileEntry(self, rec):
        """Validate if the pull request is valid"""
        if rec.get("username") is None:
            raise ValueError("username was not found in request")
        if rec.get("ip") is None:
            raise ValueError("ip was not found in request")
        if rec.get("host") is None:
            raise ValueError("host was not found in request")
        if rec.get("password") is None:
            raise ValueError("password was not found in request")
        if rec.get("port") is None:
            raise ValueError("port was not found in request")
        if rec.get("remote_source_location") is None:
            raise ValueError("remote_source_location was not found in request")

    def validatePullByUrlEntry(self, rec):
        """Validate if the pull request is valid"""
        if rec.get("target_dpm_detail") is None:
            raise ValueError("target_dpm_detail was not found in request")
        if rec["target_dpm_detail"].get("dpm_host") is None:
            raise ValueError("dpm_host was not found in request")
        if rec["target_dpm_detail"].get("dpm_port") is None:
            raise ValueError("dpm_port was not found in request")
        if rec["target_dpm_detail"].get("dpm_token") is None:
            raise ValueError("dpm_token was not found in request")
        if rec["target_dpm_detail"].get("dpm_username") is None:
            raise ValueError("dpm_username was not found in request")
        if rec["target_dpm_detail"].get("dpm_password") is None:
            raise ValueError("dpm_password was not found in request")

    def schedule(self):
        """
        # Schedules the job
        # scheduler :Scheduler object
        # interval_given:Time interval for job to rerun"""
        global job
        self.load_configuration()
        job = self.schedulerService.schedule(job, self)
