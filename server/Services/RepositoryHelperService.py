from DBUtil import Repository
import copy
from DBUtil import DeploymentUnit,Versions,Tool
from settings import mongodb
from Services import HelperServices,CustomClassLoaderService

Repositorydb = Repository.Repository()
DeploymentUnitdb=DeploymentUnit.DeploymentUnit()
Versionsdb=Versions.Versions(mongodb)
Tooldb=Tool.Tool(mongodb)

def add_repo(repo_data):
    if check_if_repo_exists_by_name(repo_data.get("name")):
        raise Exception("Repository with name " + repo_data.get("name") + " already exists") 
    else:
        validate_repo_details(repo_data)
        return Repositorydb.add(repo_data)
        
def update_repo(repo_data):
    if Repositorydb.get_repository_by_id(repo_data.get("_id").get("oid")) is None:
        raise Exception("No such Repository exists") 
    elif repo_data.get("name") and not(Repositorydb.get_repository_by_id(repo_data.get("_id").get("oid")).get("name") == repo_data.get("name")):
        raise Exception("Name of a Repository cannot be updated")
    else:
        validate_repo_details(repo_data)
        return Repositorydb.replace(repo_data) 
    
def delete_repo(object_id):
    default_repo=["DefaultNexus2Repository","DefaultNexus3Repository"]
    repo_name=Repositorydb.get_repository_by_id(object_id).get("name")
    if Repositorydb.get_repository_by_id(object_id) is None:
        raise Exception("No such Repository exists") 
    elif  repo_name in default_repo :
        raise Exception(",".join(default_repo)+" deletion not allowed")
    HelperServices.delete_plugin_repo_validation(repo_name,"repository_to_use","Repository")
    return Repositorydb.delete(object_id)
    

def check_if_repo_exists_by_name(repo_name):
    if Repositorydb.get_repository_by_name(repo_name):
        return True
    else:
        return False
    

def validate_repo_details(repo_data):
    deployer_module="Plugins.repositoryPlugins."+repo_data.get("handler")
    class_obj=CustomClassLoaderService.get_class(deployer_module)
    method = getattr(class_obj(repo_data),"trnx_handler") # MEDHOD NAME
    keyargs={"transaction_type":"validate_repository_details"}
    method(**keyargs)
