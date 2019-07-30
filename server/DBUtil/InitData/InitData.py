'''
.. module:: Init data
   :platform: Unix, Windows
   :synopsis: Some data is required to run Deployment Manager for the first time.
       This file has all the necessary data required to run Deployment Manager.
       Each List variable below is Data in key-value format and is
       populated in respective collection by InitDataHelper.py when the application comes up.
.. moduleauthor:: name <email@amdocs.com>'''

from InitDataCommon import USERS,CONFIG_DATA

#USER INSTANCE
USERS = USERS
#CONFIG_DATA INSTANCE
CONFIG_DATA=CONFIG_DATA


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
                            "MachineGroupsView", "UsersGroupsView", \
                            "DeploymentGroupCreate", "DeploymentGroupDelete", \
                            "DeploymentGroupUpdate", "TagsView", "GeneralDetails", \
                            "DeploymentUnitApprovalStatusView", "DeploymentUnitTypeView", \
                            "DeploymentUnitView", "DeploymentUnitSetView", \
                            "ReportsView", "UserView" , "StateView", "ToolsOnMachineView",\
                            "FlexibleAttributeView","ConfigView"],
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
    {
        "name": "SuperAdmin",
        "permissiongroup": [],  # Superadmin is allowed everything
        "status":"Active"
    },
    {
        "name": "Admin",  # NOTE:PLEASE ADD NEW PERMISSION GROUP TO upgradeScript.py too#
        "permissiongroup": ["AccountView", "AccountCreate", "AccountUpdate", \
                            "AccountDelete", "UserView", "UserCreate", "UserUpdate", \
                            "UserDelete", "RoleView", "RoleCreate", "RoleUpdate", \
                            "PermissionsView", "GroupView", "GroupCreate", "GroupUpdate", \
                            "GroupDelete", "ToolSetDelete", "ToolSetCreate", "ToolSetUpdate", \
                            "ToolSetView", "ToolView", "ToolCreate", "ToolUpdate", \
                            "ToolDelete", "DeploymentRequestView", "DeploymentRequestCreate", \
                            "DeploymentRequestUpdate", "DeploymentRequestDelete", \
                            "DistributionSyncView", "VersionsView", "VersionsCreate", \
                            "VersionsUpdate", "BuildView", "BuildCreate", \
                            "BuildUpdate", "DocumentView", "DocumentCreate", \
                            "DocumentUpdate", "DeploymentfieldsView", \
                            "DeploymentfieldsCreate", "DeploymentfieldsUpdate", \
                            "ToolInstallationView", "ToolInstallationCreate", \
                            "ToolInstallationUpdate", "ToolInstallationDelete", \
                            "MachineTypeView", "MachineTypeCreate", \
                            "MachineTypeUpdate", "MachineTypeDelete", \
                            "MachineFavView", "MachineFavCreate", \
                            "MachineFavUpdate", "MachineFavDelete", \
                            "MachineView", "MachineCreate", \
                            "MachineUpdate", "MachineDelete", \
                            "MediaFilesView", "MediaFilesCreate", \
                            "MediaFilesUpdate", "MediaFilesDelete", \
                            "Admin", "Catalog", "ChangePassword", \
                            "DistributionMachineView", \
                            "DistributionMachineCreate", "DistributionMachineUpdate", \
                            "DistributionMachineDelete", "SyncServices", \
                            "SystemDetailsView", \
                            "SystemDetailsCreate", "ConfigView", \
                            "ConfigUpdate", "PreRequisites", \
                            "DeploymentGroupView", "DeploymentGroupCreate", \
                            "DeploymentGroupDelete", \
                            "DeploymentGroupUpdate", "MachineGroupsDelete", \
                            "MachineGroupsView", \
                            "MachineGroupsCreate", "UsersGroupsView", \
                            "UsersGroupsCreate", \
                            "UsersGroupsUpdate", "UsersGroupsDelete", \
                            "MachineGroupsUpdate", \
                            "UsersGroupsCreate", "UsersGroupsView", \
                            "UsersGroupsDelete", \
                            "UsersGroupsUpdate", "TagsView", \
                            "TagsCreate", "TagsUpdate", \
                            "TagsDelete", "GeneralDetails", \
                            "DeploymentUnitApprovalStatusView", \
                            "DeploymentUnitApprovalStatusCreate", \
                            "DeploymentUnitApprovalStatusUpdate", \
                            "DeploymentUnitApprovalStatusDelete", \
                            "DeploymentUnitTypeView", \
                            "DeploymentUnitTypeCreate", \
                            "DeploymentUnitTypeUpdate", "DeploymentUnitTypeDelete", \
                            "DeploymentUnitView", "DeploymentUnitCreate", \
                            "DeploymentUnitUpdate", \
                            "DeploymentUnitDelete", "DeploymentUnitSetView", \
                            "DeploymentUnitSetCreate", \
                            "DeploymentUnitSetUpdate", "DeploymentUnitSetDelete", \
                            "ReportsView", "Plugins", "MonitoringView", "PersonalizeCreate",\
                            "StateView","StateAdd","StateUpdate","StateDelete","ToolsOnMachineView",\
                            "FlexibleAttributeView","FlexibleAttributeDelete","FlexibleAttributeAdd","FlexibleAttributeUpdate",\
                            "ProposedToolsCreate","ProposedToolsView","ProposedToolsDelete","AuditingView","RepositoryView","RepositoryCreate","RepositoryDelete",\
                            "SystemAdministration"],
        "status":"Active"
    },
    {
        "name": "DPMsysCI",
        "permissiongroup": ["BuildCreate"],
        "status":"Active"
    }
]