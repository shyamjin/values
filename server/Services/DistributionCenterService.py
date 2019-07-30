'''
Created on Mar 16, 2016

@author: PDINDA
'''

###############################
# DistributionCenterService Scheduler
###############################
from datetime import datetime
import logging
import os
import time
import traceback

from autologging import logged
from fabfile import copyToRemote, createFolder
from DBUtil import Config, Machine, SystemDetails
from DBUtil import DistributionMachine
from Services import SchedulerService
from Services import SyncServices, Mailer, ConfigHelperService, RemoteAuthenticationService
from settings import distribution_center_export_full_path



job = None


@logged(logging.getLogger("DistributionCenterService"))
class DistributionCenterService(object):

    # Init's Data
    def __init__(self, db):
        """Initializing Variable """
        self.configdb = Config.Config(db)
        self.distributionMachinetDB = DistributionMachine.DistributionMachine(
            db)
        self.syncService = SyncServices.SyncServices()
        self.machineDB = Machine.Machine(db)
        self.mailer = Mailer.Mailer()
        self.current_path = distribution_center_export_full_path
        self.systemDetailsDb = SystemDetails.SystemDetails(db)
        if not os.path.exists(self.current_path):
            os.makedirs(self.current_path)
        if not os.access(os.path.dirname(self.current_path), os.W_OK):
            raise ValueError(
                "The directory does not have write access :" + self.current_path)
        systemDetail = self.systemDetailsDb.get_system_details_single()
        if not systemDetail:
            raise Exception("systemDeatils not found")
        if not systemDetail.get("hostname"):
            raise Exception("hostname not found in systemDeatils")
        self.remote_trigger_api_path = "/clonerequest/distribution/pull/" + \
            systemDetail.get("hostname")
        self.config_id = 12
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()
        self.remote_authentication_service = RemoteAuthenticationService.RemoteAuthenticationService()

    def load_configuration(self):
        ConfigHelperService.load_common_configuration(self)
        if self.result.get("remote_machine_import_path") is None:
            raise Exception(
                "remote_machine_import_path not found in config")
        else:
            self.remote_machine_import_path = self.result.get(
                "remote_machine_import_path")

    # Checks no of pending requests
    # Creates sub threads to handle this requests # Minimum Threads is 1
    # The no of threads is configurable from main.py
    # (DeploymentService.DeploymentService(db).schedule(schedulerObj,1,1))
    @ConfigHelperService.run
    def job_function(self, id=None):
        """Start of DistributionCenterService"""
        print ' started running at ' + time.ctime(time.time())
        self.load_configuration()
        machines_to_distribute_to = []  # WE WILL ADD ALL MACHINE DETAILS HERE
        do_distribute = True  # IND to decide if we want to distribute
        status_email = []
        file_created = toolNameExported = toolNamesNotExported = None  # INTILIZE
        if id:
            rec = self.distributionMachinetDB.GetDistributionMachineRequest(
                str(id))
            if not rec:
                # Manual call so return an error
                raise Exception("No record with _id :" +
                                str(id) + " was found")
            else:
                machines_to_distribute_to.append(rec)
        else:
            result = self.distributionMachinetDB.GetAllDistributionMachineRequests(
                "on")
            if not result:
                print " No machine found for distribution.Skipping"
            else:
                for record in result:
                    machines_to_distribute_to.append(record)
        if len(machines_to_distribute_to) >= 1:  # IF WE HAVE ANY MACHINES TO DISTRIBUTE TO
            try:
                file_created, toolNameExported, toolNamesNotExported = self.prepareRequest()
                print 'File was created ' + file_created
                if not os.path.exists(file_created):
                    raise Exception(
                        "Created File was not found :" + file_created)
            except Exception as e_value:  # catch *all* exceptions
                print 'failed to create file:' + "with error" + str(e_value)
                do_distribute = False
                for rec in machines_to_distribute_to:
                    id_oid = str(rec["_id"])
                    rec["_id"] = {}
                    rec["_id"]["oid"] = id_oid
                    print 'failed to process request for :' \
                        + rec.get('host') + ' with error ' + str(e_value)
                    rec["distribution_status"] = "failed"
                    rec["distribution_step"] = "Error :" + str(e_value)
                    rec["tools_exported"] = str(None)
                    rec["tools_not_exported"] = str(None)
                    rec["update_date"] = datetime.now()
                    status_email.append('Host :' + rec.get('host') + ' Status :'
                                        + rec['distribution_status'] +
                                        ' Message :'
                                        + rec['distribution_step'])
                    self.distributionMachinetDB.UpdateDistributionMachineRequest(
                        rec)
                if id:
                    raise Exception(e_value)  # Manual call so return an error
        else:
            print " No machine found for distribution.Skipping"
            return  # NOTHING TO DO

        if do_distribute:
            for rec in machines_to_distribute_to:
                try:
                    id_oid = str(rec["_id"])
                    rec["_id"] = {}
                    rec["_id"]["oid"] = id_oid
                    rec["distribution_status"] = "started"
                    rec["distribution_step"] = "Starting the process"
                    rec["tools_exported"] = str(None)
                    rec["tools_not_exported"] = str(None)
                    rec["update_date"] = datetime.now()
                    self.validate(rec)
                    self.distributionMachinetDB.UpdateDistributionMachineRequest(
                        rec)
                    machine_details = self.machineDB.GetMachine(
                        rec.get("machine_id"))
                    self.remote_authentication_service.authenticate(
                        machine_details, self.push, rec, file_created)
                    rec["distribution_status"] = "success"
                    rec["distribution_step"] = "The file : " + \
                        str(file_created) + " was pushed"
                    rec["update_date"] = datetime.now()
                    rec["tools_exported"] = toolNameExported
                    rec["tools_not_exported"] = toolNamesNotExported
                    self.distributionMachinetDB.UpdateDistributionMachineRequest(
                        rec)
                    status_email.append('Host :' + rec.get('host') + ' Status :'
                                        + rec['distribution_status']
                                        + ' Message :' + rec['distribution_step'])
                except Exception as e_value:  # catch *all* exceptions
                    print 'failed to process request for :' \
                        + rec.get('host') + ' with error ' + str(e_value)
                    rec["distribution_status"] = "failed"
                    rec["distribution_step"] = "Error :" + str(e_value)
                    rec["tools_exported"] = str(None)
                    rec["tools_not_exported"] = str(None)
                    self.distributionMachinetDB.UpdateDistributionMachineRequest(
                        rec)
                    status_email.append('Host :' + rec.get('host') + ' Status :'
                                        + rec['distribution_status']
                                        + ' Message :' + rec['distribution_step'])
                    if id:
                        # Manual call so return an error
                        raise Exception(e_value)
        if len(status_email) > 0:
            self.notify(status_email, toolNameExported, toolNamesNotExported)
        print ' ended running at ' + time.ctime(time.time())

    # Notify users about the request
    def notify(self, status_email, toolNameExported, toolNamesNotExported):
        """Notify User after Pushed"""
        if self.result.get('distribution_list') is not None \
                and len(self.result.get('distribution_list')) > 0:
            try:
                self.mailer.send_html_notification(self.result.get('distribution_list'), None, None, 10, {
                    'name': 'User',
                    'list': status_email,
                    'exported': toolNameExported,
                    'notexported': toolNamesNotExported, })
                print 'Users have been notified :' \
                    + self.result.get('distribution_list')
            except Exception as e_value:
                traceback.print_exc()
                print 'failed to start with error : :' + str(e_value)
                print 'File was pushed but notification failed for :' \
                    + self.result.get('distribution_list')

    # Prepare to push to machine
    def prepareRequest(self):
        """Prepared Zip File For Push"""
        fileName = 'DPM_tools_manifest_' + datetime.now().strftime("%Y-%m-%d")        
        file_created, toolName, toolNamesNotExported = self.syncService.createZipToExport({"file_path":self.current_path,"zip_file_name":fileName,\
            "target_host":"Multiple","sync_type":"distribute","download_artifacts":False,"get_tools":True,"get_dus":False},None)
        if file_created is not None:
            if os.path.isfile(file_created) not in [True]:
                raise ValueError(
                    "Zip file was not created for push to: Multiple")
            else:
                return file_created, toolName, toolNamesNotExported
        else:
            raise ValueError(
                "Zip file was not created for push to : Multiple")

    def validate(self, rec):
        """Validate Machine Id"""
        if rec.get("host") is None:
            raise Exception("host was not found in request")
        if rec.get("machine_id") is None:
            raise Exception("machine_id was not found in request")
        machine = self.machineDB.GetMachine(rec.get("machine_id"))
        if machine is None:
            raise Exception("machine_id with id " +
                            rec.get("machine_id") + " was not found")
        else:
            if machine.get("host") and machine.get("username") and machine.get("password") in [None, ""]:
                raise Exception(
                    "Either host,username,password  was not found in request")

    def push(self, rec, file_created, **kwargs):
        """Start to Pushing file"""
        if self.result.get("remote_machine_import_path") is None:
            raise Exception("remote_machine_import_path not found in config")
        print 'Getting details for machine id :' + rec.get("machine_id")
        machine_details = self.machineDB.GetMachine(rec.get("machine_id"))
        print 'Trying to push file' + file_created \
            + ' to ' + machine_details['host']
        rec["distribution_status"] = "pushing"
        rec["distribution_step"] = "Trying to push file  "
        rec["update_date"] = datetime.now()
        self.distributionMachinetDB.UpdateDistributionMachineRequest(rec)
        if rec.get("folder_location") is not None:
            if len(rec.get("folder_location")) > 1:
                print 'folder_location was found. Pushing to :' \
                    + rec.get('folder_location')
                try:
                    createFolder(rec.get("folder_location"), **kwargs)
                except Exception as e_value:  # catch *all* exceptions
                    print ' Create folder  :' \
                        + rec.get('folder_location') + \
                        ' with error ' + str(e_value)
                    traceback.print_exc()
                copyToRemote(file_created, rec.get(
                    "folder_location"), **kwargs)
            else:
                raise ValueError("Invalid folder_location" +
                                 rec.get("folder_location"))
        else:
            print 'Pushing to :' \
                + self.result.get('remote_machine_import_path')
            try:
                createFolder(self.result.get(
                    "remote_machine_import_path"), **kwargs)
            except Exception as e_value:  # catch *all* exceptions
                print ' Create folder  :' \
                    + self.result.get('remote_machine_import_path') + ' with error ' \
                    + str(e_value)
                traceback.print_exc()
            copyToRemote(file_created, self.result.get(
                "remote_machine_import_path"), **kwargs)
            print 'Pushed file' + file_created + ' to ' \
                + machine_details['host']

    def schedule(self):
        """
        # Schedules the job
        # scheduler :Scheduler object
        # interval_given:Time interval for job to rerun"""
        global job
        self.load_configuration()
        job = self.schedulerService.schedule(job, self)
