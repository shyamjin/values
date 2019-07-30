import os,AppLogger
from DBUtil import Config
from DBUtil.InitData import InitDataHelper
from settings import mongodb, current_path, import_path, export_path,\
      distribution_center_import_path, distribution_center_export_path, key, log_path, logo_path,\
      media_path, saved_export_path,templates_path, temp_files_path


# Create Required Directories
############
for dir_path in [log_path,
                 logo_path,
                 media_path,
                 import_path,
                 export_path,
                 distribution_center_import_path,
                 distribution_center_export_path,
                 saved_export_path,
                 templates_path,
                 temp_files_path]:
    if not os.path.exists(os.path.normpath(current_path + '/' + dir_path)):
        print 'Trying to create Directory :' + os.path.normpath(current_path + '/' + dir_path)
        os.makedirs(os.path.normpath(current_path + '/' + dir_path))
        print 'Directory :' + os.path.normpath(current_path + '/' + dir_path) + ' was created'


# Logger
print "********************** STARTING LOGGING SERVICE ****************************************"
AppLogger.AppLogger()

# Initialize data
InitDataHelper.InitDataHelper(mongodb)

from Services import AuthServices, MailerService, DeploymentRequestService, CloneRequestService,\
    SyncServices, PushServices, PullServices, DistributionCenterService, DistributionSyncServices,\
    ContributionGitPushService, CleanerServices, TeamService, SchedulerService


#Authorization Handler
authService = AuthServices.AuthRequestService(mongodb, key)

# START SCHEDULER
SchedulerService.SchedulerService().start_scheduler()

configdb = Config.Config(mongodb)
mailerConfig = configdb.getConfigByName("MailerService")
deploymentConfig = configdb.getConfigByName("DeploymentRequestService")
cloneConfig = configdb.getConfigByName("CloneRequestService")
syncConfig = configdb.getConfigByName("SyncServices")
pullConfig = configdb.getConfigByName("PullServices")
pushConfig = configdb.getConfigByName("PushServices")
distributionCenterConfig = configdb.getConfigByName("PushServices")
distributionSyncConfig = configdb.getConfigByName("DistributionSyncServices")
contributionGitPushSyncConfig = configdb.getConfigByName("ContributionCenterService")
cleanerServicesConfig = configdb.getConfigByName("CleanerServices")

# SERVICES
TeamService.TeamService().generate_details()
if mailerConfig:
    MailerService.MailerService().schedule()
if deploymentConfig:
    DeploymentRequestService.DeploymentRequestService(mongodb).schedule()
if cloneConfig:
    CloneRequestService.CloneRequestService(mongodb).schedule()
if syncConfig:
    SyncServices.SyncServices().schedule()
if pullConfig:
    PullServices.PullServices().schedule()
if pushConfig:
    PushServices.PushServices().schedule()
if distributionCenterConfig:
    DistributionCenterService.DistributionCenterService(mongodb).schedule()
if distributionSyncConfig:
    DistributionSyncServices.DistributionSyncServices().schedule()
if contributionGitPushSyncConfig:
    ContributionGitPushService.ContributionGitPushService(
        mongodb).schedule()
if cleanerServicesConfig:
    CleanerServices.CleanerServices(mongodb).schedule()    