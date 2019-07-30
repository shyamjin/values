import copy,json,logging,os,time,traceback,requests,shutil,HelperServices
from os.path import join
from datetime import datetime
from autologging import logged
from bson import json_util
from requests.exceptions import ConnectionError, ReadTimeout
from DBUtil import CloneRequest, Versions, Machine, DeploymentFields, \
    Config, Tool, SystemDetails, DistributionMachine
from Services import Mailer, RemoteAuthenticationService, BuildHelperService,FileUtils,NexusHelperService,\
    CustomClassLoaderService
from Services.fabfile import getExecutables, copyToRemote, createUser, \
    cloneRepository, createUpstream, fetchUpstream, grantSudo, \
    createFolder, install_docker_containers, replaceTextInFile, \
    deleteFolder, grantFolderPermissions, checkoutRepositoryByBranch, \
    checkoutRepositoryByTag, pushUpstreamtoGitOrigin, \
    copyDirectorywithNewName, cre_hostname_external_ip, \
    getDockerVersion, dockerAddPermission, \
    dockerCreateFile, dockerDeamonReload, dockerRestart, \
    nexusAddPermission, \
    gitCredentialStore, jenkinsUpdateJobLastStep, scheduleCleaner, \
    grantWritePermissions, restart_docker_jenkins, runCommand,give_access_to_vpadmin,unzipNexus
from settings import dpm_url_prefix, remote_base_path, remote_git_path, \
    remote_jenkins_path, \
    remote_mongo_path, remote_dpm_path, remote_documents_path, remote_logos_path, \
    remote_media_files_path, remote_ssl_path, remote_sync_import_path, \
    remote_sync_export_path, remote_distribution_import_path, \
    remote_distribution_export_path, mongodb, temp_files_full_path,\
    default_admin_password, default_nexus_container_name,\
    plugin_directories_to_be_copied


# from django.db.models.functions import Substr
# from jinja2.runtime import to_string
@logged(logging.getLogger("CloneDeployment"))
class CloneDeployment(object):
    # Pay attention: In case this tuple will be changed while pending clone request,
    # a clone step id should be fixed to the new tuple indexation
    '''
    # STEPS TO BE FOLLOWED FOR CLONE##########################################
    ##########################################################################
    '''
    cloning_steps = (
        'check_connection',
        'verify_executable_installation',
        'create_validate_pack_folders',
        'create_hostname_external_ip',
        'create_git_user_for_account',
        'create_git_group_for_account',
        'assign_account_git_user_to_group',
        'copy_docker_config_file',
        'copy_docker_yml_file',
        'copy_jenkins_files',
        'copy_nexus_files',
        'copy_ssl_files',
        "copy_plugin_files",
        'install_docker_containers',
        'generate_system_details',
        'change_account_name',
        'clone_tools',
        'restart_docker_jenkins', 
        'add_into_distribution',  # add the machine to the distribution       
        'copy_default_files',  # Copy Default Logo Files
        'schedule_cleaner',
        'assign_write_permissions_to_git',
        'assign_full_access_to_dpm_directory',
        'assign_permissions_to_jenkins'
    )

    # Pay attention: In case this tuple will be changed while pending clone request,
    # a clone step id should be fixed to the new tuple indexation
    cloning_inner_steps = (
        'validate_jenkins_job',
        'validate_git_project',
        'set_tool_dependency',
        'clone_tool_to_account_dpm',  # timeout=600
        'copy_logo_media_files',  # ADDED THUMBNAIL FOR LOGO AND MEDIA FILES
        'fork_project_with_account_group',  # timeout=600
        'clone_repository_to_git',
        'create_upstream_to_original_rep',
        'jenkins_copy_job',
        'jenkins_update_job'
    )
    
    # Pay attention: In case this tuple will be changed while pending clone request,
    # a clone step id should be fixed to the new tuple indexation
    cloning_inner_steps_for_artifact_only = (
        'set_tool_dependency',
        'validate_build_structure_and_data',
        'clone_tool_to_account_dpm',  # timeout=600
        'copy_logo_media_files',  # ADDED THUMBNAIL FOR LOGO AND MEDIA FILES
        'download_builds',
        'update_build_information',
        'delete_downloaded_builds'    
    )
    
    '''
    # STEPS TO BE FOLLOWED FOR AddTool########################################
    ##########################################################################
    '''
    
    import_tool_steps = (
        'check_connection',
        'import_tools',
        'assign_write_permissions_to_git',
        'assign_full_access_to_dpm_directory',
        'restart_docker_jenkins',

    )

    # Pay attention: In case this tuple will be changed while pending clone request,
    # a clone step id should be fixed to the new tuple indexation
    import_tool_inner_steps = (
        'get_tool_data',
        'get_account_group_name_and_user',
        'validate_jenkins_job',
        'validate_git_project',
        'set_tool_dependency',
        'clone_tool_to_account_dpm',
        'copy_logo_media_files',
        'fork_project_with_account_group',
        'clone_repository_to_git',
        'create_upstream_to_original_rep',
        'jenkins_copy_job',
        'jenkins_update_job',
        'update_distribution_sync_data_in_account_dpm'
    )
    
    
    # Pay attention: In case this tuple will be changed while pending clone request,
    # a clone step id should be fixed to the new tuple indexation
    import_tool_inner_steps_for_artifact_only = (
        'get_tool_data',
        'set_tool_dependency',
        'validate_build_structure_and_data',
        'clone_tool_to_account_dpm',  # timeout=600
        'copy_logo_media_files',  # ADDED THUMBNAIL FOR LOGO AND MEDIA FILES
        'download_builds',
        'update_build_information',
        'delete_downloaded_builds',
        'update_distribution_sync_data_in_account_dpm'
    )
    
    ##########################################################################
    # STEPS TO BE FOLLOWED FOR AddTool -- END ################################
    '''
    # STEPS TO BE FOLLOWED FOR UpdateTool#####################################
    ##########################################################################
    '''
    
    update_tool_steps = (
        'check_connection',
        'update_tools',
        'assign_full_access_to_dpm_directory',
        'restart_docker_jenkins'
    )

    # Pay attention: In case this tuple will be changed while pending clone request,
    # a clone step id should be fixed to the new tuple indexation
    update_tool_inner_steps = (
        'validate_jenkins_job',
        'set_tool_dependency',
        'update_tool_to_account_dpm',
        'copy_logo_media_files',  # ADDED THUMBNAIL FOR LOGO AND MEDIA FILES
        'fetch_upstream_to_original_rep',
        'checkout_tool',
        'push_upstream_to_git',
        'copy_jenkins_files',
        'update_jenkins_files',
        'jenkins_update_job',
        'update_distribution_sync_data_in_account_dpm',
    )
    
    # Pay attention: In case this tuple will be changed while pending clone request,
    # a clone step id should be fixed to the new tuple indexation
    update_tool_inner_steps_for_artifact_only = (
        'get_tool_data',
        'set_tool_dependency',
        'validate_build_structure_and_data',
        'update_tool_to_account_dpm',
        'copy_logo_media_files',  # ADDED THUMBNAIL FOR LOGO AND MEDIA FILES
        'download_builds',
        'update_build_information',
        'delete_downloaded_builds',
        'update_distribution_sync_data_in_account_dpm',
    )
    ##########################################################################
    # STEPS TO BE FOLLOWED FOR UpdateTool - END ##############################


    '''
    DIRS TO BE CREATED IN REMOTE SERVER
    '''

    folder_list_to_create = (remote_git_path,
                             remote_jenkins_path,
                             remote_mongo_path,
                             remote_dpm_path,
                             remote_documents_path,
                             remote_logos_path,
                             remote_media_files_path,
                             remote_ssl_path,
                             remote_sync_import_path,
                             remote_sync_export_path,
                             remote_distribution_import_path,
                             remote_distribution_export_path)

    def __init__(self):
        # initiate DB collections
        self.cloneRequestDB = CloneRequest.CloneRequest(mongodb)
        self.versionsDB = Versions.Versions(mongodb)
        self.toolDB = Tool.Tool(mongodb)
        self.deploymentFieldsDB = DeploymentFields.DeploymentFields(mongodb)
        self.machineDB = Machine.Machine(mongodb)
        self.mailer = Mailer.Mailer()
        self.configDB = Config.Config(mongodb)
        self.clone_account_config_details = self.configDB.getConfigByName(
            'CloneAccountServiceDetails')        
        self.id = None
        self.current_step_id = 0
        self.current_tool_version_id = ''
        self.current_tool_step_id = -1
        self.execution_count = 0
        self.CLONE_TOOLS_STEP_NAME = None
        self.CLONE_TYPE = None
        self.CLONE_TOOLS_STEP_ID = 0
        self.CloneDetails = {}
        self.MachineDetails = {}
        self.ErrFlag = 0  # 0 -everything is ok , 1-
        self.status_message = ''
        self.systemDetailsDb = SystemDetails.SystemDetails(mongodb)
        self.systemDetail = self.systemDetailsDb.get_system_details_single()
        self.distributionDB = DistributionMachine.DistributionMachine(mongodb)
        if not self.systemDetail.get("hostname"):
            raise Exception("hostname not found in systemDeatils")
        if not self.systemDetail.get("ip"):
            raise Exception("ip not found in systemDeatils")
        # will be using this later - so that we don't need to have different
        # functions executeCloneSteps, executeToolSteps, executeToolupdateSteps
        self.curr_clonetype_step = ()
        self.timeToSleep = 100  # Seconds
        self.remote_authentication_service = RemoteAuthenticationService.RemoteAuthenticationService()

    def GetMachineDetails(self, id):
        machine = self.machineDB.GetMachine(id)
        return machine

    def GetCloneRequestDetails(self, id):
        request = self.cloneRequestDB.GetCloneRequest(id)
        return request

    def GetVersionDetalis(self, id):
        version = self.versionsDB.get_version(id, True)
        return version

    def GetToolByVersion(self, id):
        tool = self.toolDB.get_tool_by_version(id, True)
        return tool

    def GetDeploymentFieldsDetail(self, version_id):
        fields = self.deploymentFieldsDB.GetDeploymentFields(version_id)
        return fields

    def InitStepDetailsForClone(self, **kwargs):
        step_details = ""
        for step_id, step in enumerate(self.cloning_steps):
            jsonEntry = '{"step_id":"' + str(step_id) + '", "step_name":"' + step + \
                '", "step_status": "New", "step_message": "", "step_start_time":"", "step_end_time":"", "step_duration":""}'
            if step_details != "":
                step_details = step_details + ","
            # in case clone_tools step is found, we need to create for each
            # tool its own steps from cloning_inner_steps tuple
            if self.CLONE_TOOLS_STEP_NAME == step:
                tool_step_details = ""
                for version in self.ToolList:
                    jsonToolEntry = ""
                    step_to_use=self.cloning_inner_steps
                    tool_details=self.GetToolByVersion(version.get("version_id"))
                    if tool_details:
                        if str(tool_details.get("artifacts_only")).lower() == "true": # CHECK IF THIS TOOL SHOULD ONLY CLONE ARTIFACTS
                            step_to_use=self.cloning_inner_steps_for_artifact_only
                    for tool_step_id, tool_step_name in enumerate(step_to_use):
                        jsonToolEntry = jsonToolEntry + '"' + str(tool_step_id) + \
                            '": {"tool_step_id":"' + str(tool_step_id) + '","tool_step_name":"' \
                            + tool_step_name + \
                            '", "tool_step_status": "New", "tool_step_message": "", "tool_step_start_time":"", "tool_step_end_time":"", "tool_step_duration":""},'
                    tool_step_details = tool_step_details + '"' + \
                        version["version_id"] + \
                        '":{' + jsonToolEntry[:-1] + '},'
                jsonEntry = '{"step_id":"' + str(step_id) + '", "step_name":"' + step + '","tool_step_details":{' + \
                    tool_step_details[:-1] + \
                    '}, "step_status": "New", "step_message": "", "step_duration":""}'
            step_details = step_details + jsonEntry
        step_details = '{"step_details": [' + step_details + ']}'
        self.cloneRequestDB.InitStatusDetails(self.id, step_details)

    def InitStepDetailsForAddTool(self):
        step_details = ""        
        for step_id, step in enumerate(self.import_tool_steps):
            jsonEntry = '{"step_id":"' + str(step_id) + '", "step_name":"' + step + \
                '", "step_status": "New", "step_message": "", "step_start_time":"", "step_end_time":"", "step_duration":""}'
            if step_details != "":
                step_details = step_details + ","
            # in case clone_tools step is found, we need to create for each
            # tool its own steps from cloning_inner_steps tuple
            if self.CLONE_TOOLS_STEP_NAME == step:
                tool_step_details = ""
                for version in self.ToolList:
                    jsonToolEntry = ""
                    step_to_use=self.import_tool_inner_steps
                    tool_details=self.GetToolByVersion(version.get("version_id"))
                    if tool_details:
                        if str(tool_details.get("artifacts_only")).lower() == "true": # CHECK IF THIS TOOL SHOULD ONLY CLONE ARTIFACTS
                            step_to_use=self.import_tool_inner_steps_for_artifact_only
                    for tool_step_id, tool_step_name in enumerate(step_to_use):
                        jsonToolEntry = jsonToolEntry + '"' + str(tool_step_id) + \
                            '": {"tool_step_id":"' + str(tool_step_id) + '","tool_step_name":"' \
                            + tool_step_name + \
                            '", "tool_step_status": "New", "tool_step_message": "", "tool_step_start_time":"", "tool_step_end_time":"", "tool_step_duration":""},'
                    tool_step_details = tool_step_details + '"' + \
                        version["version_id"] + \
                        '":{' + jsonToolEntry[:-1] + '},'
                jsonEntry = '{"step_id":"' + str(step_id) + '", "step_name":"' + step + \
                    '","tool_step_details":{' + \
                    tool_step_details[:-1] + \
                    '}, "step_status": "New", "step_message": "", "step_duration":""}'
            step_details = step_details + jsonEntry
        step_details = '{"step_details": [' + step_details + ']}'
        self.cloneRequestDB.InitStatusDetails(self.id, step_details)

    def InitStepDetailsForUpdateTool(self):
        step_details = ""
        for step_id, step in enumerate(self.update_tool_steps):
            jsonEntry = '{"step_id":"' + str(step_id) + '", "step_name":"' + step + \
                '", "step_status": "New", "step_message": "", "step_start_time":"", "step_end_time":"", "step_duration":""}'
            if step_details != "":
                step_details = step_details + ","
            # in case clone_tools step is found, we need to create for each
            # tool its own steps from cloning_inner_steps tuple
            if self.CLONE_TOOLS_STEP_NAME == step:
                tool_step_details = ""
                for version in self.ToolList:
                    jsonToolEntry = ""
                    step_to_use=self.update_tool_inner_steps
                    tool_details=self.GetToolByVersion(version.get("version_id"))
                    if tool_details:
                        if str(tool_details.get("artifacts_only")).lower() == "true": # CHECK IF THIS TOOL SHOULD ONLY CLONE ARTIFACTS
                            step_to_use=self.update_tool_inner_steps_for_artifact_only
                    for tool_step_id, tool_step_name in enumerate(step_to_use):
                        jsonToolEntry = jsonToolEntry + '"' + str(tool_step_id) + \
                            '": {"tool_step_id":"' + str(tool_step_id) + '","tool_step_name":"' + tool_step_name + \
                            '", "tool_step_status": "New", "tool_step_message": "", "tool_step_start_time":"", "tool_step_end_time":"", "tool_step_duration":""},'
                    tool_step_details = tool_step_details + '"' + \
                        version["version_id"] + \
                        '":{' + jsonToolEntry[:-1] + '},'
                jsonEntry = '{"step_id":"' + str(step_id) + '", "step_name":"' + step + '","tool_step_details":{' + \
                    tool_step_details[:-1] + \
                    '}, "step_status": "New", "step_message": "", "step_duration":""}'
            step_details = step_details + jsonEntry
        step_details = '{"step_details": [' + step_details + ']}'
        self.cloneRequestDB.InitStatusDetails(self.id, step_details)

    def UpdateStepStatus(self, sts, msg):
        result = self.cloneRequestDB.UpdateStepDetails(
            self.id, self.current_step_id, step_status=sts, step_message=msg)
        return result

    def UpdateStepStartTime(self):
        result = self.cloneRequestDB.UpdateStepDetails(
            self.id, self.current_step_id, step_status='Processing',
            step_start_time=datetime.now(), step_message='')
        return result

    # It is assumed if step reach his end, it will get successful status
    def UpdateStepEndTime(self, duration):
        result = self.cloneRequestDB.UpdateStepDetails(
            self.id, self.current_step_id, step_status='Done', step_message='successfully completed',
            step_end_time=datetime.now(), step_duration=("%.3f" % duration))
        return result

    def updateToolList(self, version_status):
        result = self.cloneRequestDB.updateToolList(
            self.id, self.current_tool_version_id, status=version_status, current_tool_step_id=self.current_tool_step_id)
        return result

    def UpdateToolStepStatus(self, status, message):
        result = self.cloneRequestDB.UpdateToolStepDetails(
            self.id, self.current_step_id, self.current_tool_version_id,
            self.current_tool_step_id, tool_step_status=status, tool_step_message=message)
        return result

    def UpdateToolStepStartTime(self):
        result = self.cloneRequestDB.UpdateToolStepDetails(self.id,
                                                           self.current_step_id,
                                                           self.current_tool_version_id,
                                                           self.current_tool_step_id,
                                                           tool_step_status='Processing',
                                                           tool_step_message='',
                                                           tool_step_start_time=datetime.now())
        return result

    # It is assumed if tool step reach his end, it will get successful status
    def UpdateToolStepEndTime(self, duration):
        result = self.cloneRequestDB.UpdateToolStepDetails(self.id,
                                                           self.current_step_id,
                                                           self.current_tool_version_id,
                                                           self.current_tool_step_id,
                                                           tool_step_status='Done',
                                                           tool_step_message='successfully completed',
                                                           tool_step_end_time=datetime.now(),
                                                           tool_step_duration=("%.3f" % duration))
        return result

    def UpdateRequestStatus(self, sts):
        result = self.cloneRequestDB.UpdateRequestDetails(self.id, status=sts)
        return result

    def init_data(self):
        try:
            self.CloneRequestDetails = self.GetCloneRequestDetails(self.id)
            if self.CloneRequestDetails == None:
                raise ValueError(
                    "No clone request ID (" + self.id + ") is found.")
            else:
                if str(self.CloneRequestDetails.get("type")).lower() == "clone".lower():
                    self.CLONE_TOOLS_STEP_NAME = 'clone_tools'.lower()
                    self.CLONE_TYPE = "clone".lower()
                elif str(self.CloneRequestDetails.get("type")).lower() == "importtool".lower():
                    self.CLONE_TOOLS_STEP_NAME = 'import_tools'.lower()
                    self.CLONE_TYPE = "importtool".lower()
                elif str(self.CloneRequestDetails.get("type")).lower() == "updatetool".lower():
                    self.CLONE_TOOLS_STEP_NAME = 'update_tools'.lower()
                    self.CLONE_TYPE = "updatetool".lower()
                else:
                    raise ValueError(
                        "Invalid CLONE_TYPE :" + str(self.CloneRequestDetails.get("type")) + " found")
            self.logs = self.CloneRequestDetails.get("logs")
            if not self.logs or len(self.logs) < 1:
                self.logs = []
            self.handleLogs("Started with Init data")
            self.local_jenkins_job_path = self.clone_account_config_details[
                'local_jenkins_job_path']
            self.jenkins_version = self.clone_account_config_details[
                'jenkins_version']
            self.remote_vp_home_path = remote_base_path
            self.remote_dpm_home_path = self.remote_vp_home_path + "dpm/"
            self.remote_dpm_ssl_path = self.remote_vp_home_path + "dpm/ssl/"
            self.remote_dpm_plugins_path = self.remote_vp_home_path + "dpm/plugins/"
            self.remote_dpm_logos_path = self.remote_vp_home_path + "dpm/static/files/logos/"
            self.remote_jenkins_home_path = self.remote_vp_home_path + "jenkins/"
            self.remote_jenkins_job_path = self.remote_jenkins_home_path + "jobs/"
            self.remote_git_home_path = self.remote_vp_home_path + "git/"
            self.local_dpm_home_path = str(
                os.path.dirname(__file__)).rsplit(os.sep, 1)[0]
            self.local_dpm_logos_path = str(os.path.dirname(__file__)).rsplit(
                os.sep, 1)[0] + os.sep + 'static' + os.sep + 'files' + os.sep + 'logos' + os.sep
            self.local_dpm_docker_files_path = self.local_dpm_home_path + \
                os.sep + "Services" + os.sep + "docker"
            self.local_dpm_cleaner_files_path = self.local_dpm_home_path + \
                os.sep + "Services" + os.sep + "docker" + os.sep + "utility" + os.sep
            self.local_dpm_ssl_files_path = self.local_dpm_home_path + os.sep + "ssl" + os.sep
            self.local_dpm_plugins_files_path = self.local_dpm_home_path + os.sep + "Plugins" + os.sep
            self.gitlab_user = self.clone_account_config_details[
                'gitlab_user']
            self.gitlab_password = self.clone_account_config_details[
                'gitlab_password']
            self.gitlab_token = self.clone_account_config_details[
                'gitlab_token']
            self.target_artifact_auth_repo_type=self.clone_account_config_details["target_artifact_auth_repo_type"].split(":")[0] # EXPECTED nexus2:2.14.2_01
            self.target_artifact_auth_repo_type_version = self.clone_account_config_details["target_artifact_auth_repo_type"].split(":")[1]# EXPECTED nexus2:2.14.2_01
            self.account_gitlab_password = self.clone_account_config_details["account_gitlab_password"]
            self.target_dpm_user=self.clone_account_config_details["target_dpm_user"]
            self.target_dpm_password=self.clone_account_config_details["target_dpm_password"]
            self.temp_artifacts_path = temp_files_full_path + "artifacts/"+str(self.id)+"/"
            self.account_name = str(self.CloneRequestDetails["account_name"].lower(
            )).replace(" ","_")
            self.ToolList = self.CloneRequestDetails["tool_list"]
            self.current_step_id = int(
                self.CloneRequestDetails["current_step_id"])
            self.execution_count = int(
                self.CloneRequestDetails["execution_count"])
            self.MachineDetails = self.GetMachineDetails(
                self.CloneRequestDetails["machine_id"])
            self.remote_host = self.MachineDetails["host"].lower()
            self.remote_nexus_url = self.remote_host + ":8081"
            self.remote_jenkins_url = self.remote_host + ":8080"
            self.remote_dpm_url = self.remote_host + ":" + \
                str(self.clone_account_config_details[
                    'remote_dpm_port'])
            self.master_host = self.systemDetail.get("hostname")
            # TODO - To delete below hard coded value
            self.master_git_lab_url = self.clone_account_config_details[
                'git_lab_rest_api_url']
            if self.execution_count == 0:
                self.cloneRequestDB.UpdateRequestDetails(
                    self.id, status="Started", start_date=datetime.now(), status_message="")
                if self.CLONE_TYPE.lower() in "clone".lower():
                    self.CLONE_TOOLS_STEP_ID = self.cloning_steps.index(
                        self.CLONE_TOOLS_STEP_NAME)
                    self.InitStepDetailsForClone()
                    self.curr_clonetype_step = self.cloning_steps
                elif self.CLONE_TYPE.lower() in "importtool".lower():
                    self.CLONE_TOOLS_STEP_ID = self.import_tool_steps.index(
                        self.CLONE_TOOLS_STEP_NAME)
                    self.InitStepDetailsForAddTool()
                    self.curr_clonetype_step = self.import_tool_steps
                elif self.CLONE_TYPE.lower() in "updatetool".lower():
                    self.CLONE_TOOLS_STEP_ID = self.update_tool_steps.index(
                        self.CLONE_TOOLS_STEP_NAME)
                    self.InitStepDetailsForUpdateTool()
                    self.curr_clonetype_step = self.update_tool_steps
                else:
                    raise ValueError("Invalid CLONE_TYPE :" +
                                     str(self.CLONE_TYPE))
                self.CloneRequestDetails = self.GetCloneRequestDetails(self.id)
            else:
                if self.CLONE_TYPE.lower() in "clone".lower():
                    self.CLONE_TOOLS_STEP_ID = self.cloning_steps.index(
                        self.CLONE_TOOLS_STEP_NAME)
                    self.curr_clonetype_step = self.cloning_steps
                if self.CLONE_TYPE.lower() in "importtool".lower():
                    self.CLONE_TOOLS_STEP_ID = self.import_tool_steps.index(
                        self.CLONE_TOOLS_STEP_NAME)
                    self.curr_clonetype_step = self.import_tool_steps
                elif self.CLONE_TYPE.lower() in "updatetool".lower():
                    self.CLONE_TOOLS_STEP_ID = self.update_tool_steps.index(
                        self.CLONE_TOOLS_STEP_NAME)
                    self.curr_clonetype_step = self.import_tool_steps
                self.cloneRequestDB.UpdateRequestDetails(self.id, status="Resumed",
                                                         start_date=datetime.now(
                                                         ), status_message="", duration='', end_date='')
            self.load_gitlab_projects()
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "init_data:" + str(e)
            print self.status_message
            raise ValueError(self.status_message)

    def load_gitlab_projects(self):
        projects = []
        url=None
        try:
            url = self.master_git_lab_url + 'projects/search/vpgroup?per_page=100&page=1'
            headers = {'Content-Type': 'application/json',
                       'PRIVATE-TOKEN': self.gitlab_token}
            response = requests.get(
                url, headers=headers, timeout=600, verify=False)
            if response.status_code != 200:
                msg = str(response.status_code) + ' ' + response.reason + '. ' + \
                    str(response._content).translate(
                        None, '{"}') + '. ' + url
                raise ValueError(msg)
            projects.extend(json.loads(response._content))
            if response.headers:
                if response.headers.get("X-Total-Pages") and response.headers.get("X-Total-Pages").isdigit() and int(response.headers.get("X-Total-Pages")) > 1:
                    for page_no in range(2, int(response.headers.get("X-Total-Pages")) + 1):
                        url = self.master_git_lab_url + \
                            'projects/search/vpgroup?per_page=100&page=' + \
                            str(page_no)
                        headers = {'Content-Type': 'application/json',
                                   'PRIVATE-TOKEN': self.gitlab_token}
                        response = requests.get(
                            url, headers=headers, timeout=600, verify=False)
                        if response.status_code != 200:
                            msg = str(response.status_code) + ' ' + response.reason + '. ' + \
                                str(response._content).translate(
                                    None, '{"}') + '. ' + url
                            raise ValueError(msg)
                        projects.extend(json.loads(response._content))
            self.git_lab_project = {}            
            for proj in projects:
                self.git_lab_project[proj["name"]] = proj
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "load_gitlab_projects:"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message
            self.cloneRequestDB.UpdateRequestDetails(
                self.id, message="GitLab projects loading is failed: " + self.status_message)
            raise ValueError(self.status_message)

    def executeCloneSteps(self, **kwargs):
        try:
            while self.current_step_id < len(self.cloning_steps):
                step_name = self.cloning_steps[self.current_step_id]
                self.handleLogs("Calling method :" + str(step_name))
                method = getattr(self, step_name)
                method(**kwargs)
                self.handleLogs("Completed method :" + str(step_name))
                self.current_step_id = self.current_step_id + 1
                result = self.cloneRequestDB.UpdateRequestDetails(
                    self.id, current_step_id=int(self.current_step_id))
        except Exception as e:  # catch *all* exceptions
            traceback.print_exc()
            self.ErrFlag = 1
            self.status_message = "executeCloneSteps:" + str(e)
            print self.status_message
            raise ValueError(self.status_message)

    # def executeToolSteps(self):
    #    try:
    #        while self.current_step_id < len(self.import_tool_steps):
    #            step_name = self.import_tool_steps[self.current_step_id]
    #            method = getattr(self, step_name)
    #            apply(method)
    #            self.current_step_id = self.current_step_id + 1
    #            result = self.cloneRequestDB.UpdateRequestDetails(self.id, current_step_id=int(self.current_step_id))
    #    except Exception as e: # catch *all* exceptions
    #        self.ErrFlag = 1
    #        self.status_message = "executeToolSteps:" + str(e)
    #        print self.status_message
    #        raise ValueError(self.status_message)

# This one function will replace above functions later. - executeCloneSteps
    def executeToolSteps(self, **kwargs):
        if len(self.curr_clonetype_step) > 0:
            pass
        else:
            ValueError("curr_clonetype_step is not initialized : " +
                       str(self.CLONE_TYPE))
        try:
            while self.current_step_id < len(self.curr_clonetype_step):
                step_name = self.curr_clonetype_step[self.current_step_id]
                self.handleLogs("Calling method :" + str(step_name))
                method = getattr(self, step_name)
                method(**kwargs)
                self.handleLogs("Completed method :" + str(step_name))
                self.current_step_id = self.current_step_id + 1
                result = self.cloneRequestDB.UpdateRequestDetails(
                    self.id, current_step_id=int(self.current_step_id))
        except Exception as e:  # catch *all* exceptions
            traceback.print_exc()
            self.ErrFlag = 1
            self.status_message = "executeToolSteps-" + \
                self.curr_clonetype_step + ":" + str(e)
            print self.status_message
            raise ValueError(self.status_message)

    def initilizeVersionDetails(self):
        try:
            self.currentVersionDetails = self.GetVersionDetalis(
                self.current_tool_version_id)
            self.currentToolDetails = self.GetToolByVersion(
                self.current_tool_version_id)
            if (self.currentVersionDetails.has_key('gitlab_branch')):
                self.gitlab_branch = self.currentVersionDetails["gitlab_branch"]
            else:
                raise ValueError(
                    'gitlab_branch attribute is note defined for the version')
            if (self.currentVersionDetails.has_key('gitlab_repo')):
                self.gitlab_repo = self.currentVersionDetails["gitlab_repo"]
            else:
                raise ValueError(
                    'gitlab_repo attribute is note defined for the version')
            if (self.currentVersionDetails.has_key('jenkins_job')):
                self.jenkins_job_name = self.currentVersionDetails["jenkins_job"]
            else:
                raise ValueError(
                    'jenkins_job attribute is note defined for the version')
            self.tool_git_folder_name = self.gitlab_repo.split("/")[-1][:-4]
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "initilizeVersionDetails:" + str(e)
            print self.status_message
            raise ValueError(self.status_message)

    # ALWAYS Execute all tool step methods
    def executeCloneToolSteps(self, **kwargs):
        try:
            self.ToolList.sort(
                key=self.cloneRequestDB.clone_order, reverse=False)
            for version in self.ToolList:
                self.current_tool_version_id = version["version_id"]
                self.initilizeVersionDetails()
                currentVersionStatus = version["status"]
                self.new_account_version_branch = self.account_name + \
                    '_' + self.current_tool_version_id
                # remove 'requested' after it is handled from GUI, that is GIU will send status=New instead of 'requested' when clone_request add is called
                if currentVersionStatus.lower() in ['new', 'retry', 'requested']:
                    self.current_tool_step_id = version.get(
                        "current_tool_step_id")
                    if self.current_tool_step_id is None or int(self.current_tool_step_id) == -1:
                        self.current_tool_step_id = 0
                    self.current_tool_step_id = int(self.current_tool_step_id)
                    current_version_tool_step_list = self.CloneRequestDetails["step_details"][self.CLONE_TOOLS_STEP_ID]["tool_step_details"][str(
                        self.current_tool_version_id)]
                    while int(self.current_tool_step_id) < len(current_version_tool_step_list):
                        if str(currentVersionStatus).lower() == 'cancelled':
                            self.UpdateToolStepStatus(
                                "Cancelled", "Cancelled by user")
                            self.current_tool_step_id = self.current_tool_step_id + 1
                            continue
                        # LETS SAY CLONE FAILED AFTER STEP  clone_tools -- > clone_tool_to_account_dpm
                        # We need to regain self.current_new_version_id as its used later
                        for step in current_version_tool_step_list.keys():
                            if str(current_version_tool_step_list.get(step).get("tool_step_name")).lower() == "clone_tool_to_account_dpm"\
                                    and str(current_version_tool_step_list.get(step).get("tool_step_status")).lower() == "done":
                                self.current_new_version_id = str(
                                    current_version_tool_step_list.get(step)["new_version_id"])
                                break
                        current_tool_step_details = current_version_tool_step_list[str(
                            self.current_tool_step_id)]
                        tool_step_name = str(
                            current_tool_step_details["tool_step_name"])
                        tool_step_status = str(
                            current_tool_step_details["tool_step_status"])
                        self.handleLogs("executeCloneToolSteps:For step:" +
                                        tool_step_name + " status is " + tool_step_status)
                        method = getattr(self, tool_step_name)
                        self.handleLogs(
                            "executeCloneToolSteps:Calling Method:" + tool_step_name)
                        method(**kwargs)
                        self.handleLogs(
                            "executeCloneToolSteps:Method Completed:" + tool_step_name)
                        self.current_tool_step_id = self.current_tool_step_id + 1
                    self.updateToolList('Done')
        except Exception as e:  # catch *all* exceptions
            traceback.print_exc()
            self.ErrFlag = 1
            if self.CLONE_TOOLS_STEP_NAME == 'clone_tools'.lower():
                self.status_message = "executeCloneToolSteps Failed to clone tool:" + \
                    str(e) + " for version id: " + self.current_tool_version_id
                # self.updateToolList ('failed')
            elif self.CLONE_TOOLS_STEP_NAME == 'import_tools'.lower():
                self.status_message = "executeCloneToolSteps Failed to add tool:" + \
                    str(e) + " for version id: " + self.current_tool_version_id
            elif self.CLONE_TOOLS_STEP_NAME == 'update_tools'.lower():
                self.status_message = "executeCloneToolSteps Failed to update tool:" + \
                    str(e) + " for version id: " + self.current_tool_version_id
            self.updateToolList('Failed')
            print self.status_message
            raise ValueError(self.status_message)

    def handleLogs(self, newLogLine):
        print "CloneAccountServices: _id: " + str(self.id) + " " + newLogLine
        if not str(newLogLine).lower().strip() or str(newLogLine).lower().strip() in ["none", "", " "]:
            return
        for line in str(newLogLine).split('\r\n'):
            line = line.replace("'", "").replace('"', "")
            if str(line).lower().strip() and str(line).lower().strip() not in ["none", "", " "]:
                self.innerLogs["logdata"].append(line)
        logs = copy.deepcopy(self.logs)
        logs.append(self.innerLogs)
        cloneRequest = {}
        cloneRequest["_id"] = {"oid": self.id}
        cloneRequest["logs"] = logs
        self.cloneRequestDB.UpdateCloneRequest(cloneRequest)

    def startExecution(self):
        try:
            self.innerLogs = {}
            self.innerLogs["dateofdeployment"] = str(
                datetime.now()).split(".")[0]
            self.innerLogs["logdata"] = []
            #######################
            # data initialization #
            #######################
            # Send notification about starting process - In case mail
            # notification is failed don't failed the whole process
            self.init_data()
            self.senf_notification("started")
            # self.check_connection()
            ##########################
            # run all cloning steps  #
            ##########################
            if str(self.CloneRequestDetails.get("type")).lower() in ["clone".lower(),
                                                                     "importtool".lower(),
                                                                     "updatetool".lower()]:
                if str(self.CloneRequestDetails.get("type")).lower() in ["importtool".lower(),
                                                                         "updatetool".lower()]:
                    self.handleLogs("This is a tool import/update request..")
                    self.remote_authentication_service.authenticate(
                        self.MachineDetails, self.executeToolSteps)
                else:
                    self.handleLogs("This is a clone request..")
                    self.remote_authentication_service.authenticate(
                        self.MachineDetails, self.executeCloneSteps)
                    # self.executeCloneSteps()
            else:
                raise ValueError("CloneAccountService: Skipping _id :" + str(
                    self.CloneRequestDetails.get("_id")) + " as the type is invalid")

            # Send notification about ending process - In case mail
            # notification is failed don't failed the whole process
            self.senf_notification("completed")
        except Exception as e:  # catch *all* exceptions
            # what if exception is thrown by init data .... without compleating init data execution count will get incremented
            traceback.print_exc()
            self.ErrFlag = 1
            self.status_message = "startExecution:" + str(e)
            self.senf_notification("failed")
            print self.status_message
            self.handleLogs("This request failed with error :" +
                            str(self.status_message))

    def senf_notification(self, status):
        try:
            requested_by = self.CloneRequestDetails.get("requested_by")
            if not requested_by:
                requested_by = "User"
            distribution_list = self.CloneRequestDetails.get(
                "distribution_list")
            if distribution_list:
                self.mailer.send_html_notification(distribution_list, None, None, 3,
                                                   {"name": requested_by,
                                                    "machineName": self.MachineDetails.get("machine_name"),
                                                    "status": status})
        except Exception as e:  # catch *all* exceptions
            print "Failed to save email" + str(e)

    def runClone(self, id):

        self.id = id
        final_status = "Done"
        start_time = time.time()

        # Starting request execution
        self.startExecution()

        end_time = time.time()
        print "runClone " + str(self.ErrFlag)
        print
        if self.ErrFlag == 1:
            final_status = "Failed"
        else:
            self.status_message = "The cloning has been completed"
        # abhinav
        # what if start execution throws an error
        self.cloneRequestDB.UpdateRequestDetails(self.id, end_date=datetime.now(),
                                                 status_message=self.status_message,
                                                 status=final_status,
                                                 duration=str(
            ("%.3f" % float(end_time - start_time))), execution_count=str(self.execution_count + 1))
        return self.status_message

    #*************************************************************************
    #************************************************* Request steps *********
    #*************************************************************************
    def start_cloning(self):
    #     try :
        start_time = time.time()
        self.UpdateStepStartTime()
        # add method implementation
        end_time = time.time()
        self.UpdateStepEndTime(end_time - start_time)
    #    except Exception as e: # catch *all* exceptions
    #        print "Try and catch start cloning"
    #        print 'Error : start_cloning '+str(e)
    #        self.ErrFlag = 1
    #         self.UpdateStepStatus(self.current_step_id, "Failed", "Step: start_cloning" + str(e))

    def verify_executable_installation(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            machine_executables = ''
            machine_executables = getExecutables(**kwargs)
            self.handleLogs(str(machine_executables))
            if "docker" in machine_executables:
                pass
            else:
                raise ValueError(
                    "docker executable is not installed on this machine")
            if "docker-compose" in machine_executables:
                pass
            else:
                raise ValueError(
                    "docker-compose executable is not installed on this machine")
            if "git" in machine_executables:
                pass
            else:
                raise ValueError(
                    "git executable is not installed on this machine")
            if "unzip" in machine_executables:
                pass
            else:
                raise ValueError(
                    "unzip executable is not installed on this machine")
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "verify_executable_installation:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def create_validate_pack_folders(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            machine_executables = ''
            for folder in self.folder_list_to_create:
                result = createFolder(folder, **kwargs)
                self.handleLogs(str(result))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "create_validate_pack_folders:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def check_connection(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            try:
                print ('trying to run "hostname" ' +
                       str(self.MachineDetails.get('host')))
                self.handleLogs('trying to run "hostname" ' +
                                str(self.MachineDetails.get('host')))
                result = runCommand("hostname", False, **kwargs)
                self.handleLogs(str(result))
            except Exception as e:
                raise ValueError(
                    'Unable to ping machine with error : ' + str(e))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "check_connection:" + str(e)
            print self.status_message
            raise ValueError(self.status_message)

    def create_hostname_external_ip(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            machine_executables = ''

            result = cre_hostname_external_ip(**kwargs)
            self.handleLogs(str(result))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "create_hostname_external_ip:" + str(e)
            print self.status_message
            raise ValueError(self.status_message)

    def create_vpadmin_user(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            machine_executables = ''
            createUser(self.gitlab_user, **kwargs)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "create_vpadmin_user:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def checkout_tool(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            if str(self.currentVersionDetails.get("branch_tag")).lower() in ["branch"]:
                reply = checkoutRepositoryByBranch(
                    self.remote_git_home_path + "/" + self.tool_git_folder_name, self.currentVersionDetails.get("gitlab_branch"), **kwargs)
                self.handleLogs(
                    "checkout_tool:Checkout by Branch :" + str(reply))
            elif str(self.currentVersionDetails.get("branch_tag")).lower() in ["tag"]:
                reply = checkoutRepositoryByTag(
                    self.remote_git_home_path + "/" + self.tool_git_folder_name,
                    self.currentToolDetails.get("tag"), **kwargs)
                self.handleLogs(
                    "checkout_tool:Checkout by tag :" + str(reply))
            else:
                self.handleLogs(
                    "checkout_tool:branch/tag not found in currentVersionDetails")
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "checkout_tool:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def push_upstream_to_git(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()

            reply = pushUpstreamtoGitOrigin(
                self.remote_git_home_path + "/" + self.tool_git_folder_name,
                self.currentVersionDetails.get("gitlab_branch"), **kwargs)
            self.handleLogs(str(reply))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "push_upstream_to_git:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def grant_sudo_perms_to_vpadmin(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            machine_executables = ''
            grantSudo(self.gitlab_user, **kwargs)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "grant_sudo_perms_to_vpadmin:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def grant_valuepack_folder_full_control_to_vpadmin(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            grantFolderPermissions("664", self.remote_vp_home_path, **kwargs)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "grant_valuepack_folder_full_control_to_vpadmin:" + \
                str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def assign_write_permissions_to_git(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            self.handleLogs(
                "Called assign_write_permissions_to_git.grantWritePermissions :" + self.remote_git_home_path)
            result = grantWritePermissions(self.remote_git_home_path, **kwargs)
            self.handleLogs(
                "Response assign_write_permissions_to_git.grantWritePermissions :" + str(result))
            self.handleLogs(
                "Called assign_write_permissions_to_git.grantFolderPermissions :" + self.remote_git_home_path)
            result = grantFolderPermissions(
                "777", self.remote_git_home_path, **kwargs)
            self.handleLogs(
                "Response assign_write_permissions_to_git.grantFolderPermissions :" + str(result))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "assign_write_permissions_to_git:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)
        
    def assign_permissions_to_jenkins(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            self.handleLogs(
                "Called assign_permissions_to_jenkins :" + self.remote_jenkins_job_path)
            result = give_access_to_vpadmin(self.remote_jenkins_job_path, **kwargs)
            self.handleLogs(
                "Response assign_permissions_to_jenkins:" + str(result))            
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "assign_permissions_to_jenkins:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)    

    def assign_full_access_to_dpm_directory(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            self.handleLogs(
                "Called assign_full_access_to_dpm :" + self.remote_git_home_path)
            result = grantFolderPermissions(
                "777", self.remote_dpm_home_path, **kwargs)
            self.handleLogs(
                "Response assign_full_access_to_dpm :" + str(result))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "assign_full_access_to_dpm:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def create_git_user_for_account(self, **kwargs):
        url = None
        try:
            print "create new gitlab user for account"
            start_time = time.time()
            self.UpdateStepStartTime()
            url = self.master_git_lab_url + 'users/'
            payload = {"email": "vp_" + self.account_name + "@amdocs.com",
                       "password": self.account_gitlab_password,
                       "username":  self.account_name, "name":  self.account_name +
                       "_admin", "projects_limit": 9999, "confirm": "false"}
            payload_json = json.dumps(payload)
            headers = {'Content-Type': 'application/json',
                       'PRIVATE-TOKEN': self.gitlab_token}
            response = requests.post(
                url, data=payload_json, headers=headers, timeout=600, verify=False)

            if response.status_code != 201:
                raise ValueError(str(response.status_code) + ' ' + response.reason +
                                 '. ' + str(response._content).translate(None, '{"}') + '. ' + url)
            self.gitlab_account_user = json.loads(response.text)
            self.handleLogs("Called url :" + url +
                            " Response:" + str(self.gitlab_account_user))

            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "create_git_user_for_account:" 
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def create_git_group_for_account(self, **kwargs):
        url =None
        try:
            print "create new gitlab group for account"
            start_time = time.time()
            self.UpdateStepStartTime()
            url= self.master_git_lab_url + 'groups/'
            payload = {"name": self.account_name + "_group", "path": self.account_name + "_group",
                       "description": "GSS value pack account group for " + self.account_name, "visibility_level": "10"}
            headers = {'Content-Type': 'application/json',
                       'PRIVATE-TOKEN': self.gitlab_token}
            response = requests.post(url, data=json.dumps(
                payload), headers=headers, timeout=600, verify=False)
            if response.status_code != 201:
                raise ValueError(str(response.status_code) + ' ' + response.reason +
                                 '. ' + str(response._content).translate(None, '{"}') + '. ' + url)

            self.gitlab_group = json.loads(response.text)
            self.handleLogs("Called url :" + url +
                            " Response:" + str(self.gitlab_group))

            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "create_git_group_for_account:"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def assign_account_git_user_to_group(self, **kwargs):
        url = None
        try:
            print "assign_account_git_user_to_group"
            start_time = time.time()
            self.UpdateStepStartTime()
            url = self.master_git_lab_url + 'groups/' + \
               self.account_name + "_group" + '/members'
            payload = {"id": self.account_name + "_group",
                       "user_id": self.gitlab_account_user["id"], "access_level": "50"}

            headers = {'Content-Type': 'application/json',
                       'PRIVATE-TOKEN': self.gitlab_token}
            response = requests.post(url, data=json.dumps(
                payload), headers=headers, timeout=600, verify=False)
            self.handleLogs("Called url :" + url +
                            " Response:" + str(response))
            if response.status_code != 201:
                raise ValueError(str(response.status_code) + ' ' + response.reason +
                                 '. ' + str(response._content).translate(None, '{"}') + '. ' + url)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "assign_account_git_user_to_group:"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def create_alias(self):
        pass

    def copy_docker_config_file(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            dock_ver = getDockerVersion(**kwargs)
            self.handleLogs("Docker Version :" + str(dock_ver))
            ver = dock_ver.stdout.split(',')[0]

            print "*** host name " + self.MachineDetails["host"]
            print "*** " + dock_ver.stdout
            if ver.split('.')[0] == '1' and ver.split('.')[1] > '10':

                docker_config_file = self.local_dpm_docker_files_path + "/docker"
                reply = copyToRemote(docker_config_file,
                                     "/etc/sysconfig", **kwargs)
                self.handleLogs("Docker Config File Copy :" + str(reply))
                reply = dockerAddPermission(**kwargs)
                self.handleLogs("Docker Add Permission :" + str(reply))
                reply = dockerCreateFile(**kwargs)
                self.handleLogs("Docker Create File:" + str(reply))
                reply = copyToRemote(self.local_dpm_docker_files_path +
                                     "http-proxy.conf", "/etc/systemd/system/docker.service.d/http-proxy.conf", **kwargs)
                self.handleLogs("Docker Config File Copy:" + str(reply))
                reply = dockerDeamonReload(**kwargs)
                self.handleLogs("Docker Deamon Reload:" + str(reply))
                reply = dockerRestart(**kwargs)
                self.handleLogs("Docker Restart:" + str(reply))
            else:
                print "*** in else "

                docker_config_file = self.local_dpm_docker_files_path + "/docker"
                reply = copyToRemote(docker_config_file,
                                     "/etc/sysconfig", **kwargs)
                self.handleLogs("Docker Config File Copy :" + str(reply))
                reply = dockerAddPermission(**kwargs)
                self.handleLogs("Docker Add Permission :" + str(reply))
                reply = dockerRestart(**kwargs)
                self.handleLogs("Docker Restart:" + str(reply))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "copy_docker_config_file:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def copy_docker_yml_file(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            docker_yml_file = self.local_dpm_docker_files_path + "/docker-compose.yml"
            remote_docker_yml_file = self.remote_vp_home_path + "/docker-compose.yml"
            reply = copyToRemote(
                docker_yml_file, self.remote_vp_home_path, **kwargs)
            reply = replaceTextInFile(
                remote_docker_yml_file, "jenkins_version",str(self.jenkins_version), **kwargs)
            reply = replaceTextInFile(
                remote_docker_yml_file, "nexus_version",str(self.target_artifact_auth_repo_type_version), **kwargs)
            self.handleLogs("Docker copy yml file:" + str(reply))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "copy_docker_yml_file:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def copy_jenkins_files(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            jenkins_folder = os.path.join(
                self.local_dpm_docker_files_path, "jenkins_v"+str(self.jenkins_version))
            for file in os.listdir(jenkins_folder):
                reply = copyToRemote(
                    jenkins_folder, self.remote_jenkins_home_path, **kwargs)
                self.handleLogs("Jenkins copy files:" + str(reply))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "copy_jenkins_files:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def copy_ssl_files(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            ssl_folder = self.local_dpm_ssl_files_path
            for file in os.listdir(ssl_folder):
                reply = copyToRemote(
                    ssl_folder + file, self.remote_dpm_ssl_path, **kwargs)
                self.handleLogs("SSl copy files:" + str(reply))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "copy_ssl_files:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)
        
    def copy_plugin_files(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            plugins_folder = self.local_dpm_plugins_files_path
            for directory in plugin_directories_to_be_copied:
                for file in os.listdir(os.path.normpath(os.path.join(plugins_folder,directory))):
                    reply = copyToRemote(
                        os.path.normpath(os.path.join(plugins_folder,directory)) +"/"+file, self.remote_dpm_plugins_path+directory+"/", **kwargs)
                    self.handleLogs("Plugin copy files:" + str(reply))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "copy_plugin_files:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)    

    def update_jenkins_files(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            source_job_folder = self.remote_jenkins_job_path + self.jenkins_job_name
            destination_job_folder = self.remote_jenkins_job_path + self.currentToolDetails.get(
                "name") + "-" + self.currentVersionDetails.get("gitlab_branch")  # Toolname_<version_number>
            reply = copyDirectorywithNewName(
                source_job_folder, destination_job_folder, **kwargs)
            self.handleLogs(str(reply))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "update_jenkins_files:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def copy_nexus_files(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            if self.target_artifact_auth_repo_type == "nexus2":
                self.remote_nexus_home_path = self.remote_vp_home_path +"nexus/" # referred from docker-compose.yml
            elif self.target_artifact_auth_repo_type == "nexus3":
                self.remote_nexus_home_path = self.remote_vp_home_path +"nexus3/" # referred from docker-compose.yml
            else:
                raise Exception ("Unsupported repository type")    
            nexus_zip = self.local_dpm_docker_files_path + \
                os.sep + self.target_artifact_auth_repo_type.lower() + os.sep + "nexus.zip"
            reply = copyToRemote(
                nexus_zip, self.remote_nexus_home_path, **kwargs)
            self.handleLogs("Nexus Copy Files:" + str(reply))
            reply = unzipNexus(self.remote_nexus_home_path, **kwargs)
            self.handleLogs("Nexus Unzip Files:" + str(reply))
            nexusAddPermission(self.remote_nexus_home_path, **kwargs)
            self.handleLogs("Nexus Add Permission:" + str(reply))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "copy_nexus_config_file:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def install_docker_containers(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            machine_executables = ''
            reply = install_docker_containers(
                self.remote_vp_home_path, **kwargs)
            self.handleLogs("Starting to pull docker images")
            print "There is need of delay when the containers get installed. So, sleeping"
            self.handleLogs(
                "There is need of delay when the containers get installed. So, sleeping")
            time.sleep(self.timeToSleep)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "install_docker_containers:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def update_init_d_file(self):
        pass

    def clone_tools(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            print "Starting cloning tools" + self.CLONE_TYPE + " ---"
            self.handleLogs("Starting cloning tools" +
                            self.CLONE_TYPE + " ---")

            self.executeCloneToolSteps(**kwargs)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
            print "Ending cloning tools" + self.CLONE_TYPE + " ---"
            self.handleLogs("Ending cloning tools" + self.CLONE_TYPE + " ---")
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "clone_tools:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def import_tools(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            print "Starting cloning import tools"
            self.handleLogs("Starting cloning import tools")
            self.executeCloneToolSteps(**kwargs)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
            print "Ending cloning import tools"
            self.handleLogs("Ending cloning import tools")
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "import_tools:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def update_tools(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            self.handleLogs("Starting cloning update tools")
            print "Starting cloning update tools"
            self.executeCloneToolSteps(**kwargs)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
            print "Ending cloning update tools"
            self.handleLogs("Ending cloning update tools")
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "update_tools:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

#     def restart_docker_containers(self):
#         try:
#             start_time = time.time()
#             self.UpdateStepStartTime()
#             machine_executables = ''
#             with settings(host_string=self.MachineDetails["username"] + "@" +
#                           self.MachineDetails["host"], password=self.MachineDetails["password"], shell="" if self.MachineDetails.get("shell_type") is None else self.MachineDetails.get("shell_type")):
#                 reply = dockerComposeRestart()
#                 self.handleLogs("Restart Docker Containers:" + str(reply))
#             print "There is need of delay when the containers get restarted. So, sleeping"
#             self.handleLogs(
#                 "There is need of delay when the containers get restarted. So, sleeping")
#             time.sleep(self.timeToSleep)
#             end_time = time.time()
#             self.UpdateStepEndTime(end_time - start_time)
#         except Exception as e:  # catch *all* exceptions
#             self.ErrFlag = 1
#             self.status_message = "restart_docker_containers:" + str(e)
#             print self.status_message
#             self.UpdateStepStatus("Failed", self.status_message)
#             raise ValueError(self.status_message)

    def restart_docker_jenkins(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            reply = restart_docker_jenkins(**kwargs)
            self.handleLogs("Restart Jenkins Containers:" + str(reply))
            print "There is need of delay when the containers get restarted. So, sleeping"
            self.handleLogs(
                "There is need of delay when the containers get restarted. So, sleeping")
            time.sleep(self.timeToSleep)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "restart_docker_jenkins:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def add_into_distribution(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            machine_already_found_and_matched=False
            NewDistributionRequest = {}
            NewDistributionRequest["machine_id"] = self.CloneRequestDetails.get(
                "machine_id")
            if self.MachineDetails.get("status") == '1':
                NewDistributionRequest["status"] = "on"
            else:
                self.status_message = "Machine Status is unknown!"
                self.handleLogs(self.status_message)
                raise ValueError(self.status_message)
            NewDistributionRequest["host"] = self.MachineDetails.get("host")
            if  self.distributionDB.GetDistributionMachineRequestByHost(str(self.MachineDetails.get("host"))).count() >0:
                pre_machine_details_list = self.distributionDB.GetDistributionMachineRequestByHost(
                    str(self.MachineDetails.get("host")))
                if pre_machine_details_list.count() >0:
                    for pre_machine_details in pre_machine_details_list:
                        pre_machine_id = pre_machine_details.get("machine_id")
                        if pre_machine_id == str(self.CloneRequestDetails.get("machine_id")):
                            self.status_message = "Already added " + NewDistributionRequest.get(
                                "machine_id") + " for" + NewDistributionRequest.get("host") + " to distribution"
                            self.handleLogs(self.status_message)
                            machine_already_found_and_matched =True
                    
                    if not  machine_already_found_and_matched:       
                        raise ValueError("Duplicate Machine: was found for host: " + self.MachineDetails.get("host"))
            else:
                inserted_id = self.distributionDB.AddDistributionMachineRequests(
                    NewDistributionRequest)
                self.status_message ="New Machine added in Distribution: "+str(inserted_id)
                self.handleLogs(self.status_message)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "add_into_distribution:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def copy_default_files(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateStepStartTime()
            machine_executables = ''
            logos_path = self.local_dpm_logos_path
            onlyfiles = [f for f in os.listdir(logos_path) if os.path.isfile(
                os.path.join(logos_path, f)) if "default" in str(f).lower()]
            for f in onlyfiles:
                reply = copyToRemote(os.path.join(
                    logos_path, f), self.remote_dpm_logos_path, **kwargs)
                self.handleLogs("Logo Default copy file:" +
                                str(f) + " result:" + str(reply))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "copy_default_files:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    #*************************************************************************
    #**************************************** Tool steps *********************
    #*************************************************************************
    #
    # Methods creates a new branch in master repository for specific tool.
    #
    # Reference for used GitLab REST API -
    # http://doc.gitlab.com/ce/api/branches.html#create-repository-branch
# 
#     def grant_perm_to_git_tool_folder(self):
#         try:
#             start_time = time.time()
#             self.UpdateToolStepStartTime()
#             with settings(host_string=self.MachineDetails["username"] + "@" +
#                           self.MachineDetails["host"], password=self.MachineDetails["password"], shell="" if self.MachineDetails.get("shell_type") is None else self.MachineDetails.get("shell_type")):
#                 createFolder(self.remote_git_home_path +
#                              self.tool_git_folder_name)
#                 grantFolderPermissions(
#                     "777", self.remote_git_home_path + self.tool_git_folder_name)
#             end_time = time.time()
#             self.UpdateToolStepEndTime(end_time - start_time)
#         except Exception as e:  # catch *all* exceptions
#             self.ErrFlag = 1
#             self.status_message = "grant_perm_to_git_tool_folder:" + str(e)
#             print self.status_message
#             self.UpdateToolStepStatus("Failed", self.status_message)
#            raise ValueError(self.status_message)

    def account_user_authntication(self):
        url=None
        try:
            print "account_user_authntication"
            url = self.master_git_lab_url + 'session/'
            # if self.account_name == 'vpadmin':
            payload = {"login": self.account_name,
                       "password": self.account_gitlab_password}
            # else:
            #    payload= {"login": self.account_group_name , "password": self.account_group_pass }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(
                payload), headers=headers, timeout=600, verify=False)
            if response.status_code != 201:
                raise ValueError(
                    str(response.status_code) + ' ' + response.reason + '. ' +
                    str(response._content).translate(None, '{"}') + '. ' + url)
            self.gitlab_account_user = json.loads(response.text)
        except Exception as e:
            self.status_message = "account_user_authntication:"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            raise ValueError(self.status_message)
    def get_group_details(self):
        url = None
        try:
            url=self.master_git_lab_url + 'groups?search=' + self.account_name + "_group"
            headers = {'Content-Type': 'application/json',
                       'PRIVATE-TOKEN': self.gitlab_token}
            response = requests.get(
                url, headers=headers, timeout=120, verify=False)
            if response.status_code != 200:
                msg = str(response.status_code) + ' ' + response.reason + '. ' + \
                    str(response._content).translate(
                        None, '{"}') + '. ' + url
                raise ValueError(msg)
            groups = json.loads(response._content)
            self.git_lab_groups = {}
            for group in groups:
                self.git_lab_groups[group["name"]] = group
            self.handleLogs(
                "get_git_group_details_for_account:Response :" + str(self.git_lab_groups))
            if self.account_name + "_group" not in self.git_lab_groups.keys():
                raise ValueError(
                    "Group details were not found for group: " + self.account_name + "_group")
            else:
                self.git_lab_group = self.git_lab_groups[self.account_name + "_group"]
        except Exception as e:
            self.status_message = "get_group_details:"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            raise ValueError(self.status_message)

    def fork_project_with_account_group(self, **kwargs):
        url=None
        try:
            print "fork project with account group"
            start_time = time.time()
            self.UpdateToolStepStartTime()
            self.account_user_authntication()
            self.git_lab_details = self.git_lab_project[self.tool_git_folder_name]
            print str(self.git_lab_details)

            # GET GROUP DETAILS
            self.get_group_details()
            print str(self.git_lab_group)

            # PERFORM FORK FROM VPGROUP
            url = self.master_git_lab_url + 'projects/fork/' + \
                str(self.git_lab_details['id'])
            headers = {'Content-Type': 'application/json',
                       'PRIVATE-TOKEN': str(self.gitlab_account_user["private_token"])}
            response = requests.post(
                url, headers=headers, timeout=600, verify=False)
            if response.status_code != 201:
                raise ValueError(str(response.status_code) + ' ' + response.reason +
                                 '. ' + str(response._content).translate(None, '{"}') + '. ' + url)
            self.handleLogs("Calling url:" + url +
                            " response was:" + str(response))
            forked_project_data = json.loads(response._content)

            # wait_for_git_changes_on_account
            print "there is need of delay after forking the project . So, sleeping"
            self.handleLogs(
                "there is need of delay after forking the project . So, sleeping")
            time.sleep(self.timeToSleep)

            # SHARE THIS FORKED PROJECT WITH GROUP
            url = self.master_git_lab_url + 'projects/' + \
                str(forked_project_data["id"]) + '/share'
            payload = {"group_id": str(
                self.git_lab_group["id"]), "group_access": "30"}
            response = requests.post(url, data=json.dumps(
                payload), headers=headers, timeout=600, verify=False)
            if response.status_code != 201:
                raise ValueError(str(response.status_code) + ' ' + response.reason +
                                 '. ' + str(response._content).translate(None, '{"}') + '. ' + url)
            self.handleLogs("Calling url:" + url +
                            " response was:" + str(response))

            # wait_for_git_changes_on_account
            print "there is need of delay after sharing. So, sleeping"
            self.handleLogs(
                "there is need of delay after sharing. So, sleeping")
            time.sleep(self.timeToSleep)

            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "fork project with account group:"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def clone_repository_to_git(self, **kwargs):
        try:
            global forked_tool_repo
            account_tool_repo = copy.deepcopy(self.gitlab_repo)
            forked_tool_repo = account_tool_repo.replace(
                'vpgroup', self.account_name)
            forked_tool_repo = forked_tool_repo.replace(
                "://", "://" + self.account_name + ":" + self.account_gitlab_password + "@", 1)
            start_time = time.time()
            self.UpdateToolStepStartTime()
            reply = cloneRepository(
                self.remote_git_home_path, forked_tool_repo, **kwargs)
            self.handleLogs("Clone Git Repository :" + str(reply))
            gitCredentialStore(self.remote_git_home_path +
                               "/" + self.tool_git_folder_name, **kwargs)
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "clone_repository_to_git:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

# updated
# should look like this while creating any upstream
# forked_upstream_repo =
# http://comc_test121212:vpadmin123@illin4489.corp.amdocs.com/vpgroup/stuck_order_error_report.git
    def create_upstream_to_original_rep(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            forked_upstream_tool_repo = copy.deepcopy(self.gitlab_repo)
            forked_upstream_tool_repo = forked_upstream_tool_repo.replace(
                "://", "://" + self.account_name + ":" + self.account_gitlab_password + "@", 1)
            reply = createUpstream(
                self.remote_git_home_path + self.tool_git_folder_name,
                forked_upstream_tool_repo, **kwargs)
            self.handleLogs("Clone Git create upstream :" + str(reply))
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "create_upstream_to_original_rep:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

# git fetch upstream command is enough to fetch the tool
    def fetch_upstream_to_original_rep(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            reply = fetchUpstream(
                self.remote_git_home_path + "/" + self.tool_git_folder_name, **kwargs)
            self.handleLogs(str(reply))
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "fetch_upstream_to_original_rep:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def jenkins_copy_job(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            reply = createFolder(
                self.remote_jenkins_job_path + self.jenkins_job_name, **kwargs)
            reply = copyToRemote(
                self.local_jenkins_job_path + self.jenkins_job_name,
                self.remote_jenkins_job_path + self.jenkins_job_name, **kwargs)
            self.handleLogs("Jenkins copy files" + str(reply))
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            # self.ErrFlag = 1
            self.status_message = "jenkins_copy_job:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Done with errors", self.status_message)
#             raise ValueError(self.status_message)

#     def create_jenkins_slave(self):
#         try:
#             start_time = time.time()
#             self.UpdateToolStepStartTime()
#             with settings(host_string=self.MachineDetails["username"] + "@" +
#                           self.MachineDetails["host"], password=self.MachineDetails["password"], shell="" if self.MachineDetails.get("shell_type") is None else self.MachineDetails.get("shell_type")):
#                 reply = copyToRemote(
#                     self.local_jenkins_job_path + self.jenkins_job_name, self.remote_jenkins_job_path)
#                 self.handleLogs("Jenkins Create Slave" + str(reply))
#             end_time = time.time()
#             self.UpdateToolStepEndTime(end_time - start_time)
#         except Exception as e:  # catch *all* exceptions
#             # self.ErrFlag = 1
#             self.status_message = "create_jenkins_slave:" + str(e)
#             print self.status_message
#             self.UpdateToolStepStatus("Done with errors", self.status_message)
            # raise ValueError(self.status_message)

# Use this function to remove un wanted fields from json, cursor, by
# giving 4 arguments of lists
    def make_json_serializable(self, data, list_to_skip, list_having_cursor, list_to_pop):
        copyToolDetails = {}
        for key, val in data.iteritems():
            nestdict = {}
            if isinstance(val, dict):
                for nestkey, nestval in val.iteritems():
                    if nestkey in list_to_skip:
                        pass
                    elif nestkey in list_having_cursor:
                        cursor_arr = []
                        if val.get(list_having_cursor) is not None:
                            for cursor in val.get(list_having_cursor):
                                for pop_item in list_to_pop:
                                    cursor.pop(pop_item, None)
                                cursor_arr.append(cursor)
                            nestdict[nestkey] = cursor_arr
                    else:
                        nestdict[nestkey] = nestval
                copyToolDetails[key] = nestdict
            else:
                if key not in list_to_pop:
                    copyToolDetails[key] = val
        return copyToolDetails

    def clone_tool_to_account_dpm(self, **kwargs):
        url=None
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            url = dpm_url_prefix + self.remote_dpm_url + '/tool/add'
            ''' JSON serializable issue because of ObjectID so removed '''
            copyToolDetails = {}
            print self.currentToolDetails
            list_to_pass = ('_id')
            list_having_cursor = 'build'  # ,'document','deployment_field',media_file, )
            list_to_pop = ('version_id', '_id', 'tool_id','is_tool_cloneable','artifacts_only')
            copyToolDetails = self.make_json_serializable(
                self.currentToolDetails, list_to_pass, list_having_cursor, list_to_pop)
            '''version gitlab,jenkins details not to be shared with account'''

            # Update gitlab_repo
            copyToolDetails["version"]["gitlab_repo"] = self.tool_git_folder_name
            if copyToolDetails["version"].get("version_date"):
                copyToolDetails["version"]["version_date"] = str(
                    copyToolDetails["version"]["version_date"])

            payload = json.dumps(copyToolDetails, default=json_util.default)
            print payload
            headers = {'Content-Type': 'application/json',
                       'Token': self.get_access_token(), 'verify_tool': 'false'}
            print "start running"
            response = requests.post(
                url, data=payload, headers=headers, timeout=600, verify=False)
            result = json.loads(response.content)
            if response.status_code != 200:
                raise ValueError(str(response.status_code) +
                                 ' ' + result["message"] + ' at ' + url)
            self.handleLogs("Calling url:" + url + " with details :" +
                            str(copyToolDetails) + " response was:" + str(response))
            self.current_new_version_id = result["data"]["version_id"]
            result = self.cloneRequestDB.UpdateToolStepDetails(
                self.id, self.current_step_id, self.current_tool_version_id,
                self.current_tool_step_id, new_version_id=self.current_new_version_id)
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "clone_tool_to_account_dpm:" 
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message            
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def set_tool_dependency(self, **kwargs):
        url=None
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            print self.currentToolDetails
            # CHECK IF TOOL DEPENDENCY EXISTS
            dependent_tools = self.currentToolDetails["version"].get(
                "dependent_tools")
            if dependent_tools and len(dependent_tools) > 0:
                updated_list = []
                for rec in dependent_tools:
                    url = dpm_url_prefix + self.remote_dpm_url + \
                        '/tool/exists/name/' + str(rec.get("tool_name"))
                    headers = {'Content-Type': 'application/json',
                               'Token': self.get_access_token()}
                    response = requests.get(
                        url, headers=headers, timeout=600, verify=False)
                    result = json.loads(response.content)
                    if response.status_code != 200:
                        raise ValueError(str(response.status_code) +
                                         ' Response from target when trying to find _id for tool:' + str(rec.get("tool_name")) + ' ' + result["message"] + ' for url ' + url)
                    self.handleLogs("Calling url:" + url +
                                    " response was:" + str(response))
                    if str(result.get("message")) == "true":
                        try:
                            rec["tool_id"] = str(result["data"]["_id"]["$oid"])
                        except Exception as exp:
                            raise ValueError("Unable to find tool_id for dependent tool: " + str(
                                rec.get("tool_name")) + " in target machine.Error: " + str(exp))
                        try:
                            version_id = None
                            if "all_versions" not in result["data"].keys():
                                raise ValueError("")
                            for version in result["data"]["all_versions"]:
                                if version.get("version_number") == rec.get("version_number") and \
                                        version.get("version_name") == rec.get("version_name"):
                                    version_id = str(version["_id"]["$oid"])
                                    break
                            if not version_id:
                                raise ValueError("")
                            else:
                                rec["version_id"] = version_id
                        except Exception as exp:
                            raise ValueError("Unable to find version_id for dependent tool: " + str(
                                rec.get("tool_name")) + " in target machine.Error: " + str(exp))
                    updated_list.append(rec)
                self.currentToolDetails["dependent_tools"] = updated_list
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.status_message = "set_tool_dependency:"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def update_tool_to_account_dpm(self, **kwargs):
        url=None
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            url = dpm_url_prefix + self.remote_dpm_url + '/tool/update'
            # stuti
            # ##
            print self.currentToolDetails

            copyToolDetails = copy.deepcopy(self.currentToolDetails)

            if copyToolDetails.get("_id"):
                tool_id = str(copyToolDetails["_id"])
            ''' JSON serializable issue because of ObjectID so removed '''
            list_to_skip = ('_id')
            list_having_cursor = 'build'  # ,'document','deployment_field',media_file, )
            list_to_pop = ('version_id', '_id', 'tool_id')
            copyToolDetails = self.make_json_serializable(
                self.currentToolDetails, list_to_skip, list_having_cursor, list_to_pop)
            '''version gitlab,jenkins details not to be shared with account'''

            versionlist = []
            if tool_id is not None:
                all_versions = self.versionsDB.get_all_tool_versions(
                    str(tool_id), True)

            if not all_versions:
                raise ValueError(
                    "No version was found for tool_id :" + str(tool_id))

            for version in all_versions:
                if version.get("_id"):
                    version = self.versionsDB.get_version(
                        str(version.get("_id")), True)
                # Update gitlab_repo
                version["gitlab_repo"] = self.tool_git_folder_name
                if version.get("version_date"):
                    version["version_date"] = str(version["version_date"])

                list_to_skip = ('_id', 'parent_entity_id')
                list_having_cursor = 'build'  # ,'document','deployment_field',media_file, )
                list_to_pop = ('version_id', '_id', 'tool_id')
                if "build" in version.keys():
                    version.pop("build")
                version = self.make_json_serializable(version,
                                                      list_to_skip, list_having_cursor, list_to_pop)
                '''version gitlab,jenkins details not to be shared with account'''
                versionlist.append(version)
            copyToolDetails["version"] = versionlist

            payload = json.dumps(copyToolDetails, default=json_util.default)
            headers = {'Content-Type': 'application/json', 'Token': self.get_access_token()}
            response = requests.put(
                url, data=payload, headers=headers, timeout=600, verify=False)
            result = json.loads(response.content)
            if response.status_code != 200:
                raise ValueError(str(response.status_code) +
                                 ' ' + result["message"] + ' at ' + url)
            self.handleLogs("Calling url:" + url + " with details :" +
                            str(copyToolDetails) + " response was:" + str(response))
            result = self.cloneRequestDB.UpdateToolStepDetails(
                self.id, self.current_step_id, self.current_tool_version_id,
                self.current_tool_step_id, new_version_id=None)  # TODO. HANDLE VERSION ID
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "update_tool_to_account_dpm:" + str(e)
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def jenkins_update_job(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            if self.CLONE_TYPE.lower() in "updatetool".lower():
                job_folder = self.remote_jenkins_job_path + self.currentToolDetails.get(
                    "name") + "_" + self.currentVersionDetails.get("gitlab_branch") + "/"
            else:
                job_folder = self.remote_jenkins_job_path + self.jenkins_job_name + "/"
            print "Job path" + str(job_folder)
            reply = replaceTextInFile(
                job_folder + "config.xml", "<url>", "<!-- <url>", **kwargs)
            self.handleLogs(str(reply))
            reply = replaceTextInFile(
                job_folder + "config.xml", "</url>", "</url> -->", **kwargs)
            self.handleLogs(str(reply))
            reply = replaceTextInFile(job_folder + "config.xml", "<hudson.plugins.git.UserRemoteConfig>",
                                      "<hudson.plugins.git.UserRemoteConfig><url>" + '/git/' + self.tool_git_folder_name + "</url>", **kwargs)
            self.handleLogs(str(reply))
            if self.current_new_version_id:
                if self.CLONE_TYPE.lower() in "updatetool".lower():  # for update tool
                    # NewVersionOnAccountDPM
                    reply = replaceTextInFile(
                        job_folder + "config.xml", "MONGO_VERSION_ID", self.current_new_version_id, **kwargs)
                    self.handleLogs(str(reply))
                else:
                    reply = replaceTextInFile(
                        job_folder + "config.xml", self.current_tool_version_id, self.current_new_version_id, **kwargs)
                    self.handleLogs(str(reply))
            reply = deleteFolder(job_folder + "builds", **kwargs)
            self.handleLogs(str(reply))
            reply = jenkinsUpdateJobLastStep(job_folder, **kwargs)
            self.handleLogs(str(reply))
            if self.current_new_version_id:
                end_time = time.time()
                self.UpdateToolStepEndTime(end_time - start_time)
            else:
                self.status_message = "jenkins_update_job:" + \
                    "New version is not created on the account"
                print self.status_message
                self.UpdateToolStepStatus("Failed", self.status_message)

        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "jenkins_update_job:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def copy_logo_media_files(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            if FileUtils.check_if_exists(self.local_dpm_home_path + os.sep +
                                         self.currentToolDetails["logo"]):
                reply = copyToRemote(self.local_dpm_home_path + self.currentToolDetails["logo"],
                                     self.remote_dpm_home_path + self.currentToolDetails["logo"], **kwargs)
                self.handleLogs(str(reply))
            if FileUtils.check_if_exists(self.local_dpm_home_path +
                                         self.currentToolDetails["thumbnail_logo"]):
                reply = copyToRemote(self.local_dpm_home_path +
                                     self.currentToolDetails["thumbnail_logo"],
                                     self.remote_dpm_home_path + self.currentToolDetails["thumbnail_logo"], **kwargs)
                self.handleLogs(str(reply))
            if self.currentVersionDetails is not None:
                if self.currentVersionDetails.get('media_file') and self.currentVersionDetails["media_file"].has_key('media_files'):
                    for file in self.currentVersionDetails["media_file"]["media_files"]:
                        if FileUtils.check_if_exists(self.local_dpm_home_path + str(
                                file["url"])):
                            reply = copyToRemote(self.local_dpm_home_path + str(
                                file["url"]), self.remote_dpm_home_path + str(file["url"]), **kwargs)
                            self.handleLogs(str(reply))
                        if FileUtils.check_if_exists(self.local_dpm_home_path + str(
                                file["thumbnail_url"])):
                            reply = copyToRemote(self.local_dpm_home_path + str(
                                file["thumbnail_url"]), self.remote_dpm_home_path + str(file["thumbnail_url"]), **kwargs)
                            self.handleLogs(str(reply))
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "copy_logo_media_files:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)
        
    def validate_build_structure_and_data(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()  
            for build in copy.deepcopy(self.currentVersionDetails.get("build",[])):      
                BuildHelperService.validate_build_structure(build)
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "validate_build_structure_and_data:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)
        
    def download_builds(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()  
            download_build_after = None            
            try:                            
                FileUtils.mkdirs([self.temp_artifacts_path], True)
                self.handleLogs("Created artifacts directory to download builds")
                self.handleLogs("Downloading builds at location: "+self.temp_artifacts_path)
                for build in copy.deepcopy(self.currentVersionDetails.get("build",[])):                                                                                    
                    BuildHelperService.download_build_files(build,build.get("parent_entity_id"),self.temp_artifacts_path, download_build_after,None,**kwargs)
            except Exception as e:
                traceback.print_exc()
                self.ErrFlag = 1
                self.status_message = "download_builds:" + str(e)
                print self.status_message
                self.UpdateToolStepStatus("Failed", self.status_message)
                raise ValueError(self.status_message)                            
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "download_builds:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    
    def delete_downloaded_builds(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()  
            try:                            
                shutil.rmtree(self.temp_artifacts_path,True)
                self.handleLogs("Removed directory artifacts: "+self.temp_artifacts_path)                
            except Exception as e:
                traceback.print_exc()
                self.ErrFlag = 1
                self.status_message = "download_builds:" + str(e)
                print self.status_message
                self.UpdateToolStepStatus("Failed", self.status_message)
                raise ValueError(self.status_message)                            
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "download_builds:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)
                                
    
    def get_access_token(self):   
        url=None
        try:     
            passwords = [default_admin_password,self.target_dpm_password]
            url = dpm_url_prefix + self.remote_dpm_url + '/user/auth'
            headers = {'Content-Type': 'application/json'}
            print "*** authenticate to account DPM"
            for password in passwords:
                payload = {"user": self.target_dpm_user, "password": password}
                response = requests.post(url, data=json.dumps(
                    payload), headers=headers, timeout=600, verify=False)
                if response.status_code == 200:
                    result = json.loads(response.content)
                    return str(result["data"]["Token"])
            raise ValueError(' Unable to get token from target machine')
        except Exception as e:
            self.status_message="get_access_token"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message
            raise ValueError(self.status_message)
        
    
    def get_target_version_details(self,tool_name,version_name,version_number):
        url=None
        try:
            version_id = None
            repository_to_use = None
            self.handleLogs("Trying to get target version_id of tool with name: "+tool_name+" version name: "+version_name+" version number: "+version_number)
            url = dpm_url_prefix + self.remote_dpm_url + \
                '/tool/exists/name/' + str(tool_name)
            headers = {'Content-Type': 'application/json',
                       'Token': self.get_access_token()}
            response = requests.get(
                url, headers=headers, timeout=600, verify=False)
            result = json.loads(response.content)
            if response.status_code != 200:
                raise ValueError(str(response.status_code) +
                                 ' Response from target for tool:' + str(tool_name)+ ' ' + result["message"] + ' for url ' + url)
            self.handleLogs("Calling url:" + url +
                            " response was:" + str(response))
            if str(result.get("message")) == "true":
                if "all_versions" not in result["data"].keys():
                    raise ValueError("required attribute all_versions was not found in tool details")
                for version in result["data"]["all_versions"]:
                    if version.get("version_number") == version_number and \
                            version.get("version_name") == version_name:
                        version_id = str(version["_id"]["$oid"])
                        repository_to_use = str(version["repository_to_use"])
                        break
            if not version_id:
                raise ValueError("no version was found with tool name: "+tool_name+" version name: "+version_name+" version number: "+version_number)
            return version_id,repository_to_use       
        except Exception as e:
            self.status_message="get_target_version_details"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message       
            raise ValueError(self.status_message)
   
    def get_target_repository_details(self,repository_to_use):
        url=None
        try:
            self.handleLogs("Trying to get target machine repository details")
            url = dpm_url_prefix + self.remote_dpm_url + \
                '/repository/view/name/' + repository_to_use
            headers = {'Content-Type': 'application/json',
                       'Token': self.get_access_token()}
            response = requests.get(
                url, headers=headers, timeout=600, verify=False)
            result = json.loads(response.content)
            if response.status_code != 200:
                raise ValueError(str(response.status_code) +
                                 ' Response from target for repository:' + str(repository_to_use)+ ' ' + result["message"] + ' for url ' + url)
            self.handleLogs("Calling url:" + url +
                            " response was:" + str(response))
            return result.get("data")       
        except Exception as e:
            self.status_message="get_target_repository_details"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message       
            raise ValueError(self.status_message)
             
    def create_repo_and_upload_artifact(self,build,target_repository_to_use_details):
        relative_path = build.get("additional_info").get("relative_path")
        fileName = build.get("additional_info").get("file_name")
        full_file_path = join(self.temp_artifacts_path, relative_path)
        target_repository_to_use_details["upload_protocol"]="http"
        deployer_module="Plugins.repositoryPlugins."+str(target_repository_to_use_details.get("handler"))
        class_obj=CustomClassLoaderService.get_class(deployer_module)
        method = getattr(class_obj(target_repository_to_use_details),"trnx_handler") # MEDHOD NAME
        keyargs={"transaction_type":"upload",
                 "build_details":build,
                 "file_to_upload":full_file_path + '/' + fileName,
                 "directory_to_import_from":full_file_path
                }
        method(**keyargs)
        
        
    # For nexus2 file_path : http://vptestind01:8081/content/repositories/vp_builds/elastic/logstash/ga_5_0_1/logstash-ga_5_0_1-81.zip
    # For newxus3 file_path: http://vptestind01:8081/repository/vp_builds/elastic/logstash/ga_5_0_1/logstash-ga_5_0_1-81.zip   
    def generate_file_path_for_nexus(self,build,base_url):
        fileName = build.get("additional_info").get("file_name")
        relative_path = build.get("additional_info").get("relative_path")
        build["file_path"] = join(base_url,relative_path, fileName).replace("\\", '/')
                            
       
    def update_build_information(self, **kwargs):
        url=None
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            target_version_id , repository_to_use =self.get_target_version_details(self.currentToolDetails.get("name"),\
                        self.currentVersionDetails.get("version_name"),self.currentVersionDetails.get("version_number"))
            for build in copy.deepcopy(self.currentVersionDetails.get("build",[])):
                
                # ADD BUILD DETAILS
                self.handleLogs("Trying to add build no: "+str(build.get("build_number")))
                build["parent_entity_id"]=target_version_id
                if build.get("build_date"):
                    build["build_date"]=str(build["build_date"])
                if build.get("_id"):    
                    build.pop("_id")       
                                    
                #GET TARGET NEXUS DETAILS
                target_repository_to_use_details= self.get_target_repository_details(repository_to_use)
                self.handleLogs("Replacing "+default_nexus_container_name + "target repository details with "+ self.remote_host ) 
                target_repository_to_use_details=HelperServices.replace_hostname_with_actual(target_repository_to_use_details,default_nexus_container_name, self.remote_host)
                
                # UPLOAD ARTIFACT
                
                self.generate_file_path_for_nexus(build, target_repository_to_use_details.get("file_path_url"))
                self.handleLogs("Trying to upload build no: "+str(build.get("build_number"))) 
                self.create_repo_and_upload_artifact(build,target_repository_to_use_details)
                self.handleLogs("Build no: "+str(build.get("build_number"))+" was uploaded.File Path: "+build["file_path"])
                
                self.handleLogs("Replacing "+self.remote_host + "target repository details with "+ default_nexus_container_name ) 
                self.generate_file_path_for_nexus(build, HelperServices.replace_hostname_with_actual(target_repository_to_use_details.get("file_path_url"), \
                                                self.remote_host, default_nexus_container_name))
                payload = json.dumps(build, default=json_util.default)
                headers = {'Content-Type': 'application/json',
                           'Token': self.get_access_token()}
                url = dpm_url_prefix + self.remote_dpm_url + '/versions/build/add'
                response = requests.post(
                    url, data=payload, headers=headers, timeout=600, verify=False)
                result = json.loads(response.content)
                if response.status_code != 200:
                    raise ValueError("Error while adding build:"+str(build.get("build_number"))+str(response.status_code) +
                                     ' ' + result["message"] + ' for url ' + url)
                self.handleLogs("Build no was added: "+str(build.get("build_number")))    
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.status_message = "update_build_information:"
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message       
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)
        
        
# To udpate the System info and dpm on the accounts
    def change_account_name(self, **kwargs):
        url=None
        try:
            print " change_account_name started "
            start_time = time.time()
            self.UpdateStepStartTime()
            details = {}
            details["old_account_name"] = "Test"
            details["new_account_name"] = self.CloneRequestDetails["account_name"]
            url = dpm_url_prefix + self.remote_dpm_url + '/account/update/name'
            # need to add a secret key for below header
            headers = {'Content-Type': 'application/json', 'Token': self.get_access_token()}

            print json.dumps(details)
            response = requests.post(url, data=json.dumps(
                details), headers=headers, timeout=200, verify=False)
            if response.status_code != 200:
                raise ValueError(str(response.status_code) + ' ' + response.reason +
                                 '. ' + str(response._content).translate(None, '{"}') + '. ' + url)
            self.handleLogs("Calling url:" + url + " with details :" +
                            str(details) + " response was:" + str(response))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)

            print " change_account_name ended  "
        except Exception as e:  # catch *all* exceptions
            self.status_message = "change_account_name:" + str(e)
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    # To udpate the System info and dpm on the accounts
    def generate_system_details(self, **kwargs):
        url=None
        try:
            print " generate_system_details started "
            host = self.systemDetail.get("hostname")
            port = self.systemDetail.get("port")
            ip = self.systemDetail.get("ip")
            start_time = time.time()
            self.UpdateStepStartTime()
            sys_details = {}
            sys_details["created_by"] = "Master"
            sys_details["master_ip"] = ip
            sys_details["master_host"] = host
            sys_details["master_port"] = port
            sys_details["ip"] = self.MachineDetails["ip"]
            sys_details["hostname"] = self.MachineDetails["host"]
            sys_details["account_name"] = self.CloneRequestDetails["account_name"]
            url = dpm_url_prefix + self.remote_dpm_url + '/systemdetails/add'
            # need to add a secret key for below header
            headers = {'Content-Type': 'application/json', 'Token': self.get_access_token()}
            response = requests.post(url, data=json.dumps(
                sys_details), headers=headers, timeout=200, verify=False)
            if response.status_code != 200:
                raise ValueError(str(response.status_code) + ' ' + response.reason +
                                 '. ' + str(response._content).translate(None, '{"}') + '. ' + url)
            self.handleLogs("Calling url:" + url + " with details :" +
                            str(sys_details) + " response was:" + str(response))
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
            print " generate_system_details ended  "
        except Exception as e:  # catch *all* exceptions
            self.status_message = "generate_system_details:" + str(e)
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message       
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def schedule_cleaner(self, **kwargs):
        try:
            print " schedule_cleaner started "
            start_time = time.time()
            self.UpdateStepStartTime()
            cleaner_file = self.local_dpm_cleaner_files_path + "docker-cleaner.sh"
            reply = copyToRemote(
                cleaner_file, self.remote_vp_home_path, **kwargs)
            self.handleLogs("Schedule Cleaner Script:" + str(reply))
            scheduleCleaner(**kwargs)
            end_time = time.time()
            self.UpdateStepEndTime(end_time - start_time)
            print " generate_system_details ended  "
        except Exception as e:  # catch *all* exceptions
            self.status_message = "schedule_cleaner:" + str(e)
            print self.status_message
            self.UpdateStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def get_account_group_name_and_user(self, **kwargs):
        try:
            print "account group name and user started"
            start_time = time.time()
            self.UpdateToolStepStartTime()
            self.account_login_name = self.account_name + "_admin"
            self.account_group_name = self.account_login_name
            self.account_group_pass = self.account_gitlab_password
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
            print " get_tool_data ended  "
        except Exception as e:  # catch *all* exceptions
            self.status_message = "account group name and user:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def get_tool_data(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            self.current_tool_data = {}
            # Get all details of version with media, documents etc
            version_data = self.versionsDB.get_version(
                self.current_tool_version_id, True)
            current_tool_id = version_data["tool_id"]
            self.current_tool_data = self.toolDB.get_tool_by_id(
                current_tool_id, False)
            self.current_tool_data["version"] = version_data
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.status_message = "get tool data:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def validate_jenkins_job(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            if not os.path.exists(self.local_jenkins_job_path + self.jenkins_job_name):
                raise Exception("Jenkins job: " + self.jenkins_job_name +
                                " does not exists at :" + self.local_jenkins_job_path)
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.status_message = "validate_jenkins_job:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def validate_git_project(self, **kwargs):
        try:
            start_time = time.time()
            self.UpdateToolStepStartTime()
            self.git_lab_details = self.git_lab_project[self.tool_git_folder_name]
            if not self.git_lab_details:
                raise ValueError(
                    "Git project: " + self.tool_git_folder_name + " does not exist in repository")
            if str(self.git_lab_details.get("public")).lower() <> "true":
                raise ValueError(
                    "Git project: " + self.tool_git_folder_name + " does not have a public access")
            end_time = time.time()
            self.UpdateToolStepEndTime(end_time - start_time)
        except Exception as e:  # catch *all* exceptions
            self.status_message = "validate_git_project:" + str(e)
            print self.status_message
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)

    def update_distribution_sync_data_in_account_dpm(self, **kwargs):
        url=None
        try:
            print "update_distribution_sync_data_in_account_dpm started"
            start_time = time.time()
            self.UpdateToolStepStartTime()
            end_time = time.time()
            url = dpm_url_prefix + self.remote_dpm_url + \
                '/clonerequest/distribute/update/status'            
            distribution_sync_data = {}
            distribution_sync_data["tool_name"] = str(
                self.currentToolDetails.get("name"))
            payload = json.dumps(distribution_sync_data,
                                 default=json_util.default)
            headers = {'Content-Type': 'application/json', 'Token': self.get_access_token()}
            response = requests.post(
                url, data=payload, headers=headers, timeout=600, verify=False)
            if response.status_code != 200:
                raise ValueError(str(response.status_code) +
                                 ' ' + response["message"] + ' at ' + url)
            result = json.loads(response.content)
            self.handleLogs("Calling url:" + url + " with details :" +
                            str(distribution_sync_data) + " response was:" + str(result))
            self.UpdateToolStepEndTime(end_time - start_time)
            print " update_distribution_sync_data_in_account_dpm ended  "

        except Exception as e:  # catch *all* exceptions
            self.status_message = "update_distribution_sync_data_in_account_dpm:" + \
                str(e)
            if type(e) in [ConnectionError, ReadTimeout]:
                print self.status_message + str(e)
                self.status_message = self.status_message + "Unable to connect to URL: "+url
            else:
                self.status_message = self.status_message + str(e)
            print self.status_message       
            self.UpdateToolStepStatus("Failed", self.status_message)
            raise ValueError(self.status_message)
