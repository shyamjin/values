'''
Created on Dec 21, 2016

@author: pdinda
'''
# from settings import onDockerInd
from docutils.nodes import field

''' DEFAULTS '''

import base64
import random
from datetime import datetime
import hashlib
import os
import re
import sys
from Crypto import Random
from Crypto.Cipher import AES
from bson.objectid import ObjectId
from pymongo import MongoClient


default_nexus_container_name = str(os.getenv("NEXUS_CONTAINER_NAME","vp_nexus"))
taskType = "-lv"
onDockerInd = str(os.environ.get("DOCKER_IND","true")).lower() == 'true'
dpm_version = str(os.environ["DPM_VERSION"]).lower()
log_to_file = False

'''
        General description:
       
       This script has definition for functions that provides a facility to upgrade the DPM version from one to another higher version.

###################################################DATA START##################################################################################

INPUT AS upgradeScript.py -lv 3.0.0 3.0.1 true/false   (TASK TYPE CURRENT VERSION TARGET VERSION, If inside Docker provide True , if outside Docker provide false)
INPUT AS upgradeScript.py -v 3.0.0 3.0.1 true/false  (TASK TYPE CURRENT VERSION TARGET VERSION , If inside Docker provide True , if outside Docker provide false)

'''
''' KEEP THIS LIST SORTED'''

versions = ['3.1.2_hf2', '3.1.2_hf3', '3.2.0','3.2.1', '3.2.1_hf1', '3.2.1_hf2', '3.2.1_hf3', '3.2.2','3.2.2_hf1','3.2.3','3.2.3_hf1','3.2.3_hf2','3.2.3_hf3','3.2.3_hf4']  # ADD NEW VERSIONS # KEEP LOWER CASE HERE

''' KEEP THIS LIST SORTED'''
types = ["dpm_lite", 'dpm_account', 'dpm_master', "edpm", "edpm_lite"]  # DONT TOUCH
dataFound = False

SUCCESS = 0
FAILED = 0
SKIPPED = 0

'''
        General description:
       
      List the newly formatted Permission Groups in ValuePack release "2.0.2" ,"2.0.2_hf2" ,"2.0.2_HF6",
      for dpm_lite , dpm_account , dpm_master , edp_lite ,edpm_account .
'''
data = {
    "3.2.0": [
        {"dpm_master": [
            {"Admin": ["AuditingView"]},
            {"Guest": ["TagsView"]}
        ]},
        {"dpm_account": [
            {"Admin": ["AuditingView"]},
            {"Guest": ["TagsView"]}
        ]},
        {"dpm_lite": [
            {"Admin": ["AuditingView"]},
            {"Guest": ["TagsView"]}
        ]},
        {"edpm": [
            {"Admin": ["AuditingView"]},
            {"Guest": ["TagsView"]}
        ]},
        {"edpm_lite": [
            {"Admin": ["AuditingView"]},
            {"Guest": ["TagsView"]}
        ]}
    ],
    "3.2.3": [
        {"dpm_master": [
            {"Admin": ["RepositoryView","RepositoryCreate","RepositoryUpdate","RepositoryDelete","SystemAdministration"]}
        ]},
        {"dpm_account": [
            {"Admin": ["RepositoryView","RepositoryCreate","RepositoryUpdate","RepositoryDelete","SystemAdministration"]}
        ]},
        {"dpm_lite": [
            {"Admin": ["RepositoryView","RepositoryCreate","RepositoryUpdate","RepositoryDelete","SystemAdministration"]}
        ]},
        {"edpm": [
            {"Admin": ["RepositoryView","RepositoryCreate","RepositoryUpdate","RepositoryDelete","SystemAdministration"]}
        ]},
        {"edpm_lite": [
            {"Admin": ["RepositoryView","RepositoryCreate","RepositoryUpdate","RepositoryDelete","SystemAdministration"]}
        ]}
    ]
}

'''
    General description:
    DATA_DEFS :   
      List the newly formatted Methods in ValuePack release "3.0.0" ,"3.0.1" ,"3.0.2","3.1.0","3.1.1"
      for dpm_lite , dpm_account , dpm_master , edp_lite ,edpm_account .
'''
data_defs = {
             "3.2.1": {"dpm_master": ["update_deployment_settings","remove_fav_from_machines"],
                       "dpm_account": ["update_deployment_settings","remove_fav_from_machines"],
                       "dpm_lite": ["update_deployment_settings","remove_fav_from_machines"],
                       "edpm": ["update_deployment_settings","remove_fav_from_machines"],
                       "edpm_lite": ["update_deployment_settings","remove_fav_from_machines"]
                       },
             "3.2.1_hf1": {"dpm_master": ["remove_fav_from_machines"],
                       "dpm_account": ["remove_fav_from_machines"],
                       "dpm_lite": ["remove_fav_from_machines"],
                       "edpm": ["remove_fav_from_machines"],
                       "edpm_lite": ["remove_fav_from_machines"],
                       },
             "3.2.2": {"dpm_master":["adding_jenkins_version_to_config"],
                       "dpm_account": ["adding_jenkins_version_to_config"],
                       "dpm_lite": ["adding_jenkins_version_to_config"],
                       "edpm": ["adding_jenkins_version_to_config"],
                       "edpm_lite": ["adding_jenkins_version_to_config"],
                       },
             "3.2.3": {"dpm_master":["adding_nexus_version_to_config","add_repository_plugin","remove_artifact_auth_from_config",\
                                     "remove_repo_type_from_builds","rm_tgt_artifact_frm_clone","allow_multi_user_session",\
                                     "add_log_to_console_to_config"],
                       "dpm_account": ["adding_nexus_version_to_config","add_repository_plugin","remove_artifact_auth_from_config",\
                                       "remove_repo_type_from_builds","rm_tgt_artifact_frm_clone","allow_multi_user_session",\
                                       "add_log_to_console_to_config"],
                       "dpm_lite": ["adding_nexus_version_to_config","add_repository_plugin","remove_artifact_auth_from_config",\
                                    "remove_repo_type_from_builds","rm_tgt_artifact_frm_clone","allow_multi_user_session",\
                                    "add_log_to_console_to_config"],
                       "edpm": ["adding_nexus_version_to_config","add_repository_plugin","remove_artifact_auth_from_config",\
                                "remove_repo_type_from_builds","rm_tgt_artifact_frm_clone","allow_multi_user_session",\
                                "add_log_to_console_to_config"],
                       "edpm_lite": ["adding_nexus_version_to_config","add_repository_plugin","remove_artifact_auth_from_config",\
                                "remove_repo_type_from_builds","rm_tgt_artifact_frm_clone","allow_multi_user_session","add_log_to_console_to_config"],
                       },
             "3.2.3_hf1": {"dpm_master":["adding_enable_callback_sync_services"],
                       "dpm_account": ["adding_enable_callback_sync_services"],
                       "dpm_lite": ["adding_enable_callback_sync_services"],
                       "edpm": ["adding_enable_callback_sync_services"],
                       "edpm_lite": ["adding_enable_callback_sync_services"],
                       }
            }


'''
################################################### STATIC DATA END##################################################################################
'''

'''
###################################################DYNAMIC DATA START##################################################################################
'''

cuttentPath = os.path.dirname(os.path.abspath(__file__))

if log_to_file:
    print "####Logs of upgradeScript.py will be written to:" + cuttentPath + "/upgradelogs.log####"
    sys.stdout = open(cuttentPath + "/upgradelogs.log", 'a', 0)
    sys.stderr = open(cuttentPath + "/upgradelogs.log", 'a', 0)

print " ############################################################## "
print " UPGRADE STARTED AT :" + str(datetime.now())


print '######################################################'
print "TaskType :" + taskType
print "onDockerInd :" + str(onDockerInd)
print "Current Path: " + cuttentPath

sys.path.insert(0, cuttentPath)
print "System Path is: " + ",".join(sys.path)

from DBUtil.InitData import InitDataHelper

#Helper Methods

def decrypt(enc):
    global key
    key1=hashlib.sha256(key.encode()).digest()
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key1, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]
    
# Password Key
myvars = {}
with open(os.path.join(cuttentPath, 'secret.p')) as myfile:
    for line in myfile:
        name, var = line.partition("=")[::2]
        myvars[name.strip()] = str(var)
if not myvars.get("key"):
    raise ValueError("Key used to encrypt/decrypt password was not found")
key = myvars["key"]    


mongo_cred_path = os.path.join(cuttentPath, 'credentials.txt')
''' MONGO START OK'''
# CONNECT MONGO
client = MongoClient(
    str(os.environ.get("DPM_DB_HOST","mongo_sec")), int(os.environ.get("DPM_DB_PORT","64254")))
myvars = {}
if str(os.environ.get("MONGO_SECURED","true")).lower() == 'true':
    if os.environ.get("MONGO_USER") and os.environ.get("MONGO_PASS"):
        client.admin.authenticate(
        decrypt(str(os.environ.get("MONGO_USER")).strip()),decrypt(str(os.environ.get("MONGO_PASS")).strip()))
    else:
        with open(mongo_cred_path) as myfile:
            for line in myfile:
                name, var = line.partition("=")[::2]
                myvars[name.strip()] = str(var)
            if not myvars.get("mongo_user") or not myvars.get("mongo_pass"):
                raise ValueError("Key used to encrypt/decrypt mongo was not found")
            client.admin.authenticate(
                decrypt(str(myvars["mongo_user"]).strip()),decrypt(str(myvars["mongo_pass"]).strip()))
            print " Looks like a authenticated mongo login...."
else:
    print " Looks like a simple mongo login...."
''' MONGO END'''

# PLEASE DONT MOVE IT FROM HERE.ITS USED BELOW ON MANUAL VALIDATION
targetVersionOfDpm = str(dpm_version).lower()
print "Target DPM Version: " + targetVersionOfDpm
if targetVersionOfDpm not in versions:
    raise Exception("Given target version is invalid")

if "DeploymentManager" in client.database_names():
    db = client.DeploymentManager
else:
    print "DeploymentManager db does not exists.Looks like a new installation.Skipping upgradeScript"
    sys.exit(0)

systemDetailsDb = db.SystemDetails.find_one({})
if not systemDetailsDb:
    raise ValueError("System details were not found")

if not systemDetailsDb.get("dpm_type"):
    raise ValueError("dpm_type details were not found in system details")
dpmType = systemDetailsDb.get("dpm_type").lower()
print "Current DPM Type from DB:" + dpmType
if dpmType not in types:
    raise Exception("Given dpm type is invalid")
if str(os.environ.get("DPM_TYPE")).lower() <> dpmType.lower():
    raise Exception("Validation error.DPM_TYPE from Env: "+str(os.environ.get("DPM_TYPE")).lower()\
        + " and from DB: "+dpmType)

if not systemDetailsDb.get("dpm_version"):
    raise ValueError("dpm_version details were not found in system details")
currentVersionOfDpm = str(systemDetailsDb.get("dpm_version")).lower()
print "Current DPM Version DB:" + currentVersionOfDpm
if currentVersionOfDpm not in versions:
    raise Exception("Given current version is invalid")

if currentVersionOfDpm == targetVersionOfDpm:
    print "Version not changed.No need to run UpgradeScript..."
    sys.exit(0)
else:
    print "Version change was found. UpgradeScript should run..."


'''
###################################################DYNAMIC DATA END#################################
'''

print '######################################################'


try:
    db_backup_name = 'Upgrade_DPM_' + str(currentVersionOfDpm).replace(".", "_") + "_" + str(datetime.now(
    )).split(" ")[0].replace("-", "").replace(":", "").replace(" ", "_") + "_" + str(random.randint(1, 20))
    if db_backup_name in client.database_names():
        raise ValueError("Cannot create db backup as it already exists: " +
                         db_backup_name + " Please remove it")
    print 'Taking Backup of your database: ' + db_backup_name
    client.admin.command('copydb',
                         fromdb='DeploymentManager',
                         todb=db_backup_name)
    print 'Backup Successful'
except Exception as e:
    print 'Backup Failed'
    raise e
print '######################################################'


class MethodsHandler():
    '''
        General description:

       This class has definition for functions that provides upgrade for ValuePack VERSIONS for all 5 flavours .
    '''
    # Init's Data

    def __init__(self, db):
        '''
           General description:
            This function initializes the database variables and \
            index to refer in functions.
        '''
        self.bs = 32
        self.db = db
        key = ' GSSPSO2016'
        self.key = hashlib.sha256(key.encode()).digest()

    def pading(self, s, bs):
        return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

    def encrypt(self, data):
        '''
        General description:
        Args:
        Param 1 : data (JSON ) : Takes argument is JSON format for \
        the data that needs to be encrypted .
        Returns:
                Changes the data in encrypted format .
        Example :
             get_all_media_files(data)
        '''
        raw = self.pading(data, self.bs)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        '''
        General description:
        Args:
        Param 1 : enc (string ) : Takes argument is string format for \
        the data that needs to be decrypted .
        Returns:
                Changes the data in decrypted format .
        Example :
             get_all_media_files(enc)
        '''
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def isAlreadyEncoded(self, data):
        '''
        General description:
        Args:
         Param 1 : data (JSON ) : Takes argument is JSON format for \
        the data that needs to be Encoded .
        Returns:
                Runs a check and confirms the data is in encoded format .
        Example :
             get_all_media_files(data)
        '''
        print "trying to check if encoded: " + data
        try:
            if not data:
                return False
            base64.b64decode(data)
            print "It is encoded: " + data
            return True
        except TypeError as e:
            print "It is Not Encoded: " + data
            return False

    def encrypt_to_decrypt(self, keys_to_check=None):
        '''
        General description:
        Args:
         Param 1 : keys_to_check (string ) : Takes argument is string format for \
         encrypting regular data like Jenkins password.
        Returns:
                Returns the data in encoded format .
        Example :
             encrypt_to_decrypt(keys_to_check)
        '''
        global SUCCESS, FAILED, SKIPPED
        if not keys_to_check:
            # PROVIDE ALL KEYS THAT ARE REQUIRED TO BE ENCRYPTED
            keys_to_check = ["jenkins_pass"]
        configDB = self.db.Config
        # key=' GSSPSO2016'
        # enc_keys = hashlib.sha256(key.encode()).digest()
        for rec in configDB.find({}):
            is_updated = False
            try:
                for key1 in rec.keys():
                    if key1 in keys_to_check and not self.isAlreadyEncoded(rec.get(key1)):
                        rec[key1] = self.encrypt(rec.get(key1))
                        is_updated = True
                if is_updated:
                    configDB.update_one({"_id": rec["_id"]},
                                        {"$set": rec}, upsert=False)
                    SUCCESS += 1
                    print 'configDB _id: ' + str(rec["_id"]) + " was updated"
            except Exception as e:  # catch *all* exceptions
                FAILED += 1
                print str('Error for configDB _id' + str(id))

    def add_dependent_tools_array(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                Returns the count of successful updated or SKIPPED for Dependent tools array .
        Example :
             add_dependent_tools_array()
        '''
        global SUCCESS, FAILED
        versionsDb = self.db.Versions
        for rec in versionsDb.find():
            id = str(rec["_id"])
            try:
                json_new_entry = {}
                for key in rec.keys():
                    if key != "_id":
                        json_new_entry[key] = rec[key]
                if not json_new_entry.get("dependent_tools"):
                    json_new_entry["dependent_tools"] = []
                versionsDb.update_one({"_id": rec["_id"]},
                                      {"$set": json_new_entry}, upsert=False)
                print "versionsDb _id:" + str(rec["_id"]) + " was updated"
                SUCCESS += 1
            except Exception as e:  # catch *all* exceptions
                FAILED += 1
                print str('Error for versionsDb _id' + str(id) + ": " + str(e))    
    
    def UpdateCounter(self, counterData):
        '''
        General description:
        Args:
         Param1 : counterData(JSON): This parameter holds values for Count_no and ID .
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             update_counter(counterData)
        '''
        counterDB = db.Counter
        result = counterDB.update_one({'_id': counterData["_id"]},
                                      {"$set": {"count_no": counterData["count_no"]}})
        return result

    def AddCounter(self, record):
        '''
        General description:
        Args:
         Param1 : record(JSON): This parameter holds values for Count_no and ID .
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             add_counter(record)
        '''
        counterDB = db.Counter
        result = counterDB.insert_one(record)
        return(result.inserted_id)

    def get_counter(self):
        '''
        General description:
        Args: None
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             get_counter(record)
        '''
        counterDB = db.Counter
        result = counterDB.find_one()
        if result is None:
            self.AddCounter({"count_no": "1"})
            return str(1)
        result["count_no"] = str(int(result["count_no"]) + 1)
        self.UpdateCounter(result)
        return str(result["count_no"])

    
    def update_deployment_settings(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             update_deployment_settings()
        '''
        global SUCCESS, FAILED, SKIPPED
        configDB = self.db.Config
        try:
            data = configDB.find_one({"name": "DeploymentRequestService"})
            if data and not data.get("enable_callback"):
                configDB.update_one({"name": "DeploymentRequestService"},
                                    {"$set": {"enable_callback": "false"}}, upsert=False)
                configDB.update_one({"name": "DeploymentRequestService"}, {"$push": {"field_types":
                    {
                        "type": "dropdown",
                        "name": "enable_callback",
                        "available_values": [
                            "true",
                            "false"
                        ]
                    }
                }},upsert=False)
            if data and not data.get("callback_timeout"):
                configDB.update_one({"name": "DeploymentRequestService"},
                                    {"$set": {"callback_timeout": 30}}, upsert=False)
                configDB.update_one({"name": "DeploymentRequestService"}, {"$push": {"field_types":
                    {
                        "type": "number",
                        "name": "callback_timeout"
                    }
                }},upsert=False)
            SUCCESS += 1
        except Exception as e:
            FAILED += 1

    def remove_fav_from_machines(self):
            '''
            General description:
            Args:
             No Arguments
            Returns:
                    Returns the count of records being updated or SKIPPED successfully.
            Example :
                 remove_fav_from_machines()
            '''
            global SUCCESS, FAILED, SKIPPED
            configDB = self.db.Machine
            try:
                configDB.update_many({}, {"$unset": {"fav":1}}, upsert=False)    
                SUCCESS += 1
            except Exception as e:
                FAILED += 1
                print str('message : FAILED to update machineDB')
                
    def adding_jenkins_version_to_config(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             adding_jenkins_version_to_config()
        '''
        global SUCCESS, FAILED, SKIPPED
        configDB = self.db.Config
        try:
            data=configDB.find_one({"configid": 7})
            if data and not data.get("jenkins_version"):
                configDB.update_one({"configid": 7}, {
                                                      "$set": {"jenkins_version":"1.651.3"}}, upsert=False)
                configDB.update_one({"configid": 7}, {"$push": {"field_types":
                                                                 {"name": "jenkins_version", "type": "dropdown","available_values": ["1.651.3","2.140","2.149"]}}}, upsert=False)
            SUCCESS += 1
        except Exception as e:
            FAILED += 1
            print str('message : FAILED to update configDB')      

    def adding_nexus_version_to_config(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             adding_nexus_version_to_config()
        '''
        global SUCCESS, FAILED, SKIPPED
        configDB = self.db.Config
        try:
            data=configDB.find_one({"configid": 7})
            if data and not data.get("target_artifact_auth_repo_type"):
                configDB.update_one({"configid": 7}, {
                                                      "$set": {"target_artifact_auth_repo_type":"nexus2:2.14.2_01"}}, upsert=False)
                configDB.update_one({"configid": 7}, {"$push": {"field_types":
                                                                 {"name": "target_artifact_auth_repo_type", "type": "dropdown","available_values": ["nexus2:2.14.2_01", "nexus3:3.12.0"]}}}, upsert=False)
            SUCCESS += 1
        except Exception as e:
            FAILED += 1
            print str('message : FAILED to update configDB')            

    def add_repository_plugin(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                None.
        Example :
             add_repository_plugin()
        '''
        global SUCCESS, FAILED, SKIPPED
        try:            
                self.db.DeploymentUnit.update_many({},
                {"$set": {"repository_to_use" : "DefaultNexus2Repository"}}, upsert=False)
                self.db.Versions.update_many({},
                {"$set": {"repository_to_use" : "DefaultNexus2Repository"}}, upsert=False)
                                        
                SUCCESS += 1
        except Exception as e:
            FAILED += 1
            print str('message : FAILED to update DeployemtnUnitDB/VersionDB')
            
    def remove_artifact_auth_from_config(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                None.
        Example :
             remove_artifact_auth_from_config()
        '''
        global SUCCESS, FAILED, SKIPPED
        configDB = self.db.Config
        try:
            data=configDB.delete_one({"name": "ArtifactAuth"})
            SUCCESS += 1
        except Exception as e:
            FAILED += 1     
              
    def remove_repo_type_from_builds(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                None.
        Example :
             remove_artifact_auth_from_config()
        '''
        global SUCCESS, FAILED, SKIPPED
        buildDb = self.db.repo_type
        try:
            data=buildDb.find()
            for rec in data :
                if rec.get("repo_type"):
                    oid=rec.get("_id")
                    rec.pop("_id")
                    rec.pop("repo_type")
                    buildDb.update_one({"_id": oid}, {"$set": rec}, upsert=False)
            SUCCESS += 1
        except Exception as e:
            FAILED += 1
            print str('message : FAILED to update Build Collection')    

    def rm_tgt_artifact_frm_clone(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             rm_tgt_artifact_frm_clone()
        '''

        global SUCCESS, FAILED, SKIPPED
        configDB = self.db.Config
        try:
            data=configDB.find_one({"configid": 7})
            if data:
                if data.get("target_artifact_auth_url"):
                    configDB.update_one({"configid": 7}, {
                                                      "$unset": {"target_artifact_auth_url":1}}, upsert=False)  
                    configDB.update_one({"configid": 7}, {"$pull": {"field_types":
                                                             {"name": "target_artifact_auth_url", "type": "textbox"}}}, upsert=False)            
                if data.get("target_artifact_auth_user"):
                    configDB.update_one({"configid": 7}, {
                                                      "$unset": {"target_artifact_auth_user":1}}, upsert=False)  
                    configDB.update_one({"configid": 7}, {"$pull": {"field_types":
                                                             {"name": "target_artifact_auth_user", "type": "textbox"}}}, upsert=False)  
                if data.get("target_artifact_auth_password"):
                    configDB.update_one({"configid": 7}, {
                                                      "$unset": {"target_artifact_auth_password":1}}, upsert=False)  
                    configDB.update_one({"configid": 7}, {"$pull": {"field_types":
                                                             {"name": "target_artifact_auth_password", "type": "password"}}}, upsert=False)                                
            SUCCESS += 1
        except Exception as e:
            FAILED += 1
            print str('message : FAILED to update configDB')
            
            
    def allow_multi_user_session(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             allow_multi_user_session()
        '''
        global SUCCESS, FAILED, SKIPPED
        configDB = self.db.Config
        try:
            data=configDB.find_one({"configid": 6})
            if data and not data.get("allow_multi_user_session"):
                configDB.update_one({"configid": 6}, {
                                                      "$set": {"allow_multi_user_session":"false"}}, upsert=False)
                configDB.update_one({"configid": 6}, {"$push": {"field_types":
                                                                 {"name": "allow_multi_user_session", \
                                                                  "type": "dropdown","available_values": ["true","false"]}}}, upsert=False)
            SUCCESS += 1
        except Exception as e:
            FAILED += 1
            print str('message : FAILED to update configDB')            


    def add_log_to_console_to_config(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             add_log_to_console_to_config()
        '''
        global SUCCESS, FAILED, SKIPPED
        configDB = self.db.Config
        try:
            data=configDB.find_one({"configid": 5})
            if data and not data.get("log_to_console"):
                configDB.update_one({"configid": 5}, {
                                    "$set": {"log_to_console":"true"}}, upsert=False)
                configDB.update_one({"configid": 5}, {"$push": {"field_types":
                                    {"name": "log_to_console", "type": "dropdown","available_values": ["true", "false"]}}}, upsert=False)
            if data and not data.get("backupCount"):
                configDB.update_one({"configid": 5}, {
                                    "$set": {"backupCount":0}}, upsert=False)
                configDB.update_one({"configid": 5}, {"$push": {"field_types":
                                    {"name": "backupCount", "type": "number"}}}, upsert=False)
            SUCCESS += 1
        except Exception as e:
            FAILED += 1
            print str('message : FAILED to update configDB')           
              
    
    def adding_enable_callback_sync_services(self):
        '''
        General description:
        Args:
         No Arguments
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             adding_skip_deployment_request_ind()
        '''
        global SUCCESS, FAILED, SKIPPED
        configDB = self.db.Config
        try:
            data=configDB.find_one({"configid": 9})
            if data and not data.get("enable_callback"):
                configDB.update_one({"configid": 9}, {
                                                      "$set": {"enable_callback":"false"}}, upsert=False)
                configDB.update_one({"configid": 9}, {"$push": {"field_types":
                                                                 {"name": "enable_callback", "type": "dropdown","available_values": ["true", "false"]}}}, upsert=False)
                configDB.update_one({"configid": 9}, {"$set": {"callback_timeout": 30}}, upsert=False)
                configDB.update_one({"configid": 9}, {"$push": {"field_types":{"name": "callback_timeout", "type": "number"}}}, upsert=False)
            SUCCESS += 1
        except Exception as e:
            FAILED += 1
            print str('message : FAILED to update configDB')      
            
print '######## ############################# METHODS HANDLER END ##################################'


def roles_data_populate(data):
    '''
        General description:
        Args:
        Param1 : data(JSON) : This parameter has data respective to Roles collection .
        Returns:
                Returns the count of records being updated or SKIPPED successfully.
        Example :
             roles_data_populate(data)
    '''
    global SUCCESS, FAILED, SKIPPED
    roleDb = db.Role
    permissionGroupCollectionDb = db.PermissionGroup
    for rec in data:
        for key in rec.keys():
            roleData = roleDb.find_one(
                {"name": re.compile(key, re.IGNORECASE)})
            if roleData:
                for permissionGroup in rec[key]:
                    permissionGroupData = permissionGroupCollectionDb.find_one(
                        {"groupname": re.compile(permissionGroup, re.IGNORECASE)})
                    if permissionGroupData:
                        permissionGroupEcistsinRole = roleDb.find_one(
                            {"name": key, "permissiongroup": str(permissionGroupData["_id"])})
                        if not permissionGroupEcistsinRole:
                            roleDb.update_one({"_id": roleData["_id"]},
                                              {"$push": {"permissiongroup": str(permissionGroupData["_id"])}})
                            print "For Role:" + roleData["name"] + " PermissionGroup:" + permissionGroup + " was added"
                            SUCCESS += 1
                        else:
                            print "For Role:" + roleData["name"] + " PermissionGroup:" + permissionGroup + " already Exists"
                            SKIPPED += 1
                    else:
                        print "PermissionGroup:" + permissionGroup + " was not found in DB.Failed record.."
                        FAILED += 1
    return True


# DECIDE WHICH FILE TO RUN
if dpmType.lower() in ["dpm_lite","edpm_lite"]:
    from DBUtil.InitData import InitDataLite
    dynamicInstanceOfInitData = InitDataLite
elif dpmType.lower() in ["dpm_account","edpm"]:
    from DBUtil.InitData import InitDataAccount
    dynamicInstanceOfInitData = InitDataAccount
elif dpmType.lower() == "dpm_master":
    from DBUtil.InitData import InitData
    dynamicInstanceOfInitData = InitData
else:
    raise ValueError("Invalid DPM type found")


# START UPGRADE

upgradeToVersionList = []
if taskType.lower() in ["-lv"]:
    tarLoc = versions.index(targetVersionOfDpm.lower())
    # print tarLoc
    curLoc = versions.index(currentVersionOfDpm.lower())
    # print curLoc
    if (tarLoc) <= float(curLoc):
        raise Exception(
            "Given current version is greater/equal to target version")
    for rec in range(len(versions)):
        if int(rec) > curLoc and int(rec) <= tarLoc:
            upgradeToVersionList.append(versions[rec])
elif taskType.lower() in ["-v"]:
    upgradeToVersionList.append(targetVersionOfDpm.lower())
else:
    raise Exception("Invalid Task Type")

print "Versions to upgrade to: " + ",".join(upgradeToVersionList)
print '######################################################'

initDataExuecuted = False

for version in upgradeToVersionList:
    print ''
    print "Working on version:" + version

    print ""
    print "Calling method Updates"
    print "#####################"
    # CALL METHODS
    if data_defs.get(version.lower()):
        print "We have Methods to run for this"
        if data_defs.get(version.lower()).get(dpmType.lower()):
            for method_name in data_defs.get(version.lower()).get(dpmType.lower()):
                print "Calling Method:" + method_name
                methodsHandler = MethodsHandler(db)
                method = getattr(methodsHandler, method_name)
                try:
                    apply(method)
                except Exception as e:  # catch *all* exceptions
                    print str(e)
                print "Done Calling Method:" + method_name

    # CALL INIT DATA
    if not initDataExuecuted:
        print ""
        print "Calling InitDataHelper"
        print "#####################"
        InitDataHelper.InitDataHelper(db)
        initDataExuecuted = True
    else:
        print ""
        print "InitDataHelper was already called before.Skipping..."
        print "#####################"

    # MAP ROLES
    print ""
    print "Calling Roles_DataPopulate"
    print "#####################"
    if data.get(version):
        print "We have Roles Updates for this"
        for rec in data.get(version.lower()):
            if rec.get(dpmType.lower()):
                status = roles_data_populate(rec.get(dpmType.lower()))



print ''
print '###### REPORT ######'
print "Total Success Count: " + str(SUCCESS)
print "Total Skipped Count: " + str(SKIPPED)
print "Total Failed Count: " + str(FAILED)
print ''

print 'Am Done!!!!'
print " ############################################################## "
print " UPGRADE ENDED AT :" + str(datetime.now())




#########################METHODS#############################################