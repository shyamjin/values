'''
Created on Mar 27, 2018

@author: PDINDA
'''
import subprocess,os

class Handler():
    '''                                                                                
    General description :                                                           
    This class has definition for functions that enable to perform docker downloads.                   
    '''
    def __init__(self,repo_details):
        '''                                                            
          General description:                                           
          This function initializes the database variables and           
          index to refer in functions.                                   
        '''
        self.repo_user = ""
        self.repo_password = ""
        self.repo_url = ""
    
    '''
    DATA FORMAT:
    "additional_artifacts" : {
                    "artifacts" : [ 
                        {
                            "file_name" : "illin4489.corp.amdocs.com:10005/slamdata"                            
                        }
                    ],
                    "repo_provider" : "Docker"
                }
    '''
    
    ############### USER IMPLEMENTED METHODS START ####################
    
    #USER IMPLEMENTED METHOD
    #docker save illin4489.corp.amdocs.com:10005/edpm_lite:2.0.5_HF2 > edpm_lite_2_0_5_HF2.tar.gz
    def handle_download_request(self, artifact_details,base_directory_path,**kwargs):
        file_name=self.get_file_name(artifact_details, base_directory_path)
        get_file_full_path=self.get_file_full_path(artifact_details, base_directory_path)
        command ="sudo /usr/bin/docker save "+file_name+" > "+file_name+".tar.gz"      
        self.execute_request(command, get_file_full_path)
        return get_file_full_path
        
                    
    #USER IMPLEMENTED METHOD
    def handle_upload_request(self, artifact_details,base_directory_path,**kwargs):       
        file_name=self.get_file_name(artifact_details, base_directory_path)
        get_file_full_path=self.get_file_full_path(artifact_details, base_directory_path)
        command ="sudo /usr/bin/docker load  < "+file_name+".tar.gz"      
        self.execute_request(command, get_file_full_path)
        return get_file_full_path
    
    
    
    ############### HELPER METHODS START ####################   
    
    #HELPER METHOD
    def get_file_name(self,artifact_details,base_directory_path,**kwargs):
        return artifact_details.get("file_name")
    
    #HELPER METHOD
    def get_file_full_path(self,artifact_details,base_directory_path,**kwargs):
        relative_path = artifact_details.get("relative_path")
        full_file_path = os.path.join(base_directory_path, relative_path)
        if not os.path.exists(full_file_path):os.makedirs(full_file_path)
        return os.path.normpath(os.path.join(full_file_path,\
                                             self.get_file_name(artifact_details, base_directory_path)))
    #HELPER METHOD
    def get_file_dir_path(self,artifact_details,base_directory_path,**kwargs):
        relative_path = artifact_details.get("relative_path")
        full_file_path = os.path.join(base_directory_path, relative_path)
        if not os.path.exists(full_file_path):os.makedirs(full_file_path)
        return full_file_path      
    
    #HELPER METHOD
    def execute_request(self,command,file_to_upload):
        dir_to_switch_to=os.path.dirname(file_to_upload)
        print " execute_request:Execute :" + command + " at: " + os.path.normpath(dir_to_switch_to)
        os.chdir(dir_to_switch_to)
        print " execute_request:Changed Directory to: " + dir_to_switch_to
        print subprocess.check_output(command, shell=True)