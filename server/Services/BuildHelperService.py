'''
Created on Dec 18, 2017

@author: pdinda
'''

import os,shutil,traceback
from datetime import datetime
from DBUtil import Build,State,Repository
from settings import mongodb
from Services import HelperServices,CustomClassLoaderService
from Services import ExternalRepoDownloadHelper



buildsDB = Build.Build()
stateDB=State.State(mongodb)
repositoryDB=Repository.Repository()

def get_build_for_parent(parent_entity_id, build_id=None,state_id=None,build_number=None):
    '''
    General description:
    Args:
    param1 (object_id) : This is the ID of the existing \
       Build which we have to set active.
       parent_entity_id(object) : This is the parameter which has details of Build.
    Returns:
             Returns the count of the records set active successfully \
             for the given id of the build.
    Example :
         get_build_for_parent(parent_entity_id, build_id,state_id,build_number)
    '''
    build=None
    if state_id:
        state_details=stateDB.get_state_by_id(state_id, False)
        if not state_details:
            raise ValueError("No state was found with _id"+str(state_id))
        else:
            if not state_details.get("build_id"):
                raise ValueError("Given state_id is invalid as build_id was not found in its details")
            state_build=buildsDB.get_build_by_id(state_details.get("build_id"), True)
            if not state_build:
                raise ValueError("The build_id found in state is invalid.No such build was found: build_id"+\
                                  state_details.get("build_id"))
            if build_id and str(build_id) <> str(state_details.get("build_id")):
                raise ValueError("Build_id mismatch was found.Provided State has build_id: "\
                                 +str(state_details.get("build_id"))+" and request contains build_id :"+str(build_id))
            if build_number and str(build_number) <> str(state_build.get("build_number")):
                raise ValueError("Build_number mismatch was found.Provided State has build_number: "\
                         +str(state_build.get("build_number"))+" and request contains :"+str(build_number))
            if not state_build.get("parent_entity_id"):
                raise ValueError("Fetched build is invalid as parent_entity_id was not found in its details.build_id: "+str(state_details.get("build_id")))
            elif parent_entity_id and str(state_build.get("parent_entity_id")) <> str(parent_entity_id):
                raise ValueError("Fetched build is invalid as its parent_entity_id is different.build_id: "+str(state_details.get("build_id")))
            return state_build
            
    if build_id:
        build = buildsDB.get_build_by_id(build_id, True)
        if not build:
            raise ValueError("No Build was found with _id: "+str(build_id))
        if not build.get("parent_entity_id"):
                raise ValueError("Fetched build is invalid as parent_entity_id was not found in its details.build_id: "+str(build.get("_id")))
        elif parent_entity_id and str(build.get("parent_entity_id")) <> str(parent_entity_id):
            raise ValueError("Fetched build is invalid as its parent_entity_id is different.build_id: "+str(build.get("_id")))
        if build_number:
                if build_number and str(build_number) <> str(build.get("build_number")):
                    raise ValueError("Build_number mismatch was found.Build details has build_number: "\
                             +str(build.get("build_number"))+" and request contains :"+str(build_number))
        return build  
   
    if build_number:
        build = buildsDB.get_build_by_number(parent_entity_id, build_number, False)
        if not build:
            raise ValueError("No Build was found with build_number: "+str(build_number)+ " and parent_entity_id: "+str(parent_entity_id))
        return build     
    return buildsDB.get_last_active_build(parent_entity_id) #SEND LATEST BUILD
    

def validate_build_structure(build):
    parent_details = None
    keys_to_validate=["build_number","status","package_type"]
    keys_to_pop=["state_details","create_state_ind","operation"]
    validate_keys_exists(build, "build", keys_to_validate)
    for key in keys_to_pop:
        if build.get(key): build.pop(key) 
    if build.get("parent_entity_id"): 
        parent_details = HelperServices.get_details_of_parent_entity_id(build.get("parent_entity_id"))   
    if build.get("build_date"):
        build["build_date"] = datetime.strptime(
            (str(build["build_date"]).split(".")[0]), "%Y-%m-%d %H:%M:%S")
    validate_by_repository_to_use(build,parent_details.get("repository_to_use"))    



def validate_by_repository_to_use(build,repository_to_use,**keyargs):
    if not repository_to_use : raise Exception("Missing key: repository_to_use in parent details")
    repo_details = repositoryDB.get_repository_by_name(repository_to_use, False)
    deployer_module="Plugins.repositoryPlugins."+repo_details.get("handler")
    class_obj=CustomClassLoaderService.get_class(deployer_module)
    method = getattr(class_obj(repo_details),"trnx_handler") # MEDHOD NAME
    keyargs={"transaction_type":"validate_build_structure","build_details":build}
    method(**keyargs)            

def validate_keys_exists(obj, obj_name, keys):
    for key in keys:
        if not obj.get(key):
            raise Exception("mandatory key: " + key + " is missing in " + obj_name)

def add_update_build(build, parent_entity_id, directory_to_import_from=None):
    """Add Update a Build"""
    if build.get("to_process"):build.pop("to_process")
    if build.get("to_process_reason"):build.pop("to_process_reason")
    build["parent_entity_id"] = parent_entity_id
    validate_build_structure(build)
    parent_details = HelperServices.get_details_of_parent_entity_id(parent_entity_id)
    if not parent_details.get("repository_to_use") : raise Exception("Missing key: repository_to_use in parent details")
    repo_details = repositoryDB.get_repository_by_name(parent_details.get("repository_to_use"), False)
    deployer_module="Plugins.repositoryPlugins."+repo_details.get("handler")
    class_obj=CustomClassLoaderService.get_class(deployer_module)
    method = getattr(class_obj(repo_details),"trnx_handler") # MEDHOD NAME
    if build["status"] == "1" and directory_to_import_from:
        keyargs={"transaction_type":"upload","build_details":build,"directory_to_import_from":directory_to_import_from}
        method(**keyargs)            

        # UPLOAD ADDITIONAL ARTIFACTS
        additional_artifacts_upload=str(repo_details.get("additional_artifacts_upload","false")).lower() == "true"
        if additional_artifacts_upload and build.get("additional_artifacts"):
            ExternalRepoDownloadHelper.handle_request("upload",build.get("additional_artifacts"),\
                                                          directory_to_import_from,config=repo_details)
    
    if build["status"] == "1" :
        keyargs={"transaction_type":"validate_if_file_is_present_in_repository","build_details":build}
        method(**keyargs)
    
    BuildRecord = buildsDB.get_build_by_number(
        parent_entity_id, build["build_number"], False)
    if BuildRecord:
        build["_id"] = {}
        build["_id"]["oid"] = str(BuildRecord.get("_id"))
        Buildresult = buildsDB.update_build(build)
    else:
        Buildresult = buildsDB.add_build(build)
    if Buildresult is None:
        raise Exception("Unable to add new Build in DB")

    return str(Buildresult)


def download_build_files(build,parent_entity_id,directory_to_export_to, download_build_after,external_artifacts, **keyargs):
    """Download Build Files"""
    try:
        if not os.path.exists(directory_to_export_to):
            os.makedirs(directory_to_export_to) 
        if download_build_after and "none" not in str(download_build_after).lower():
            if build.get("build_date") and \
                    datetime.strptime(
                    (str(str(build['build_date']).split(".")[0])), "%Y-%m-%d %H:%M:%S") < datetime.strptime(
                    (str(str(download_build_after).split(".")[0])), "%Y-%m-%d %H:%M:%S"):
                return  # SKIP DOWNLOADING THIS BUILD
        
        parent_details = HelperServices.get_details_of_parent_entity_id(parent_entity_id)
        if not parent_details.get("repository_to_use") : raise Exception("Missing key: repository_to_use in parent details")
        repo_details = repositoryDB.get_repository_by_name(parent_details.get("repository_to_use"), False)
        deployer_module="Plugins.repositoryPlugins."+repo_details.get("handler")
        class_obj=CustomClassLoaderService.get_class(deployer_module)
        method = getattr(class_obj(repo_details),"trnx_handler") # MEDHOD NAME
        keyargs.update({"transaction_type":"download","build_details":build,"directory_to_export_to":directory_to_export_to})
        method(**keyargs)
        
        if  external_artifacts and build.get("additional_artifacts"):
            ExternalRepoDownloadHelper.handle_request("download",build.get("additional_artifacts"),directory_to_export_to)        
    
    except Exception:
        print "Unable to execute download_build_files : build:"+str(build)+" directory: "+directory_to_export_to
        traceback.print_exc()        