import traceback,os,shutil
from bson.json_util import dumps
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from werkzeug import secure_filename
from DBUtil import Plugins,ExitPointPlugins
from Services.AppInitServices import authService
from Services.SingeltonServicesManager import plugin_manager
from settings import mongodb, relative_path,deployment_plugin_full_path,\
    sync_plugin_full_path, plugin_static_path, deployment_plugin_static_path,\
    sync_plugin_static_path,repository_plugin_full_path,repository_plugin_static_path
from Services import CustomClassLoaderService,DeploymentServices,PluginHelperService,\
    Utils
from genericpath import isfile
from modules.apimodels import PluginModel, ExitPointPluginsModel
from flask_restplus import Resource
from modules.apimodels.Restplus import api, header_parser
from modules.apimodels import GenericReponseModel
from datetime import datetime
import json


# blueprint declaration
PluginAPI = Blueprint('PluginAPI', __name__)
PluginAPINs = api.namespace('plugin', description='Plugin Operations')

# get global db connection
db = mongodb

# collections
PluginsDB = Plugins.Plugins(db)
exitPointPluginsDB=ExitPointPlugins.ExitPointPlugins()
# classes
plugins_manager = plugin_manager  # PluginsManagerService()


@PluginAPI.route('/plugin/reload', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/PluginAPI/reload_plugin.yml')
def reload_plugin():
    plugins_manager.load_plugin()
    return jsonify(json.loads(dumps(
        {"result": "success", "message": "plugin reloaded successfully", "data": PluginsDB.get_all_plugin()}))), 200


@PluginAPI.route('/plugin/install/<string:name>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/PluginAPI/install_plugin.yml')
def install_plugin(name):
    result = plugins_manager.install_plugin(name)
    return jsonify(json.loads(dumps(
        {"result": "success", "message": result, "data": ""}))), 200
    
    
@PluginAPI.route('/plugin/uninstall/<string:name>', methods=['GET'])
@authService.authorized
@swag_from(relative_path + '/swgger/PluginAPI/uninstall_plugin.yml')
def uninstall_plugin(name):
    result = plugins_manager.uninstall_plugin(name)
    return jsonify(json.loads(dumps(
        {"result": "success", "message": result, "data": ""}))), 200

@PluginAPINs.route('/inactive/<string:name>', methods=['GET'])
class deactivate_plugin(Resource):
    @api.param('name', 'plugin name')
    @api.expect(header_parser, validate=True)
    @api.marshal_with(PluginModel.activate_deactivate_plugin_response_model)
    @authService.authorized
    def get(self,name):
        plugins_manager.deactivate(name)
        return {"result": "success", "message": "plugin deactivated successfully", "data": ""}, 200


@PluginAPINs.route('/active/<string:name>', methods=['GET'])
class activate_plugin(Resource):
    @api.param('name', 'plugin name')
    @api.expect(header_parser, validate=True)
    @api.marshal_with(PluginModel.activate_deactivate_plugin_response_model)
    @authService.authorized
    def get(self,name):
        plugins_manager.activate(name)
        return {"result": "success", "message": "plugin activated successfully", "data": ""}, 200

@PluginAPINs.route('/all', methods=['GET'])
class get_all_plugins(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(PluginModel.get_all_plugin_response_model)
    @authService.authorized
    def get(self):
        data = []
        for rec in PluginsDB.get_all_plugin():
            data.append(rec)
        return {"result": "success", "message": "plugin list", "data":  data}, 200

@PluginAPINs.route('/view/<id>', methods=['GET'])
@api.doc(params={'id': 'plugin id'})
class get_plugin_by_id(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(PluginModel.get__plugin_by_id_response_model)
    @authService.authorized
    def get(self,id):
        return {"result": "success", "message": " plugin found", "data":  PluginsDB.get_plugin_by_id(id)}, 200

@PluginAPINs.route('/file/upload', methods=['POST'])
class add_new_plugin(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(GenericReponseModel.generic_response_model)
    @authService.authorized
    def post(self):
        """
        Add a new plugin
        """
        file_path = None
        file_path_temp = None 
        try:
            plugin_types=["DeploymentPlugin","SyncPlugin","RepositoryPlugin"]
            uploaded_file = request.files['file']
            upload_type = request.form.get('type')
            if upload_type is None:
                raise Exception("upload_type not specified")
            filename = ('.' in uploaded_file.filename and
                        uploaded_file.filename.rsplit('.', 1)[1] in ['py'])
            if filename not in [True]:
                raise Exception("Invalid file .Please select file of type 'py'")
            for type in plugin_types:
                if type in uploaded_file.filename:
                    break
            else:
                raise Exception("Invalid file name.File should have name including"\
                 " any of the following: "+", ".join(plugin_types))
            # Check if the file is one of the allowed types/extensions
            if uploaded_file and filename:
                filename = secure_filename(uploaded_file.filename)  
                filename_without_py=filename.replace(".py","")              
                if "DeploymentPlugin" in filename:
                    file_path_temp = str(deployment_plugin_full_path + '/' + filename_without_py+"_temp"+".py")
                    file_path = str(deployment_plugin_full_path + '/' + filename)
                    deployer_module="Plugins.deploymentPlugins."+filename_without_py+"_temp"
                if  "SyncPlugin" in filename:
                    file_path_temp = str(sync_plugin_full_path + '/' + filename_without_py+"_temp"+".py")
                    file_path = str(sync_plugin_full_path + '/' + filename)
                    deployer_module="Plugins.syncPlugins."+filename_without_py+"_temp"
                if  "RepositoryPlugin" in filename:
                    file_path_temp = str(repository_plugin_full_path + '/' + filename_without_py+"_temp"+".py")
                    file_path = str(repository_plugin_full_path + '/' + filename)
                    deployer_module="Plugins.repositoryPlugins."+filename_without_py+"_temp"
                if os.path.exists(file_path) and upload_type.lower() == "new":
                    if exitPointPluginsDB.get_by_plugin_name(filename_without_py):
                        raise Exception ("File with same name already exists: "+filename_without_py)   
                uploaded_file.save(file_path_temp)
                if not os.path.isfile(file_path_temp): raise Exception("unable to save this file")
                #reload the modules in cache
                CustomClassLoaderService.get_class(deployer_module, True)
                shutil.move(file_path_temp, file_path) 
                CustomClassLoaderService.get_class(deployer_module.replace("_temp",""), True)
                # remove pyc's
                if os.path.isfile(file_path_temp+"c"): os.remove(file_path_temp+"c")
                if os.path.isfile(file_path+"c"): os.remove(file_path+"c")   
            return {"result": "success", "message": "File was uploaded"}, 200        
        except Exception as e:  # catch *all* exceptions
            traceback.print_exc()
            if "'module' object has no attribute 'Handler'" in str(e):
                raise Exception ("Invalid File Detected : Expected class 'Handler' was not found")
            raise e
        finally:
            if file_path_temp and os.path.isfile(file_path_temp):
                os.remove(file_path_temp)
                file_path_temp_pyc=file_path_temp+"c"
                if file_path_temp_pyc and os.path.isfile(file_path_temp_pyc):
                    os.remove(file_path_temp_pyc)
                
            
        

@PluginAPINs.route('/file/remove/<file_name>', methods=['DELETE'])
@api.doc(params={'file_name':'Plugin Name'})
class remove_plugin(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(GenericReponseModel.generic_response_model)
    @authService.authorized
    def delete(self,file_name):
        """
        delete plugin
        """
        return PluginHelperService.delete_plugin(file_name, True)
        
            
@PluginAPINs.route('/file/list/<plugin_type>', methods=['GET'])
@api.doc(params={'plugin_type':'Plugin Type'})
class list_plugins(Resource):
    @api.expect(header_parser, validate=True)
    @api.marshal_with(ExitPointPluginsModel.ep_all_response)
    @authService.authorized
    def get(self,plugin_type="all"):
        """
        List  ExitPoint plugins
        """
        show_dep_plugins = str(plugin_type).lower() in ["deployment","all"]
        show_sync_plugins = str(plugin_type).lower() in ["sync","all"]
        show_repo_plugins = str(plugin_type).lower() in ["repository","all"]
        files_list= []
        final_list=[]
        if show_dep_plugins :
            files_list.extend([f for f in (os.listdir(deployment_plugin_full_path)) \
                if (str(str(f).lower()).endswith(".py") and "__init__" not in str(str(f).lower())) ])
        if show_sync_plugins:
            files_list.extend([f for f in (os.listdir(sync_plugin_full_path)) \
                if (str(str(f).lower()).endswith(".py") and "__init__" not in str(str(f).lower())) ])
        if show_repo_plugins:
            files_list.extend([f for f in (os.listdir(repository_plugin_full_path)) \
                if (str(str(f).lower()).endswith(".py") and "__init__" not in str(str(f).lower())) ])     
        for file_name in  files_list:
            data = exitPointPluginsDB.get_by_plugin_name(file_name.split(".")[0])
            if data:
                if "DeploymentPlugin" in data.get("plugin_name"):
                    data["file_path"]=os.path.normpath(os.path.join(deployment_plugin_static_path,data.get("plugin_name"))+".py")
                elif "SyncPlugin" in data.get("plugin_name"):    
                    data["file_path"]=os.path.normpath(os.path.join(sync_plugin_static_path,data.get("plugin_name"))+".py")
                elif "RepositoryPlugin" in data.get("plugin_name"):    
                    data["file_path"]=os.path.normpath(os.path.join(repository_plugin_static_path,data.get("plugin_name"))+".py")
                final_list.append({"_id":data["_id"],"plugin_name":data["plugin_name"],"file_path":data["file_path"]})
        return {"result": "success", "message": "","data":final_list},200 
    
@PluginAPINs.route('/file/view/<_id>', methods=['GET'])
@api.doc(params={'_id':'Plugin _id'})
class get_plugin_det_by_id(Resource):
    @api.expect(header_parser, validate=True)
    @authService.authorized
    def get(self,_id=None):
        for plugin in list_plugins().get("all")[0].get("data"):
            if str(_id) ==  str(plugin.get("_id").get("$oid")):
                if "DeploymentPlugin" in plugin.get("plugin_name"):
                    plugin["file_contents"]=open(os.path.join(deployment_plugin_full_path,plugin.get("plugin_name"))+".py", "r").readlines()
                    plugin["file_path"]=os.path.join(deployment_plugin_static_path,plugin.get("plugin_name"))+".py"
                elif "SyncPlugin" in plugin.get("plugin_name"):    
                    plugin["file_contents"]=open(os.path.join(sync_plugin_full_path,plugin.get("plugin_name"))+".py", "r").readlines()
                    plugin["file_path"]=os.path.join(sync_plugin_static_path,plugin.get("plugin_name"))+".py"
                elif "RepositoryPlugin" in plugin.get("plugin_name"):    
                    plugin["file_contents"]=open(os.path.join(repository_plugin_full_path,plugin.get("plugin_name"))+".py", "r").readlines()
                    plugin["file_path"]=os.path.join(repository_plugin_static_path,plugin.get("plugin_name"))+".py"
                data = exitPointPluginsDB.get_by_plugin_name(plugin.get("plugin_name"))
                if data : plugin.update(data)
                return json.loads(Utils.JSONEncoder().encode({"result": "success", "message": "","data":plugin})), 200                              
        raise Exception("No Plugin with _id: "+_id+" was found")    

@PluginAPINs.route('/exitpoint/new', methods=['POST'])
class CreateEP(Resource):
    @api.expect(header_parser, ExitPointPluginsModel.add_ep_input_model, validate=True)
    @api.marshal_with(ExitPointPluginsModel.ep_create_response)
    @authService.authorized
    def post(self):
        """
        Create new ExitPointPlugin definition
        """
        data = request.get_json()       
        
        return {"result": "success", "message": "Record was created successfully",\
                 "data": {"_id": exitPointPluginsDB.add(data)}}, 200
                 
@PluginAPINs.route('/exitpoint/update', methods=['PUT'])
class UpdateEP(Resource):
    @api.expect(header_parser, ExitPointPluginsModel.ep_update_request, validate=True)
    @api.marshal_with(ExitPointPluginsModel.ep_create_response)
    @authService.authorized
    def put(self):
        """
        Update ExitPointPlugin definition
        """
        data = request.get_json()        
        return {"result": "success", "message": "Record was Updated",\
                 "data": {"_id": exitPointPluginsDB.replace(data)}}, 200




