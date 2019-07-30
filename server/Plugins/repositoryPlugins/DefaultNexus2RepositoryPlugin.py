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
        
        # Start by validating build_details
        self.validate_build_structure(**keyargs)
        #1.0 INITIALISE VARIABLES
        artifact_already_exists = False
        upload_skipped_ind = False # if full_file_path + '/' + fileName does not exists then we skip upload of artifact as per design
        force_upload_artifacts=str(self.repository_details.get("force_upload","false")).lower() == "true"
        relative_path = keyargs["build_details"].get("additional_info").get("relative_path")  
        fileName = keyargs["build_details"].get("additional_info").get("file_name")      
        keyargs["build_details"]["file_path"] = join(self.repository_details.get("base_url"), join(relative_path, fileName)).\
                                                replace("\\", '/').replace("repository", "content/repositories") # NOT REQUIRED IN NEXUS 3
        actual_build_details = copy.deepcopy(keyargs["build_details"])
        
        file_to_upload = keyargs.get("file_to_upload",None)
        if file_to_upload:
            keyargs["file_to_upload"] = file_to_upload
            keyargs["directory_to_import_from"] = os.path.dirname(file_to_upload)
        else:
            keyargs["directory_to_import_from"] = keyargs.get("directory_to_import_from")
            keyargs["file_to_upload"] = join(keyargs["directory_to_import_from"],relative_path,fileName)
        
        if keyargs.get("file_to_upload") is None and keyargs.get("directory_to_import_from") is None:
            raise Exception("Cannot upload build as both file_to_upload and directory_to_import_from were not provided.")
        
        #1.1 CHECK IF BUILD ALREADY EXISTS        
        try:
            url=actual_build_details["file_path"]
            if (default_nexus_container_name in url):
                url=HelperServices.replace_hostname_with_actual(actual_build_details["file_path"],default_nexus_container_name,socket.gethostbyname(default_nexus_container_name))
            ret = urllib2.urlopen(url)
            if ret.code == 200:
                artifact_already_exists = True
        except Exception as e:  # catch *all* exceptions
            pass
        
        #1.2 UPLOAD ARTIFACTS
        if keyargs["directory_to_import_from"] and (not artifact_already_exists or force_upload_artifacts):
            if os.path.exists(keyargs.get("file_to_upload")):            
                keyargs["build_details"] = {
                              "repo":actual_build_details.get("additional_info").get("repo_id"),
                              "extension":actual_build_details.get("package_type"),
                              "groupId":actual_build_details.get("additional_info").get("package"),
                              "artifactId": actual_build_details.get("additional_info").get("artifact"),
                              "version":actual_build_details.get("additional_info").get("version"),
                              "package":actual_build_details.get("package_type"),
                              "classifier":str(actual_build_details.get("build_number")),
                              "file_path":actual_build_details["file_path"],    
                              "relative_path":relative_path                             
                              }
                    
                #UPLOAD OR COPY FILE
                self.serviceHandler.upload(**keyargs)
                
            else:
                upload_skipped_ind = True # Skip upload as source server did not provide this file
                print "### We did not try to upload file: "+keyargs["file_to_upload"]+" as its not present in source directory ###"
            
        
        #1.3 validate_build_structure IF UPLOAD SUCCESSFUL
        if (not artifact_already_exists or force_upload_artifacts):
            try:
                url=actual_build_details["file_path"]
                if (default_nexus_container_name in url):
                    url=HelperServices.replace_hostname_with_actual(actual_build_details["file_path"],default_nexus_container_name,socket.gethostbyname(default_nexus_container_name))
                ret = urllib2.urlopen(url)
                if ret.code == 200:
                    print actual_build_details["file_path"] + " was uploaded properly !!"
            except Exception as e:  # catch *all* exceptions
                message = "But uploaded file was not found in repository: "+ str(actual_build_details["file_path"])+" Error: "+str(e)
                if upload_skipped_ind :
                    message = "Upload mechanism was skipped."+message
                else:    
                    message = "Upload mechanism was completed."+message                                          
                raise ValueError(message)
               
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
        url=keyargs["build_details"]["file_path"]
        if (default_nexus_container_name in url):
            url=HelperServices.replace_hostname_with_actual(url,default_nexus_container_name,socket.gethostbyname(default_nexus_container_name))
        ret = urllib2.urlopen(url)
        if ret.code == 200:
            print url + " is present in repository !!"
        
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
    
    
    
    