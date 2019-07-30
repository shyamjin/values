'''
Created on Feb 15, 2018

@author: pdinda
'''
import importlib
from exceptions import ImportError

PluginMethods={
"deploymentPlugins" :[   'verify_prerequisites',
        'create_directories',
        'transfer_packages',
        'extract_packages',        
        'execute_packages',
        'clean_pakages'      
    ],

"syncPlugins" :[
        "handle_download_request",
        "handle_upload_request",
        "__init__"       
    ],

"repositoryPlugins" :[
        "trnx_handler",
        "upload",
        "download",
        "validate_build_structure",
        "validate_if_file_is_present_in_repository",
        "delete",
        'validate_repository_details'        
    ]
}
class_name="Handler"

def get_class(module_path,do_reload=False):
    try:
        module = importlib.import_module(module_path)
        my_class = getattr(module, class_name)
        if do_reload : reload(module)
        validate_plugin_methods(module_path,my_class)
        return my_class
    except Exception as e:
        if type(e) == ImportError: 
            raise Exception (str(e)+". Please check if the handler plugin file exists")
        else:
            raise e
        
def validate_plugin_methods(module_path,class_obj):
    for method_name in PluginMethods.get(str(module_path.split(".")[len(module_path.split("."))-2])):
        if method_name not in dir(class_obj):
            raise Exception("Mandatory method: "+method_name+" was not found in uploaded file")     