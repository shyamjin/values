'''
Created on OCT 12, 2016

@author: PDINDA
'''

###############################
# CleanerServices Scheduler
###############################

from datetime import datetime
import logging
from os import listdir
import os,json
from os.path import isfile, join  # , basename, dirname, isdir
import shutil
import subprocess
import time
import traceback

from autologging import logged

from DBUtil import Config, Tool, Versions, MediaFiles, Users, Role, \
    Emails, ContributionGitPushLogs, Sync, DistributionSync, Build, \
    DeploymentRequest, CloneRequest,DeploymentUnit,Auditing,Repository
from Services import SchedulerService, ConfigHelperService, FileUtils,Utils,\
    HelperServices, CustomClassLoaderService
from settings import import_full_path, \
    export_full_path, distribution_center_import_full_path, \
    distribution_center_export_full_path, current_path, logo_path, \
    media_path, media_full_path, archives_full_path




job = None


@logged(logging.getLogger("CleanerServices"))
class CleanerServices(object):

    # Init's Data
    def __init__(self, db):
        '''
           General description :
           This function initializes the database variables and \
           index to refer in functions.
        '''
        self.db = db
        self.configdb = Config.Config(db)
        self.toolDB = Tool.Tool(self.db)
        self.userDB = Users.Users(self.db)
        self.roleDB = Role.Role(self.db)
        self.buildsDB = Build.Build()
        self.versionsDB = Versions.Versions(db)
        self.emailsDB = Emails.Emails(self.db)
        self.deploymentRequestDB = DeploymentRequest.DeploymentRequest(db)
        self.CloneRequestDB = CloneRequest.CloneRequest(db)
        self.contributionGitPushLogs = ContributionGitPushLogs.ContributionGitPushLogs(
            db)
        self.sync = Sync.Sync(db)
        self.auditingDB = Auditing.Auditing()
        self.distributionSync = DistributionSync.DistributionSync(db)
        self.mediaFilesDB = MediaFiles.MediaFiles(self.db)
        self.logo_path = logo_path
        self.full_logo_path = str(current_path) + self.logo_path
        self.media_files_path = media_path
        self.full_media_files_path = media_full_path
        self.folder_list_to_clean = [
            export_full_path,
            distribution_center_export_full_path
        ]
        self.config_id = 15
        self.load_configuration()
        self.schedulerService = SchedulerService.SchedulerService()
        self.deploymentUnitDB = DeploymentUnit.DeploymentUnit()
        self.repositoryDB=Repository.Repository()
        
    def load_configuration(self):
        '''
        General description:This method configures the load
        Args:
            none
        Returns:none

        '''
        ConfigHelperService.load_common_configuration(self)
        if self.result.get("olderthandays") is not None:
            self.olderthandays = int(self.result["olderthandays"])
        else:
            raise Exception("olderthandays not found for CleanerServices")
        if self.result.get("buildolderthandays"):
            self.buildolderthandays = int(self.result["buildolderthandays"])
        else:
            raise Exception("buildolderthandays not found for CleanerServices")
        if self.result.get("buildcount"):
            self.buildCount = int(self.result["buildcount"])
        else:
            raise Exception("buildcount not found for CleanerServices")
        if self.result.get("RemoveActualArtifacts"):
            self.remove_actual_artifacts = self.result["RemoveActualArtifacts"]
        else:
            raise Exception("RemoveActualArtifacts value not found for CleanerServices")
        if self.result.get("EntitiesToHandle") is not None:
            self.entities_to_handle = self.result.get("EntitiesToHandle")
        else:
            raise Exception("EntitiesToHandle value not found for CleanerServices")
            
    # Checks no of pending requests
    # Creates sub threads to handle this requests # Minimum Threads is 1
    @ConfigHelperService.run
    def job_function(self):
        '''
        General description:start of a cleaner sevice
        Args:
            none
        Returns:none

        '''
        print ' started running at ' + time.ctime(time.time())
        self.load_configuration()
        now = datetime.now().replace(tzinfo=None)
        # CLEAN LOGOS
        if self.entities_to_handle.get("0") is True:
            self.clean_logos()
        # CLEAN MEDIAFILES
        if self.entities_to_handle.get("1") is True:
            self.clean_media_files()
        # CLEAN EMAILS
        if self.entities_to_handle.get("2") is True:
            self.clean_emails(now)
        # CLEAN GUEST USERS
        if self.entities_to_handle.get("3") is True:
            self.clean_guest_users(now)
        # CLEAN GIT PUSH
        if self.entities_to_handle.get("4") is True:
            self.clean_git_logs(now)
        # CLEAN SYNC
        # LOGIC IS TO FIND OUT ALL SYNC THAT WERE COMPLETELY SUCESSFULL
        # DETELE ALL RELATED RECORDS AND THERE FILES AD FOLDERS
        if self.entities_to_handle.get("5") is True:
            self.clean_sync(now)
        # CLEAN DISTRIBUTION
        # LOGIC IS TO FIND OUT ALL DISTRIBUTION THAT WERE CANCELLED
        # DETELE ALL RELATED RECORDS AND THERE FILES AD FOLDERS
        if self.entities_to_handle.get("6") is True:
            self.clean_distribution(now)
        # CLEAN ALL INACTIVE BUILDS
        if self.entities_to_handle.get("7") is True:
            self.clean_invalid_builds(now)
    
        # CLEAN ACTIVE BUILDS WHERE COUNT IS GREATER AND OLDER THAN LIMIT
        if self.entities_to_handle.get("8") is True:
            self.clean_active_builds(now,self.versionsDB.get_all_version())
            self.clean_active_builds(now,self.deploymentUnitDB.GetAllDeploymentUnits())
        # Check if we have 30 days old log in deployementRequestDb then clean
        # this log.
        if self.entities_to_handle.get("9") is True:
            self.clean_dep_req_logs(now)
        # Check if we have 30 days old log in CloneRequestDB then clean this
        # log.
        if self.entities_to_handle.get("10") is True:
            self.clean_clone_req_logs(now)
        
        # CLEAN FOLDERS FILES
        # DELETE ALL FILES AND FOLDERS FROM EXPORT DIRECTORY
        if self.entities_to_handle.get("11") is True:
            self.clean_old_data(self.folder_list_to_clean, None, self.olderthandays)
        
        if self.entities_to_handle.get("12") is True:
            self.clean_auditing(now)
    # Check if we have old data
    def clean_old_data(self, path_list, file_Name=None, olderthandays=30):
        '''
        General description:This method cleans the old data.
        Args:
            param1:path_list:this is path of files/directories which needs to be cleaned.
            param2:file_name:this is name of files/directories which needs to be cleaned.
            param3:olderthandays:this is no of days old for which a file needs to be deleted.
        Returns:none

        '''
        now = time.time()
        # Number of seconds in two days
        days_ago = now - 60 * 60 * 24 * float(olderthandays)
        for location in path_list:

            filesOrDirs = [f for f in [listdir(location)]]
            if filesOrDirs is not None:
                if len(filesOrDirs) <= 0:
                    print 'clean_old_data:No pending files/directories to remove'
                for rec in filesOrDirs:
                    for fileOrDir in rec:
                        try:  # CAN FAIL PER LINE
                            if os.path.exists(join(location, fileOrDir)):
                                path = join(location, fileOrDir)
                                if (os.path.isfile(path) or os.path.isdir(path)) \
                                        and os.access(path, os.W_OK):
                                    fileCreation = os.path.getctime(path)
                                    if fileCreation < days_ago:
                                        print '' \
                                            + str(path) + ' is more than ' + str(olderthandays) \
                                            + ' days old.Deleteing It'
                                    if file_Name:
                                        print 'Will delete files/directory having name ' \
                                            + file_Name + 'present at path :' + path
                                        if os.path.isfile(path) \
                                                and file_Name in path:
                                            os.remove(path)
                                            print 'File' \
                                                + str(path) + 'was deleted'
                                        elif os.path.isdir(path) \
                                                and file_Name in path:
                                            shutil.rmtree(path)
                                            print ' Directory ' \
                                                + str(path) + ' was deleted'
                                    else:
                                        print 'Will delete all files/directory present at path :' \
                                            + path
                                        if os.path.isfile(path):
                                            os.remove(path)
                                            print 'File' \
                                                + str(path) + 'was deleted'
                                        elif os.path.isdir(path):
                                            shutil.rmtree(path)
                                            print ' Directory ' \
                                                + str(path) + ' was deleted'
                        except Exception, e_value:
                            print 'clean_old_data: Error while deleting file :' \
                                + str(e_value)
    def clean_logos(self):   
        if os.path.isdir(self.full_logo_path):
                for f in [f for f in listdir(self.full_logo_path)
                          if isfile(join(self.full_logo_path, f)) if 'default'
                          not in f if not self.toolDB.is_file_present(str(f))]:
                    os.remove(join(self.full_logo_path, f))
                    print ' File ' + str(join(self.full_logo_path, f)) + ' was deleted'
    def clean_media_files(self): 
        if os.path.isdir(self.full_media_files_path):
                for f in [f for f in listdir(self.full_media_files_path)
                          if isfile(join(self.full_media_files_path, f))
                          if not self.mediaFilesDB.is_file_present(str(f))]:
                    os.remove(join(self.full_media_files_path, f))
                    print "File" + str(join(self.full_media_files_path, f)) + "was deleted"
    def clean_emails(self,now):
        for rec in self.emailsDB.GetAllEmails():
                if (now - rec['_id'].generation_time.replace(tzinfo=None)).days > self.olderthandays:
                    self.emailsDB.RemoveEmail(str(rec['_id']))
                    print "Document of Collection Emails" + str(rec['_id']) + "was deleted"
    def clean_guest_users(self,now):
        for rec in self.userDB.get_all_users():
                role = self.roleDB.get_role_by_id(rec["roleid"], False)
                if role and str(role.get("name")).lower() in ["Guest".lower()]:
                    if(now - rec['_id'].generation_time.replace(tzinfo=None)).days > self.olderthandays:
                        self.userDB.delete_user(str(rec['_id']))
                        print "Document of Users" + str(rec['_id']) + "was deleted"
    def clean_git_logs(self,now):
        for rec in self.contributionGitPushLogs.ContributionGitPushLogsAll():
                if (now - rec['_id'].generation_time.replace(tzinfo=None)).days > self.olderthandays:
                    self.contributionGitPushLogs.DeleteContributionGitPushLogs(
                        str(rec['_id']))
                    print ' Document of Collection ContributionGitPushLogs ' \
                        + str(rec['_id']) + ' was deleted'
                        
    def clean_sync(self,now):
        sync_data_to_archive=[]
        sync_archive_dir=os.path.join(archives_full_path,"sync",now.strftime("%d%m%Y%H%M%S"))
        sync_file_name=os.path.join(sync_archive_dir,now.strftime("%d%m%Y%H%M%S")+".json")
        for rec in self.sync.sync_all():
                if (now - rec['_id'].generation_time.replace(tzinfo=None)).days > self.olderthandays:
                    if set(list(self.sync.sync_distinct_status(rec['sync_id']))) <= set(["success","skipped"]) :
                        sync_data_to_archive.append(json.loads(Utils.JSONEncoder().encode(rec)))
                        print "Document of Collection Sync " + str(rec['_id']) + " was archived"
        if sync_data_to_archive:
            FileUtils.mkdirs([sync_archive_dir], True)
            FileUtils.jsontoFile(sync_file_name,sync_data_to_archive)
            FileUtils.createZipFile(sync_archive_dir,sync_archive_dir)
            shutil.rmtree(sync_archive_dir, True)
            for rec in sync_data_to_archive:
                print "Document of Collection Sync" + str(rec['_id']) + "was removed"
                self.sync.remove_sync(str(rec['_id']))                
                # WE WILL DELETE FOLDERS HERE.THE FILES ARE NOT REQUIRED SO
                # THEY WERE CLEANED AS PART OF clean_old_data
                folder_list_to_clean = [import_full_path]
                if rec.get("stored_folder_name"):
                    self.clean_old_data(folder_list_to_clean, os.path.basename(
                        rec.get("stored_folder_name")), 0)
  
    def clean_auditing(self,now):
        auditing_data_to_archive=[]
        auditing_archive_dir=os.path.join(archives_full_path,"auditing",now.strftime("%d%m%Y%H%M%S"))
        auditing_file_name=os.path.join(auditing_archive_dir,now.strftime("%d%m%Y%H%M%S")+".json")
        for rec in self.auditingDB.get_all():
                if (now - rec['_id'].generation_time.replace(tzinfo=None)).days > self.olderthandays:
                    auditing_data_to_archive.append(json.loads(Utils.JSONEncoder().encode(rec)))
                    print "Document of Collection Auditing " + str(rec['_id']) + " was archived"
        if auditing_data_to_archive:
            FileUtils.mkdirs([auditing_archive_dir], True)
            FileUtils.jsontoFile(auditing_file_name,auditing_data_to_archive)
            FileUtils.createZipFile(auditing_archive_dir,auditing_archive_dir)
            shutil.rmtree(auditing_archive_dir, True)
            self.auditingDB.remove_all_older_than_date(self.olderthandays)               
                
                                      
    def clean_distribution(self,now):
        for rec in self.distributionSync.GetDistributeRequestAll():
                if (now - rec['_id'].generation_time.replace(tzinfo=None)).days > self.olderthandays:
                    self.distributionSync.DeleteDistribution(str(rec['_id']))
                    print ' Document of Collection DistributionSync ' \
                        + str(rec['_id']) + ' was deleted'
                    # WE WILL DELETE FOLDERS HERE.THE FILES ARE NOT REQUIRED SO
                    # THEY WERE CLEANED AS PART OF clean_old_data
                    folder_list_to_clean = [distribution_center_import_full_path]
                    if rec.get("stored_folder_name"):
                        self.clean_old_data(folder_list_to_clean, os.path.basename(
                            rec.get("stored_folder_name")), 0)
                        
    def remove_artifact(self,build_details):
        parent_details = HelperServices.get_details_of_parent_entity_id(build_details.get("parent_entity_id")) 
        repository_to_use = parent_details.get("repository_to_use")  
        if not repository_to_use : raise Exception("Missing key: repository_to_use in parent details")
        repo_details = self.repositoryDB.get_repository_by_name(repository_to_use, False)
        deployer_module="Plugins.repositoryPlugins."+repo_details.get("handler")
        class_obj=CustomClassLoaderService.get_class(deployer_module)
        method = getattr(class_obj(repo_details),"trnx_handler") # MEDHOD NAME
        keyargs={"transaction_type":"delete","build_details":build_details}
        method(**keyargs)            

                            
    def clean_invalid_builds(self,now):
        for rec in self.buildsDB.get_handled_build():
                if (now - rec['_id'].generation_time.replace(tzinfo=None)).days > self.buildolderthandays:
                    
                    try:
                        if self.remove_actual_artifacts == "true" :
                            print "Trying to delete file from nexus:" + rec 
                            self.remove_artifact(rec)
                        self.buildsDB.delete_build(str(rec['_id']))
                        print "Document of Collection Build" + str(rec['_id']) + "was deleted"
                    except Exception as e_value:  # catch *all* exceptions
                        traceback.print_exc()
                        print ' Error while deleting this build :' + str(e_value)
    def clean_active_builds(self,now,records):
        for record in records:
                count = 0
                all_builds = self.buildsDB.get_active_build(str(record["_id"]))
                if all_builds.count() > self.buildCount and all_builds.count() > 1:
                    for rec in all_builds:
                        count += 1
                        if count > self.buildCount and ((now - rec['_id'].generation_time.replace(tzinfo=None)).days > self.buildolderthandays):
                            if str(rec.get("retain_build_indicator","false")).lower() == "false":
                                try:
                                    if self.remove_actual_artifacts == "true" :
                                        print "Trying to delete file from nexus:" +str(rec) 
                                        self.remove_artifact(rec)
                                    self.buildsDB.delete_build(str(rec['_id']))
                                    print 'Document of Collection Build' + str(rec['_id']) \
                                    + 'was deleted'                                        
                                except Exception as e_value:  # catch *all* exceptions
                                    traceback.print_exc()
                                    print ' Error while deleting this build :' + str(e_value)
                    print ' ended running at ' + time.ctime(time.time())
    
    def clean_dep_req_logs(self,now):
        for deploymentElement in self.deploymentRequestDB.GetDeploymentRequestAll():
                if "logs" in deploymentElement.keys():
                    deploymentLogs = []
                    for deploymentLog in deploymentElement.get('logs'):
                        if deploymentLog.get("dateofdeployment"):
                            if not (now - datetime.strptime(str(deploymentLog.get("dateofdeployment")), '%Y-%m-%d %H:%M:%S')).days > self.olderthandays:
                                deploymentLogs.append(deploymentLog)
                    if deploymentLogs:
                        self.deploymentRequestDB.UpdateDeploymentRequest(
                            {"_id": {"oid": str(deploymentElement["_id"])}, "logs": deploymentLogs})
    
    def clean_clone_req_logs(self,now):
        for cloneElement in self.CloneRequestDB.GetCloneRequestAll():
            if "logs" in cloneElement.keys():
                cloneLogs = []
                for cloneLog in cloneElement.get("logs"):
                    if cloneLog.get("dateofdeployment"):
                        if not (now - datetime.strptime(str(cloneLog.get("dateofdeployment")), '%Y-%m-%d %H:%M:%S')).days > self.olderthandays:
                            cloneLogs.append(cloneLog)
                if cloneLogs:
                    self.CloneRequestDB.UpdateCloneRequest(
                        {"_id": {"oid": str(cloneElement["_id"])}, "logs": cloneLogs})
        print ' ended running at ' + time.ctime(time.time())
    
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
