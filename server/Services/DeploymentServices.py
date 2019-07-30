from datetime import datetime
import logging
import traceback
import shutil
import time
import os
import subprocess
import copy

from autologging import logged
from concurrent.futures import ThreadPoolExecutor, wait
from fabfile import copy_dir_to_remote, getExecutables, runCommand, getExecutables_rpm, getExecutablesversion, getExecutablesParversion, getSize,copyToRemote

from DBUtil import DeploymentRequest, DeploymentRequestGroup, Versions, Build, Machine, ToolsOnMachine, Tool, PreRequisites, Users, DeploymentUnit,State,SystemDetails, Config
import Mailer
from Services import RemoteAuthenticationService,BuildHelperService,CustomClassLoaderService
from SingeltonServicesManager import plugin_manager
from settings import mongodb, current_path


@logged(logging.getLogger("DeploymentServices"))
class Deployment():

    deployment_steps = (
        'run_pre_deployment_plugins',
        'verify_tool_dependencies',
        # 'set_env_variables', CALLED FROM execute_packages
        'change_log_type_to_deploy_process',
        'verify_prerequisites',
        'create_directories',
        'transfer_packages',
        'extract_packages',
        # 'set_prev_env_variables', CALLED FROM execute_packages
        'execute_packages',        
        'save_deployment_in_db',
        'clean_pakages',
        'change_log_type_post_deploy_process',
        'run_post_deployment_plugins'
    )

    preDeploymentsteps = (
        'validate_mandatory_details',
        'check_tunneling_and_deploy'
    )
    
    deployer_steps = (
        'verify_prerequisites',
        'create_directories',
        'transfer_packages',
        'extract_packages',        
        'execute_packages',
        'clean_pakages',        
    )
    
    def __init__(self):
        self.deploymentRequestDB = DeploymentRequest.DeploymentRequest(mongodb)
        self.group_deployment_request_db = DeploymentRequestGroup.DeploymentRequestGroup(
            mongodb)
        self.versionsDB = Versions.Versions(mongodb)
        self.toolDB = Tool.Tool(mongodb)
        self.buildDB = Build.Build()
        self.machineDB = Machine.Machine(mongodb)
        self.mailer = Mailer.Mailer()
        self.ToolsonmachineDB = ToolsOnMachine.ToolsOnMachine(mongodb)
        self.PreRequisitesDB = PreRequisites.PreRequisites(mongodb)
        self.userDB = Users.Users(mongodb)
        self.stateDB = State.State(mongodb)
        self.deploymentUnitDB = DeploymentUnit.DeploymentUnit()
        self.remote_authentication_service = RemoteAuthenticationService.RemoteAuthenticationService()
        self.id = None
        self.RequestDetails = {}
        self.MachineDetails = {}
        self.BuildDetail = {}
        self.previous_build_detail = {}
        self.parent_entity_details = {}
        self.Toolsonmachinedetails = {}
        self.ErrFlag = 0
        self.warning_flag = False
        self.inner_warning = 0
        self.logs = []
        self.innerLogs = {}
        self.log_type = "pre_deployment"
        self.step_msg = ""
        self.deployment_type = ""
        self.duration = 0
        self.deployment_fields = ' '
        self.prev_deployment_fields = ' '
        self.deployment_fields_to_hide = []        
        self.TargetMachinePackgesFolder = "DeploymentMangerPackages"        
        self.deployed_class="Handler"
        self.use_deployer=True      
        self.system_details_db = SystemDetails.SystemDetails(mongodb)
        self.system_details = self.system_details_db.get_system_details_single()
        self.configdb = Config.Config(mongodb)

    def copy_file_to_remote(self,file_path,remote_directory_path, **kwargs):
        result = copyToRemote(file_path, remote_directory_path, **kwargs)
        self.handleLogs(str(result)) 
        return result

    def add_dep_field(self, key, value):
        self.deployment_fields = self.deployment_fields + "export "+str(key) + "='" + str(value) + "';"

    def add_prev_dep_field(self, key, value):
        self.prev_deployment_fields = self.prev_deployment_fields + "export " + "prev_" + str(key) + "='" + str(value) + "';"

    def get_all_dep_fileds(self, **kwargs):
        return self.prev_deployment_fields + self.deployment_fields

    def change_log_type_to_deploy_process(self, **kwargs):
        self.log_type = "deploy_process"
        self.step_msg = "deploy_process started"

    def change_log_type_post_deploy_process(self, **kwargs):
        self.log_type = "post_deployment"
        self.step_msg = "post deploy_process started"

    def UpdateStepStatus(self, sts, msg):
        result = self.deploymentRequestDB.UpdateStepDetails(
            self.id, self.current_step_id, step_status=sts, step_message=msg)
        return result

    def UpdateStepStartTime(self, **kwargs):
        result = self.deploymentRequestDB.UpdateStepDetails(
            self.id, self.current_step_id, step_status='Processing', step_start_time=datetime.now(), step_message='')
        return result

    # It is assumed if step reach his end, it will get successful status
    def UpdateStepEndTime(self, duration):
        result = self.deploymentRequestDB.UpdateStepDetails(
            self.id, self.current_step_id, step_status='Done', step_end_time=datetime.now(), step_duration=("%.3f" % duration))
        return result

    def UpdateStepEndTimeNotChecked(self, duration):
        result = self.deploymentRequestDB.UpdateStepDetails(self.id, self.current_step_id, step_status='Done', step_end_time=datetime.now(
        ), step_duration=("%.3f" % duration), step_message='Tool Without PreRequisites')
        return result

    def GetMachineDetails(self, machine_id):
        machine = self.machineDB.GetMachine(machine_id)
        return machine

    def GettoolInstallationDetail(self, machine_id):
        toolInstallations = self.ToolsonmachineDB.get_tools_on_machine_by_machine_id(
            machine_id)
        return toolInstallations

    def GetToolsOnMachineByMachineIdAndParentEntityId(self, machineid, parent_entity_id):
        toolInstallations = self.ToolsonmachineDB.get_tools_on_machine_by_machine_id_and_parent_entity_id(
            machineid, parent_entity_id)
        return toolInstallations

    def GetRequestDetails(self, req_id):
        request = self.deploymentRequestDB.GetDeploymentRequest(req_id)
        return request
    
    def get_group_request_details(self, req_id):
        request = self.group_deployment_request_db.get_grp_depreq_by_inner_depreq_ids(req_id)
        return request
    

    def GetVersionDetalis(self, versionid):
        version = self.versionsDB.get_version(versionid, False)
        return version

    def GetDuDetalis(self, duid):
        version = self.deploymentUnitDB.GetDeploymentUnitById(duid, False)
        return version

    def GetBuildDetail(self, parent_entity_id, build_id=None,state_id=None):
        build=BuildHelperService.get_build_for_parent(parent_entity_id, build_id, state_id)
        if not build:
            raise Exception("Active build was not found")
        return build

    def GetVersionCommand(self, Name):
        versioncommand = self.PreRequisitesDB.get_pre_requisites(Name)
        return versioncommand

    def CheckEnv(self, **kwargs):
        return None

    def UpdateRequestStatus(self, status, status_message):
        status_message = status_message.replace("'", "")
        status_message = status_message.replace('"', "")
        self.deploymentRequestDB.UpdateDeploymentRequestStatus(
            self.id, status, status_message)

    def UpdateTime(self, type):
        self.deploymentRequestDB.UpdateDeploymentRequestTime(self.id, type)

    def add_to_tools_on_machine(self):
        existingEntry = self.ToolsonmachineDB.get_tools_on_machine_by_machine_id_and_parent_entity_id(
            self.RequestDetails["machine_id"], self.RequestDetails["parent_entity_id"])
        jsonEntry = {}
        jsonEntry["status"] = "1"
        jsonEntry["host"] = self.MachineDetails.get('host')
        jsonEntry["machine_id"] = self.RequestDetails["machine_id"]
        if self.RequestDetails.get("machine_group_id"):
            jsonEntry["machine_group_id"] = self.RequestDetails["machine_group_id"]
        jsonEntry["parent_entity_id"] = self.RequestDetails["parent_entity_id"]
        jsonEntry["deployment_request_id"] = str(self.id)
        jsonEntry["group_deployment_request_id"] = str(self.group_request_details.get("_id"))        
        jsonEntry["build_no"] = str(self.BuildDetail.get("build_number"))
        jsonEntry["build_id"] = str(self.BuildDetail.get("_id"))
        if self.RequestDetails.get('request_type').lower() in ['revert']\
         and self.RequestDetails.get("previous_build_id") and self.RequestDetails.get("previous_build_number"):
            jsonEntry["previous_build_number"] = self.RequestDetails.get(
                "previous_build_number")
            jsonEntry["previous_build_id"] = self.RequestDetails.get(
                "previous_build_id")            
        if existingEntry:
            jsonEntry["_id"] = {"oid": existingEntry["_id"]}
            self.ToolsonmachineDB.update_tools_on_machine(jsonEntry)
        else:
            self.ToolsonmachineDB.add_tool_on_machine(jsonEntry)       

    def remove_from_tools_on_machine(self):
        existingEntry = self.ToolsonmachineDB.get_tools_on_machine_by_machine_id_and_parent_entity_id(
            self.RequestDetails["machine_id"], self.RequestDetails["parent_entity_id"])
        if existingEntry:
            existingEntry={"_id":{"oid":str(existingEntry["_id"])},"status":"0"}
            self.ToolsonmachineDB.update_tools_on_machine(existingEntry)
        else:
            raise ValueError("No such entry found in ToolsOnMachine")

    def run_pre_deployment_plugins(self, **kwargs):
        try:
            self.handleLogs("starting pre deployment plugin")
            plugin_manager.preform_all_in_category('PreDeploymentPlugin', machine_details=self.MachineDetails,
                                                   request_details=self.RequestDetails)
            self.step_msg = "Done"
        except Exception as error:
            self.handleLogs("Exception :" + str(error))
            raise Exception(error)

    def run_post_deployment_plugins(self, **kwargs):
        try:
            self.handleLogs("starting post deployment plugin")
            plugin_manager.preform_all_in_category('PostDeploymentPlugin', machine_details=self.MachineDetails,
                                                   request_details=self.RequestDetails)
            self.step_msg = "Done"
        except Exception as error:
            self.handleLogs("Exception :" + str(error))
            raise Exception(error)

    def verify_prerequisites(self, *args, **kwargs):
        self.handleLogs("Starting deployment prechecks")
        start_time = time.time()
        error = False
        self.step_msg = ""
        MachineExecutables = None
        MachineExecutables_rpm = None

        if self.parent_entity_details.get("pre_requiests"):
            try:
                MachineExecutables = getExecutables(**kwargs)
            except Exception as e:  # catch *all* exceptions
                self.handleLogs(
                    "Exception while executing compgen -c :" + str(e))
            try:
                MachineExecutables_rpm = getExecutables_rpm(**kwargs)
            except Exception as e:  # catch *all* exceptions
                self.handleLogs("Exception while executing rpm -qa :" + str(e))
            # make sure that MachineExecutables MachineExecutables_RPM are not None
            if MachineExecutables == None:
                MachineExecutables = []
            if MachineExecutables_rpm == None:
                MachineExecutables_rpm = []

            PreRequisests = self.parent_entity_details["pre_requiests"]
            ##################################################
            #structure of pre_requisites in DB is like     ###
            # "pre_requiests" : [                          ###
            #                     {                        ###
            #                         "version" :"1.7",    ###
            #                         "name" : "java"      ###
            #                     },                       ###
            #                     {                        ###
            #                         "version" : "2.6",   ###
            #                         "name" : "python"    ###
            #                     }                        ###
            #                 ]                            ###
            # so tool_pre["version"] is pre_requuisite version#
            ##################################################
            self.handleLogs("Warning Flag is set to  : " +
                            str(self.warning_flag))

            if len(PreRequisests) > 0 or not PreRequisests == [{}]:
                for tool_pre in PreRequisests:
                    if tool_pre.get("name") is not None:
                        try:
                            version_tool_command = self.GetVersionCommand(
                                tool_pre["name"])
                            if version_tool_command["prerequisites_status"] == 'active':
                                if version_tool_command["prerequisites_name"] in [MachineExecutables, MachineExecutables_rpm]:
                                    self.checkPrerequisetVersion(
                                        version_tool_command, tool_pre, start_time)
                                    self.step_msg += '     ' + \
                                        tool_pre["name"] + \
                                        str(tool_pre["version"]) + " was found"
                                else:
                                    raise ValueError(
                                        tool_pre["name"] + str(tool_pre["version"]) + " not found")
                            else:
                                self.step_msg += '     ' + \
                                    tool_pre["name"] + \
                                    " not checked as not active in PreRequisests"
                        except Exception:  # catch *all* exceptions
                            error = True
                            self.step_msg += '     ' + \
                                str(tool_pre["name"]) + str(tool_pre["version"]) + \
                                " was not found in PreRequisites"
            else:
                self.step_msg += 'Tool Without PreRequisites'
            self.handleLogs(self.step_msg)
            if error:
                if self.warning_flag == True:
                    self.inner_warning = 1
                    self.handleLogs(
                        'warning_flag = True. Deployment will continue with warning')
                else:
                    self.handleLogs(
                        'aborting Deployment : warning_flag is false and verify prerequisites failed')
                    raise ValueError(str(self.step_msg))
        else:
            self.step_msg += ' No PreRequisites were found to check'
                                
    def checkPrerequisetVersion(self, version_tool_command, tool_pre, start_time):
        if version_tool_command["parse_version"] == '':
            Executables_ver = getExecutablesversion(
                version_tool_command["prerequisites_name"], version_tool_command["version_command"])
        else:
            Executables_ver = getExecutablesParversion(
                version_tool_command["parse_version"])
        if str(tool_pre["version"]).lower() != "any":
            if tool_pre["version"] in Executables_ver:
                self.handleLogs("Check prerequisites passed successfully " +
                                tool_pre["name"] + tool_pre["version"])
            else:
                self.handleLogs("Check prerequisites version failed " +
                                tool_pre["name"] + tool_pre["version"])
                self.step_msg = "Warning : " + \
                    tool_pre["name"] + tool_pre["version"] + " not found"
                raise ValueError(
                    tool_pre["name"] + tool_pre["version"] + " not found")
        else:
            self.handleLogs(
                "Check prerequisites passed successfully " + tool_pre["name"])

    def verify_tool_dependencies(self, **keyargs):
        try:
            if self.deployment_type == "toolgroup":
                start_time = time.time()
                # self.UpdateStepStartTime()
                tool_Dep_check = []
                if self.parent_entity_details.get("dependent_tools"):
                    dependent_tools = self.parent_entity_details["dependent_tools"]
                    i = 0
                    for tool_dep in dependent_tools:
                        if tool_dep.get("tool_id") is not None:
                            tool = self.toolDB.get_tool_by_version(
                                tool_dep.get("parent_entity_id"), False)
                            versionchk = None
                            if tool_dep.get("parent_entity_id") is not None:
                                if tool_dep.get("parent_entity_id").lower() == "any":
                                    versionsonmachine = self.ToolsonmachineDB.get_tools_on_machine_by_machine_id(
                                        self.RequestDetails["machine_id"])
                                    for version in versionsonmachine:
                                        if tool_dep.get("tool_id") == self.versionsDB.get_version(version.get("parent_entity_id"), False).get("tool_id"):
                                            versionchk = self.versionsDB.get_version(
                                                version.get("parent_entity_id"), False)
                                        if versionchk:
                                            break
                                else:
                                    version = self.versionsDB.get_version(
                                        tool_dep.get("parent_entity_id"), False)
                                    versionchk = self.ToolsonmachineDB.get_tools_on_machine_by_parent_entity_id(
                                        tool_dep.get("parent_entity_id"))
                                if not versionchk:
                                    if (tool_dep.get("is_mandatory")).lower() == "true":
                                        if tool_dep.get("parent_entity_id").lower() == "any":
                                            self.handleLogs("Check for mandatory tool dependencies failed." + "Tool name:" + tool.get(
                                                "name") + "Tool id :" + tool_dep["tool_id"] + "for any version.")
                                            tool_Dep_check.append("Check for mandatory tool dependencies failed." + "Tool name:" + tool.get(
                                                "name") + "Tool id :" + tool_dep["tool_id"] + +"for any version.")
                                            self.step_msg = tool_Dep_check[i]
                                            raise Exception(tool_Dep_check[i])
                                        else:
                                            self.handleLogs("Check for mandatory tool dependencies failed." + "Tool name:" + tool.get("name") + "Tool id :" +
                                                            tool_dep["tool_id"] + ", version name :" + version.get("version_name") + "version id : " + tool_dep["parent_entity_id"])
                                            tool_Dep_check.append("Check for mandatory tool dependencies failed." + "Tool name:" + tool.get(
                                                "name") + "Tool id :" + tool_dep["tool_id"] + ", version name :" + version.get("version_name") + "version id : " + tool_dep["parent_entity_id"])
                                            # self.UpdateStepStatus("Failed", tool_Dep_check[i])
                                            self.step_msg = tool_Dep_check[i]
                                            raise Exception(tool_Dep_check[i])
                                    else:
                                        if tool_dep.get("parent_entity_id").lower() == "any":
                                            self.handleLogs("Check for optional tool dependencies failed." + "Tool name:" + tool.get(
                                                "name") + "Tool id :" + tool_dep["tool_id"] + +"for any version.")
                                            tool_Dep_check.append("Check for optional tool dependencies failed." + "Tool name:" + tool.get(
                                                "name") + "Tool id :" + tool_dep["tool_id"] + +"for any version.")
                                        else:
                                            self.handleLogs("Check for optional tool dependencies failed." + "Tool name:" + tool.get(
                                                "name") + "Tool id :" + tool_dep["tool_id"] + ", version name :" + version.get("version_name") + "version id : " + tool_dep["version"])
                                            tool_Dep_check.append("Check for optional tool dependencies failed." + "Tool name:" + tool.get(
                                                "name") + "Tool id :" + tool_dep["tool_id"] + ", version name :" + version.get("version_name") + "version id : " + tool_dep["version"])
                        i = i + 1
                    tool = self.toolDB.get_tool_by_id(
                        self.parent_entity_details["tool_id"], False)
                    self.handleLogs(
                        "Check for tool dependency passed successfully " + "Tool name:" + tool.get("name"))
                    # self.UpdateStepStatus("Success", (".").join(tool_Dep_check))
                    # end_time = time.time()
                    # self.UpdateStepEndTime(end_time - start_time)
                    self.step_msg = (".").join(tool_Dep_check)
                else:
                    tool = self.toolDB.get_tool_by_id(
                        self.parent_entity_details["tool_id"], False)
                    self.handleLogs("No tool dependency exists " +
                                    "Tool name:" + tool.get("name"))
                    self.step_msg = "No tool dependency exists"
                    # self.UpdateStepStatus("Success", "No tool dependency exists")
                    # end_time = time.time()
                    # self.UpdateStepEndTime(end_time - start_time)
            elif self.deployment_type == "dugroup":
                self.step_msg = "Step skipped ,deployment is of type DUGROUP "
                self.handleLogs(
                    "DeploymentStep :verify_tool_dependencies skipped as deployment is of type DUGROUP")
        except Exception as e:  # catch *all* exceptions
            self.ErrFlag = 1
            self.step_msg = "executeDeploymentSteps: " + str(e)
            raise ValueError(self.step_msg)

    def transfer_packages(self, build_details=None, **keyargs):
        try:
            if build_details == None:
                build_details = []
                if self.RequestDetails.get('request_type').lower() in ['revert']:
                    build_details.append(self.previous_build_detail)
                    build_details.append(self.BuildDetail)
                else:
                    build_details.append(self.BuildDetail)
            for BuildDetail in build_details:
                self.UpdateRequestStatus("Processing", "Downloading Package")
                self.handleLogs("Creating Directory " + current_path + "/" +
                                self.id + "/" + str(BuildDetail.get('build_number')))
                if not os.path.exists(current_path + "/" + self.id + "/" + str(BuildDetail.get('build_number'))):
                    os.makedirs(current_path + "/" + self.id +
                                "/" + str(BuildDetail.get('build_number')))
                
                self.handleLogs(
                    "Pulling file to  " + current_path + "/" + self.id + "/" + str(BuildDetail.get('build_number')))
                keyargs.update({"create_inside_relative_path":False})
                BuildHelperService.download_build_files(BuildDetail,BuildDetail.get("parent_entity_id"),\
                                                    current_path + "/" + self.id + "/" + str(BuildDetail.get('build_number')), None,None,\
                                                    **keyargs)# This is keyargs for NexusHelperService
                
                self.handleLogs(
                    "Pulled file to  " + current_path + "/" + self.id + "/" + str(BuildDetail.get('build_number')))
            
            source_size = long(self.get_size(current_path + "/" + self.id))
            self.UpdateRequestStatus(
                "Processing", "Transferring Package. Status: 0% Size: 0 of " + str(source_size))
            self.handleLogs("Coping file :" + current_path + "/" + self.id +
                            " to  " + self.TargetMachinePackgesFolder)
            futures = []
            self.is_copying = True
            pool = ThreadPoolExecutor(2,__name__+".transfer_packages")
            futures.append(pool.submit(self.start_copy, self.id,
                                       os.path.normpath(current_path + "/" + self.id), self.TargetMachinePackgesFolder, current_path, **keyargs))
            futures.append(pool.submit(
                self.copy_status, source_size, **keyargs))
            wait(futures)

            # CHECK EXCEPTIONS
            for future in futures:
                if future.exception():
                    raise future.exception()

            # Mark Copy to 100%
            self.copy_status_final_mark(source_size, **keyargs)
            self.step_msg = "transfer_packages Done"

        except Exception as e:
            traceback.print_exc()
            self.step_msg = "transfer_packages failed"
            raise e
        finally:
            self.handleLogs("Removing Directory " +
                            current_path + "/" + self.id)
            if os.path.exists(current_path + "/" + self.id):
                shutil.rmtree(current_path + "/" + self.id)
                self.handleLogs("Removed Directory " +
                                current_path + "/" + self.id)

    def copyfileobj(self, fsrc, fdst, length=50 * 1024):
        copied = 0
        per = long(10)
        self.handleLogs("Downloading package: Status: " + str(round(100 * float(copied) /
                                                                    float(fsrc.headers["Content-Length"]), 2)) + "% Size: " + str(copied) + " of " + fsrc.headers["Content-Length"])
        while True:
            buf = fsrc.read(length)
            if not buf:
                break
            fdst.write(buf)
            copied += len(buf)
            if long(round(100 * float(copied) /
                          float(fsrc.headers["Content-Length"]), 2)) == per:
                per += 10
                self.handleLogs("Downloading package: Status: " + str(round(100 * float(copied) /
                                                                            float(fsrc.headers["Content-Length"]), 2)) + "% Size: " + str(copied) + " of " + fsrc.headers["Content-Length"])

    def start_copy(self, RequestId, From, To, current_path, **keyargs):
        self.is_copying = True
        try:
            copy_dir_to_remote(RequestId, From, To, current_path, **keyargs)
        finally:
            self.is_copying = False

    def copy_status(self, source_size, **keyargs):
        time.sleep(10)
        depRequest = {}
        depRequest["_id"] = {"oid": self.id}
        depRequest["original_size"] = str(source_size)
        while self.is_copying:
            try:
                time.sleep(10)
                current_size = long(
                    str(getSize(str(self.id), self.TargetMachinePackgesFolder, **keyargs).stdout))
                if current_size > source_size:
                    current_size = source_size

                status = round(100 * float(current_size) /
                               float(source_size), 2)
                depRequest["progress"] = str(status) + "%"
                depRequest["current_size"] = str(current_size)
                self.deploymentRequestDB.UpdateDeploymentRequest(depRequest)
                self.handleLogs("Transferring Package. Status: " + str(status) +
                                "% Size: " + str(current_size) + " of " + str(source_size))
            except Exception:
                pass

    def copy_status_final_mark(self, source_size, **keyargs):
        depRequest = {}
        depRequest["_id"] = {"oid": self.id}
        depRequest["original_size"] = str(source_size)
        try:
            current_size = long(
                str(getSize(self.id, self.TargetMachinePackgesFolder, **keyargs).stdout))
            if current_size > source_size:
                current_size = source_size
            status = round(100 * float(current_size) /
                           float(source_size), 2)
            depRequest["progress"] = str(status) + "%"
            depRequest["current_size"] = str(current_size)
            self.deploymentRequestDB.UpdateDeploymentRequest(depRequest)
            self.handleLogs("Transferring Package. Status: " + str(status) +
                            "% Size: " + str(current_size) + " of " + str(source_size))
        except Exception:
            pass

    def get_size(self, start_path):
        folder_size = 1  # DEFAULT SIZE
        try:
            cmd = ["du -Psk ", start_path + " | cut -f1 "]
            self.handleLogs(subprocess.check_output("pwd", shell=True))
            out = subprocess.check_output("".join(cmd), shell=True)
            self.handleLogs("Source file Size: " + out)
            folder_size = long(out.split()[0])
        except Exception:
            pass
        return folder_size

    def extract_packages(self, build_details=None, **keyargs):
        if build_details == None:
            build_details = []
            if self.RequestDetails.get('request_type').lower() in ['revert']:
                build_details.append(self.previous_build_detail)
                build_details.append(self.BuildDetail)
            else:
                build_details.append(self.BuildDetail)
        for BuildDetail in build_details:
            self.handleLogs("Unpacking Archive for build :" +
                            str(BuildDetail.get('build_number')))
            self.UpdateRequestStatus(
                "Processing", "Extracting Package for build : " + str(BuildDetail.get('build_number')))
            self.file_location = self.TargetMachinePackgesFolder + "/" + \
                self.id + "/" + str(BuildDetail.get('build_number'))

            if str(BuildDetail.get("package_type")).lower() == "zip":
                if self.MachineDetails.get("reload_command"):
                    self.handleLogs("Running Command: " + self.MachineDetails.get(
                        "reload_command") + ' ; echo "n" | unzip -o {0} -d {1} '.format(self.file_location +"/*.zip",self.file_location +"/"))
                    result = runCommand(self.MachineDetails.get(
                        "reload_command") + ' ; echo "n" | unzip -o {0} -d {1} '.format(self.file_location +"/*.zip",self.file_location +"/"), **keyargs)
                else:
                    self.handleLogs(
                        "Running Command: " + ' ; echo "n" | unzip -o {0} -d {1} '.format(self.file_location +"/*.zip",self.file_location +"/"))
                    result = runCommand(
                         'echo "n" | unzip {0} -d {1} '.format(self.file_location +"/*.zip",self.file_location +"/"), **keyargs)
                    

                self.handleLogs("Unpacking Archive" + str(result))
                if not result or result.return_code != 0:
                    raise Exception(" unable to unzip file with unknown error")
                result = runCommand(
                    'chmod -R +x {}'.format(self.file_location), **keyargs)
                self.handleLogs(str(result))
                self.step_msg = str(result)
            else:
                raise Exception("Unsupported package_type. We only support .zip for now")    
    def clean_pakages(self, **keyargs):
        ###############################
        # Clean installation package  #
        ###############################
        result = runCommand(
            'rm -r -f {}'.format(self.TargetMachinePackgesFolder+"/"+ self.id), **keyargs)
        self.handleLogs("Clean Package :" + str(result))
        self.step_msg = str(result)

    def RunProcess(self, fileName, build_number=None, **keyargs):
        fileToProcess= self.get_file_to_process(fileName, build_number, **keyargs)
        self.handleLogs("Running File :" + str(fileToProcess))
        self.execute(fileToProcess, **keyargs)

    def get_file_to_process(self, file_name , build_number = None, **keyargs):
        if build_number == None:
            build_number = str(self.BuildDetail.get('build_number'))
        self.handleLogs("RunProcess")
        self.file_location = self.TargetMachinePackgesFolder + "/" + self.id + "/" + build_number
        fileToProcess = runCommand(
            'ls {}'.format(self.file_location) +"/"+ file_name + '*', **keyargs)
        self.handleLogs("Files Found to Process :" + str(fileToProcess))
        if not fileToProcess:
            raise Exception("No file with name:" + file_name + " was found")
        # check if exists installer
        ###########################
        temp = fileToProcess.stdout.split('\n')
        matching = [s for s in temp if any(
            word in s for word in [file_name + ".py", file_name + ".sh", file_name + ".jar", file_name + ".pyc"])]
        if len(matching) > 1:
            raise Exception(" more then one installer file was found with same name: "+file_name)            
        elif len(matching) < 1:
            raise Exception(" No installer file with name starting with: "+file_name)
        fileToProcess = matching[0]
        fileToProcess = self.file_location + "/" + fileToProcess.rsplit('/',1)[1]
        return fileToProcess
        
    def get_extracted_directory_path(self):
        return self.TargetMachinePackgesFolder + "/" + self.id
    
    def get_export_variables(self):
        if self.MachineDetails.get("reload_command"):
            return self.MachineDetails.get(
                "reload_command") + ";" + self.get_all_dep_fileds()
        else:
            return self.get_all_dep_fileds()
    
    def replace_sensistive_data(self,command):
        for text in self.deployment_fields_to_hide:
            command = command.replace('"'+text+'"','"'+"*"*len(text)+'"')
        return command
        
    
    def execute(self, fileToProcess, **keyargs):
        result = None
        self.set_env_variables() # SET ENV VARIABLES
        self.set_prev_env_variables()  # SET PREV ENV VARIABLES
        command = self.get_export_variables()
        print "******* started to excute"
        fileToProcess = fileToProcess.strip()
        print "fileToProcess.endswith('.pyc')", fileToProcess.endswith('.pyc')
        installer_location, install_file = fileToProcess.rsplit('/', 1)

        if fileToProcess.endswith('.pyc') or fileToProcess.endswith('.py'):
            print "******* found python installer "
            self.handleLogs(self.replace_sensistive_data("Execute Package:" + str(command +
                                                     ' python ' + fileToProcess)))
            result = runCommand(command +
                                ' cd {} && python '.format(installer_location) + install_file, **keyargs)
        elif fileToProcess.endswith('.sh'):
            self.handleLogs(self.replace_sensistive_data("Execute Package:" + command +
                            'cd {};'.format(installer_location) + "./" + install_file))
            result = runCommand(
                command + ' cd {};'.format(installer_location) + "./" + install_file, **keyargs)

        elif fileToProcess.endswith('.jar'):
            self.handleLogs(self.replace_sensistive_data("Execute Package:" + command +
                            'java ' + fileToProcess))
            result = runCommand(command +
                                ' cd {} && java '.format(installer_location) + install_file, **keyargs)
            
        else:
            raise Exception(" unable to run file as its of invalid type ")

        if not result or result.return_code != 0:
            raise Exception(" unable to run file with unknown error")

        self.handleLogs("Result:" + str(result))        
        return result 
    
    def validateConnectionSettings(self, *args, **kwargs):
        if self.MachineDetails.get("username") is None:
            raise ValueError("username was not found in request")
        if self.MachineDetails.get("ip") is None:
            raise ValueError("ip was not found in request")
        if self.MachineDetails.get("host") is None:
            raise ValueError("host was not found in request")
        if self.MachineDetails.get("password") is None:
            raise ValueError("password was not found in request")
        if self.MachineDetails.get("port") is None:
            raise ValueError("port was not found in request")
    
    def set_prev_env_variables(self, **keyargs):    
        # Load Request
        request_type = str(self.RequestDetails["request_type"]).lower()
        if request_type in ['deploy']:
            pass
        elif request_type in ['redeploy','upgrade','undeploy','revert']:
            self.SetPrevEnvVariables()        
        self.step_msg = "Done"
    def execute_packages(self, **keyargs):
        # Load Request
        RequestType = str(self.RequestDetails["request_type"]).lower()
        #################
        # run installer #
        #################
        self.handleLogs("Starting to Exceute")
        self.UpdateRequestStatus("Processing", "Executing Package")
        if RequestType in ['deploy']:
            # PREVIOUS DEPLOYMENT FIELDS NOT REQUIRED WHEN WE DEPLOY
            self.RunProcess("install", **keyargs)
            self.step_msg = "Installation was completed successfully"
            self.UpdateRequestStatus(
                "Processing", "Installation was completed successfully")
        elif RequestType == 'redeploy':
            self.RunProcess("redeploy", **keyargs)
            self.UpdateRequestStatus(
                "Processing", "ReDeployment was completed successfully")
            self.step_msg = "ReDeployment was completed successfully"
        elif RequestType == 'upgrade':
            self.RunProcess("upgrade", **keyargs)
            self.UpdateRequestStatus(
                "Processing", "Upgrade was completed successfully")
            self.step_msg = "Upgrade was completed successfully"
        elif RequestType == 'undeploy':
            self.RunProcess("uninstall", **keyargs)
            self.UpdateRequestStatus(
                "Processing", "Uninstallation was completed successfully")
            self.step_msg = "Uninstallation was completed successfully"
        elif RequestType == 'revert':
            self.handleLogs("Uninstallation of build " +
                            str(self.previous_build_detail.get('build_number')) + " started")
            self.RunProcess("uninstall", str(
                self.previous_build_detail.get('build_number')), **keyargs)
            self.step_msg = "UnInstallation of build " + \
                str(self.previous_build_detail.get('build_number')) + \
                " completed successfully"
            self.handleLogs("Uninstallation of build " + str(
                self.previous_build_detail.get('build_number')) + " was completed successfully")
            ######################Install older build #####################################
            self.handleLogs("Installation of build " + str(
                self.BuildDetail.get('build_number')) + " started")
            self.RunProcess("install", str(
                self.BuildDetail.get('build_number')), **keyargs)
            self.step_msg = "Installation of build " + \
                str(self.BuildDetail.get('build_number')) + \
                " was completed successfully"
            self.handleLogs("Installation of build " + str(
                self.BuildDetail.get('build_number')) + "was completed successfully")        
            
    def save_deployment_in_db(self, **keyargs):
        requuest_type = str(self.RequestDetails["request_type"]).lower()
        if requuest_type in ['deploy','redeploy','revert','upgrade']:
            self.add_to_tools_on_machine()
        elif requuest_type == 'undeploy':
            self.remove_from_tools_on_machine()        
        else:
            self.UpdateRequestStatus("Failed", "Invalid Request Type")
            self.step_msg = "Invalid Request Type"
            raise ValueError("Invalid Request Type")
        self.step_msg = "Updated in Database"            

    def deployProcess(self, *args, **kwargs):
        try:
            # self.validateConnectionSettings(*args, **kwargs)   @i.p redundant connection checking , this check should be done in the RemoteAuthenticationService
            self.ErrFlag = 0
            # LOAD Handler
            if self.use_deployer is True:
                class_obj=CustomClassLoaderService.get_class(self.deployer_module)
                self.deployer_instance=class_obj(self)
            self.executDeploymentSteps(*args, **kwargs)
        except Exception as e:  # catch *all* exceptions
            traceback.print_exc()
            self.handleLogs("Failed with error :" + str(e))
            # self.UpdateRequestStatus("Failed",  str(e))
            raise ValueError(
                "Step: deployProcess failed with error: " + str(e))

    def InitStepDetails(self, **kwargs):
        step_details = ""
        for step_id, step in enumerate(self.preDeploymentsteps):
            if (str(step) == 'check_tunneling_and_deploy'):
                nested_step_details = ""
                nested_jsonEntry = ""
                for deployment_step_id, deployment_step in enumerate(self.deployment_steps):
                    nested_jsonEntry = '"' + str(deployment_step_id) + '": {"step_id":"' + str(deployment_step_id) + '", "step_name":"' + deployment_step + \
                        '", "step_status": "New", "step_message": "", "step_start_time":"", "step_end_time":"", "step_duration":""}'
                    if nested_step_details != "":
                        nested_step_details = nested_step_details + ","
                    nested_step_details = nested_step_details + nested_jsonEntry
                jsonEntry = '{"step_id":"' + str(step_id) + '", "step_name":"' + step + \
                    '", "step_status": "New", "step_message": "", "step_start_time":"", "step_end_time":"", "step_duration":"","current_step_id":"0", "nested_step_details":{' + nested_step_details + '}}'
            else:
                jsonEntry = '{"step_id":"' + str(step_id) + '", "step_name":"' + step + \
                    '", "step_status": "New", "step_message": "", "step_start_time":"", "step_end_time":"", "step_duration":""}'
            if step_details != "":
                step_details = step_details + ","
            step_details = step_details + jsonEntry
        step_details = '{"step_details": [' + step_details + ']}'
        self.RequestDetails['step_details'] = '[' + step_details + ']'
        self.deploymentRequestDB.InitStatusDetails(self.id, step_details)
        self.deploymentRequestDB.UpdateRequestDetails(
            self.id, execution_count="1")

    def addStepDetails(self, step_tuple):
        step_details = ""
        num_of_deployment_step_in_db = self.deploymentRequestDB.StepDetailsCount(
            self.id)
        for step_id, step in enumerate(self.step_tuple):
            step_id = step_id + num_of_deployment_step_in_db
            jsonEntry = '{"step_id":"' + str(step_id) + '", "step_name":"' + step + \
                '", "step_status": "New", "step_message": "", "step_start_time":"", "step_end_time":"", "step_duration":""}'
            if step_details != "":
                step_details = step_details + ","
            # in case clone_tools step is found, we need to create for each
            # tool its own steps from tool_steps tuple
            step_details = step_details + jsonEntry
        step_details = '[' + step_details + ']'
        self.deploymentRequestDB.addDeploymentSteps(self.id, step_details)

    def handleLogs(self, newLogLine):
        print "DeploymentServices: _id: " + str(self.id) + " " + newLogLine
        if not str(newLogLine).lower().strip() or str(newLogLine).lower().strip() in ["none", "", " "]:
            return
        for line in str(newLogLine).split('\n'):
            line = line.replace("'", "").replace('"', "")
            if str(line).lower().strip() and str(line).lower().strip() not in ["none", "", " "]:
                if self.log_type in self.innerLogs["logdata"].keys():
                    self.innerLogs["logdata"][self.log_type].append(line)
                else:
                    l_type = []
                    l_type.append(line)
                    self.innerLogs['logdata'][self.log_type] = l_type
        logs = copy.deepcopy(self.logs)
        logs.append(self.innerLogs)
        depRequest = {}
        depRequest["_id"] = {"oid": self.id}
        depRequest["logs"] = logs
        self.deploymentRequestDB.UpdateDeploymentRequest(depRequest)

    def setParentEntitydetails(self, **kwargs):
        if self.deployment_type.lower() == "dugroup":
            if self.GetDuDetalis(self.RequestDetails.get("parent_entity_id")) != None:
                self.parent_entity_details = self.GetDuDetalis(
                    self.RequestDetails.get("parent_entity_id"))
            else:
                self.step_msg = "DU not found"
                raise Exception("DU not found")
        elif self.deployment_type.lower() == "toolgroup":
            if self.GetVersionDetalis(self.RequestDetails.get("parent_entity_id")) != None:
                self.parent_entity_details = self.GetVersionDetalis(
                    self.RequestDetails.get("parent_entity_id"))
                self.handleLogs("parent_entity Details was found")
                self.step_msg = "parent_entity Details was found"
            else:
                self.step_msg = "tool as no version"
                raise Exception("tool as no version")
        else:
            self.step_msg = "deployment_type not valid"
            raise Exception("deployment_type not valid")

    def setBuildDetails(self, **kwargs):
        # ,'upgrade','undeploy'
        if self.RequestDetails.get('request_type').lower() in ['revert']:
            if self.RequestDetails.get("previous_build_id"):
                if self.GetBuildDetail(self.RequestDetails.get("parent_entity_id"), self.RequestDetails.get("previous_build_id"),self.RequestDetails.get("previous_state_id")) is not None:
                    self.previous_build_detail = self.GetBuildDetail(self.RequestDetails.get(
                        "parent_entity_id"), self.RequestDetails.get("previous_build_id"),self.RequestDetails.get("previous_state_id"))
                    self.handleLogs("Previous Build Details was found.Build No: "+str(self.previous_build_detail.get("build_number")))
                    self.step_msg = "Previous Build Details was found.Build No: "+str(self.previous_build_detail.get("build_number"))
                else:
                    self.step_msg = "previous build was not found"
                    raise Exception("previous build was not found")
            else:
                raise Exception(
                    "request is of type revert but previous_build_id was not found")

        if self.GetBuildDetail(self.RequestDetails.get("parent_entity_id"), self.RequestDetails.get("build_id"),self.RequestDetails.get("state_id")) is not None:
            self.BuildDetail = self.GetBuildDetail(self.RequestDetails.get(
                "parent_entity_id"), self.RequestDetails.get("build_id"),self.RequestDetails.get("state_id"))  # NEW REQUIRMENT TO HAVE ALL OLD BUILD ACTIVE
            self.handleLogs("Build Details was found: "+str(self.BuildDetail.get("build_number")))
            self.step_msg = "Build Details was found: "+str(self.BuildDetail.get("build_number"))
        else:
            self.step_msg = "No Active build was found"
            raise Exception("No Active build was found")
        
        data={"_id": {"oid": str(self.RequestDetails.get("_id"))}}
        if self.BuildDetail and len(self.BuildDetail.keys())>0:
                data["build_id"]=str(self.BuildDetail.get("_id"))
                data["build_number"]=self.BuildDetail.get("build_number")
        if self.previous_build_detail and len(self.previous_build_detail.keys())>0:        
                data["previous_build_id"]=str(self.previous_build_detail.get("_id"))
                data["previous_build_number"]=self.previous_build_detail.get("build_number")        
        self.deploymentRequestDB.UpdateDeploymentRequest(data)
        
        
    def setMachineDetails(self, **kwargs):
        if self.GetMachineDetails(self.RequestDetails["machine_id"]) != None:
            self.MachineDetails = self.GetMachineDetails(
                self.RequestDetails["machine_id"])
            self.handleLogs("Machine Details was found")
            self.step_msg = "Machine Details was found"
            if not self.MachineDetails.get('port'):
                self.MachineDetails['port'] = 22
            self.step_msg = "Machine Details was found but port was not there, default port set to 22"
        else:
            self.step_msg = "unable to get machine details "
            raise Exception("unable to get machine details ")
        
    def set_deployer(self, **kwargs):
        self.deployer_module="Plugins.deploymentPlugins.DefaultDeploymentPlugin"
        if self.parent_entity_details.get("deployer_to_use"):
            path_to_check=os.path.join(current_path,\
                                       self.deployer_module\
                .replace(".","/").replace("DefaultDeploymentPlugin", \
                                          self.parent_entity_details.get("deployer_to_use")))+".py"
            if os.path.exists(path_to_check):
                self.deployer_module=self.deployer_module.replace("DefaultDeploymentPlugin", \
                                          self.parent_entity_details.get("deployer_to_use"))
            else:
                raise Exception("Given Handler:"+self.parent_entity_details.get("deployer_to_use")+" was not found in FS")    
            
    def pingMachine(self, **keyargs):
        try:
            self.handleLogs('pinging ' + str(self.MachineDetails.get('host')))
            result = runCommand("hostname", False, **keyargs)
            self.handleLogs('Result: ' + str(result))
        except Exception as e:
            raise ValueError('ping machine failed with error : ' + str(e))

    def validate_mandatory_details(self, **kwargs):
        self.step_msg = "valid upgrade"
        if str(self.RequestDetails["request_type"]).lower() == 'upgrade' and not self.RequestDetails.get("previous_parent_entity_id"):
            self.step_msg = "For Upgrade Previous version id was not found in request"
            raise Exception(
                "For Upgrade Previous version id was not found in request")
        if  str(self.RequestDetails["request_type"]).lower() not in ['deploy','upgrade','redeploy','undeploy','revert']:
            raise Exception(
                "Invalid RequestType was found")

    def check_tunneling_and_deploy(self, **kwargs):
        try:
            if self.MachineDetails.get("steps_to_auth") and len(self.MachineDetails.get("steps_to_auth")) > 0:
                self.UpdateRequestStatus(
                    "Processing", "We will proceed with tunneling")
                self.handleLogs("Authenticating via Tunneling")
            else:
                self.UpdateRequestStatus(
                    "Processing", "We will proceed without tunneling")
                self.handleLogs("Authenticating without Tunneling")
            self.step_msg = "remoteAuthenticationService.authenticate"
            self.deployProcess(**kwargs)
        except Exception as e:
            raise ValueError(str(e))

    def create_directories(self, **keyargs):
        self.handleLogs("Creating Directory")
        self.UpdateRequestStatus("Processing", "Creating Directory")
        if self.previous_build_detail:
            runCommand('mkdir -p -m 777 ' + self.TargetMachinePackgesFolder+"/"+self.id+"/"+str(self.previous_build_detail.\
                                            get("build_number")),True, **keyargs)
        if self.BuildDetail:
            runCommand('mkdir -p -m 777 ' + self.TargetMachinePackgesFolder+"/"+self.id+"/"+str(self.BuildDetail.\
                                            get("build_number")),True, **keyargs)            
        self.step_msg = "Directory: " + self.TargetMachinePackgesFolder + " was created"

    def start_deployment_process(self, request_id, **keyargs):
        try:
            self.innerLogs = {}
            self.innerLogs["dateofdeployment"] = str(
                datetime.now()).split(".")[0]
            self.innerLogs["logdata"] = {}
            self.id = request_id
            self.UpdateRequestStatus("Processing", "Execution is in progress")
            self.UpdateTime("start_time")
            if self.GetRequestDetails(self.id) != None:
                self.RequestDetails = self.GetRequestDetails(self.id)
                self.group_request_details = self.get_group_request_details(self.id)
                self.deployment_type = self.RequestDetails.get(
                    "deployment_type")
                if str(self.RequestDetails.get("execution_count")) in [None, "None", 0, "0"]:
                    self.InitStepDetails()
                # FOUND ISSUE WITH execution_count.Adding extra validation
                if self.RequestDetails.get("step_details") is None:
                    raise ValueError(
                        "step_details not found in request.Looks like issue with execution_count")
                self.current_step_id = int(
                    self.RequestDetails.get("current_step_id"))
                self.logs = self.RequestDetails.get("logs")
                if not self.logs or len(self.logs) < 1:
                    self.logs = []
                self.handleLogs("Installation started")
                self.handleLogs("Request is of type :" +
                                self.RequestDetails.get("deployment_type"))
            else:
                raise Exception("missing request details")
            self.setParentEntitydetails()
            self.setBuildDetails()
            self.setMachineDetails()
            self.set_deployer()
            if not self.use_deployer:
                self.remote_authentication_service.authenticate(
                    self.MachineDetails, self.pingMachine)              
            self.remote_authentication_service.authenticate(
                    self.MachineDetails, self.executePreDeploymentsteps) 
            self.UpdateRequestStatus(
                "Done", "Deployment completed successfully")
        except Exception as e:
            traceback.print_exc()
            self.handleLogs("Execution has failed with error :" + str(e))
            self.UpdateRequestStatus(
                "Failed", "Execution has failed with error :" + str(e))
        finally:
            self.UpdateTime("end_time")

    def SetPrevEnvVariables(self):
        toolOnMachineRec = self.ToolsonmachineDB.get_tools_on_machine_by_machine_id_and_parent_entity_id(
            self.RequestDetails["machine_id"], self.RequestDetails["parent_entity_id"])
        self.handleLogs(
            "Previous Deployment was found in ToolOnMachine: " + str(toolOnMachineRec))
        if toolOnMachineRec and toolOnMachineRec.get("deployment_request_id"):
            existingInstallationVersion = self.GetVersionDetalis(
                toolOnMachineRec["parent_entity_id"])
            existingInstallationDeatils = self.deploymentRequestDB.GetDeploymentRequest(
                toolOnMachineRec["deployment_request_id"])
            # SET PREV DEPLOYMENT VALUES
            if existingInstallationDeatils:
                self.handleLogs("Previous Deployment Details was found")
                if existingInstallationDeatils.get("build_number"):
                    self.add_prev_dep_field(
                        "build_number", existingInstallationDeatils.get("build_number"))
                if existingInstallationDeatils.get("tool_deployment_value"):
                    for depField in existingInstallationDeatils.get("tool_deployment_value"):
                        '''
                            When the deployment fields have passwords we should not print it in logs
                        '''
                        if depField.get("input_type","").lower() == "password" :
                            self.deployment_fields_to_hide.append(depField.get("input_value"))
                            
                        self.add_prev_dep_field(depField.get(
                            "input_name"), depField.get("input_value"))
                else:
                    self.handleLogs(
                        "Error while setting PrevEnv Varialbles:No Deployment fields found for Previous Deployment")
            else:
                self.handleLogs(
                    "Error while setting PrevEnv Varialbles:Previous Deployment Details was not found")

            # SET PREV VERSION GENRAL DETAILS
            if existingInstallationVersion:
                self.handleLogs("Previous Version Details was found")
                if existingInstallationVersion.get("version_name"):
                    self.add_prev_dep_field(
                        "version_name", existingInstallationVersion["version_name"])
                if existingInstallationVersion.get("version_number"):
                    self.add_prev_dep_field(
                        "version_number", existingInstallationVersion["version_number"])
            else:
                self.handleLogs(
                    "Error while setting PrevEnv Varialbles:No Version Detail was found")
        else:
            self.handleLogs("Previous Deployment details:" + str(toolOnMachineRec) +
                            " does not have deployment_request_id saved")

    def executePreDeploymentsteps(self, **kwargs):
        try:
            while self.current_step_id < len(self.preDeploymentsteps):
                step_name = self.preDeploymentsteps[self.current_step_id]
                method = getattr(self, step_name)
                duration = 0
                result = self.deploymentRequestDB.UpdateRequestDetails(
                    self.id, current_step_id=int(self.current_step_id))
                start_time = time.time()
                self.UpdateStepStartTime()
                self.handleLogs(
                    "Calling method : preDeploymentsteps." + str(step_name))
                method(**kwargs)
                self.handleLogs(
                    "Completed method : preDeploymentsteps." + str(step_name))
                duration = time.time() - start_time
                self.deploymentRequestDB.UpdateStepDetails(self.id, self.current_step_id, step_status='Done', step_end_time=datetime.now(
                ), step_duration=("%.3f" % duration), step_message=self.step_msg)
                self.current_step_id = self.current_step_id + 1
        except Exception as e:  # catch *all* exceptions
            self.duration = time.time() - start_time
            self.deploymentRequestDB.UpdateStepDetails(self.id, self.current_step_id, step_status='Failed', step_end_time=datetime.now(
            ), step_duration=("%.3f" % duration), step_message=self.step_msg + str(e))
            raise ValueError("Step: " + step_name +
                             " failed with error: " + str(e))

    def executDeploymentSteps(self, *args, **kwargs):
        try:
            ####################################
            # for 2.0.4 all steps are mandatory#
            # error flag is not being used     #
            # it is for future use             #
            ####################################
            step_status_check = ""
            start_time = time.time()

            if not self.GetRequestDetails(self.id).get("step_details"):
                raise ValueError("step_details not found in request")

            # for depl_step in self.RequestDetails.get('step_details'):
            for depl_step in self.GetRequestDetails(self.id)["step_details"]:
                if depl_step.get('step_name').lower() == 'check_tunneling_and_deploy'.lower():
                    self.nested_current_step_id = int(
                        depl_step.get('current_step_id'))
                    step_status_check = depl_step.get('nested_step_details')
                    if not step_status_check:
                        raise ValueError(
                            "nested_step_details for executDeploymentSteps not present")
                    while self.nested_current_step_id < len(self.deployment_steps):
                        self.inner_warning = 0
                        step_name = self.deployment_steps[self.nested_current_step_id]
                        # inside the kwargs exists the connection details
                        if self.use_deployer and step_name in self.deployer_steps:
                            method = getattr(self.deployer_instance, step_name)
                        else:
                            method = getattr(self, step_name)
                        if int(self.nested_current_step_id) > int(self.deployment_steps.index('change_log_type_to_deploy_process')) and self.log_type != "deploy_process":
                            self.change_log_type_to_deploy_process()  # added  to check log type in retry
                        if int(self.nested_current_step_id) > int(self.deployment_steps.index('change_log_type_post_deploy_process')) and self.log_type != "post_deployment":
                            self.change_log_type_post_deploy_process()  # added  to check log type in retry
                        if self.RequestDetails.get("warning_flag") is not None:
                            self.warning_flag = self.RequestDetails.get(
                                "warning_flag")
                        if str(self.nested_current_step_id) in step_status_check.keys() and step_status_check.get(str(self.nested_current_step_id)).get("step_status").lower() in ['new', "retry", "processing"]:
                            start_time = time.time()
                            self.deploymentRequestDB.UpdateNestedStepDetails(
                                self.id, self.current_step_id, self.nested_current_step_id, step_status='processing', step_start_time=start_time)
                            self.handleLogs(
                                "Calling method : deployment_steps." + str(step_name))
                            assert method, "method in executDeploymentSteps is empty"
                            response_message = method(**kwargs)
                            if response_message:
                                self.step_msg=response_message 
                            self.handleLogs(
                                "Completed method : deployment_steps." + str(step_name))
                            self.duration = time.time() - start_time
                            if self.inner_warning == 1:
                                self.deploymentRequestDB.UpdateNestedStepDetails(self.id, self.current_step_id, self.nested_current_step_id, step_status='Warning', step_end_time=datetime.now(
                                ), step_duration=("%.3f" % self.duration), step_message=self.step_msg)
                            else:
                                self.deploymentRequestDB.UpdateNestedStepDetails(self.id, self.current_step_id, self.nested_current_step_id, step_status='Done', step_end_time=datetime.now(
                                ), step_duration=("%.3f" % self.duration), step_message=self.step_msg)
                                # self.step_msg=""
                        self.nested_current_step_id = self.nested_current_step_id + 1
                        result = self.deploymentRequestDB.UpdateStepDetails(
                            self.id, self.current_step_id, current_step_id=int(self.nested_current_step_id))
        except Exception as e:  # catch *all* exceptions
            self.handleLogs("failed with error:" + str(e))
            self.ErrFlag = 1
            self.duration = time.time() - start_time
            self.deploymentRequestDB.UpdateNestedStepDetails(self.id, self.current_step_id, self.nested_current_step_id, step_status='Failed', step_end_time=datetime.now(
            ), step_duration=("%.3f" % self.duration), step_message=str(e))
            raise ValueError("Step: " + step_name +
                             " failed with error: " + str(e))

    def set_env_variables(self, **kwargs):
        # SET DEPLOYMENT VALUES
        for depField in self.RequestDetails.get("tool_deployment_value"):
            '''
                When the deployment fields have passwords we should not print it in logs
            '''
            if depField.get("input_type","").lower() == "password" :
                self.deployment_fields_to_hide.append(depField.get("input_value"))
            
            self.add_dep_field(str(depField.get("input_name")),
                               str(depField.get("input_value")))
        # SET VERSION GENRAL DETAILS
        if self.parent_entity_details:
            if self.parent_entity_details.get("version_name"):
                self.add_dep_field(
                    "version_name", self.parent_entity_details["version_name"])
            if self.parent_entity_details.get("version_number"):
                self.add_dep_field(
                    "version_number", self.parent_entity_details["version_number"])
        if self.RequestDetails:
            self.add_dep_field(
                "requested_by", self.RequestDetails["requested_by"])
        if self.BuildDetail:
            self.add_dep_field(
                "build_number", self.BuildDetail["build_number"])

        self.add_machine_details()
        self.step_msg = "Done"

    def add_machine_details(self):
        self.add_machine_environment_variables()
        self.add_machine_attributes_to_environment_variables()
        self.add_entity_attributes_to_environment_variables()

    def add_entity_attributes_to_environment_variables(self):
        export_entity_attribute_list = self.configdb.getConfigByName('Deployment')['entity_exposed_attributes'].split(',')
        for attr in export_entity_attribute_list:
            if attr in self.parent_entity_details:
                self.add_dep_field(str('entity_' + attr),
                                   str(self.parent_entity_details.get(attr)))

    def add_machine_attributes_to_environment_variables(self):
        export_machine_attribute_list = self.configdb.getConfigByName('Deployment')['machine_exposed_attributes'].split(',')
        for attr in export_machine_attribute_list:
            if attr in self.MachineDetails:
                self.add_dep_field(str('machine_' + attr),
                                   str(self.MachineDetails.get(attr)))

    def add_machine_environment_variables(self):
        if "environment_variables" in self.MachineDetails:
            for env_var in self.MachineDetails["environment_variables"]:
                self.add_dep_field('machine_' + env_var.get("name"),
                                   str(env_var.get("value")))

    def run_command(self, command_to_execute, set_dep_fileds=True, warn=False, timeout=None, **keyargs):
        if set_dep_fileds:
            result = runCommand(str(self.get_export_variables())+" "+command_to_execute,warn,timeout, **keyargs)
        else:             
            result = runCommand(command_to_execute,warn,timeout, **keyargs)
        self.handleLogs(str(result))
        return result    
    
    def local_artifiacts_path(self,build_number):
        if not os.path.exists(current_path + "/" + self.id + "/" + str(build_number)):
                    os.makedirs(current_path + "/" + self.id +
                                "/" + str(build_number))
        return str(current_path + "/" + self.id +
                                "/" + str(build_number))
