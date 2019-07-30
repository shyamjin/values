'''
Created on Feb 27, 2018

@author: PDINDA
'''

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
        
        
        '''
        STRUCTURE:
        {
        "build_details": {
                        "status": "1",# MANDATORY 
                        "build_number": 22,# MANDATORY 
                        "parent_entity_id": "5abbbf5ff13a94007945f01a",# MANDATORY
                        "package_type":"zip" # MANDATORY ONLY .zip supported for now
                        "additional_artifacts": {# OPTIONAL 
                            "artifacts": [],
                            "repo_provider": "Yum"
                        }
        }, 
        "transaction_type": "upload", # MANDATORY Values are method names . Add as many as you need
        }
        
        '''  
    #Mandatory Method
    def trnx_handler(self, **keyargs):
        '''
        The trnx_handler is getting called from the core code.
        Depending on the transaction_type the actual methods will be called internally
        '''
        method = getattr(self,keyargs.get("transaction_type")) # transaction_type == MEDHOD NAME e.g upload,download
        return method(**keyargs)
    
    #Mandatory Method . Called from Sync/Clone/Import/Export Service
    def upload(self, **keyargs):
        '''
        When trying to upload a new artifact use this plugin. 
        Its a good idea to validate_build_structure the build structure before and after uploading anything
        '''
        self.validate_build_structure(**keyargs)
        '''
            Do your thing !!!
        '''
        return
    
    #Mandatory Method . Called from Deployment/Sync/Clone/Import/Export Service
    def download(self, **keyargs):
        '''
        Whenever we need to download a existing build.
        '''
        return
    
    #Mandatory Method. Called from build add API/Deployment/Sync/Clone/Import/Export Service
    def validate_build_structure(self, **keyargs): 
        '''
        ***Note /build/add api is calling this method before adding a build***  
        Make sure to validate_build_structure if the build structure is proper.The mandatory keys like parent_entity_id,build_number 
        are already validated by core code.
            validate_build_structure(**keyargs)
        '''
        return

    #Mandatory Method
    def validate_if_file_is_present_in_repository(self, **keyargs):
        '''
        Whenever we need to validate_build_structure if artifact was uploaded properly
        '''
        return 
    
    #Mandatory Method. Called from Cleaner Service
    def delete(self, **keyargs):
        '''
        Whenever we need to remove a existing build 
        '''
        return
    
    #Mandatory Method. Called from Repository Service
    def validate_repository_details(self, **keyargs):
        '''
        validate all repository details are present in database
        '''
        mandatory_keys=[]
        missing_keys=[]
        for key in mandatory_keys:
            if key not in self.repository_details.keys():
                missing_keys.append(key)
        if len(missing_keys)>0:
            raise Exception("Missing Mandatory repository field : "+",".join(missing_keys))
        return