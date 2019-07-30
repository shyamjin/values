'''
Created on Nov 14, 2018

@author: PDINDA
'''

from requests.exceptions import ConnectionError
from DBUtil.Machine import Machine
from DBUtil.DeploymentUnit import DeploymentUnit
from DBUtil.Repository import Repository
from DBUtil.DeploymentRequestGroup import DeploymentRequestGroup
from settings import mongodb
import os,subprocess,requests,shutil,urllib2
from DBUtil.State import State


class Handler():
    '''                                                                                
    General description :                                                           
    This class has definition for functions that enable to perform deployment.                   
    '''
    def __init__(self,request,depricated_details={} ):
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
            self.repositorydb = Repository()            
                      
    #Default Declarations for methods # User needs to Override them
    def verify_group_deployment_request(self, **keyargs):
        '''
            This method is invoked while adding new deployments.
            If an exception is raised here it will be returned as API faliure response
        '''
#         deploymentRequestGroupDB = DeploymentRequestGroup(mongodb)
#         statedb = State(mongodb)
#         deployed_package_states = []
#         machine_group_id = keyargs.get("input_group_dep_request_dict")[0].get("machine_group_id")
#         package_state_id = keyargs.get("input_group_dep_request_dict")[0].get("package_state_id")
#         to_deploy_state_package = statedb.get_state_by_id(package_state_id,False).get("name")
#         
#         #get all state package ids
#         for grp in  deploymentRequestGroupDB.get_all_group_deployment_request_by_condition({"machine_group_id": machine_group_id}):   
#             if grp.get("package_state_id",None):
#                 if grp.get("package_state_id") not in deployed_package_states : deployed_package_states.append(grp.get("package_state_id"))
#         
#         # get package state names
#         for idx, item in enumerate(deployed_package_states):
#             state_package = statedb.get_state_by_id(item,False)
#             if state_package : deployed_package_states[idx] = state_package.get("name")
#             
#         deployed_package_states = [k for k in deployed_package_states if to_deploy_state_package.split("-")[0] in k]
#         print ("Latest deployed Package State: "+deployed_package_states.sort(reverse=True)[0])          
        return "All good :)"
        
    def verify_deployment_request(self, **keyargs):
        '''
            This method is invoked while adding new deployments.
            If an exception is raised here it will be returned as API faliure response
        '''
        #input_dep_request_dict=keyargs.get("input_dep_request_dict")
        #parent_entity_id = input_dep_request_dict.get("parent_entity_id")
        #if parent_entity_id:
        #    received_parent_entity_details = DeploymentUnit().GetDeploymentUnitById(parent_entity_id, False)
        #machine_id = input_dep_request_dict.get("machine_id")
        #if machine_id:
        #    received_machine_details = Machine(mongodb).GetMachine(machine_id)
        #received_deployment_fileds = input_dep_request_dict.get("tool_deployment_value")
        #try:
        #    print "No validation added"        
        #    print received_parent_entity_details
        #    print received_machine_details 
        #    print received_deployment_fileds
        #except Exception as e:
        #    if type(e) is ConnectionError: raise ValueError("Dummy ConnectionError raised for parent_entity_id: "+parent_entity_id+" and machine_id: "+machine_id)    
        return "All good :)"
        
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
        if file_length_in_kb * 5 > free_space_in_kb :
            raise Exception("Insufficient space. At least "+str(file_length_in_kb*5)+" kb of free space is required on FS")
        
    def transfer_packages(self, **keyargs):
        repo_details=self.get_repo(filter_to_fetch_from_db = {'name':'DefaultNexus2Repository'})
        if len(repo_details) == 0 : raise ValueError("Unable to find repository details of DefaultNexus2Repository")
        #-- check space available       
        self.check_if_space_available(**keyargs)
        #-- download the file
        self.run_command('cd ' + self.get_extracted_directory_path_with_build()\
        +" && curl -X GET -u "+repo_details[0].get("repo_user")+":"+repo_details[0].get("repo_pass")+" "+self.received_build_details["file_path"]+" -O",**keyargs)
        return "Artifact transferred directly to machine"
        
    def extract_packages(self, **keyargs):
        #-- check space available       
        self.check_if_space_available(**keyargs)
        return self.caller.extract_packages(**keyargs)
        
    def execute_packages(self, **keyargs):        
        ''' 
         # Development request to have additional key store values kept in Repository db
        '''
        for repository in self.get_repo():
            for key in repository.keys():
                if key not in ["additional_artifacts_upload","handler","is_default_repo_ind"]:
                    self.add_dep_field(repository["name"]+"_"+key,repository[key])
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
    
    
    # Development request to have additional key store values kept in Repository db
    '''
    Method to get all repositories. 
    Default is get all repositories starting with name "SWPPP"
        
    Usage :
        get_repo(filter_to_fetch_from_db = {}) ---> returns list of all repositories
        get_repo(filter_to_fetch_from_db = {'name':{'$regex':'^SWPPP'}}) ---> returns list of all repositories which have name starting with SWPPP
        get_repo(filter_to_fetch_from_db = {'name':'SWPPPKeyStorePluginRepository'}) ---> returns repository details of SWPPPKeyStorePluginRepository
    '''
    def get_repo(self,filter_to_fetch_from_db = {'name':{'$regex':'^SWPPP'}}):
        result = list(self.repositorydb.get_all(filter_to_fetch_from_db))
        return result
    
    # Development request to have additional key store values kept in Repository db
    '''
    Method to add additional env variables for deployment
    
    If the key contains "pass" it will be marked as sensitive            
    Usage :
        add_dep_field("dbuser","admin") -- not sensitive
        add_dep_field("dbpass","admin") -- sensitive
        add_dep_field("dbpassword","admin") -- sensitive
    '''
    def add_dep_field(self,key,value):
        dep_field = {"order_id" : 99,"input_type" : "text","input_name" : key,"input_value" : value}
        if "pass" in key.lower():dep_field["input_type"] ="password"
        self.caller.RequestDetails.get("tool_deployment_value").append(dep_field)
