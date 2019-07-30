import traceback,os
from DBUtil import ExitPointPlugins
from settings import  sync_plugin_full_path,deployment_plugin_full_path
from Services import HelperServices

exitPointPlugins=ExitPointPlugins.ExitPointPlugins()


def delete_plugin(file_name , validation_indicator=True):
    """Start Plugin Deletion"""
    try:
        if validation_indicator == True :
            HelperServices.delete_plugin_repo_validation(str(file_name),"deployer_to_use","Repository")
            
        file_path = str(deployment_plugin_full_path + '/' + file_name+".py")
        if os.path.isfile(file_path): os.remove(file_path)
        file_path = str(sync_plugin_full_path + '/' + file_name+".py")
        if os.path.isfile(file_path): os.remove(file_path)
        present_in_db=exitPointPlugins.get_by_plugin_name(file_name)
        if present_in_db: exitPointPlugins.delete(str(present_in_db.get("_id")))  
        return {"result": "success", "message": "File was removed"}, 200
    except Exception as e:
        traceback.print_exc()
        raise Exception (e)
    