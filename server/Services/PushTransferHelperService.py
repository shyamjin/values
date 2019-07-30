'''
Created on Mar 29, 2018

@author: PDINDA
'''

import os,shutil,subprocess,traceback
from dircache import listdir
import collections
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
from Services.fabfile import  createFolder, runCommand,copyToRemote
from Services import SyncHelperService,RemoteAuthenticationService,\
    PushHelperService
from DBUtil import Config,SyncRequest
from settings import mongodb

# collection
configdb = Config.Config(mongodb)
pushConfig = configdb.getConfigByName("PushServices")
syncRequestdb = SyncRequest.SyncRequest(mongodb)

if pushConfig.get("remote_machine_import_path") is None:
        raise Exception("remote_machine_import_path not found in config of PushServices")
remote_import_path = pushConfig["remote_machine_import_path"]
count_of_files = int(pushConfig["count_of_files"])
allow_split = str(pushConfig.get("allow_split")).lower()


remoteAuthenticationService = RemoteAuthenticationService.RemoteAuthenticationService()

def handle_input_for_push(file_created,allow_split,rec,exported_list=None,not_exported_list=None):
    is_file_ind = True
    if ((os.path.getsize(file_created)) / (1024 * 1024 * 1024.0)) > 0.5 and str(allow_split).lower() == "true":
        is_file_ind = False
        forder_path = os.path.join(os.path.dirname(
            file_created), os.path.basename(file_created).split(".")[0])
        if os.path.exists(forder_path):
            shutil.rmtree(forder_path)
        os.mkdir(forder_path)
        try:
            os.chdir(os.path.dirname(forder_path))
            print ' Push Service: split --verbose ' + os.path.basename(file_created) + ' -b 200M -d ' + os.path.normpath(forder_path) + '/' + os.path.basename(file_created)
            print subprocess.check_output('split --verbose ' + os.path.basename(file_created) + ' -b 200M -d ' + os.path.normpath(forder_path) + '/' + os.path.basename(file_created), shell=True, stderr=subprocess.STDOUT)
            
        except Exception as e_value:  # catch *all* exceptions
            traceback.print_exc()
            print 'Push Service: Error while split file :' + str(e_value)
        if len(listdir(forder_path)) > 0:
            os.remove(file_created)
        else:
            raise ValueError("Push Service :Unable to split file: " +
                             file_created + " to: " + forder_path + " to host " + rec["host"])
        file_created = forder_path  # WE ARE NOW SENDING A FOLDER
    if file_created is not None:
        rec["file_created"] = file_created
        rec["zip_file_name"] = os.path.basename(file_created)
        rec["toolNames"] = exported_list
        rec["toolNamesNotExported"] = not_exported_list
        rec = add_details_to_file(file_created, rec, is_file_ind)       
        PushHelperService.update_request_in_database(rec)
        return rec
    else:
        raise ValueError(
            "Push Service : The zip file was not created for push to :") + rec["host"]
            
def add_details_to_file(file_created, rec, is_file_ind):
    file_id = 0
    rec["file_list"] = collections.OrderedDict()
    if not is_file_ind:
        for file in listdir(file_created):
            rec["file_list"][str(file_id)] = {"file_path": str(os.path.normpath(
                os.path.join(file_created, file))), "file_name": str(file), "file_status": "new"}
            file_id = file_id + 1
    else:
        rec["file_list"][str(0)] = {"file_path": str(file_created), "file_name": str(
            os.path.basename(file_created)), "file_status": "new"}
    rec["copy_in_progress"] = "true"    
    return rec

def start_push_to_remote(rec, **kwargs):
    folder_to_push_to = PushHelperService.get_folder_to_push_to(rec)
    create_lock(rec, "WIP", **kwargs)
    if(os.path.isfile(rec["file_created"])):
        start_thread(rec, folder_to_push_to)
    else:
        folder_to_push_to = (
            folder_to_push_to + "/" + os.path.basename(rec["file_created"])).split(".")[0]
        createFolder(folder_to_push_to, **kwargs)
        file_count_to_push = 0
        file_count_of_pushed = 0
        file_remaining_to_push = 0
        if rec.get("file_list"):
            for f in rec.get("file_list").keys():
                file_count_to_push = file_count_to_push + 1
                if rec.get("file_list").get(f)["file_status"] not in ["new", "processing"]:
                    file_count_of_pushed = file_count_of_pushed + 1
                else:
                    file_remaining_to_push = file_remaining_to_push + 1
        runCommand("echo Last locked by push at $(date) file_count_to_push: " + str(file_count_to_push) + " file_count_of_pushed: " + str(
            file_count_of_pushed) + " file_remaining_to_push: " + str(file_remaining_to_push) + " >" + folder_to_push_to + "/wip", False, None, **kwargs)
        start_thread(rec, folder_to_push_to)
        runCommand("rm -f " + folder_to_push_to +
                   "/wip", False, None, **kwargs)
    create_lock(rec, "DONE", **kwargs)
    copy_rec = {}
    copy_rec["_id"] = str(rec["_id"])
    copy_rec["copy_in_progress"] = "false"
    copy_rec["last_success_push_date"] = datetime.now()
    PushHelperService.update_request_in_database(copy_rec)
    
    

def create_lock(rec, status, **kwargs):
        lock_directory = PushHelperService.get_folder_to_push_to(rec)
        createFolder(lock_directory, **kwargs)
        if rec.get("zip_file_name") and str(rec.get("zip_file_name")).strip() <> "":
            SyncHelperService.create_lock(rec, lock_directory, rec["zip_file_name"] + ".lock", str(
                len(rec["file_list"])) + "," + status.upper(), **kwargs)
        else:
            raise Exception(
                "zip_file_name not found in SyncRequest collection")
            
            
def start_thread(rec, folder_to_push_to):
        futures = []
        pool = ThreadPoolExecutor(int(count_of_files),__name__+".start_thread")
        for f in rec.get("file_list").keys():
            if rec.get("file_list").get(f)["file_status"] in ["new", "processing"]:
                futures.append(pool.submit(start_push, rec, f, rec.get("file_list").get(
                    f)["file_name"], rec.get("file_list").get(f)["file_path"], folder_to_push_to))
        wait(futures)
        Total_thread = 0
        Failed_thread = 0
        exception_value = []
        for future in futures:
            Total_thread = Total_thread + 1
            if future.exception() is not None:
                exception_value.append(str(future.exception()))
                Failed_thread = Failed_thread + 1
                raise ValueError(
                    "Push Service :Unable to Push file: to host " + rec["host"])
            else:
                exception_value.append("pass")
        i = 0
        for excep_type in exception_value:
            if excep_type is not "pass":
                print "Thread " + str(i) + ":" + excep_type
            i = i + 1
            
def start_push(rec, file_num, file_name, source_file, folder_to_push_to):
    remoteAuthenticationService.authenticate(
        rec, do_push, rec, file_num, file_name, source_file, folder_to_push_to)
    
def do_push(rec, file_num, file_name, source_file, folder_to_push_to, **kwargs):
    syncRequestdb.update_step_status(
        rec["_id"], file_name, file_num, "processing")
    copyToRemote(source_file, folder_to_push_to +
                 "/" + file_name + ".wip", **kwargs)
    runCommand("mv " + folder_to_push_to + "/" + file_name + ".wip " +
               folder_to_push_to + "/" + file_name, False, None, **kwargs)
    try:
        runCommand("chmod -R 777 " + folder_to_push_to, False, None, **kwargs)
    except Exception:  # catch *all* exceptions
        traceback.print_exc()                
        print '##### YOU CAN IGNORE THIS ERROR ####'    
    syncRequestdb.update_step_status(
        rec["_id"], file_name, file_num, "Done")
    
def check_if_lock_exists(rec, **kwargs):
    lock_directory = PushHelperService.get_folder_to_push_to(rec)
    if rec.get("zip_file_name") and str(rec.get("zip_file_name")).strip() <> "":
        return SyncHelperService.read_lock(rec, lock_directory, rec["zip_file_name"] + ".lock", **kwargs)
    
 