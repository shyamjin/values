'''
Created on Mar 29, 2018

@author: PDINDA
'''

import copy,traceback,json,os,shutil,requests
from DBUtil import SyncRequest,SystemDetails,Config
from settings import mongodb,dpm_url_prefix
from Services import Mailer
from requests.exceptions import ConnectionError
from Services.fabfile import  runCommand

# collection
syncRequestdb = SyncRequest.SyncRequest(mongodb)
mailer = Mailer.Mailer()
systemDetailsDb = SystemDetails.SystemDetails(mongodb)
systemDetail = systemDetailsDb.get_system_details_single()
if not systemDetail:raise Exception("systemDeatils not found")
if not systemDetail.get("hostname"):raise Exception("hostname not found in systemDeatils")
remote_trigger_api_path = "/sync/push/trigger/" +systemDetail.get("hostname")
# collection
configdb = Config.Config(mongodb)
pushConfig = configdb.getConfigByName("PushServices")
syncRequestdb = SyncRequest.SyncRequest(mongodb)
if pushConfig.get("remote_machine_import_path") is None:
        raise Exception("remote_machine_import_path not found in config of PushServices")
remote_import_path = pushConfig["remote_machine_import_path"]
count_of_files = int(pushConfig["count_of_files"])
allow_split = str(pushConfig.get("allow_split")).lower()



def update_request_in_database(rec):
    rec_for_update_in_db = copy.deepcopy(rec)
    rec_for_update_in_db["_id"] = {"oid": str(rec_for_update_in_db["_id"])}
    syncRequestdb.update_sync_request(rec_for_update_in_db)
    
# Notify users about the request
def notify(rec):
    """Email user for a record"""
    if rec.get("distribution_list") is not None:
        try:
            mailer.send_html_notification(rec.get("distribution_list"), None, None, 5,
                                               {"name": "User", "host": rec["host"], "file_name": rec.get("file_created"), "toolNames": rec.get("toolNames")})
            print "Users have been notified :" + rec.get("distribution_list")
        except Exception:
            print "File was pushed but notification failed for :" + rec.get("distribution_list")


def remove_old_file(rec):
    try:
        if rec.get("file_created"):
            if(os.path.isfile(rec["file_created"])):
                os.remove(rec["file_created"])
            elif(os.path.isdir(rec["file_created"])):
                shutil.rmtree(rec["file_created"])
    except Exception as exception:
        print "Push Service :Failed to remove file." + rec.get("file_created") + " Error: " + str(exception)

def validatePushFile(rec):
    """Validate if the push request is valid"""
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

def validateTriggerRequest(rec):
    """Validate if the trigger request is valid"""
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
    
# Once Push is completed
# It trigress service in target machine to perform sync on the file pushed
def triggerRequest(rec):
    """Perform a trigger request"""
    try:
        validateTriggerRequest(rec)
        payload = {"user": "admin", "password": "12345"}
        url = dpm_url_prefix + rec["target_dpm_detail"]["dpm_host"] + \
            ":" + rec["target_dpm_detail"]["dpm_port"] + '/user/auth'
        headers = {'Content-Type': 'application/json'}
        print "*** authenticate to account DPM"
        print "Trying to authnticate :" + url
        response = requests.post(url, data=json.dumps(
            payload), headers=headers, timeout=600, verify=False)
        result = json.loads(response.content)
        token = str(result["data"]["Token"])
        trigger_url = dpm_url_prefix + rec["target_dpm_detail"]["dpm_host"] + \
            ":" + rec["target_dpm_detail"]["dpm_port"] + \
            remote_trigger_api_path
        trigger_headers = {
            'Content-Type': 'application/json',
            'dpm_token': rec["target_dpm_detail"]["dpm_token"],
            'dpm_username': rec["target_dpm_detail"]["dpm_username"],
            'dpm_password': rec["target_dpm_detail"]["dpm_password"],
            'Token': token
        }
        print "Trying to call :" + trigger_url
        response = requests.get(
            trigger_url, headers=trigger_headers, timeout=600, verify=False)
        if response.status_code != 200:
            msg = str(response.status_code) + ' ' + response.reason + '. ' + \
                str(response._content).translate(
                    None, '{"}') + '. ' + trigger_url
            syncRequestdb.update_deployment_request_status(str(rec["_id"]), "Trigger Failed", "File" + str(
                os.path.basename(rec["file_created"])) + " is pushed.But trigger failed with error: " + str(msg))
        else:
            syncRequestdb.update_deployment_request_status(str(
                rec["_id"]), "Trigger Completed", "File" + str(os.path.basename(rec["file_created"])) + " is pushed.And Triggered")
    except Exception as exception:  # catch *all* exceptions
        print ' failed to triggerRequest after pushing file with error : ' + str(exception)
        traceback.print_exc()
        if type(exception) is ConnectionError:
            exception = "Unable to connect:" + \
                rec["target_dpm_detail"]["dpm_host"] + ":" + \
                rec["target_dpm_detail"]["dpm_port"]
        syncRequestdb.update_deployment_request_status(str(rec["_id"]), "Trigger Failed", "File" + str(
            os.path.basename(rec["file_created"])) + " is pushed.But trigger failed with error :" + str(exception))


def decide_on_build_time(rec):
    if str(rec.get("incremental_push_ind")).lower() == "true":
        if not rec.get("last_success_push_date"):
            return None
        else:
            if not rec.get("last_zip_cre_dt"):
                return rec.get("last_success_push_date")
            else:
                if rec.get("last_zip_cre_dt") and rec.get("last_success_push_date") > rec.get("last_zip_cre_dt"):
                    # CONSIDER LAST 1 HOURS
                    return rec.get("last_zip_cre_dt")
                else:
                    return rec.get("last_success_push_date")
    else:
        return None
    
def clear_sync_data(rec):
    rec["toolNamesNotExported"] = ""
    rec["toolNames"] = ""
    rec["file_created"] = ""
    rec["file_list"] = {}
    rec["zip_file_name"] = ""
    
def clear_old_data(rec,**kwargs):
    # ANY OLD ZIP ?.LETS REMOVE THEM
    remove_old_file(rec)
    # MOVE ONY IF ITS NEW SYNC
    if rec.get("zip_file_name") and str(rec.get("zip_file_name")).strip() <> "":
        try:
            runCommand("rm -rf " + get_folder_to_push_to(rec) +
                       "/" + rec["zip_file_name"], True, None, **kwargs)
        except Exception as exception:
            print "Push Service :Failed to move files to ../SyncOld. Error: " + str(exception)
   
    clear_sync_data(rec)
    update_request_in_database(rec)
    
def get_folder_to_push_to(rec):
    folder_to_push_to = remote_import_path
    if rec.get("folder_location") and len(rec.get("folder_location")) > 1:
        print "Push Service :folder_location was found. Pushing to :" + rec.get("folder_location")
        folder_to_push_to = rec.get("folder_location")
    return folder_to_push_to
