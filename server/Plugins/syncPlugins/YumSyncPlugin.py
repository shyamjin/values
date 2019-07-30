'''
Created on Mar 27, 2018

@author: PDINDA
'''
import subprocess,os

class Handler():
    '''                                                                                
    General description :                                                           
    This class has definition for functions that enable to perform rpm downloads.                   
    '''
    def __init__(self,repo_details):
        '''                                                            
          General description:                                           
          This function initializes the database variables and           
          index to refer in functions.                                   
        '''
        self.repo_user = repo_details.get("repo_user")
        self.repo_password = repo_details.get("repo_password")
        self.repo_url = repo_details.get("repo_url")
    
    '''
    DATA FORMAT:
    "additional_artifacts" : {
                    "artifacts" : [ 
                        {
                            "repo_id" : "yum-test-remote",
                            "package" : "com.amdocs.core.crm",
                            "file_name" : "amdocs-crm-admin_cluster_top-1-10.2.0.3.106.rpm",
                            "artifact" : "amdocs-crm-admin_cluster_top-1",
                            "relative_path" : "yum-test-remote/com/amdocs/core/crm/amdocs-crm-admin_cluster_top-1/10.2.0.3.106",
                            "version" : "10.2.0.3.106",
                            "type" : "rpm"
                        }
                    ],
                    "repo_provider" : "Yum"
                }
    '''
    
    
    #IMPLEMENTED METHOD
    def handle_download_request(self, artifact_details,base_directory_path,**kwargs):
        file_name=self.get_file_name(artifact_details, base_directory_path)
        get_file_full_path=self.get_file_full_path(artifact_details, base_directory_path)
        command ="sudo /usr/bin/yumdownloader "+file_name.split(".rpm")[0]        
        self.execute_request(command, get_file_full_path)
        return   get_file_full_path
                    
    #IMPLEMENTED METHOD    
    def handle_upload_request(self, artifact_details,base_directory_path,**kwargs): 
        if kwargs.get("config"):
            self.repo_password=kwargs.get("config").get("artifact_repo_pass")
            self.repo_user=kwargs.get("config").get("artifact_repo_user")
            self.repo_url=kwargs.get("config").get("url").replace("repository","service/local/artifact/maven/content")
        
        file_name=self.get_file_name(artifact_details, base_directory_path)
        full_file_path=self.get_file_full_path(artifact_details, base_directory_path)
        command ="curl -v -F r=" + artifact_details.get("repo_id") +\
         " -F hasPom=false -F e=" + artifact_details.get("type") + \
         " -F g=" + artifact_details.get("package") + " -F a=" +\
        artifact_details.get("artifact") + " -F v=" + artifact_details.get("version") +\
        " -F p=" + artifact_details.get("type") +" -F c=" + artifact_details.get("classifier","")+\
        "  -F file=@" + file_name + " -u " + self.repo_user  +\
        ":" + self.repo_password + " " + self.repo_url        
        self.execute_request(command, full_file_path)  
        return   full_file_path
    
    #HELPER
    def get_file_name(self,artifact_details,base_directory_path,**kwargs):
        return artifact_details.get("file_name")
    
    #HELPER
    def get_file_full_path(self,artifact_details,base_directory_path,**kwargs):
        relative_path = artifact_details.get("relative_path")
        full_file_path = os.path.join(base_directory_path, relative_path)
        if not os.path.exists(full_file_path):os.makedirs(full_file_path)
        return os.path.normpath(os.path.join(full_file_path,\
                                             self.get_file_name(artifact_details, base_directory_path)))
    #HELPER
    def get_file_dir_path(self,artifact_details,base_directory_path,**kwargs):
        relative_path = artifact_details.get("relative_path")
        full_file_path = os.path.join(base_directory_path, relative_path)
        if not os.path.exists(full_file_path):os.makedirs(full_file_path)
        return full_file_path      
    
    #HELPER
    def execute_request(self,command,file_to_upload):
        dir_to_switch_to=os.path.dirname(file_to_upload)
        print " execute_request:Execute :" + command + " at: " + os.path.normpath(dir_to_switch_to)
        os.chdir(dir_to_switch_to)
        print " execute_request:Changed Directory to: " + dir_to_switch_to
        print subprocess.check_output(command, shell=True)