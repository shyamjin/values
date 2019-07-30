import os,logging
import traceback
import threading
import thread
import time
from flask import Flask,jsonify,request
from flasgger import Swagger
from flask_compress import Compress
from modules.apimodels.Restplus import api_v1
from flask_cors import CORS


try:
    from Services import AppInitServices
    from modules import AccountAPI, UserAPI, RoleAPI, PermissionAPI, ToolAPI, DeploymentRequestAPI,\
     VersionsAPI, MachineAPI, MediaFilesAPI, CloneRequestAPI, SyncAPI, ConfigAPI, DistributionCenterAPI,\
      SystemDetailsAPI, DistributionSyncAPI, ToolSetAPI, PreRequisitesAPI, MachineGroupsAPI, ManageTeamsAPI,\
       TagAPI, GeneralAPI, DeploymentUnitApprovalStatusAPI, DeploymentUnitTypeAPI, DeploymentUnitAPI,\
       DeploymentUnitSetAPI, DeploymentGroupRequestAPI, PluginAPI, ReportsAPI, BuildAPI, StateAPI,\
       ToolsOnMachineAPI, FlexibleAttributesAPI,ProposedToolAPI,AuditingAPI,RepositoryAPI
    from settings import devMode, template, current_path,dpm_port

    
    application = Flask(__name__, static_folder=os.path.join(current_path, '../client/static'))
    application.config['ERROR_404_HELP'] = False
    application.config['SESSION_COOKIE_HTTPONLY'] = True
    application.config['REMEMBER_COOKIE_HTTPONLY'] = True
    application.config['SESSION_COOKIE_SECURE'] = True
    application.config['REMEMBER_COOKIE_SECURE'] = True
    Compress(application)
    CORS(application,methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE'])


    @application.route('/', methods=['GET'])
    def index():
        return application.send_static_file('index.html')
    
    
    Swagger(application, template=template)
    application.register_blueprint(api_v1)
    application.register_blueprint(AccountAPI.accountAPI)
    application.register_blueprint(UserAPI.userAPI)
    application.register_blueprint(RoleAPI.roleAPI)
    application.register_blueprint(PermissionAPI.permissionAPI)
    application.register_blueprint(DeploymentRequestAPI.deploymentrequestAPI)
    application.register_blueprint(DeploymentGroupRequestAPI.deploymentgrouprequestAPI)
    application.register_blueprint(VersionsAPI.versionAPI)
    application.register_blueprint(MachineAPI.machineAPI)
    application.register_blueprint(MediaFilesAPI.mediafilesAPI)
    application.register_blueprint(CloneRequestAPI.clonerequestAPI)
    application.register_blueprint(ToolAPI.toolAPI)
    application.register_blueprint(SyncAPI.syncAPI)
    application.register_blueprint(ConfigAPI.configAPI)
    application.register_blueprint(DistributionCenterAPI.distributionCenterAPI)
    application.register_blueprint(SystemDetailsAPI.systemdetailsAPI)
    application.register_blueprint(DistributionSyncAPI.distributionSyncAPI)
    application.register_blueprint(ToolSetAPI.toolSetAPI)
    application.register_blueprint(PreRequisitesAPI.preRequisitesAPI)
    application.register_blueprint(MachineGroupsAPI.machineGroupsAPI)
    application.register_blueprint(ManageTeamsAPI.manageTeamsAPI)
    application.register_blueprint(TagAPI.tagAPI)
    application.register_blueprint(GeneralAPI.generalAPI)
    application.register_blueprint(DeploymentUnitApprovalStatusAPI.deploymentUnitApprovalStatusAPI)
    application.register_blueprint(DeploymentUnitTypeAPI.deploymentUnitTypeAPI)
    application.register_blueprint(DeploymentUnitAPI.deploymentUnitAPI)
    application.register_blueprint(DeploymentUnitSetAPI.deploymentUnitSetAPI)
    application.register_blueprint(PluginAPI.PluginAPI)    
    application.register_blueprint(ReportsAPI.reportAPI)
    application.register_blueprint(BuildAPI.buildAPI)
    application.register_blueprint(StateAPI.stateAPI)
    application.register_blueprint(ToolsOnMachineAPI.toolsOnMachineAPI)
    
    
    @application.before_request
    def before_request():
        if request.method == 'OPTIONS':
            return flask_exception_method_not_allowed("error")
    
    @application.errorhandler(404)
    @application.errorhandler(500)
    def flask_exception(error):
        return jsonify({"result": "failed", "message": str(error)}), 404
    
    @application.errorhandler(405)
    def flask_exception_method_not_allowed(error):
        return jsonify({"result": "failed", "message": "The method is not allowed for the requested URL."}), 405
    
    # MONITOR ACTIVE THREAD COUNT
    def print_thread_count():
        while str((os.getenv('MONITOR_THREADS', False))).lower() == "true":
            print "%%%%%%%%%%%%%%%%%%%% CURRENT ACTIVE THREAD COUNT IS: " + str(threading.active_count()) + " %%%%%%%%%%%%%%%%%%%%%%%%%"
            for idx, thread in enumerate(threading.enumerate()):
                print(str(idx + 1) + ": " + thread.name)
            time.sleep(60)
    if str((os.getenv('MONITOR_THREADS', False))).lower() == "true":
        print "Thread Monitoring is set as: " + str(os.getenv('MONITOR_THREADS', False)) + ".Checking every 60 sec's"
        thread.start_new_thread(print_thread_count, ())

    if __name__ == '__main__':
        if devMode == True:
            print "###### THE APPLICATION IS RUNNING ON DEVELOPMET MODE ######"
            print "The Application is up and running..."
            application.run(port=int(dpm_port), host='0.0.0.0',debug=True)
        else:
            print "The Application is up and running..."
            application.run(port=int(dpm_port), host='0.0.0.0',debug=False)
           

except Exception as e:
    print "############# SYSTEM CRASHED ##############"
    traceback.print_exc()
