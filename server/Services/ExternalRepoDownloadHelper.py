'''
Created on Mar 27, 2018

@author: PDINDA
'''

from enum import Enum
from Services import CustomClassLoaderService
import os,shutil,sys
from DBUtil.ExitPointPlugins import ExitPointPlugins


sync_plugin_dir_mod="Plugins.syncPlugins."

class SupportedRepos(Enum):
        
    @classmethod
    def has_name(cls, name):
        return ExitPointPlugins().get_by_repo_provider(name)
        
    
    @classmethod
    def invoke_plugin_instance(cls,module_name,method_name,artifact_details,base_directory_path,**kwargs):        
        class_obj=CustomClassLoaderService.get_class(sync_plugin_dir_mod+SupportedRepos.has_name(module_name).get("plugin_name")) # CLASS NAME
        method = getattr(class_obj(SupportedRepos.has_name(module_name)),method_name) # MEDHOD NAME
        return method(artifact_details,base_directory_path,**kwargs)
        
def validate_repo(repo_provider):
    if not SupportedRepos.has_name(repo_provider):
        raise Exception("Unsupported REPO provider: " + repo_provider)


def handle_request(transaction_type,additional_artifacts, base_directory_path,**kwargs):
    validate_repo(additional_artifacts.get("repo_provider"))
    if transaction_type == "download":
        return handle_download_request(additional_artifacts, base_directory_path,**kwargs)
    elif transaction_type == "upload": 
        return handle_upload_request(additional_artifacts, base_directory_path,**kwargs)
    raise Exception ("Invalid transaction_type: "+transaction_type)
        
def handle_download_request(additional_artifacts, base_directory_path,**kwargs):
    downloaded_list=[]
    try:
        for artifact_details in additional_artifacts.get("artifacts"):
            downloaded_list.append(SupportedRepos.invoke_plugin_instance\
            (additional_artifacts.get("repo_provider"),sys._getframe().f_code.co_name,\
              artifact_details, base_directory_path,**kwargs))
    except Exception as e_value:  # catch *all* exceptions
        for path_to_remove in downloaded_list:
            if os.path.isdir(path_to_remove):
                shutil.rmtree(path_to_remove, True)
            elif os.path.isfile(path_to_remove):
                os.remove(path_to_remove)
        raise e_value
    
def handle_upload_request(additional_artifacts, base_directory_path,**kwargs):
    for artifact_details in additional_artifacts.get("artifacts"):
        SupportedRepos.invoke_plugin_instance\
        (additional_artifacts.get("repo_provider"),sys._getframe().f_code.co_name,\
          artifact_details, base_directory_path,**kwargs)
