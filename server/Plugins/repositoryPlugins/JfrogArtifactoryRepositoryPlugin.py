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
    def __init__(self,repository_details):
        '''                                                            
          General description:                                           
          This function initializes the database variables and           
          index to refer in functions.                                   
        '''
        self.repository_details = repository_details     
        
        '''
        BASE URL IS :http://vp_jfrog_artifactory:9045/artifactory
        
        
        DOCKER:
        
        #  jfrog_artifactory:
        #      image: docker.bintray.io/jfrog/artifactory-oss:6.3.3
        #      container_name: jfrog_artifactory
        #      ports:
        #       - 9045:8081
        #      volumes:
        #       - ./jfrog/artifactory:/var/opt/jfrog/artifactory
        #  #    Add extra Java options by uncommenting the following lines
        #  #    environment:
        #  #     - EXTRA_JAVA_OPTIONS=-Xmx4g
        #      restart: always
        #      ulimits:
        #        nproc: 65535
        #        nofile:
        #         soft: 32000
        #         hard: 40000

        
        STRUCTURE:
        {
        "build_details": {
                            "status": "1",
                            "build_number": 22,
                            "parent_entity_id": "5ad2dc9b254e5e007b30d4a4",
                            "repo_id": "vp_builds",
                            "relative_path": "my/new/artifact/directory",
                            "package_name": "test.pdf",
                            "package_type":"zip"
                            "file_path": "http://illin4489:9045/artifactory/vp_builds/my/new/artifact/directory/test.pdf"
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
        method = getattr(self,keyargs.get("transaction_type")) # transaction_type == MEDHOD NAME e.g upload,download
        return method(**keyargs)
    
    #Mandatory Method . Called from Sync/Clone/Import/Export Service
    def upload(self, **keyargs):
        '''
        When trying to upload a new artifact use this plugin. 
        Its a good idea to validate_build_structure the build structure before and after uploading anything
        '''
        self.validate_build_structure(**keyargs)
        
        
        if not os.path.isfile(os.path.join(keyargs.get("directory_to_import_from"),keyargs.get("build_details").get("package_name"))) \
            : raise  Exception("File :"+str(keyargs.get("build_details").get("package_name"))+" does not exists at: "+str(keyargs.get("directory_to_import_from")))
        command = "curl -u "+self.repository_details.get("repo_user")+":"+self.repository_details.get("repo_pass")+\
            " -X PUT "+self.repository_details.get("base_url")+"/"+keyargs.get("build_details").get("repo_id")+\
            "/"+keyargs.get("build_details").get("relative_path")\
            +"/"+keyargs.get("build_details").get("package_name")+" -T "+keyargs.get("build_details").get("package_name")
        print " execute_request:Execute :" + command + " at: " + os.path.normpath(keyargs.get("directory_to_import_from"))
        os.chdir(keyargs.get("directory_to_import_from"))
        print " execute_request:Changed Directory to: " + keyargs.get("directory_to_import_from")
        print subprocess.check_output(command, shell=True)
        
        return
    
    #Mandatory Method . Called from Deployment/Sync/Clone/Import/Export Service
    def download(self, **keyargs):
        '''
        Whenever we need to download a existing build.
        '''        
        self.validate_build_structure(**keyargs)
        
        build = keyargs.get("build_details")
        fname = keyargs.get("build_details").get("package_name")
        directory_to_export_to = keyargs.get("directory_to_export_to")
        if build.get("file_path"):
            print "download: Trying to download :" + build["file_path"]
            try:
                r = requests.get(build["file_path"], verify=False, stream=True)
                if r.status_code != 200:
                    raise ValueError(
                        "Unable to download file from URL: " + build["file_path"] + ".Invalid URL ??")
                else:
                    print build["file_path"] + " is a valid url !! "
                if not os.path.exists(directory_to_export_to): os.makedirs(directory_to_export_to)
                with open(os.path.join(directory_to_export_to,fname), 'wb') as f:
                    total_length = int(r.headers.get('content-length'))
                    if total_length is None: # no content length header
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                    else:
                        dl = 0
                        printed = 0
                        total_length = int(total_length)
                        for data in r.iter_content(chunk_size=4096*2):
                            dl += len(data)
                            f.write(data)
                            done = int(50 * dl / total_length)
                            if  printed <> done:
                                printed = done
                                print fname+" "+str(done*2)+"%" +" |%s%s|" % ("=" * done, ' ' * (50-done))+" "+str(dl)+"/"+str(total_length)      
                print "download:Completed downloading :" + build["file_path"]
            except Exception as e:
                raise Exception(
                    "Build URL is valid.But failed to download or save file !!!: " + build["file_path"]+" with error: "+str(e.message))
        
        
        return
    
    #Mandatory Method. Called from build add API/Deployment/Sync/Clone/Import/Export Service
    def validate_build_structure(self, **keyargs): 
     
        build_Details = keyargs.get("build_details")
        keys_to_validate = ["repo_id","relative_path","package_name","file_path"]
        for key in keys_to_validate:
            if key not in build_Details.keys() or build_Details.get(key) in ["",None]:
                raise Exception ("Mandatory key: "+key+" is not provided")
     
        return

    #Mandatory Method
    def validate_if_file_is_present_in_repository(self, **keyargs):
        '''
        Whenever we need to validate if artifact was uploaded properly
        '''        
        url=keyargs["build_details"]["file_path"]
        ret = urllib2.urlopen(url)
        if ret.code == 200:
            print url + " is present in repository !!"
        
        return 
    
    #Mandatory Method. Called from Cleaner Service
    def delete(self, **keyargs):
        '''
        Whenever we need to remove a existing build 
        '''
        command = "curl -u "+self.repository_details.get("repo_user")+":"+self.repository_details.get("repo_pass")+\
            " -X DELETE "+keyargs.get("build_details").get("file_path")
        print subprocess.check_output(command, shell=True)
        
        return
    
    #Mandatory Method. Called from Repository Service
    def validate_repository_details(self, **keyargs):
        '''
        validate all repository details are present in database
        '''
        mandatory_keys=['repo_user', 'base_url', 'repo_pass']

        missing_keys=[]
        for key in mandatory_keys:
            if key not in self.repository_details.keys():
                missing_keys.append(key)
        if len(missing_keys)>0:
            raise Exception("Missing Mandatory repository field : "+",".join(missing_keys))
        return