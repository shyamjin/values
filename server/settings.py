# from fabric.api import env
''' FABRIC START'''
# env.abort_on_prompts = True
''' FABRIC END'''

import os
import platform
import base64
from Crypto.Cipher import AES
import hashlib
from pymongo import MongoClient

platform = platform.system()

onDockerInd = str(os.environ.get("DOCKER_IND","true")).lower() == 'true'
current_path = relative_path = os.path.dirname(os.path.abspath(__file__))
# THIS INDICATOR DECIDES IF APPLICATION IS WORKING IN LITE MODE
# dpm_type can be dpm_lite,dpm_account,dpm_master,edpm,edpm_lite
dpm_type = str(os.environ["DPM_TYPE"]).lower()
if dpm_type not in ["dpm_lite", "dpm_account", "dpm_master", "edpm", "edpm_lite", "dpm_master"]:
    raise ValueError("Invalid dpm_type found")
dpm_version = str(os.environ["DPM_VERSION"]).upper()
dpm_port = str(os.environ.get("DPM_PORT","8000")).upper()
pipeline = os.environ["DPM_PIPELINE_NUMBER"]
build = os.environ["DPM_BUILD_NUMBER"]
build_date = str(os.environ["BUILD_DATE"]).upper()   
devMode = str(os.environ.get("DEV_MODE","false")).lower() == 'true'
hostname = str(os.getenv("HOSTNAME"))
test_host = str(os.environ.get("TEST_HOST",hostname)).upper()
ip = str(os.getenv("IP"))
account_name = str(os.getenv("ACCOUNT_NAME"))    
default_admin_password = str(os.getenv("DEFAULT_ADMIN_PASSWORD","12345"))
default_nexus_container_name = str(os.getenv("NEXUS_CONTAINER_NAME","vp_nexus"))



dpm_url_prefix = str(os.environ.get("REMOTE_DPM_URL_PREFIX","https://"))
selenium_test_url = dpm_url_prefix + test_host + ":" + dpm_port + "/#/login"
unittest_test_url = dpm_url_prefix + test_host + ":" + dpm_port + "/"
phantomjs_path = r'/usr/local/lib/node_modules/phantomjs-prebuilt/lib/phantom/bin/phantomjs'


# Password Key
myvars = {}
with open(os.path.join(relative_path, 'secret.p')) as myfile:
    for line in myfile:
        name, var = line.partition("=")[::2]
        myvars[name.strip()] = str(var)
if not myvars.get("key"):
    raise ValueError("Key used to encrypt/decrypt password was not found")
key = myvars["key"]


if dpm_type.lower() == "dpm_lite":
    print "######Application is running in DPM LITE mode... Welcome...#######"
elif dpm_type.lower() == "dpm_account":
    print "######Application is running in DPM Account mode... Welcome...#######"
elif dpm_type.lower() == "dpm_master":
    print "######Application is running in DPM Master mode... Welcome...######"
elif dpm_type.lower() == "edpm":
    print "######Application is running in DPM ENTERPRISE mode... Welcome...#######"
elif dpm_type.lower() == "edpm_lite":
    print "######Application is running in DPM ENTERPRISE LITE mode... Welcome...#######"
else:
    raise ValueError("Invalid DPM TYPE was found")


''' ALL PATHS START'''
base_path = str(os.getenv("DPM_BASE_PATH","/home/valuepack/"))
log_path = "/logs"
log_full_path = current_path + log_path
logo_path = "/static/files/logos"
logo_full_path = current_path + logo_path
media_path = "/static/files/media_files"
media_full_path = current_path + media_path
import_path = "/static/DPMDataUpdates/imports"
import_full_path = current_path + import_path
export_path = "/static/DPMDataUpdates/exports"
export_full_path = current_path + export_path
saved_export_path = "/static/DPMDataUpdates/SavedExports"
saved_export_full_path = current_path + saved_export_path
distribution_center_import_path = "/static/DPMDistributionCenter/imports"
distribution_center_import_full_path = current_path + \
    distribution_center_import_path
distribution_center_export_path = "/static/DPMDistributionCenter/exports"
distribution_center_export_full_path = current_path + \
    distribution_center_export_path
templates_path = "/static/files/templates"
templates_full_path = current_path + templates_path
temp_files_path = "/static/temp_files/" # need to mount as if container restart dn dir will get removed # docker-compose.yml
temp_files_full_path = current_path + temp_files_path  
plugin_full_path = current_path + "/Plugins"
plugin_static_path = "/static/Plugins"
deployment_plugin_full_path = plugin_full_path+"/deploymentPlugins"
deployment_plugin_static_path = plugin_static_path + "/deploymentPlugins"
sync_plugin_full_path = plugin_full_path+"/syncPlugins"
sync_plugin_static_path = plugin_static_path + "/syncPlugins"
repository_plugin_full_path = plugin_full_path+"/repositoryPlugins"
repository_plugin_static_path = plugin_static_path + "/repositoryPlugins"
proposed_tool_git_full_path = current_path + "/utilities/ProposedTools/git"      
proposed_tool_jenkins_full_path = current_path + "/utilities/ProposedTools/jenkins"
archives_full_path = current_path + "/archives"
plugin_directories_to_be_copied = ["syncPlugins","deploymentPlugins","repositoryPlugins"]
''' ALL PATHS END'''


''' ALL REMOTE MACHINE PATHS START'''
remote_base_path = str(os.getenv("DPM_REMOTE_BASE_PATH","/home/valuepack/"))
remote_git_path = remote_base_path+'git'
remote_jenkins_path = remote_base_path+'jenkins/jobs'
remote_mongo_path = remote_base_path+'mongo'
remote_dpm_path = remote_base_path+'dpm'
remote_documents_path = remote_base_path+'dpm/static/files/documents'
remote_logos_path = remote_base_path+'dpm/static/files/logos'
remote_media_files_path = remote_base_path+'dpm/static/files/media_files'
remote_ssl_path = remote_base_path+'dpm/ssl'
remote_sync_import_path = remote_base_path+"dpm/static/DPMDataUpdates/imports"
remote_sync_export_path = remote_base_path+"dpm/static/DPMDataUpdates/exports"
remote_distribution_import_path = remote_base_path+"dpm/static/DPMDistributionCenter/imports"
remote_distribution_export_path = remote_base_path+"dpm/static/DPMDistributionCenter/exports"
''' ALL REMOTE MACHINE PATHS END'''


template = {
    "swagger": "2.0",
    'uiversion': "3",
    "info": {
        "title": "eDPM API ",
        "description": "list of API that can used from external service",
        "contact": {
            "responsibleOrganization": "AIO",
            "responsibleDeveloper": "TBD",
            #     "email": "me@me.com",
            #     "url": "www.me.com",
        },
        "termsOfService": "TBD",
        "version": str(dpm_version)
    },
    # "host": "mysite.com",  # overrides localhost:500
    # "basePath": "/api",  # base bash for blueprint registration
    "schemes":
    [
        "http",
        "https"
    ],
    "operationId": "getmyData"
}

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

''' MONGO START OK'''
# CONNECT MONGO
client=MongoClient(str(os.environ.get("DPM_DB_HOST","mongo_sec")), int(os.environ.get("DPM_DB_PORT","64254")))
if str(os.environ.get("MONGO_SECURED","true")).lower() == 'true':
    if os.environ.get("MONGO_USER") and os.environ.get("MONGO_PASS"):
        client.admin.authenticate(
        decrypt(str(os.environ.get("MONGO_USER")).strip()),decrypt(str(os.environ.get("MONGO_PASS")).strip()))
    else:
        with open(os.path.join(relative_path, 'credentials.txt')) as myfile:
            for line in myfile:
                name, var = line.partition("=")[::2]
                myvars[name.strip()] = str(var)
            if not myvars.get("mongo_user") or not myvars.get("mongo_pass"):
                raise ValueError("Key used to encrypt/decrypt mongo was not found")
            client.admin.authenticate(
                decrypt(str(myvars["mongo_user"]).strip()),decrypt(str(myvars["mongo_pass"]).strip()))
            print "******************MONGO IS AUTHENTICATED ***************************."
else:
    print "****************** DANGER !! -- MONGO IS NOT AUTHENTICATED ***************************."    
    
mongodb = client.rabiaDB
''' MONGO END'''


