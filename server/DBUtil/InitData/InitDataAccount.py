'''
Created on Mar 21, 2018

@author: PDINDA
'''

'''
.. module:: Init data
   :platform: Unix, Windows
   :synopsis: Some data is required to run Deployment Manager for the first time.
       This file has all the necessary data required to run Deployment Manager.
       Each List variable below is Data in key-value format and is
       populated in respective collection by InitDataHelper.py when the application comes up.
.. moduleauthor:: name <email@amdocs.com>'''

from InitDataCommon import USERS,CONFIG_DATA


users_to_remove=["SuperAdmin"] # REMOVE THESE USERS
config_to_remove=["CloneRequestService"] # REMOVE THESE CONFIG_DATA
config_to_update=[{"name":"DistributionSyncServices","enable":"true"},# UPDATE THESE CONFIG_DATA
                  {"name":"ContributionCenterService","enable":"true"}]

#USER INSTANCE
USERS=USERS
for rec in users_to_remove:
    for user in USERS :
        if user.get("user") == rec:
            USERS.remove(user)

#CONFIG_DATA INSTANCE
CONFIG_DATA=CONFIG_DATA

for rec in config_to_remove:
    for config in CONFIG_DATA :
        if config.get("name") == rec:
            CONFIG_DATA.remove(config)

for rec in config_to_update:
    for index,config in enumerate(CONFIG_DATA) :
        if config.get("name") == rec.get("name"):
            CONFIG_DATA[index].update(rec)




# Connect routes and routes group
ROLE_GROUPING = [
    {
        "name": "Operator",  # NOTE:PLEASE ADD NEW PERMISSION GROUP TO upgradeScript.py too#
        "permissiongroup": ["ToolSetView", "ToolView", "DeploymentRequestView", \
                            "DeploymentRequestCreate", "DeploymentRequestDelete", \
                            "DeploymentRequestUpdate", "VersionsView", "DocumentView", \
                            "DeploymentfieldsView", "ToolInstallationView", \
                            "MachineTypeView", "MachineFavView", "MachineView", \
                            "MediaFilesView", "Catalog", "ChangePassword", \
                            "SystemDetailsView", "DeploymentGroupView", \
                            "MachineGroupsView", "DeploymentGroupCreate", \
                            "DeploymentGroupDelete", "DeploymentGroupUpdate", \
                            "TagsView", "GeneralDetails", \
                            "DeploymentUnitApprovalStatusView", "DeploymentUnitTypeView", \
                            "DeploymentUnitTypeView", "DeploymentUnitView", \
                            "DeploymentUnitSetView", "ReportsView", "UserView", \
                            "UsersGroupsView" ,"StateView", "ToolsOnMachineView","FlexibleAttributeView","ConfigView"],
        "status":"Active"
    },
    {
        "name": "Guest",  # NOTE:PLEASE ADD NEW PERMISSION GROUP TO upgradeScript.py too#
        "permissiongroup": ["ToolSetView", "ToolView",\
                            "VersionsView","Catalog", \
                            "ChangePassword", "SystemDetailsView","GeneralDetails", \
                            "DeploymentUnitApprovalStatusView", "DeploymentUnitTypeView", \
                            "DeploymentUnitView", "DeploymentUnitSetView","FlexibleAttributeView"],
        "status":"Active"
    },
    #             {
    #                "name":"SuperAdmin",
    #               "permissiongroup":[], # Superadmin is allowed everything
    #                "status":"Active"
    #             },
    {
        "name": "Admin",  # NOTE:PLEASE ADD NEW PERMISSION GROUP TO upgradeScript.py too#
        "permissiongroup": [
            "AccountView", "AccountCreate", "AccountUpdate", \
            "AccountDelete", "UserView", "UserCreate", \
            "UserUpdate", "UserDelete", "RoleView", "RoleCreate", \
            "RoleUpdate", "PermissionsView", "GroupView", \
            "GroupCreate", "GroupUpdate", "GroupDelete", \
            "ToolSetDelete", "ToolSetCreate", "ToolSetUpdate", \
            "ToolSetView", "ToolView", "ToolCreate", "ToolUpdate", \
            "ToolDelete", "DeploymentRequestView", "DeploymentRequestCreate", \
            "DeploymentRequestUpdate", "DeploymentRequestDelete", \
            "VersionsView", "VersionsCreate", "VersionsUpdate", \
                            "BuildView", "BuildCreate", "BuildUpdate", \
                            "DocumentView", "DocumentCreate", "DocumentUpdate", \
                            "DeploymentfieldsView", "DeploymentfieldsCreate", \
                            "DeploymentfieldsUpdate", "ToolInstallationView", \
                            "ToolInstallationCreate", "ToolInstallationUpdate", \
                            "ToolInstallationDelete", "MachineTypeView", \
                            "MachineTypeCreate", "MachineTypeUpdate", "MachineTypeDelete", \
                            "MachineFavView", "MachineFavCreate", "MachineFavUpdate", \
                            "MachineFavDelete", "MachineView", "MachineCreate", \
                            "MachineUpdate", "MachineDelete", "MediaFilesView", \
                            "MediaFilesCreate", "MediaFilesUpdate", "MediaFilesDelete", \
                            "DistributionSyncView", "Admin", "Catalog", "ChangePassword", \
                            "ConfigView", "ConfigUpdate", "DistributionSyncView", \
                            "DistributionSyncCreate", "DistributionSyncUpdate", \
                            "DistributionSyncDelete", "SyncServices", "SystemDetailsView", \
                            "SystemDetailsCreate", \
                            "PreRequisites", "DeploymentGroupView", "DeploymentGroupCreate", \
                            "DeploymentGroupDelete", "DeploymentGroupUpdate", \
                            "MachineGroupsView", "MachineGroupsDelete", \
                            "MachineGroupsCreate", "UsersGroupsView", \
                            "UsersGroupsCreate", "UsersGroupsUpdate", "UsersGroupsDelete", \
                            "MachineGroupsUpdate", "UsersGroupsCreate", "UsersGroupsView", \
                            "UsersGroupsDelete", "UsersGroupsUpdate", "TagsView", \
                            "TagsCreate", "TagsUpdate", "TagsDelete", "GeneralDetails", \
                            "DeploymentUnitApprovalStatusView", \
                            "DeploymentUnitApprovalStatusCreate", \
                            "DeploymentUnitApprovalStatusUpdate", \
                            "DeploymentUnitApprovalStatusDelete", "DeploymentUnitTypeView", \
                            "DeploymentUnitTypeCreate", "DeploymentUnitTypeUpdate", \
                            "DeploymentUnitTypeDelete", "DeploymentUnitCreate", \
                            "DeploymentUnitUpdate", "DeploymentUnitDelete", \
                            "DeploymentUnitSetView", \
                            "DeploymentUnitSetCreate", \
                            "DeploymentUnitSetUpdate", "DeploymentUnitSetDelete", \
                            "ReportsView", "DeploymentUnitView", "Plugins", "MonitoringView", "PersonalizeCreate",\
                            "StateView","StateAdd","StateUpdate","StateDelete","ToolsOnMachineView",\
                            "FlexibleAttributeView","FlexibleAttributeDelete","FlexibleAttributeAdd","FlexibleAttributeUpdate",\
                            "ProposedToolsCreate","ProposedToolsView","ProposedToolsDelete","AuditingView",\
                            "RepositoryView","RepositoryCreate","RepositoryDelete","RepositoryUpdate",\
                            "SystemAdministration"],
        "status":"Active"
    },
    {
        "name": "DPMsysCI",
        "permissiongroup": ["BuildCreate"],
        "status":"Active"
    }
]