'''
Created on Feb 27, 2018

@author: PDINDA
'''

import os,subprocess,requests,shutil,urllib2

class Handler():
    '''                                                                                
    General description :                                                           
    This class has definition for functions that enable to perform deployment.                   
    '''
    def __init__(self,request,depricated_details={}):
        '''                                                            
          General description:                                           
          This function initializes the database variables and           
          index to refer in functions. 
          
          request --> is getting details from 'DeploymentServices'. this 
                      is a python object that was called.This object is available when deployment is in process
                      
          input_dep_request_dict -->is getting details from  'DeploymentGroupRequestAPI'. This 
                      is a dict which was provided to deployment add api
                                            
        '''     
        # DONT TOUCH START
        if request:
            self.caller=request # USER CANNOT TOUCH THE CALLER DATA
            self.received_request_details = request.RequestDetails
            self.received_machine_details = request.MachineDetails
            self.received_system_details = request.system_details
            self.received_build_details = request.BuildDetail 
            self.received_previous_build_detail = request.previous_build_detail 
            self.received_parent_entity_details = request.parent_entity_details 
            self.received_toolsonmachine_details = request.Toolsonmachinedetails  
            self.request_type=self.received_request_details.get('request_type').lower()
            self.received_system_type = request.system_details.get("dpm_type")        
        # DONT TOUCH END              
    
    def verify_prerequisites(self, **keyargs):
        return self.caller.verify_prerequisites(**keyargs)
        
    def create_directories(self, **keyargs):
        return self.caller.create_directories(**keyargs)
        
    def check_if_space_available(self, **keyargs):            
        r = requests.get(self.received_build_details["file_path"], verify=False)
        if r.status_code != 200:
            raise ValueError(
                "Unable to validate: " + self.received_build_details["file_path"] + ".Invalid URL ??")
        file_length_in_kb = int(r.headers.get('content-length'))/1024
        result=self.run_command("cd " + self.get_extracted_directory_path_with_build()\
        +" &&  df -Pk . | tail -1 | awk '{print $4}'",**keyargs)
        free_space_in_kb = int(result.stdout.strip().split("\n")[-1])
        if file_length_in_kb * 3 > free_space_in_kb :
            raise Exception("Insufficient space. At least "+str(file_length_in_kb*5)+" kb of free space is required on FS")
        else:
            print "Sufficient space. At least "+str(file_length_in_kb*5)+" kb of free space is available on FS"    

    def transfer_packages(self, **keyargs):
        #-- check space available       
        self.check_if_space_available(**keyargs)
        return self.caller.transfer_packages(**keyargs)
        
    def extract_packages(self, **keyargs):
        #-- check space available       
        self.check_if_space_available(**keyargs)
        return self.caller.extract_packages(**keyargs)
    
    def execute_packages(self, **keyargs):
        #get_extracted_directory_path= self.get_extracted_directory_path_with_build()
        #self.run_command('cd '+get_extracted_directory_path+";./install.sh",**keyargs)
        keyargs["use_sudo"]=True # ENABLE WHEN YOU WANT TO RUN AS SUDO
        keyargs["use_pty"]=True # RUN IF YOU NEED TTY TERMINAL
        return self.caller.execute_packages(**keyargs)
        
    def clean_pakages(self, **keyargs):
        return self.caller.clean_pakages(**keyargs)           
    
    
    '''
     BELOW GIVEN ARE HELPER METHODS FOR YOU TO UTILIZE
    
    '''
    def run_command(self,command,set_dep_fileds=True,warn_only=False,timeout=None, **keyargs):
        # THE DEPLOYMENT FIELDS AND RELOAD COMMAND ARE ADDED AUTOMATICALLY if set_env_variables ==  True
        return self.caller.run_command(command,set_dep_fileds,warn_only,timeout,**keyargs)
        
    def get_export_variables(self):
        self.caller.get_export_variables()      
    
    def get_file_to_process(self,file_name = "install",build_number = None, **keyargs):  
        if not file_name : raise Exception ("Please provide file_name to execute")       
        if not build_number :build_number = str(self.received_build_details.get('build_number')).lower()
        return self.caller.get_file_to_process(file_name , build_number = None, **keyargs)    
     
    def get_extracted_directory_path(self):
        return self.caller.get_extracted_directory_path()
    
    def get_extracted_directory_path_with_build(self):
        return self.get_extracted_directory_path()+"/"+str(self.received_build_details.get("build_number"))