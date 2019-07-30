'''
Created on Mar 16, 2016

@author: PDINDA
'''
import logging
import threading
import time
import traceback
import requests
from datetime import datetime
from autologging import logged
from concurrent.futures import ThreadPoolExecutor, wait
from wrapt.decorators import synchronized

from DBUtil import DeploymentRequest, DeploymentRequestGroup, Config, \
    Users, Machine, Build, Versions, Teams, Tool, DeploymentUnit, ToolsOnMachine
from Services import DeploymentServices, Mailer, TeamService
from Services import SchedulerService, ConfigHelperService



job = None


@logged(logging.getLogger("DeploymentRequestService"))
class DeploymentRequestService(object):
    """
    ###############################
    # DeploymentRequestService Scheduler
    ###############################
    # Includes:
    # Runs DeploymentRequest in parallel
    # Threads consume less memory
    # Runs in interval (Resource Friendly)
    # Scheduler main thread waits for sub threads to complete (New instance
    # will not be triggered even if interval)
    """
    # Init's Data

    def __init__(self, db):
        """
        # Checks no of pending requests
        # Creates sub threads to handle this requests # Minimum Threads is 1
        # The no of threads is configurable from main.py
        # (DeploymentService.DeploymentService(db).schedule(schedulerObj,1,1))
        """
        self.deploymentRequestDB = DeploymentRequest.DeploymentRequest(db)
        self.deploymentRequestGroupDB = DeploymentRequestGroup.DeploymentRequestGroup(
            db)
        self.userDB = Users.Users(db)
        self.configdb = Config.Config(db)
        self.deploymentServices = DeploymentServices.Deployment
        self.mailer = Mailer.Mailer()
        self.machineDB = Machine.Machine(db)
        self.buildDB = Build.Build()
        self.versionsDB = Versions.Versions(db)
        self.noOfThreads = 1  # Minimum Threads is 1
        self.teamdb = Teams.Teams(db)
        self.toolDB = Tool.Tool(db)
        self.deploymentunitDB = DeploymentUnit.DeploymentUnit()
        self.teamService = TeamService.TeamService()
        self.config_id = 3
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()
        self.ToolsonmachineDB = ToolsOnMachine.ToolsOnMachine(db)

    def load_configuration(self):
        '''
        General description:This method configures the load
        Args:
            none
        Returns:none

        '''
        ConfigHelperService.load_common_configuration(self)
        self.noOfThreads = int(self.result['noOfThreads'])
        if self.noOfThreads <= 0:
            raise ValueError(
                'CloneRequestService : No of parallel threads cannot be less than 1')
        self.depTimeoutInSec = int(self.result.get('depTimeoutInSec',60*60*2))
            

    def GetMachineDetails(self, machine_id):
        machine = self.machineDB.GetMachine(machine_id)
        return machine

    @ConfigHelperService.run
    def job_function(self):
        '''
        General description:# NEED TO HAVE THIS AS WHILE UPDATING CONFIG NEED TO RELOAD THIS
        # VARIABLE FOR RESCHEDULING
        Args:
            none
        Returns:none

        '''
        self.load_configuration()
        print 'started running at ' + time.ctime(time.time()) + \
            ' with ' + str(self.noOfThreads) + ' parallel threads'
        self.handleGroupDuAndToolDeploymentRequest()        
        print 'ended running at ' + time.ctime(time.time())

    def deployment_order(self, json):
        '''
        General description:
        Args:
            param1:json
        Returns:deployement order converted to int type

        '''
        """
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2"."""
        try:
            return int(json['deployment_order'])
        except KeyError:
            return 0

    # TODO NEED TO PERFORM CODE REVIEW
    def handleGroupDuAndToolDeploymentRequest(self):
        '''
        General description:This method HANDLE EACH GROUP DEPLOYMENT IN A SINGLE THREAD
        # GET ANY PENDING GROUP DEPLOYMENT REQUEST
        Args:
            none
        Returns:None

        '''
        pool = ThreadPoolExecutor(self.noOfThreads,__name__+".handleGroupDuAndToolDeploymentRequest")
        futures = []
        all_active_request = self.deploymentRequestGroupDB.get_pending_grp_depreq()
        for groupDeployment in all_active_request:
            groupDeployment = self.deploymentRequestGroupDB.get_group_deployment_request(
                str(groupDeployment['object_id']), False,False)
            groupDeployment.get("details").sort(
                key=self.deployment_order, reverse=False)
            failedDeploymentId = None
            for deploymentRequest in groupDeployment.get("details"):
                if str(deploymentRequest["status"]).lower() in ["New".lower(),
                                                                "Retry".lower(), "Processing".lower()]:
                    valid, failMessage, failedDeploymentId = \
                        self.validate_if_this_request_has_to_be_executed(
                            deploymentRequest["deployment_id"], groupDeployment)
                    if valid.lower() == "true":
                        print "Adding  _id:" + str(deploymentRequest["deployment_id"]) + " to deployment queue"
                        futures.append(pool.submit(self.do_stuff, deploymentRequest["deployment_id"]))            
                    elif valid.lower() == "false":
                        dep_data_update = {}
                        dep_data_update["_id"] = {"oid": failedDeploymentId}
                        dep_data_update["status"] = "Failed"
                        dep_data_update["status_message"] = failMessage
                        self.deploymentRequestDB.UpdateDeploymentRequest(
                            dep_data_update)
                        self.update_DeploymentGroups(failedDeploymentId),
                    elif valid.lower() == 'skip':
                        if failMessage is not None: #if there is a message, show it in the "response"
                            print 'Skipping _id: ' + failedDeploymentId + ' as it is already deployed on this machine'
                            dep_data_update = {}
                            dep_data_update["_id"] = {"oid": failedDeploymentId}
                            dep_data_update["status"] = 'Done'
                            dep_data_update["skipped_ind"] = True
                            dep_data_update["status_message"] = failMessage
                            dep_data_update["start_time"] = datetime.now()
                            dep_data_update["end_time"] = datetime.now()
                            self.deploymentRequestDB.UpdateDeploymentRequest(dep_data_update)                            
                        else:
                            print "Skipping _id:" + failedDeploymentId + " as the previous deployments are yet to take place"
            if failedDeploymentId :self.update_DeploymentGroups(failedDeploymentId)
        wait(futures)

    def validate_if_this_request_has_to_be_executed(self, deploymentRequestId, groupDeployment):
        '''
        General description:This method CHECK IF THIS REQUEST EXISTS
        Args:
            param1:deployementRequestId():This is the unique Id of deployementRequest which is stored in database
            param2:groupDeployment():
        Returns:none

        '''

        dep_data = self.deploymentRequestDB.GetDeploymentRequest(
            deploymentRequestId)
        if not dep_data:
            return "False", "The deployment_id: " + deploymentRequestId + \
                " does not exists in database", deploymentRequestId
        if not groupDeployment.get("details"):
            return "False", "The deployment does not have details list", deploymentRequestId
        if str(groupDeployment.get("deployment_type")).lower() not in ["dugroup", "toolgroup"]:
            return "False", "The deployment does not have deployment_type", deploymentRequestId
            # THE ENDING TRUE MEANS WE WANT TO BREAK
            # THE LOOP AND MARK THE GROUP DEPLOYMENT AS FAILED
            # WE NEED VALIDATIONS ONLY FOR DU GROUP
        if str(groupDeployment.get("deployment_type")).lower() in ["dugroup"]:
            if str(dep_data.get("dependent")).lower() in ["true"]:
                # THIS LIST IS SORTED BY DEPLOYMENT_ORDER
                for dep in groupDeployment.get("details"):
                    # WE CANNOT DEPLOY THIS
                    # ASSUMPTION IS THAT THE LIST IS SORTED SO FAILED REQUEST WILL COME EARLIER IN THIS LIST
                    if str(dep.get("deployment_id")) <> str(deploymentRequestId):
                        if str(dep.get("status")).lower() == "failed":
                            return "False", "Marked failed as _id: " + dep.get("deployment_id") + " has failed", deploymentRequestId
                        elif str(dep.get("status")).lower() in ["new", "retry", "processing"]:
                            return "Skip", None, deploymentRequestId
                        
            #CHECK DU MACHINE MATCHING CRITERIA
            is_skip = self.check_for_du_machine_matching(dep_data)
            if str(is_skip).lower() in ['true']:  # handle all types
                return 'skip', 'Skipped as deployment does not fulfill Du and Machine matching criteria', deploymentRequestId        
        
        #CHECK ALREADY DEPLOYED CRITERIA
        is_skip = self.is_skip_already_deployed(dep_data)
        if str(is_skip).lower() in ['true']:  # handle all types
            return 'skip', 'Skipped as build is already deployed on this machine and skip is true', deploymentRequestId
        
        return "True", None, deploymentRequestId

    def is_skip_already_deployed(self, dep_data):
        '''
        General description: This method CHECK IF NEED TO SKIP DEPLOYMENT OF ALREADY EXISTING BUILD ON THE MACHINE
        Returns: 'true' if need to skip deployment, or 'false' if needs to deploy this build
        '''           
        is_global_skip_flag = 'true'
        is_local_skip_flag = 'true'
        if_to_skip_decision = 'false'  # default is not to skip
        
        if str(dep_data.get("request_type")).lower() not in ["deploy", "redeploy"]:
            return if_to_skip_decision
        else:  
            machine_id = str(dep_data.get('machine_id'))
            build_id = str(dep_data.get('build_id'))
            parent_entity_id = str(dep_data.get('parent_entity_id'))
            existing_entry = self.ToolsonmachineDB.get_tools_on_machine_by_filter(machine_id, parent_entity_id, build_id)
    
            if existing_entry is not None:  # Meaning it is already deployed once
                configdb_data = self.configdb.getConfigByName("DeploymentRequestService")
                if configdb_data.get('skipDeploymentInd') is not None:
                    is_global_skip_flag = configdb_data.get('skipDeploymentInd') # if it is none, keep default value as true
    
                if dep_data.get('skip_dep_ind') is not None:  # Need to define it in the GUI
                    if_to_skip_decision = is_local_skip_flag = dep_data.get('skip_dep_ind')
                else:
                    if_to_skip_decision = is_global_skip_flag  # if local flag is not defined, take the global value
    
            else:  # If it is not deployed, always deploy it, ignoring the skip flags, return false to skip.
                if_to_skip_decision = 'false'
    
            return if_to_skip_decision
        
    def check_for_du_machine_matching(self, dep_data):
        '''
        General description: This method CHECK IF NEED TO SKIP DEPLOYMENT IF THE FA for DU and Machine do not match
        Returns: 'true' if need to skip deployment, or 'false' if needs to deploy this build
        '''           
        if_to_match_decision  = 'false'
        
        configdb_data = self.configdb.getConfigByName("DeploymentRequestService")        
        if dep_data.get('check_matching_ind') is not None:  # Need to define it in the GUI
            if_to_match_decision = str(dep_data.get('check_matching_ind')).lower()
        else:
            if configdb_data.get('machineMatchingInd') is not None:
                if_to_match_decision = str(configdb_data.get('machineMatchingInd')).lower()       
        
        # IF MATCHING IS NOT REQUIRED TO BE DONE RETURN SKIP AS FALSE
        if if_to_match_decision == "false" or str(dep_data.get("request_type")).lower() not in ["deploy", "redeploy"]:
            return "false" 
        else:  
            return self.decide_on_matching("compTypes",str(dep_data.get('machine_id')),str(dep_data.get('parent_entity_id')))
            
        
    def decide_on_matching(self,fa_name,machine_id,du_id): 
        #GET DETAILS
        machine_details=self.machineDB.GetMachine(machine_id)
        du_details=self.deploymentunitDB.GetDeploymentUnitById(du_id, True)
        
        #IF FA IS NOT PRESENT WE WILL NOT SKIP    
        if not du_details.get("flexible_attributes") or not machine_details.get("flexible_attributes"):
            return "true"
        if fa_name not in du_details.get("flexible_attributes").keys() or fa_name not in machine_details.get("flexible_attributes").keys():
            return "true" #THE FA IS NOT PRESENT SO WE WILL SKIP
        if du_details.get("flexible_attributes").get(fa_name) not in machine_details.get("flexible_attributes").get(fa_name).split(","):
            return "true" #THE FA IN DU IS NOT PRESENT IN MACHINE SO WE WILL SKIP
        return "false"                
           

    def do_stuff(self, deploymentRequestId):
        '''
        General description:Actual implementation
        Args:
            param1:deployementRequestId():This is the unique Id of deployementRequest which is stored in database
        Returns:none

        '''
        try:
            deployService = DeploymentServices.Deployment()
            ######################
            #  PERFORM ACTUAL task
            ######################
            print '' + threading.currentThread().getName(), \
                'Started for _id :' + str(deploymentRequestId)
            deployService.start_deployment_process(deploymentRequestId)
            self.update_DeploymentGroups(deploymentRequestId)
            self.groupDeploymentMail(deploymentRequestId)
            print '' + threading.currentThread().getName(), \
                'Ended for _id :' + str(deploymentRequestId)
        except Exception as e:  # catch *all* exceptions
            print '' + threading.currentThread().getName(), \
                '_id :' + str(deploymentRequestId) + \
                ' failed with Error :' + str(e)
            traceback.print_exc()

    @synchronized
    def groupDeploymentMail(self, deployment_request_id):
        '''
        General description:This method create content data for mail o be sent after deployment and
         save it in database after converting to mail template using mailer.send_html_notification
        Args:
            param1:deployment_request_id():This is the unique Id of deployementRequest which is stored in database
        Returns:none

        '''

        try:
            groupDeployment = \
                self.deploymentRequestGroupDB.get_grp_depreq_by_inner_depreq_ids(
                    deployment_request_id)
            if groupDeployment.get("status").lower() == \
                    "done" or groupDeployment.get("status").lower() == "failed":
                if groupDeployment.get("requested_by"):
                    requested_by = groupDeployment.get("requested_by")
                    if requested_by:
                        user_details = self.userDB.get_user(
                            requested_by, False)
                        if user_details and user_details.get("email"):
                            all_tool_du_data = []
                            successCount = 0
                            for unit in groupDeployment.get("details"):
                                unit_data = {}
                                if unit.get("status"):
                                    unit_data["status"] = unit.get("status")
                                    if unit.get("status").lower() == "done":
                                        successCount = successCount + 1
                                if unit.get("status_message"):
                                    unit_data["status_message"] = unit.get(
                                        "status_message")
                                if unit.get("deployment_order"):
                                    unit_data["deployment_order"] = unit.get(
                                        "deployment_order")
                                if unit.get("deployment_id"):
                                    deploymentRequestId = unit.get(
                                        "deployment_id")
                                    unit_data["deployment_id"] = deploymentRequestId
                                    unitDeploymentData = \
                                        self.deploymentRequestDB.GetDeploymentRequest(
                                            deploymentRequestId)
                                    if unitDeploymentData:
                                        if unitDeploymentData.get("machine_id"):
                                            machineDetails = \
                                                self.machineDB.GetMachine(
                                                    unitDeploymentData.get("machine_id"))
                                            if machineDetails and machineDetails.get("machine_name"):
                                                unit_data["machine_name"] = machineDetails.get(
                                                    "machine_name")
                                            if machineDetails and machineDetails.get("host"):
                                                unit_data["machine_host"] = machineDetails.get(
                                                    "host")
                                        if unitDeploymentData.get("deployment_type") == 'toolgroup':
                                            if unitDeploymentData.get("parent_entity_id"):
                                                toolDetails = self.toolDB.get_tool_by_version(
                                                    unitDeploymentData.get("parent_entity_id"), True)
                                                if toolDetails.get(
                                                        "version", {}).get('version_number'):
                                                    unit_data["version_number"] = toolDetails.get(
                                                        "version", {}).get('version_number')
                                                if toolDetails.get(
                                                        "version", {}).get('version_name'):
                                                    unit_data["version_name"] = toolDetails.get(
                                                        "version", {}).get('version_name')
                                                if toolDetails.get(
                                                        "version", {}).get('tool_id'):
                                                    unit_data["parent_entity_id"] = toolDetails.get(
                                                        "version", {}).get('tool_id')
                                                if toolDetails.get("name"):
                                                    unit_data["parent_entity_name"] = toolDetails.get(
                                                        "name")
                                        else:
                                            duData = self.deploymentunitDB.GetDeploymentUnitById(
                                                unitDeploymentData.get("parent_entity_id"), False)
                                            unit_data["parent_entity_id"] = str(
                                                duData["_id"])
                                            unit_data["parent_entity_name"] = duData["name"]
                                        if unitDeploymentData.get("build_id"):
                                            buildDetail = self.buildDB.get_build(
                                                unitDeploymentData.get("build_id"))
                                            if buildDetail and buildDetail.get("build_number"):
                                                unit_data["build_number"] = buildDetail.get(
                                                    "build_number")
                                        if unitDeploymentData.get("request_type"):
                                            unit_data["type"] = unitDeploymentData.get(
                                                "request_type")
                                        if unitDeploymentData.get("unitDeploymentData"):
                                            unit_data["type"] = buildDetail.get(
                                                "unitDeploymentData")
                                        if unitDeploymentData.get("start_time"):
                                            unit_data["start_time"] = unitDeploymentData.get(
                                                "start_time")
                                        if unitDeploymentData.get("end_time"):
                                            unit_data["end_time"] = unitDeploymentData.get(
                                                "end_time")

                                all_tool_du_data.append(unit_data)
                                # end of "for unit in  groupDeployment.get("
                            numOfUnits = len(all_tool_du_data)
                            finalData = {
                                "goup_data": {

                                    "name": requested_by,
                                    "type": groupDeployment.get("deployment_type"),
                                    "status": groupDeployment.get("status"),
                                    "request_id": deployment_request_id,
                                    "create_date": groupDeployment.get("create_date"),
                                    "total_requested": numOfUnits,
                                    "total_compleated": successCount
                                },
                                "all_tool_du_data": all_tool_du_data
                            }

                            email_to = self.teamService.get_user_permissions(str(user_details.get("_id")))[
                                "distribution_list_list"]
                            self.mailer.send_html_notification(
                                ','.join(email_to), None, None, 13, finalData)
                        print "DeploymentServices :Email was sent with details:" + str(finalData)
                    else:
                        print "DeploymentServices :Email was not sent as request_by is missing"
        except Exception as e:  # catch *all* exceptions
            print "Failed to save email" + str(e)
            traceback.print_exc()

    @synchronized
    def callbackUrl(self, groupDeployment):
        # CALLBACK URL
        enable_callback = self.configdb.getConfigByName('DeploymentRequestService').get("enable_callback")
        if enable_callback == "false" or not enable_callback:
            return
        if not groupDeployment.get("status") in ["Done","Failed"]:
            return
        if not groupDeployment.get("callback"):
            return
        callback_url = groupDeployment.get("callback").get("callback_url")
        if not callback_url:
            return
        callback_json = {"_id": groupDeployment["_id"]["oid"], "status": groupDeployment["status"],
                         "status_message": groupDeployment["status_message"]}
        callback_timeout = self.configdb.getConfigByName('DeploymentRequestService').get("callback_timeout",30)
        callback_status = "Done"
        try:
            response = requests.post(callback_url, json=callback_json, timeout=callback_timeout, verify=False)
            response.raise_for_status()
        except Exception as e:  # catch *all* exceptions
            callback_status = 'Error in request to callback url ' + callback_url + ' : ' + str(e)
            print callback_status
            traceback.print_exc()
        finally:
            groupDeployment["callback"]["callback_status"] = callback_status

    @synchronized
    def update_DeploymentGroups(self, deployment_request_id):
        '''
        General description:This method GEt the group of deployment request associated with this request
        Args:
           param1: deployement_request_id():This is the unique Id of deployementRequest which is stored in database
        Returns:none

        '''
        group_status_details = []
        groupDeployment = \
            self.deploymentRequestGroupDB.get_grp_depreq_by_inner_depreq_ids(
                deployment_request_id)
        if groupDeployment:
            if groupDeployment.get("details") and len(groupDeployment.get("details")) > 0:
                status_list = []
                for deploymentRequestEntry in groupDeployment.get("details"):
                    deploymentRequestData = self.deploymentRequestDB.GetDeploymentRequest(
                        deploymentRequestEntry["deployment_id"])
                    if deploymentRequestData:
                        if deploymentRequestData.get("status"):
                            if deploymentRequestData.get("status").lower() not in status_list:
                                status_list.append(deploymentRequestData.get(
                                    "status").lower())  # SAME ALL DISTINCT STATUS
                        # ADD TO GROUP STATUS
                        deploymentRequestEntry["status"] = str(
                            deploymentRequestData.get("status"))
                        if "skipped_ind" in deploymentRequestData.keys():
                            deploymentRequestEntry["skipped_ind"]=deploymentRequestData.get("skipped_ind")
                        deploymentRequestEntry["status_message"] = str(
                            deploymentRequestData.get("status_message"))
                        group_status_details.append(deploymentRequestEntry)

                # CONDITION CHECK AND UPDATE THE GROUP
                if "Retry".lower() in status_list or "New".lower() in \
                        status_list or "Processing".lower() in status_list:
                    groupDeployment["status"] = "Processing"
                    groupDeployment["status_message"] = "Execution is in progress"
                elif "Failed".lower() in status_list and len(status_list) == 1:
                    groupDeployment["status"] = "Failed"
                    groupDeployment["status_message"] = "The request has failed"
                elif "Done".lower() in status_list and len(status_list) == 1:
                    groupDeployment["status"] = "Done"
                    groupDeployment["status_message"] = "The request has completed"
                elif "Done".lower() in status_list and \
                        "Failed".lower() in status_list and len(status_list) == 2:
                    groupDeployment["status"] = "Failed"
                    groupDeployment["status_message"] = "The request has partially completed"
                # UPDATE THE GROUP
                groupDeployment["_id"] = {"oid": str(groupDeployment["_id"])}
                groupDeployment["details"] = group_status_details

                self.callbackUrl(groupDeployment)
                self.deploymentRequestGroupDB.upd_group_depreq(groupDeployment)

    @synchronized
    def retryDeploymentRequest(self, deployment_id):
        '''
        General description:This method retries the deployement request for the given deployement
        _id
        Args:
            param1:deployement_id():This is the unique Id of deployement which is stored in database
        Returns:none

        '''
        try:
            ###########################################
            # looping around current step id           #
            # only current step will be update to retry#
            # for now all steps are mandatory in deployment#
            ###########################################
            deployment_request = self.deploymentRequestDB.GetDeploymentRequest(
                deployment_id)
            if deployment_request.get('status').lower() != 'failed':
                return -1
            deployment_request_id = deployment_request["_id"]
            deployment_request["_id"] = {
                "oid": str(deployment_request["_id"])}
            deployment_request["status"] = "Retry"
            self.deploymentRequestDB.UpdateDeploymentRequest(
                deployment_request)
            retryCount = deployment_request.get("retry_count")
            if retryCount is None:
                retryCount = "1"
            else:
                retryCount = str(int(retryCount) + 1)
            for step in deployment_request.get("step_details"):
                if step.get("step_status").lower() == "Failed".lower():
                    self.deploymentRequestDB.UpdateStepDetails(deployment_request_id, step.get(
                        "step_id"), step_status='Retry', step_end_time="", step_duration="", step_message="")
                    if step.get("nested_step_details"):
                        #######################################################################
                        # in future if it is decided to update all Failed step                 #
                        # that is including non mandatory Failed steps, then we need to loop on#
                        #######################################################################
                        # for inner_steps in step.get("nested_step_details"):
                            # if inner_steps.get("status")=="Failed"
                            # current_inner_step_id=inner_steps.get("step_id")
                            # self.deploymentRequestDB.UpdateNestedStepDetails(deployment_request_id,step.get("step_id"),current_inner_step_id, step_status='Retry',step_end_time="",step_duration="",step_message="")
                        #######################################################################
                        current_inner_step_id = step.get("current_step_id")
                        self.deploymentRequestDB.UpdateNestedStepDetails(deployment_request_id, step.get(
                            "step_id"), current_inner_step_id, step_status='Retry', step_end_time="", step_duration="", step_message="")
            self.update_DeploymentGroups(deployment_id)
            return 1
        except Exception as e:
            return (str(e))

    def schedule(self):
        '''
        General description:# Schedules the job
        # scheduler :Scheduler object
        # interval_given:Time interval for job to rerun
        Args:
            none
        Returns:none

        '''
        global job
        self.load_configuration()
        job = self.schedulerService.schedule(job, self)