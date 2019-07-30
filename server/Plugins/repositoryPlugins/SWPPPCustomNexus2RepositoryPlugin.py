'''
Created on Feb 27, 2018

@author: PDINDA
'''
import urllib2,os,socket,copy
from os.path import join
from Services import Nexus2RepositoryServiceHandler,HelperServices
from settings import default_nexus_container_name

class Handler():
    '''                                                                                
    General description :                                                           
    This class has definition for functions that enable to perform deployment.                   
    '''
    def __init__(self,repository_details):
        '''                                                            
          General description:                                           
          This function initializes the database variables and           
          index to refer in functions.                                   
        '''
        self.repository_details = repository_details      
        self.serviceHandler = Nexus2RepositoryServiceHandler.\
                                                Nexus2RepositoryServiceHandler(self.repository_details)
        '''
        STRUCTURE:
        {
        "build_details": {
                        "status": "1",
                        "file_size": "4.0K",
                        "type": "url",
                        "file_path": "http://illin4490:8081/nexus/content/repositories/yum-test/com/amdocs/core/crm/crm-playbooks/10.2.4-1620/crm-playbooks-10.2.4-1620.tar",
                        "build_number": 22,
                        "package_name": "crm-playbooks-10.2.4-1620.tar",
                        "package_type": "tar",
                        "parent_entity_id": "5abbbf5ff13a94007945f01a",
                        "additional_artifacts": {
                            "artifacts": [{
                                "repo_id": "yum-test",
                                "package": "com.amdocs.core.crm",
                                "file_name": "amdocs-crm-admin_cluster_top-1-10.2.0.3.106.rpm",
                                "artifact": "amdocs-crm-admin_cluster_top-1",
                                "relative_path": "yum-test/com/amdocs/core/crm/amdocs-crm-admin_cluster_top-1/10.2.0.3.106",
                                "version": "10.2.0.3.106",
                                "type": "rpm",
                                "classifier": "1"
                            }],
                            "repo_provider": "Yum"
                        },
                        "additional_info": {
                            "repo_id": "yum-test",
                            "package": "com.amdocs.core.crm",
                            "file_name": "crm-playbooks-10.2.4-1620.tar",
                            "artifact": "crm-playbooks",
                            "relative_path": "yum-test/com/amdocs/core/crm/crm-playbooks/10.2.4-1620",
                            "version": "10.2.4-1620"
                        }
        }, 
        "transaction_type": "upload", # MANDATORY Values are method names . Add as many as you need
        "file_to_upload":"/home/vp/abc/hello.zip" # Mandatory for 'upload' 
        "directory_to_import_from":"/home/vp/abc" # Optional if  file_to_upload is provided 
        "directory_to_export_to":"/home/vp/abc"" # Optional.Can be used when downloading a artifact to a specified directory
        }
        
        '''  
    #Mandatory Method
    def trnx_handler(self, **keyargs):
        '''
        The trnx_handler is getting called from the core code.
        Depending on the transaction_type the actual methods will be called internally
        '''
        method = getattr(self,keyargs.get("transaction_type")) # transaction_type == MEDHOD NAME
        return method(**keyargs)
    
    #Mandatory Method
    def upload(self, **keyargs):
        '''
        Whenever we need to upload a existing/new build
        '''
        relative_path = keyargs["build_details"].get("additional_info").get("relative_path")  
        fileName = keyargs["build_details"].get("additional_info").get("file_name")      
        keyargs["build_details"]["file_path"] = join(self.repository_details.get("base_url"), join(relative_path, fileName)).\
                                                replace("\\", '/').replace("repository", "content/repositories") # NOT REQUIRED IN NEXUS 3
        return True
    
    #Mandatory Method
    def download(self, **keyargs):
        '''
        Whenever we need to download a existing build
        '''
        return self.serviceHandler.download(**keyargs)
    
    #Mandatory Method
    def validate_build_structure(self, **keyargs):
        '''
        Whenever we need to validate_build_structure a existing build existence/structure
        '''
        return self.serviceHandler.validate_build_structure(**keyargs)
    
    #Mandatory Method
    def validate_if_file_is_present_in_repository(self, **keyargs):
        '''
        Whenever we need to validate if artifact was uploaded properly
        '''        
        return 
    
    
    #Mandatory Method
    def delete(self, **keyargs):
        '''
        Whenever we need to remove a existing build 
        '''
        return self.serviceHandler.delete(**keyargs)
    
    #Mandatory Method. Called from Repository Service
    def validate_repository_details(self, **keyargs):
        '''
        validate all repository details are present in database
        '''
        mandatory_keys=['repo_user', 'mvn_url', 
                        'upload_type', 'create_repo_url', 
                        'force_upload', 'repo_pass', 'upload_protocol', 
                        'base_url','file_path_url', 'list_all_repositories_url', 'http_url', 'repo_path']
        missing_keys=[]
        for key in mandatory_keys:
            if key not in self.repository_details.keys():
                missing_keys.append(key)
        if len(missing_keys)>0:
            raise Exception("Missing Mandatory repository field : "+",".join(missing_keys))
        return