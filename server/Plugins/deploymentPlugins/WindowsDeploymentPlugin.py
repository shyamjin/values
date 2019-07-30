'''
Created on Feb 27, 2018

@author: PDINDA
'''

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
    
    def verify_prerequisites(self, **keyargs):
        return self.caller.verify_prerequisites(**keyargs)
        
    def create_directories(self, **keyargs):
        return self.caller.create_directories(**keyargs)
        
    def transfer_packages(self, **keyargs):
        local_path=self.caller.local_artifiacts_path(str(self.received_build_details.get("build_number")))
        get_extracted_directory_path= self.get_extracted_directory_path_with_build()
        with open(local_path+"/install_caller.sh","w") as file:
            for dep_field in self.caller.get_export_variables().split(";"):
                if len(dep_field.strip())>0:
                    file.write(dep_field.strip()+"; ")
            file.write("sh "+get_extracted_directory_path+"/install.sh")    
        return self.caller.transfer_packages(**keyargs)
        
    def extract_packages(self, **keyargs):
        return self.caller.extract_packages(**keyargs)
        
    def execute_packages(self, **keyargs):
        get_extracted_directory_path= self.get_extracted_directory_path_with_build()
        return self.run_command("sh "+get_extracted_directory_path+"/install_caller.sh",set_dep_fileds=False,**keyargs)
    
                 
        
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