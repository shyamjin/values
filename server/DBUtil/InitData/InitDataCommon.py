'''
Created on Feb 21, 2018

@author: PDINDA
'''

from settings import base_path, remote_sync_import_path,remote_distribution_import_path,\
    default_admin_password,default_nexus_container_name

# list Permissions for Reference data  (For any new permissions please add
# in below list)
PERMISSIONS = [
    {"name": "/account/all"},
    {"name": "/account/view/~"},
    {"name": "/account/new"},
    {"name": "/account/update"},
    {"name": "/account/update/name"},
    {"name": "/account/delete"},
    {"name": "/user/new"},
    {"name": "/user/update"},
    {"name": "/user/change/password"},
    {"name": "/user/suspend"},
    {"name": "/user/activate/"},
    {"name": "/user/delete/"},
    {"name": "/user/all"},
    {"name": "/user/view/~"},
    {"name": "/user/name/~"},
    {"name": "/machine/user/"},
    {"name": "/user/auth"},
    {"name": "/user/basicauth"},
    {"name": "/user/auth/verify"},
    {"name": "/user/signup"},
    {"name": "/role/all"},
    {"name": "/role/view/~"},
    {"name": "/role/new"},
    {"name": "role/update"},
    {"name": "/role/add/permissiongroup"},
    {"name": "/role/remove/permissiongroup"},
    {"name": "/role/delete"},
    {"name": "/permissions/all"},
    {"name": "/permissions/view/~"},
    {"name": "/permissions/new"},
    {"name": "/permissions/update"},
    {"name": "/permissions/delete"},
    {"name": "/grouppermissions/all"},
    {"name": "/grouppermissions/view/~"},
    {"name": "/grouppermissions/new"},
    {"name": "/grouppermissions/update"},
    {"name": "/grouppermissions/delete/"},
    {"name": "/tool/add"},
    {"name": "/tool/view/~"},
    {"name": "/tool/view/version/~"},
    {"name": "/tool/view/version/~/prevversion/~/machine/~"},
    {"name": "/tool/all"},
    {"name": "/tool/search/name/~"},
    {"name": "/tool/search/tag/~"},
    {"name": "/tool/update"},
    {"name": "/tool/delete"},
    {"name": "/tool/upload/logo"},
    {"name": "/edit/tool/:id"},
    {"name": "/deploymentrequest/view/~"},
    {"name": "/deploymentrequest/all"},
    {"name": "/deploymentrequest/add"},
    {"name": "/deploymentrequest/run/view/~"},
    {"name": "/deploymentrequest/cancel"},
    {"name": "/deploymentrequest/retry"},
    {"name": "/deploymentrequest/group/all"},
    {"name": "/deploymentrequest/group/view/~"},
    {"name": "/deploymentrequest/group/add"},
    {"name": "/deploymentrequest/group/retry"},
    {"name": "/deploymentrequest/group/cancel/~"},
    {"name": "/deploymentrequest/group/toolset/add"},
    {"name": "/tool/versions/add"},
    {"name": "/tool/~/versions/all"},
    {"name": "/tool/versions/view/~"},
    {"name": "/versions/build/view/~"},
    {"name": "/versions/~/build/active"},
    {"name": "/versions/~/build/all"},
    {"name": "/versions/build/add"},
    {"name": "/build/add"},
    {"name": "/build/view/~"},
    {"name": "/tool/versions/uploadScreenshot"},
    {"name": "/versions/build/update"},
    {"name": "/versions/build/setactive"},
    {"name": "/versions/~/documents"},
    {"name": "/versions/documents/add"},
    {"name": "/versions/documents/update"},
    {"name": "/versions/~/deploymentfields"},
    {"name": "/versions/deploymentfields/add"},
    {"name": "/versions/deploymentfields/update"},
    {"name": "/versions/~/installation/all"},
    {"name": "/machine/~/installation/all"},
    {"name": "/installation/add"},
    {"name": "/installation/update"},
    {"name": "/installation/delete"},
    {"name": "/machine/type/view/~"},
    {"name": "/machine/type/all"},
    {"name": "/machine/type/new"},
    {"name": "/machine/type/update"},
    {"name": "/machine/type/delete"},
    {"name": "/machine/all/fav"},
    {"name": "/machine/fav/view/~"},
    {"name": "/machine/fav/machine/~"},
    {"name": "/machine/fav/user/~"},
    {"name": "/machine/fav/machine/~/user/~"},
    {"name": "/machine/fav/new"},
    {"name": "/machine/fav/update"},
    {"name": "/machine/fav/delete"},
    {"name": "/machine/view/~"},
    {"name": "/machine/alias/~"},
    {"name": "/machine/view/all"},
    {"name": "/machine/hostname/~"},
    {"name": "/machine/ip/~"},
    {"name": "/machine/user/~"},
    {"name": "/machine/new"},
    {"name": "/machine/test"},
    {"name": "/machine/import"},
    {"name": "/machine/update"},
    {"name": "/machine/refresh"},
    {"name": "/machine/update/userdetails"},
    {"name": "/machine/update/usertype"},
    {"name": "/machine/add/permission"},
    {"name": "/machine/delete/permission"},
    {"name": "/machine/remove/~"},
    {"name": "/machine/disable"},
    {"name": "/mediafiles/view/~"},
    {"name": "/versions/~/mediafiles/all"},
    {"name": "/mediafiles/add"},
    {"name": "/mediafiles/update"},
    {"name": "/mediafiles/delete"},
    {"name": "/clonerequest/all"},
    {"name": "/clonerequest/view/~"},
    {"name": "/clonerequest/add"},
    {"name": "/clonerequest/distribution/all"},
    {"name": "/clonerequest/distribution/update"},
    {"name": "/clonerequest/distribution/add"},
    {"name": "/clonerequest/run/~"},
    {"name": "/clonerequest/update"},
    {"name": "/clonerequest/cancel/~"},
    {"name": "/clonerequest/retry"},
    {"name": "/clonerequest/distribution/run/all"},
    {"name": "/clonerequest/distribution/run/~"},
    {"name": "/clonerequest/distribution/cancel/~"},
    {"name": "/clonerequest/distribution/view/all"},
    {"name": "/clonerequest/distribution/view/tool/~"},
    {"name": "/config/all"},
    {"name": "/config/view/~"},
    {"name": "/config/view/configid/~"},
    {"name": "/config/sync/all"},
    {"name": "/config/update"},
    {"name": "/config/delete"},
    {"name": "/config/distribution/schedule"},
    {"name": "/sync/import"},
    {"name": "/sync/delete/~"},    
    {"name": "/sync/savedexports"},
    {"name": "/sync/manual/clean/~"},
    {"name": "/sync/manual/export"},
    {"name": "/sync/pull/export"},
    {"name": "/syncrequest/all"},
    {"name": "/syncrequest/view/~"},
    {"name": "/syncrequest/type/~"},
    {"name": "/syncrequest/update"},
    {"name": "/syncrequest/delete/~"},
    {"name": "/syncrequest/add"},
    {"name": "/sync/push/trigger/~"},
    {"name": "/syncrequest/run/~"},
    {"name": "/clonerequest/distribution/tool"},
    {"name": "/clonerequest/distribution/tool/status/~"},
    {"name": "/clonerequest/distribute/add"},
    {"name": "/clonerequest/distribute/status/~"},
    {"name": "/systemdetails/all"},
    {"name": "/systemdetails/add"},
    {"name": "/toolset/add"},
    {"name": "/toolset/all"},
    {"name": "/toolset/view/~"},
    {"name": "/toolset/delete/~"},
    {"name": "/toolset/update"},
    {"name": "/prerequisites/add"},
    {"name": "/prerequisites/view"},
    {"name": "/prerequisites/view/~"},
    {"name": "/prerequisites/update"},
    {"name": "/prerequisites/delete/~"},
    {"name": "/machinegroups/add"},
    {"name": "/machinegroups/view"},
    {"name": "/machinegroups/view/~"},
    {"name": "/machinegroups/update"},
    {"name": "/machinegroups/delete/~"},
    {"name": "/teams/add"},
    {"name": "/teams/view"},
    {"name": "/teams/view/~"},
    {"name": "/teams/update"},
    {"name": "/teams/delete/~"},
    {"name": "/tag/all"},
    {"name": "/tag/view/~"},
    {"name": "/tag/new"},
    {"name": "/tag/update"},
    {"name": "/tag/delete/~"},
    {"name": "/currenttime"},
    {"name": "/user/generateaccesstoken"},
    {"name": "/role/list/update"},
    {"name": "/deploymentunitapprovalstatus/all"},
    {"name": "/deploymentunitapprovalstatus/view/~"},
     {"name": "/deploymentunitapprovalstatus/view/name/~"},
    {"name": "/deploymentunitapprovalstatus/add"},
    {"name": "/deploymentunitapprovalstatus/update"},
    {"name": "/deploymentunitapprovalstatus/delete/~"},
    {"name": "/deploymentunittype/all"},
    {"name": "/deploymentunittype/view/~"},
    {"name": "/deploymentunittype/new"},
    {"name": "/deploymentunittype/update"},
    {"name": "/deploymentunittype/delete/~"},
    {"name": "/deploymentunit/all"},
    {"name": "/deploymentunit/view/~"},
    {"name": "/deploymentunit/search/name/~"},
    {"name": "/deploymentunit/search/tag/~"},
    {"name": "/deploymentunit/new"},
    {"name": "/deploymentunit/update"},
    {"name": "/deploymentunit/delete/~"},
    {"name": "/deploymentunitset/all"},
    {"name": "/deploymentunitset/view/~"},
    {"name": "/deploymentunitset/new"},
    {"name": "/deploymentunitset/update"},
    {"name": "/deploymentunitset/delete/~"},
    {"name": "/deploymentunitset/view/getbuilds/~"},
    {"name": "/deploymentunitset/view/states/~"},    
    {"name": "/deploymentrequest/deploymentfield/upload"},
    {"name": "/deploymentrequest/group/machine/add"},
    {"name": "/user/deleteaccesstoken/~"},
    {"name": "/plugin/reload"},
    {"name": "/plugin/install"},
    {"name": "/plugin/all"},
    {"name": "/plugin/uninstall/~"},
    {"name": "/plugin/inactive/~"},
    {"name": "/plugin/active/~"},
    {"name": "/deploymentrequest/group/saved/all"},
    {"name": "/deploymentrequest/group/saved/add"},
    {"name": "/deploymentrequest/group/saved/update"},
    {"name": "/deploymentrequest/group/saved/delete/~"},
    {"name": "/deploymentrequest/group/saved/view/~"},
    {"name": "/plugin/view/~"},
    {"name": "/toolset/upload/logo"},
    {"name": "/deploymentunit/upload/logo"},
    {"name": "/deploymentunitset/upload/logo"},
    {"name": "/build/update"},
    {"name": "/systemdetails/logoupload"},
    {"name": "/user/import"},
    {"name" : "/state/all/"},
    {"name" : "/state/add"},
    {"name" : "/state/update"},
    {"name" : "/state/view/~"},
    {"name" : "/state/view/parent/~"},
    {"name" : "/state/view/parent/~/name/~"},
    {"name" : "/state/delete/~"},
    {"name": "/machinegroups/view/name/~"},
    {"name": "/deployed/view/all"},    
    {"name": "/deployed/view/machine_id/~/parent_entity_id/~/build_id/~"},
    {"name": "/machine/bulk/load"},
    {"name": "/machinegroups/bulk/load"},
    {"name": "/flexattributes/new"},
    {"name": "/flexattributes/update"},
    {"name": "/flexattributes/view/all"},
    {"name": "/flexattributes/view/entity/~"},
    {"name": "/flexattributes/view/~"},    
    {"name": "/plugin/file/upload"},
    {"name": "/plugin/file/list/~"},    
    {"name": "/plugin/file/remove/~"},    
    {"name": "/deploymentrequest/group/machinegroup/new"},
    {"name": "/proposed/tool/view/all"},
    {"name": "/proposed/tool/view/~"},
    {"name": "/proposed/tool/delete/~"},
    {"name": "/proposed/tool/approve"},
    {"name" : "/machine/view/deployment/history/entity/~/~"},
    {"name": "/deploymentrequest/group/add/undeploy"},
    {"name": "/deploymentrequest/group/view/revert/~"},
    {"name": "/plugin/exitpoint/new"},
    {"name": "/plugin/exitpoint/update"},
    {"name": "/plugin/file/view/~"},
    {"name": "/machine/search/tag/~"},
    {"name": "/machine/search/name/~"},
    {"name": "/auditing/view/all"},
    {"name": "/sync/view/all"},
    {"name": "/sync/view/syncid/~"},
    {"name": "/auditing/view/id/~"},
    {"name": "/sync/retry"},
    {"name": "/repository/add"},
    {"name": "/repository/update"},
    {"name": "/repository/view/all"},
    {"name": "/repository/view/name/~"},
    {"name": "/repository/view/~"},
    {"name": "/repository/delete/~"},
    {"name":"/repository/view/byparententity/~"},
    {"name": "/server/restart"},
    {"name": "/user/logout"},
    {"name": "/reports/all"},
    {"name" : "/tool/update/buildmarkup"}
]

# Define all routes
ROUTES = [
    {"name": "/clonerequests/:id"},
    {"name": "/clonerequests/steps/tools/:id"},
    {"name": "/clonerequests"},
    {"name": "/createclone"},
    {"name": "/createaccount"},
    {"name": "/adduser"},
    {"name": "/edit/user/:id"},
    {"name": "/delete/user/:id"},
    {"name": "/users"},
    {"name": "/manageroles"},
    {"name": "/editrole/:id"},
    {"name": "/addrole"},
    {"name": "/deleterole"},
    {"name": "/tool/view/:id"},
    {"name": "/tools/all"},
    {"name": "/dashboard"},
    {"name": "/tool/new"},
    {"name": "/AddNewMachine"},
    {"name": "/MachineDetails/:id"},
    {"name": "/editmachine/:id"},
    {"name": "/settings"},
    {"name": "/deploymentrequests"},
    {"name": "/deploy/tool/:id/:build_number"},
    {"name": "/viewRequestDetail/:id"},
    {"name": "/machines"},
    {"name": "/importexport"},
    {"name": "/synchronization"},
    {"name": "/edit/sync/:id"},
    {"name": "/admin"},
    {"name": "/catalog"},
    {"name": "/changepassword"},
    {"name": "/redeploy/version/:version_id/build_number/:build_number/build_id/:build_id/machine/:machine_id"},
    {"name": "/upgrade/oldversion/:old_version_id/newversion/:new_version_id/machine/:machine_id"},
    {"name": "/undeploy/version/:version_id/build_number/:build_number/build_id/:build_id/machine/:machine_id"},
    {"name": "/edit/tool/:id"},
    {"name": "/distribution"},
    {"name": "/distribution/cancel/:id"},
    {"name": "/distribution/resend/:id"},
    {"name": "/tools/new"},
    {"name": "/tools/updates"},
    {"name": "/import/tool/:id"},
    {"name": "/update/tool/:id"},
    {"name": "/tool/new/:id"},
    {"name": "/tool/updated/:id"},
    {"name": "/systemdata"},
    {"name": "/toolset/new"},
    {"name": "/toolset/all"},
    {"name": "/toolset/view/:id"},
    {"name": "/toolset/delete/:id"},
    {"name": "/edit/toolset/:id"},
    {"name": "/view/log/deploy/:id"},
    {"name": "/view/log/clone/:id"},
    {"name": "/manage/users/groups"},
    {"name": "/view/user/group/:id"},
    {"name": "/create/user/group"},
    {"name": "/edit/user/group/:id"},
    {"name": "/delete/user/group/:id"},
    {"name": "/delete/machine/group/:id"},
    {"name": "/manage/machine/groups"},
    {"name": "/view/machine/group/:id"},
    {"name": "/add/machine/group"},
    {"name": "/edit/machine/group/:id"},
    {"name": "/manage/prerequisites"},
    {"name": "/add/new/prerequisite"},
    {"name": "/edit/prerequisite/:id"},
    {"name": "/view/prerequisite/:id"},
    {"name": "/delete/prerequisite/:id"},
    {"name": "/deploy/toolset/:id"},
    {"name": "/deploy/tools/:tools"},
    {"name": "/view/reports"},
    {"name": "/deploymentunit/new"},
    {"name": "/deploymentunit/edit/:id"},
    {"name": "/dashboard/du"},
    {"name": "/deploymentunit/view/:id"},
    {"name": "/deploymentunitset/new"},
    {"name": "/deploymentunitset/view/:id"},
    {"name": "/deploymentunitset/all"},
    {"name": "/deploymentunitset/edit/:id"},
    {"name": "/manage/tags"},
    {"name": "/tag/view/:id"},
    {"name": "/tag/new"},
    {"name": "/tag/update"},
    {"name": "/tag/delete/:id"},
    {"name": "/deploy/duset/:id"},
    {"name": "/bulk/machines"},
    {"name": "/machine/remove/:id"},
    {"name": "/manage/synchronization/services"},
    {"name": "/undeploy/du/:du_id/build_number/:build_number/build_id/:build_id/machine/:machine_id"},
    {"name": "/redeploy/du/:du_id/build_number/:build_number/build_id/:build_id/machine/:machine_id"},
    {"name": "/saved/requests"},
    {"name": "/recent/requests"},
    {"name": "/plugin"},
    {"name": "/revert/du/:id"},
    {"name": "/edit/saved/deployment/tool/:request_id"},
    {"name": "/edit/saved/deployment/du/:request_id"},
    {"name": "/dashboard/deployment/:request_id"},
    {"name": "/dashboard/importupdate/:request_id"},
    {"name": "/dashboard/du/:request_id"},
    {"name": "/delete/tool/:id"},
    {"name": "/delete/deploymentunit/:id"},
    {"name": "/deploy/du/:id"},
    {"name": "/team/view/:id"},
    {"name": "/view/monitoring"},
    {"name": "/view/monitoring/runningservices"},
    {"name": "/users/import"},
    {"name": "/deploy/dus/:dus"},
    {"name": "/view/du/state"},
    {"name": "/view/duset/state"},
    {"name": "/create/du/state"},
    {"name": "/create/duset/state"},
    {"name": "/state/delete/:id"},
    {"name": "/new/flexibleattributes"},
    {"name": "/manage/flexibleattributes"},
    {"name": "/manage/plugins/deployment"},
    {"name": "/plugin/deployment/upload"},
    {"name": "/proposed/tools/all"},
    {"name": "/view/proposed/tool/:id"},
    {"name": "/deploymentrequest/view/:id"},
    {"name": "/edit/tool/proposed/:id"},
    {"name": "/approve/tool/proposed/:id"},
    {"name": "/machine/view/deployment/history/entity/:entity/:id"},
    {"name": "/deploymentrequest/group/revert/:id"},
    {"name": "/view/sync/requests"},
    {"name": "/view/sync/request/:id"},
    {"name": "/view/audits"},
    {"name": "/view/repository"},
    {"name": "/new/repository"}
    

]

PERMISSION_GROUPS = [
    {
        "groupname": "AccountView",
        "group_description": "AccountView",
        "permissions": ["/account/all", "/account/view/~"],
        "routes":[]
    },
    {
        "groupname": "AccountCreate",
        "group_description": "AccountCreate",
        "permissions": ["/account/new"],
        "routes":["/createaccount"]
    },
    {"groupname": "AccountUpdate",
     "group_description": "AccountUpdate",
     "permissions": ["/account/update", "/account/update/name"],
     "routes":[]
     },
    {"groupname": "AccountDelete",
     "group_description": "AccountDelete",
     "permissions": ["/account/delete"],
     "routes":[]
     },
    {"groupname": "UserCreate",
     "group_description": "UserCreate",
     "permissions": ["/user/new", "/user/import"],
     "routes":["/adduser", "/users/import"]
     },
    {"groupname": "UserUpdate",
     "group_description": "UserUpdate",
     "permissions": ["/user/update", "/user/suspend", "/user/activate/",
                     "/user/generateaccesstoken",
                     "/user/deleteaccesstoken/~"],
     "routes":["/edit/user/:id"]
     },
    {"groupname": "UserDelete",
     "group_description": "UserDelete",
     "permissions": ["/user/delete/"],
     "routes":["/delete/user/:id"]
     },
    {"groupname": "UserView",
     "group_description": "UserView",
     "permissions": ["/user/all", "/user/view/~", "/user/name/~"],
     "routes":["/users"]
     },
    {"groupname": "RoleView",
     "group_description": "RoleView",
     "permissions": ["/role/all", "/role/view/~"],
     "routes":["/manageroles", "/editrole/:id"]
     },
    {"groupname": "RoleCreate",
     "group_description": "RoleCreate",
     "permissions": ["/role/new"],
     "routes":["/addrole"]
     },
    {"groupname": "RoleUpdate",
     "group_description": "RoleUpdate",
     "permissions": ["role/update", "/role/add/permissiongroup",
                     "/role/remove/permissiongroup", "/role/list/update"],
     "routes":["/editrole/:id"]
     },
    {"groupname": "RoleDelete",
     "group_description": "RoleDelete",
     "permissions": ["/role/delete"],
     "routes":["/deleterole"]
     },
    {"groupname": "PermissionsView",
     "group_description": "PermissionsView",
     "permissions": ["/permissions/all", "/permissions/view/~"],
     "routes":[]
     },
    {"groupname": "PermissionsCreate",
     "group_description": "PermissionsCreate",
     "permissions": ["/permissions/new"],
     "routes":[]
     },
    {"groupname": "PermissionsUpdate",
     "group_description": "PermissionsUpdate",
     "permissions": ["/permissions/update"],
     "routes":[]
     },
    {"groupname": "PermissionsDelete",
     "group_description": "PermissionsDelete",
     "permissions": ["/permissions/delete"],
     "routes":[]
     },
    {"groupname": "GroupView",
     "group_description": "GroupView",
     "permissions": ["/grouppermissions/all", "/grouppermissions/view/~"],
     "routes":[]
     },
    {"groupname": "GroupCreate",
     "group_description": "GroupCreate",
     "permissions": ["/grouppermissions/new"],
     "routes":[]
     },
    {"groupname": "GroupUpdate",
     "group_description": "GroupUpdate",
     "permissions": ["/grouppermissions/update"],
     "routes":[]
     },
    {"groupname": "GroupDelete",
     "group_description": "GroupDelete",
     "permissions": ["/grouppermissions/delete/"],
     "routes":[]
     },
    {"groupname": "ToolView",
     "group_description": "ToolView",
     "permissions": ["/tool/view/~", "/tool/view/version/~", "/tool/all",
                     "/tool/search/name/~", "/tool/search/tag/~",
                     "/tool/view/version/~/prevversion/~/machine/~"],
     "routes":["/tool/view/:id", "/tools/all", "/dashboard", "/dashboard/deployment/:request_id", "/dashboard/importupdate/:request_id"]
     },
    {"groupname": "ToolCreate",
     "group_description": "ToolCreate",
     "permissions": ["/tool/add"],
     "routes":["/tool/new"]
     },
    {"groupname": "ToolUpdate",
     "group_description": "ToolUpdate",
     "permissions": ["/tool/update", "/tool/upload/logo", "/tool/update/buildmarkup"],
     "routes":["/edit/tool/:id"]
     },
    {"groupname": "ToolDelete",
     "group_description": "ToolDelete",
     "permissions": ["/tool/delete"],
     "routes":["/delete/tool/:id"]
     },
    {"groupname": "DeploymentRequestView",
     "group_description": "DeploymentRequestView",
     "permissions": ["/deploymentrequest/view/~", "/deploymentrequest/all"],
     "routes":["/deploymentrequests", "/viewRequestDetail/:id", "/view/log/deploy/:id", "/saved/requests", "/recent/requests","/deploymentrequest/view/:id"]
     },
    {"groupname": "DeploymentRequestCreate",
     "group_description": "DeploymentRequestCreate",
     "permissions": ["/deploymentrequest/add", "/deploymentrequest/deploymentfield/upload"],
     "routes":["/deploy/tool/:id/:build_number",
               "/redeploy/version/:version_id/build_number/:build_number/build_id/:build_id/machine/:machine_id",
               "/upgrade/oldversion/:old_version_id/newversion/:new_version_id" +
               "/machine/:machine_id",
               "/undeploy/version/:version_id/build_number/:build_number/build_id/:build_id/machine/:machine_id", "/deploy/tools/:tools",
               "/deploy/du/:id", "/deploy/duset/:id",
               "/revert/du/:id",
               "/deploy/dus/:dus"]
     },
    {"groupname": "DeploymentRequestDelete",
     "group_description": "DeploymentRequestDelete",
     "permissions": ["/deploymentrequest/cancel"],
     "routes":[]
     },
    {"groupname": "DeploymentRequestUpdate",
     "group_description": "DeploymentRequestUpdate",
     "permissions": ["/deploymentrequest/run/view/~", "/deploymentrequest/retry"],
     "routes":["/edit/saved/deployment/tool/:request_id", "/edit/saved/deployment/du/:request_id"]
     },
    {"groupname": "VersionsCreate",
     "group_description": "VersionsCreate",
     "permissions": ["/tool/versions/add"],
     "routes":[]
     },
    {"groupname": "VersionsUpdate",
     "group_description": "VersionsUpdate",
     "permissions": ["/tool/versions/uploadScreenshot"],
     "routes":[]
     },
    {"groupname": "BuildView",
     "group_description": "BuildView",
     "permissions": ["/versions/build/view/~", "/versions/~/build/active",
                     "/versions/~/build/all"],
     "routes":[]
     },
    {"groupname": "BuildCreate",
     "group_description": "BuildCreate",
     "permissions": ["/versions/build/add","/build/add"],
     "routes":[]
     },
    {"groupname": "BuildUpdate",
     "group_description": "BuildUpdate",
     "permissions": ["/versions/build/update", "/versions/build/setactive", "/build/update"],
     "routes":[]
     },
    {"groupname": "DocumentView",
     "group_description": "DocumentView",
     "permissions": ["/versions/~/documents"],
     "routes":[]
     },
    {"groupname": "DocumentCreate",
     "group_description": "DocumentCreate",
     "permissions": ["/versions/documents/add"],
     "routes":[]
     },
    {"groupname": "DocumentUpdate",
     "group_description": "DocumentUpdate",
     "permissions": ["/versions/documents/update"],
     "routes":[]
     },
    {"groupname": "DeploymentfieldsCreate",
     "group_description": "DeploymentfieldsCreate",
     "permissions": ["/versions/deploymentfields/add"],
     "routes":[]
     },
    {"groupname": "DeploymentfieldsUpdate",
     "group_description": "DeploymentfieldsUpdate",
     "permissions": ["/versions/deploymentfields/update"],
     "routes":[]
     },
    {"groupname": "ToolInstallationCreate",
     "group_description": "ToolInstallationCreate",
     "permissions": ["/installation/add"],
     "routes":[]
     },
    {"groupname": "ToolInstallationUpdate",
     "group_description": "ToolInstallationUpdate",
     "permissions": ["/installation/update"],
     "routes":[]
     },
    {"groupname": "ToolInstallationDelete",
     "group_description": "ToolInstallationDelete",
     "permissions": ["/installation/delete"],
     "routes":[]
     },
    {"groupname": "MachineTypeCreate",
     "group_description": "MachineTypeCreate",
     "permissions": ["/machine/type/new"],
     "routes":[]
     },
    {"groupname": "MachineTypeUpdate",
     "group_description": "MachineTypeUpdate",
     "permissions": ["/machine/type/update"],
     "routes":[]
     },
    {"groupname": "MachineTypeDelete",
     "group_description": "MachineTypeDelete",
     "permissions": ["/machine/type/delete"],
     "routes":[]
     },
    {"groupname": "MachineFavCreate",
     "group_description": "MachineFavCreate",
     "permissions": ["/machine/fav/new"],
     "routes":[]
     },
    {"groupname": "MachineFavUpdate",
     "group_description": "MachineFavUpdate",
     "permissions": ["/machine/fav/update"],
     "routes":[]
     },
    {"groupname": "MachineFavDelete",
     "group_description": "MachineFavDelete",
     "permissions": ["/machine/fav/delete"],
     "routes":[]
     },
    {"groupname": "MachineCreate",
     "group_description": "MachineCreate",
     "permissions": ["/machine/new", "/machine/add/permission", "/machine/import","/machine/bulk/load"],
     "routes":["/AddNewMachine", "/bulk/machines"]
     },
    {"groupname": "MachineUpdate",
     "group_description": "MachineUpdate",
     "permissions": ["/machine/update", "/machine/refresh",
                     "/machine/update/userdetails", "/machine/update/usertype", "/machine/disable","/machine/bulk/load"],
     "routes":["/MachineDetails/:id", "/editmachine/:id"]
     },
    {"groupname": "MachineDelete",
     "group_description": "MachineDelete",
     "permissions": ["/machine/delete/permission", "/machine/remove/~"],
     "routes":["/machine/remove/:id"]
     },
    {"groupname": "MediaFilesCreate",
     "group_description": "MediaFilesCreate",
     "permissions": ["/mediafiles/add"],
     "routes":[]
     },
    {"groupname": "MediaFilesUpdate",
     "group_description": "MediaFilesUpdate",
     "permissions": ["/mediafiles/update"],
     "routes":[]
     },
    {"groupname": "MediaFilesDelete",
     "group_description": "MediaFilesDelete",
     "permissions": ["/mediafiles/delete"],
     "routes":[]
     },
    {"groupname": "CloneView",
     "group_description": "CloneView",
     "permissions": ["/clonerequest/all", "/clonerequest/view/~"],
     "routes":["/clonerequests", "/clonerequests/:id",
               "/clonerequests/steps/tools/:id", "/view/log/clone/:id"]
     },
    {"groupname": "CloneCreate",
     "group_description": "CloneCreate",
     "permissions": ["/clonerequest/add"],
     "routes":["/createclone"]
     },
    {"groupname": "CloneUpdate",
     "group_description": "CloneUpdate",
     "permissions": ["/clonerequest/run/~", "/clonerequest/update", "/clonerequest/retry"],
     "routes":[]
     },
    {"groupname": "CloneDelete",
     "group_description": "CloneDelete",
     "permissions": ["/clonerequest/cancel/~"],
     "routes":[]
     },
    {"groupname": "DistributionMachineView",
     "group_description": "DistributionMachineView",
     "permissions": ["/clonerequest/distribution/all", "/clonerequest/distribute/status/~"],
     "routes":["/distribution"]
     },
    {"groupname": "DistributionMachineCreate",
     "group_description": "DistributionMachineCreate",
     "permissions": ["/clonerequest/distribution/add", "/clonerequest/distribute/add"],
     "routes":[]
     },
    {"groupname": "DistributionMachineUpdate",
     "group_description": "DistributionMachineUpdate",
     "permissions": ["/clonerequest/distribution/update",
                     "/clonerequest/distribution/run/all", "/clonerequest/distribution/run/~"],
     "routes":["/distribution/cancel/:id", "/distribution/resend/:id"]
     },
    {"groupname": "DistributionMachineDelete",
     "group_description": "DistributionMachineDelete",
     "permissions": ["/clonerequest/distribution/cancel/~"],
     "routes":[]
     },
    {"groupname": "DistributionSyncView",
     "group_description": "DistributionSyncView",
     "permissions": ["/clonerequest/distribution/view/all",
                     "/clonerequest/distribution/view/tool/~",
                     "/clonerequest/distribution/tool/status/~"],
     "routes":["/tools/new", "/tools/updates", "/tool/new/:id", "/tool/updated/:id"]
     },
    {"groupname": "DistributionSyncCreate",
     "group_description": "DistributionSyncCreate",
     "permissions": ["/clonerequest/distribution/tool"],
     "routes":["/import/tool/:id", "/update/tool/:id"]
     },
    {"groupname": "DistributionSyncUpdate",
     "group_description": "DistributionSyncUpdate",
     "permissions": [],
     "routes":[]
     },
    {"groupname": "DistributionSyncDelete",
     "group_description": "DistributionSyncDelete",
     "permissions": [],
     "routes":[]
     },
    {"groupname": "ConfigView",
     "group_description": "ConfigView",
     "permissions": ["/config/all", "/config/view/~", "/config/sync/all","/config/view/configid/~","/config/distribution/schedule"],
     "routes":["/settings"]
     },
    {"groupname": "ConfigUpdate",
     "group_description": "ConfigUpdate",
     "permissions": ["/config/update"],
     "routes":[]
     },
    {"groupname": "VersionsView",
     "group_description": "VersionsView",
     "permissions": ["/tool/~/versions/all", "/tool/versions/view/~"],
     "routes":[]
     },
    {"groupname": "DeploymentfieldsView",
     "group_description": "DeploymentfieldsView",
     "permissions": ["/versions/~/deploymentfields"],
     "routes":[]
     },
    {"groupname": "ToolInstallationView",
     "group_description": "ToolInstallationView",
     "permissions": ["/versions/~/installation/all", "/machine/~/installation/all"],
     "routes":[]
     },
    {"groupname": "MachineTypeView",
     "group_description": "MachineTypeView",
     "permissions": ["/machine/type/view/~", "/machine/type/all"],
     "routes":[]
     },
    {"groupname": "MachineFavView",
     "group_description": "MachineFavView",
     "permissions": ["/machine/all/fav", "/machine/fav/view/~",
                     "/machine/fav/machine/~", "/machine/fav/user/~",
                     "/machine/fav/machine/~/user/~"],
     "routes":[]
     },
    {"groupname": "MachineView",
     "group_description": "MachineView",
     "permissions": ["/machine/view/~", "/machine/alias/~",
                     "/machine/view/all", "/machine/hostname/~",
                     "/machine/ip/~", "/machine/user/~", "/machine/test",\
                     "/machine/view/deployment/history/entity/~/~","/machine/search/tag/~","/machine/search/name/~"],
     "routes":["/MachineDetails/:id", "/machines", "/machine/view/deployment/history/entity/:entity/:id"]
     },
    {"groupname": "MediaFilesView",
     "group_description": "MediaFilesView",
     "permissions": ["/mediafiles/view/~", "/versions/~/mediafiles/all"],
     "routes":[]
     },
    {"groupname": "SyncServices",
     "group_description": "SyncServices",
     "permissions": ["/sync/import", "/sync/manual/export", "/sync/pull/export",
                     "/sync/push/trigger/~", "/syncrequest/all", "/syncrequest/view/~",
                     "/syncrequest/type/~", "/syncrequest/update", "/syncrequest/delete/~",
                     "/syncrequest/add", "/sync/manual/clean/~",
                      "/syncrequest/run/~", "/sync/savedexports","/sync/view/all","/sync/view/syncid/~","/sync/retry","/sync/delete/~"],
     "routes":["/importexport", "/synchronization", "/edit/sync/:id",
               "/manage/synchronization/services", "/view/sync/requests", "/view/sync/request/:id"]
     },
    {"groupname": "Admin",
     "group_description": "Admin",
     "permissions": [],
     "routes":["/admin"]
     },
    {"groupname": "Catalog",
     "group_description": "Catalog",
     "permissions": [],
     "routes":["/catalog"]
     },
    {"groupname": "ChangePassword",
     "group_description": "ChangePassword",
     "permissions": ["/user/change/password","/user/logout"],
     "routes":["/changepassword"]
     },
    {"groupname": "SystemDetailsView",
     "group_description": "SystemDetailsView",
     "permissions": ["/systemdetails/all"],
     "routes":["/systemdata"]
     },
    {"groupname": "SystemDetailsCreate",
     "group_description": "SystemDetailsCreate",
     "permissions": ["/systemdetails/add"],
     "routes":[]
     },
    {"groupname": "ToolSetView",
     "group_description": "ToolSetView",
     "permissions": ["/toolset/all", "/toolset/view/~"],
     "routes":["/toolset/all", "/toolset/view/:id"]
     },
    {"groupname": "ToolSetUpdate",
     "group_description": "ToolSetUpdate",
     "permissions": ["/toolset/update", "/toolset/upload/logo"],
     "routes":["/edit/toolset/:id"]
     },
    {"groupname": "ToolSetCreate",
     "group_description": "ToolSetCreate",
     "permissions": ["/toolset/add"],
     "routes":["/toolset/new"]
     },
    {"groupname": "ToolSetDelete",
     "group_description": "ToolSetDelete",
     "permissions": ["/toolset/delete/~"],
     "routes":["/toolset/delete/:id"]
     },
    {"groupname": "PreRequisites",
     "group_description": "PreRequisites",
     "permissions": ["/prerequisites/add", "/prerequisites/view", \
                     "/prerequisites/delete/~", "/prerequisites/update", \
                     "/prerequisites/view/~"],
     "routes":["/manage/prerequisites", "/add/new/prerequisite", \
               "/edit/prerequisite/:id", "/view/prerequisite/:id", \
               "/delete/prerequisite/:id"]
     },
    {"groupname": "MachineGroupsDelete",
     "group_description": "MachineGroupsDelete",
     "permissions": ["/machinegroups/delete/~"],
     "routes":["/delete/machine/group/:id"]
     },
    {"groupname": "MachineGroupsView",
     "group_description": "MachineGroupsView",
     "permissions": ["/machinegroups/view", "/machinegroups/view/~","/machinegroups/view/name/~"],
     "routes":["/manage/machine/groups", "/view/machine/group/:id"]
     },
    {"groupname": "MachineGroupsCreate",
     "group_description": "MachineGroupsCreate",
     "permissions": ["/machinegroups/add","/machinegroups/bulk/load"],
     "routes":["/add/machine/group"]
     },
    {"groupname": "MachineGroupsUpdate",
     "group_description": "MachineGroupsUpdate",
     "permissions": ["/machinegroups/update","/machinegroups/bulk/load"],
     "routes":["/edit/machine/group/:id"]
     },
    {"groupname": "DeploymentGroupView",
     "group_description": "DeploymentGroupView",
     "permissions": ["/deploymentrequest/group/view/~", "/deploymentrequest/group/all", "/deploymentrequest/group/saved/all", "/deploymentrequest/group/saved/view/~","/deploymentrequest/group/view/revert/~"],
     "routes":["/saved/requests", "/recent/requests","/deploymentrequest/group/revert/:id"]
     },
    {"groupname": "DeploymentGroupCreate",
     "group_description": "DeploymentGroupCreate",
     "permissions": ["/deploymentrequest/group/add",
                     "/deploymentrequest/group/toolset/add",
                     "/deploymentrequest/group/machine/add", "/deploymentrequest/group/saved/add",
                     "/deploymentrequest/group/machinegroup/new","/deploymentrequest/group/add/undeploy"],
     "routes":["/deploy/toolset/:id", "/deploy/duset/:id"]
     },
    {"groupname": "DeploymentGroupDelete",
     "group_description": "DeploymentGroupDelete",
     "permissions": ["/deploymentrequest/group/cancel/~", "/deploymentrequest/group/saved/delete/~"],
     "routes":[]
     },
    {"groupname": "DeploymentGroupUpdate",
     "group_description": "DeploymentGroupUpdate",
     "permissions": ["/deploymentrequest/group/retry", "/deploymentrequest/group/saved/update"],
     "routes":[]
     },
    {"groupname": "UsersGroupsView",
     "group_description": "UsersGroupsView",
     "permissions": ["/teams/view", "/teams/view/~"],
     "routes":["/manage/users/groups", "/view/user/group/:id", "/team/view/:id"]
     },
    {"groupname": "UsersGroupsCreate",
     "group_description": "UsersGroupsCreate",
     "permissions": ["/teams/add"],
     "routes":["/create/user/group"]
     },
    {"groupname": "UsersGroupsUpdate",
     "group_description": "UsersGroupsUpdate",
     "permissions": ["/teams/update"],
     "routes":["/edit/user/group/:id"]
     },
    {"groupname": "UsersGroupsDelete",
     "group_description": "UsersGroupsDelete",
     "permissions": ["/teams/delete/~"],  # To DO
     "routes":["/delete/user/group/:id"]
     },
    {"groupname": "TagsView",
     "group_description": "TagsView",
     "permissions": ["/tag/all", "/tag/view/~"],
     "routes":["/manage/tags", "/tag/view/:id"]
     },
    {"groupname": "TagsCreate",
     "group_description": "TagsCreate",
     "permissions": ["/tag/new"],
     "routes":["/tag/new"]
     },
    {"groupname": "TagsUpdate",
     "group_description": "TagsUpdate",
     "permissions": ["/tag/update"],
     "routes":["/tag/update"]
     },
    {"groupname": "TagsDelete",
     "group_description": "TagsDelete",
     "permissions": ["/tag/delete/~"],
     "routes":["/tag/delete/:id"]
     },
    {"groupname": "GeneralDetails",
     "group_description": "GeneralDetails",
     "permissions": ["/currenttime"],
     "routes":[]
     },
    {"groupname": "DeploymentUnitApprovalStatusView",
     "group_description": "DeploymentUnitApprovalStatusView",
     "permissions": ["/deploymentunitapprovalstatus/all", \
                     "/deploymentunitapprovalstatus/view/~",
                      "/deploymentunitapprovalstatus/view/name/~"],
     "routes":[]
     },
    {"groupname": "DeploymentUnitApprovalStatusCreate",
     "group_description": "DeploymentUnitApprovalStatusCreate",
     "permissions": ["/deploymentunitapprovalstatus/add"],
     "routes":[]
     },
    {"groupname": "DeploymentUnitApprovalStatusUpdate",
     "group_description": "DeploymentUnitApprovalStatusUpdate",
     "permissions": ["/deploymentunitapprovalstatus/update"],
     "routes":[]
     },
    {"groupname": "DeploymentUnitApprovalStatusDelete",
     "group_description": "DeploymentUnitApprovalStatusDelete",
     "permissions": ["/deploymentunitapprovalstatus/delete/~"],
     "routes":[]
     },
    {"groupname": "DeploymentUnitTypeView",
     "group_description": "DeploymentUnitTypeView",
     "permissions": ["/deploymentunittype/all", \
                     "/deploymentunittype/view/~"],
     "routes":[]
     },
    {"groupname": "DeploymentUnitTypeCreate",
     "group_description": "DeploymentUnitTypeCreate",
     "permissions": ["/deploymentunittype/new"],
     "routes":[]
     },
    {"groupname": "DeploymentUnitTypeUpdate",
     "group_description": "DeploymentUnitTypeUpdate",
     "permissions": ["/deploymentunittype/update"],
     "routes":[]
     },
    {"groupname": "DeploymentUnitTypeDelete",
     "group_description": "DeploymentUnitTypeDelete",
     "permissions": ["/deploymentunittype/delete/~"],
     "routes":[]
     },
    {"groupname": "DeploymentUnitView",
     "group_description": "DeploymentUnitView",
     "permissions": ["/deploymentunit/all", "/deploymentunit/view/~", \
                     "/deploymentunit/search/tag/~", "/deploymentunit/search/name/~"],
     "routes":["/dashboard/du", "/deploymentunit/view/:id", \
               "/redeploy/du/:du_id/build_number/:build_number/build_id/:build_id/machine/:machine_id", \
               "/undeploy/du/:du_id/build_number/:build_number/build_id/:build_id/machine/:machine_id", "/dashboard/du/:request_id"]
     },
    {"groupname": "DeploymentUnitCreate",
     "group_description": "DeploymentUnitCreate",
     "permissions": ["/deploymentunit/new"],
     "routes":["/deploymentunit/new"]
     },
    {"groupname": "DeploymentUnitUpdate",
     "group_description": "DeploymentUnitUpdate",
     "permissions": ["/deploymentunit/update", "/deploymentunit/upload/logo"],
     "routes":["/deploymentunit/edit/:id"]
     },
    {"groupname": "DeploymentUnitDelete",
     "group_description": "DeploymentUnitDelete",
     "permissions": ["/deploymentunit/delete/~"],
     "routes":["/delete/deploymentunit/:id"]
     },
    {"groupname": "DeploymentUnitSetView",
     "group_description": "DeploymentUnitSetView",
     "permissions": ["/deploymentunitset/all", "/deploymentunitset/view/~","/deploymentunitset/view/getbuilds/~","/deploymentunitset/view/states/~"],
     "routes":["/deploymentunitset/view/:id", "/deploymentunitset/all"]
     },
    {"groupname": "DeploymentUnitSetCreate",
     "group_description": "DeploymentUnitSetCreate",
     "permissions": ["/deploymentunitset/new"],
     "routes":["/deploymentunitset/new"]
     },
    {"groupname": "DeploymentUnitSetUpdate",
     "group_description": "DeploymentUnitSetUpdate",
     "permissions": ["/deploymentunitset/update", "/deploymentunitset/upload/logo"],
     "routes":["/deploymentunitset/edit/:id"]
     },
    {"groupname": "DeploymentUnitSetDelete",
     "group_description": "DeploymentUnitSetDelete",
     "permissions": ["/deploymentunitset/delete/~"],
     "routes":[]
     },
    {"groupname": "ReportsView",
     "group_description": "ReportsView",
     "permissions": ["/reports/all"],
     "routes":["/view/reports"]
     },
    {"groupname": "Plugins",
     "group_description": "Plugins",
     "permissions": ["/plugin/reload", "/plugin/install", "/plugin/uninstall/~",\
                      "/plugin/inactive/~", "/plugin/active/~", "/plugin/all",
                       "/plugin/view/~","/plugin/file/upload","/plugin/file/list/~","/plugin/file/remove/~",
                       "/plugin/exitpoint/new","/plugin/exitpoint/update","/plugin/file/view/~"],
     "routes":["/plugin", "/manage/plugins/deployment", "/plugin/deployment/upload"]
     },
    {"groupname": "MonitoringView",
     "group_description": "MonitoringView",
     "permissions": [],
     "routes":["/view/monitoring", "/view/monitoring/runningservices"]
     },
    {"groupname": "PersonalizeCreate",
     "group_description": "PersonalizeCreate",
     "permissions": ["/systemdetails/logoupload"],
     "routes":[]
     },
     {"groupname": "StateView",
     "group_description": "StateView",
     "permissions": ["/state/all/","/state/view/~", "/state/view/parent/~" ,"/state/view/parent/~/name/~"],
     "routes":["/view/du/state","/view/duset/state"]
     },
     {"groupname": "StateAdd",
     "group_description": "StateAdd",
     "permissions": ["/state/add"],
     "routes":["/create/du/state","/create/duset/state"]
     },
     {"groupname": "StateUpdate",
     "group_description": "StateUpdate",
     "permissions": ["/state/update"],
     "routes":[]
     },
     {"groupname": "StateDelete",
     "group_description": "StateDelete",
     "permissions": ["/state/delete/~"],
     "routes":["/state/delete/:id"]
     },
     {"groupname": "ToolsOnMachineView",
      "group_description": "ToolsOnMachineView",
      "permissions": ["/deployed/view/all","/deployed/view/machine_id/~/parent_entity_id/~/build_id/~"],
      "routes": []
     },
    {"groupname": "FlexibleAttributeView",
      "group_description": "View Flexible Attributes",
      "permissions": ["/flexattributes/view/all", "/flexattributes/view/entity/~","/flexattributes/view/~"],
      "routes": []
     },
      {"groupname": "FlexibleAttributeDelete",
      "group_description": "Delete Flexible Attributes",
      "permissions": [],
      "routes": []
     },
      {"groupname": "FlexibleAttributeAdd",
      "group_description": "Add Flexible Attributes",
      "permissions": ["/flexattributes/new"],
      "routes": ["/new/flexibleattributes"]
     },
      {"groupname": "FlexibleAttributeUpdate",
      "group_description": "Update Flexible Attributes",
      "permissions": ["/flexattributes/update"],
      "routes": ["/manage/flexibleattributes"]
     },
    {"groupname": "ProposedToolsCreate",
      "group_description": "ProposedToolsCreate",
      "permissions": ["/proposed/tool/approve"],
      "routes": ["/edit/tool/proposed/:id","/approve/tool/proposed/:id"]
     },
      {"groupname": "ProposedToolsView",
      "group_description": "ProposedToolsView",
      "permissions": ["/proposed/tool/view/all","/proposed/tool/view/~"],
      "routes": ["/proposed/tools/all","/view/proposed/tool/:id"]
     },
      {"groupname": "ProposedToolsDelete",
      "group_description": "ProposedToolsDelete",
      "permissions": ["/proposed/tool/delete/~"],
      "routes": []
     },
      {"groupname": "AuditingView",
      "group_description": "AuditingView",
      "permissions": ["/auditing/view/all","/auditing/view/id/~"],
      "routes": ["/view/audits"]
     },
    {"groupname": "RepositoryCreate",
      "group_description": "RepositoryCreate",
      "permissions": ["/repository/add"],
      "routes": ["/new/repository"]
     },
      {"groupname": "RepositoryUpdate",
      "group_description": "RepositoryUpdate",
      "permissions": ["/repository/update"],
      "routes": []
     },
      {"groupname": "RepositoryView",
      "group_description": "RepositoryView",
      "permissions": ["/repository/view/all","/repository/view/name/~","/repository/view/~","/repository/view/byparententity/~"],
      "routes": ["/view/repository"]
     },
      {"groupname": "RepositoryDelete",
      "group_description": "RepositoryDelete",
      "permissions": ["/repository/delete/~"],
      "routes": []
     }, 
      {"groupname": "SystemAdministration",
      "group_description": "SystemAdministration",
      "permissions": ["/server/restart"],
      "routes": []
     }
]

# list for Email Template reference data
EMAIL_TEMPLATE = [
    {
        "templateid": 1,
        "html": "passwordreset.html",
        "subject": "Password Reset Alert"
    },
    {
        "templateid": 2,
        "html": "deploymentcompleted.html",
        "subject": "Deployment Manager-Deployment Request Status"
    },
    {
        "templateid": 3,
        "html": "clonecompleted.html",
        "subject": "Deployment Manager-Clone Request Status"
    },
    {
        "templateid": 4,
        "html": "pullcompleted.html",
        "subject": "Deployment Manager-Pull Request Status"
    },
    {
        "templateid": 5,
        "html": "pushcompleted.html",
        "subject": "Deployment Manager-Push Request Status"
    },
    {
        "templateid": 6,
        "html": "syncstatus.html",
        "subject": "SyncServices - Status"
    },
    {
        "templateid": 7,
        "html": "newsync.html",
        "subject": "SyncServices - New Entry"
    },
    {
        "templateid": 8,
        "html": "forgotreset.html",
        "subject": "Password Reset Alert"
    },
    {
        "templateid": 9,
        "html": "pushstatus.html",
        "subject": "Push Status Alert"
    },
    {
        "templateid": 10,
        "html": "distributioncompleted.html",
        "subject": "DistributionCenterService - Status"
    },
    {
        "templateid": 11,
        "html": "newdistribution.html",
        "subject": "DistributionSyncServices  - New Entry"
    },
    {
        "templateid": 12,
        "html": "comparedistribution.html",
        "subject": "DistributionSyncServices  - Processed Entry"
    },
    {
        "templateid": 13,
        "html": "groupdeploymentcomplete.html",
        "subject": "groupdeploymentcompleted",
    },
    {
        "templateid": 14,
        "html": "newuser.html",
        "subject": "New user created",
    },
    {
        "templateid": 15,
        "html": "newtoolproposal.html",
        "subject": "New Tool Proposal-Approval Required",
    },
    {
        "templateid": 16,
        "html": "toolproposalapproved.html",
        "subject": "Your Proposed Tool was approved !",
    },
    {
        "templateid": 17,
        "html": "newtoolproposalforuser.html",
        "subject": "New Tool Proposal was received",
    },
    {
        "templateid": 18,
        "html": "toolproposalrejected.html",
        "subject": "Your Proposed Tool was rejected !",
    }]

# list for Machine Type reference data
MACHINE_TYPE = [
    {"type": "Production"},
    {"type": "IUT"},
    {"type": "UT"},
    {"type": "ST"},
    {"type": "Value Package Master"},
    {"type": "Other"},
    {"type": "UAT"},    
    {"type": "SIT"},
    {"type": "PET"},
    {"type": "eDPM"}]

# list for Dummy Accounts reference data
ACCOUNT = [
    {"mps_version": "mps 1",
     "status": "1",
     "name": "Test"
     }]

# list for Dummy Deployment Unit Type s reference data
DEPLOYMENT_UNIT_TYPE = [
    {"name": "Fast Track"},
    {"name": "Hot Fix"},
    {"name": "Version"}]

# DeploymentUnitApprovalStatus
DEPLOYMENT_UNIT_APPROVAL_STATUS = [
    {"name": "Created"},
    {"name": "Tested"},
    {"name": "Certified"}]


# FLEX_ATTRIBUTES
FLEX_ATTRIBUTES =[
    {
        "name": "compTypes",
        "title": "Component Type",
        "type": "Select",
        "entity": "DeploymentUnit",
        "default_value": "",
        "description": "Application component type (CRM-BACKEND, CRM-CLIENT)",
        "is_mandatory": False,
        "is_active": True,
        "valid_values": [
            "CRM-DB",
            "CRM-BACKEND",
            "CRM-CLIENT",
            "OMS-DB",
            "OMS-BACKEND"
        ]
    },
    {
        "name": "compTypes",
        "title": "Component Type",
        "type": "MultiSelect",
        "entity": "Machine",
        "default_value": "",
        "description": "Application component type (CRM-BACKEND, CRM-CLIENT)",
        "is_mandatory": False,
        "is_active": True,
        "valid_values": [
            "CRM-DB",
            "CRM-BACKEND",
            "CRM-CLIENT",
            "OMS-DB",
            "OMS-BACKEND"
        ]
    }
]

# Connect routes and routes group
USERS = [
    {
        "status": "active",
        "accountid": "Test",
        "employeeid": "99999",
        "roleid": "Admin",
        "user": "Admin",
        "password": default_admin_password,
        "email": "testAdmin@amdocs.com"
    },
    {
        "status": "active",
        "accountid": "Test",
        "employeeid": "99999",
        "roleid": "SuperAdmin",
        "user": "SuperAdmin",
        "password": default_admin_password,
        "email": "SuperAdmin@amdocs.com"
    },
    {
        "status": "active",
        "accountid": "Test",
        "employeeid": "99999",
        "roleid": "Operator",
        "user": "Operator",
        "password": "12345",
        "email": "testOperator@amdocs.com"
    },
    {
        "status": "active",
        "accountid": "Test",
        "employeeid": "99999",
        "roleid": "Guest",
        "user": "Guest",
        "password": "guest",
        "email": "testGuest@amdocs.com"
    },
    {
        "status": "active",
        "accountid": "Test",
        "employeeid": "99999",
        "roleid": "DPMsysCI",
        "user": "DPMsysCI",
        "password": "dpmsysci",
        "email": "testDPMsysCI@amdocs.com"
    }
]

CONFIG_DATA = [
    {
        "name": "Mailer",
        "configid": 1,
        "debug": "False",
        "host": "umg.corp.amdocs.com",
        "server": "umg.corp.amdocs.com",
        "port": "587",
        "tls": "True",
        "ssl": "False",
        "username": "",
        "password": "",
        "defaultsender": "DeploymentManager-DoNotReply@amdocs.com",
        "socketip": "127.0.0.1",
        "socketport": "8080",
        "field_types": [
            {"name": "username", "type": "textbox"},
            {"name": "tls", "type": "dropdown",
                "available_values": ["true", "false"]},
            {"name": "password", "type": "password"},
            {"name": "port", "type": "number"},
            {"name": "defaultsender", "type": "textbox"},
            {"name": "debug", "type": "dropdown",
                "available_values": ["true", "false"]},
            {"name": "server", "type": "textbox"},
            {"name": "ssl", "type": "dropdown",
                "available_values": ["true", "false"]},
            {"name": "host", "type": "textbox"},
            {"name": "socketip", "type": "textbox"},
            {"name": "port", "type": "number"}
        ]
    },
    {
        "name": "MailerService",
        "intervalGiven": "1",
        "configid": 2,
        "enable": "true",
        "type": "interval",
        "hrs": "00",
        "min": "00",
        "field_types": [
            {"name": "intervalGiven", "type": "number"},
            {"name": "enable", "type": "dropdown",
                "available_values": ["true", "false"]},
            {"name": "type", "type": "dropdown",
                "available_values": ["interval", "scheduled"]},
            {"name": "hrs", "type": "number"},
            {"name": "min", "type": "number"}
        ]
    },
    {
        "name": "DeploymentRequestService",
        "intervalGiven": "0.5",
        "noOfThreads": "2",
        "configid": 3,
        "enable": "true",
        "type": "interval",
        "hrs": "00",
        "min": "00",
        "skipDeploymentInd":"true",
        "machineMatchingInd":"false",
        "enable_callback": "false",
        "callback_timeout": 30,
        "field_types": [
            {"name": "intervalGiven", "type": "number"},
            {"name": "noOfThreads", "type": "number"},
            {"name": "enable", "type": "dropdown",
                "available_values": ["true", "false"]},
            {"name": "type", "type": "dropdown",
                "available_values": ["interval", "scheduled"]},
            {"name": "hrs", "type": "number"},
            {"name": "min", "type": "number"},
            {"name": "skipDeploymentInd", "type": "dropdown",
                "available_values": ["true", "false"]},
            {"name": "machineMatchingInd", "type": "dropdown",
             "available_values": ["true", "false"]},
            {"name": "enable_callback", "type": "dropdown", "available_values": ["true", "false"]},
            {"name": "callback_timeout", "type": "number"}
        ]
    },
    {
        "name": "CloneRequestService",
        "intervalGiven": "0.5",
        "noOfThreads": "2",
        "configid": 4,
        "enable": "true",
        "type": "interval",
        "hrs": "00",
        "min": "00",
        "field_types": [
            {"name": "intervalGiven", "type": "number"},
            {"name": "noOfThreads", "type": "number"},
            {"name": "enable", "type": "dropdown",
                "available_values": ["true", "false"]},
            {"name": "type", "type": "dropdown",
                "available_values": ["interval", "scheduled"]},
            {"name": "hrs", "type": "number"},
            {"name": "min", "type": "number"}
        ]
    },
    {
        "name": "AppLogger",
        "loggingLevel": "TRACE",
        "configid": 5,
        "enable": "true",
        "log_to_console": "true",
        "backupCount" : 0,
        "logFormat" :"%(asctime)s[%(levelname)-5.5s]%(message)s",
        "dateFormat":"%d-%m-%Y %H:%M:%S",
        "field_types": [{"name": "enable", "type": "dropdown", "available_values": ["true", "false"]},
                        {"name": "loggingLevel", "type": "dropdown",
                         "available_values":
                         ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET', 'TRACE']},
                        {"name": "logFormat", "type": "textbox"},
                        {"name": "dateFormat", "type": "textbox"},
                        {"name": "log_to_console", "type": "dropdown", "available_values": ["true", "false"]},
                        {"name": "backupCount", "type": "number"}
                        ]
    },
    {
        "name": "AuthService",
        "expiration": "6000",
        "configid": 6,
        "enable_ldap":"false",
        "allow_multi_user_session":"false",
        "ldap_server": "ldap://raappdc1.corp.amdocs.com:3268",
        "ldap_base_dn": "DC=corp,DC=amdocs,DC=com",
        "email_domain": "@amdocs.com",
        "admin_role_groups": "eDPMDev",
        "operator_role_groups": "",
        "field_types": [{"name": "expiration", "type": "number"},
                        {"name": "enable_ldap", "type": "dropdown", "available_values": ["true", "false"]},
                        {"name": "ldap_server", "type": "textbox"},
                        {"name": "ldap_base_dn", "type": "textbox"},
                        {"name": "email_domain", "type": "textbox"},
                        {"name": "admin_role_groups", "type": "textbox"},
                        {"name": "operator_role_groups", "type": "textbox"},
                        {"name": "allow_multi_user_session", "type": "dropdown", "available_values": ["true", "false"]}]
    },
    {
        "name": "CloneAccountServiceDetails",
        "gitlab_token": "oiV1nt2VWEFtUJZfgM8F",
        "gitlab_user": "vpadmin",
        "gitlab_password": "Unix11!!",
        "local_jenkins_job_path": "/var/lib/jenkins/jobs/",
        "jenkins_version": "1.651.3",
        "git_lab_rest_api_url": "http://illin4467:80/api/v3/",
        "remote_dpm_port": "8000",
        "configid": 7,
        "target_artifact_auth_repo_type": "nexus2:2.14.2_01",
        "target_dpm_user": "admin",
        "target_dpm_password" :"12345",
        "account_gitlab_password":"vpadmin123",
        "field_types": [{"name": "gitlab_token", "type": "textbox"},
                        {"name": "gitlab_user", "type": "textbox"},
                        {"name": "gitlab_password", "type": "password"},
                        {"name": "local_jenkins_job_path", "type": "textbox"},
                        {"name": "git_lab_rest_api_url", "type": "textbox"},
                        {"name": "remote_dpm_port", "type": "number"},
                        {"name": "target_dpm_user", "type": "textbox"},
                        {"name": "account_gitlab_password", "type": "password"},
                        {"name": "target_dpm_password", "type": "password"},
                        {"name": "jenkins_version", "type": "dropdown", "available_values": ["1.651.3", "2.140","2.149"]},
                        {"name": "target_artifact_auth_repo_type","type": "dropdown", "available_values": ["nexus2:2.14.2_01", "nexus3:3.12.0"]},
                        ]
    },
    {
        "name": "JenkinsAuth",
        "jenkins_user": "vpadmin",
        "jenkins_pass": "vpadmin",
        "configid": 8,
        "field_types": [{"name": "jenkins_user", "type": "textbox"},
                        {"name": "jenkins_pass", "type": "password"},
                        ]
    },
    {
        "name": "SyncServices",
        "intervalGiven": "10",
        "enable": "false",
        "full_sync_flag": "true",
        "distribution_list": "admin@amdocs.com",
        "configid": 9,
        "type": "scheduled",
        "hrs": "00",
        "min": "00",
        "enable_callback": "false",
        "callback_timeout": 30,
        "field_types": [{"name": "intervalGiven", "type": "number"},
                        {"name": "full_sync_flag",
                         "type": "dropdown", "available_values": ["true", "false"]},
                        {"name": "enable", "type": "dropdown",
                            "available_values": ["true", "false"]},
                        {"name": "distribution_list", "type": "email"},
                        {"name": "type", "type": "dropdown",
                         "available_values": ["interval", "scheduled"]},
                        {"name": "hrs", "type": "number"},
                        {"name": "min", "type": "number"},
                        {"name": "enable_callback",
                         "type": "dropdown", "available_values": ["true", "false"]},
                         {"name": "callback_timeout", "type": "number"}
                        ]
    },
    {
        "name": "PullServices",
        "intervalGiven": "10",
        "configid": 10,
        "enable": "false",
        "timeout": "600",  # 5 mins,
        "type": "scheduled",
        "hrs": "00",
        "min": "00",
        "count_of_files": "2",
        "field_types": [{"name": "intervalGiven", "type": "number"},
                        {"name": "enable", "type": "dropdown", \
                         "available_values": ["true", "false"]},
                        {"name": "timeout", "type": "number"},
                        {"name": "type", "type": "dropdown", \
                         "available_values": ["interval", "scheduled"]},
                        {"name": "hrs", "type": "number"},
                        {"name": "min", "type": "number"}
                        ]
    },
    {
        "name": "PushServices",
        "intervalGiven": "10",
        "configid": 11,
        "enable": "false",
        "remote_machine_import_path": remote_sync_import_path,
        "type": "scheduled",
        "hrs": "00",
        "min": "00",
        "count_of_files": "2",
        "allow_split": "true",
        "field_types": [{"name": "intervalGiven", "type": "number"},
                        {"name": "enable", "type": "dropdown",
                            "available_values": ["true", "false"]},
                        {"name": "remote_machine_import_path", "type": "textbox"},
                        {"name": "type", \
                         "type": "dropdown", "available_values": ["interval", "scheduled"]},
                        {"name": "hrs", "type": "number"},
                        {"name": "min", "type": "number"},
                        {"name": "count_of_files", "type": "number"},
                        {"type": "dropdown", "name": "allow_split",
                            "available_values": ["true", "false"]}
                        ]
    },
    {
        "name": "DistributionCenterService",
        "hrs": "00",
        "min": "00",
        "configid": 12,
        "enable": "false",
        "distribution_list": "admin@amdocs.com",
        "remote_machine_import_path": remote_distribution_import_path,
        "type": "scheduled",
        "intervalGiven": "10",
        "field_types": [{"name": "intervalGiven", "type": "number"},
                        {"name": "enable", "type": "dropdown",
                            "available_values": ["true", "false"]},
                        {"name": "remote_machine_import_path", "type": "textbox"},
                        {"name": "distribution_list", "type": "email"},
                        {"name": "type", \
                         "type": "dropdown", "available_values": ["interval", "scheduled"]},
                        {"name": "hrs", "type": "number"},
                        {"name": "min", "type": "number"}
                        ]
    },
    {
        "name": "DistributionSyncServices",
        "intervalGiven": "10",
        "enable": "false",
        "distribution_list": "admin@amdocs.com",
        "configid": 13,
        "type": "scheduled",
        "hrs": "00",
        "min": "00",
        "field_types": [{"name": "intervalGiven", "type": "number"},
                        {"name": "enable", "type": "dropdown",
                            "available_values": ["true", "false"]},
                        {"name": "distribution_list", "type": "email"},
                        {"name": "type", \
                         "type": "dropdown", "available_values": ["interval", "scheduled"]},
                        {"name": "hrs", "type": "number"},
                        {"name": "min", "type": "number"}
                        ]
    },
    {
        "name": "ContributionCenterService",
        "intervalGiven": "10",
        "enable": "false",
        "git_path": base_path + "git",
        "distribution_list": "admin@amdocs.com",
        "configid": 14,
        "type": "scheduled",
        "hrs": "00",
        "min": "00",
        "field_types": [{"name": "intervalGiven", "type": "number"},
                        {"name": "enable", "type": "dropdown",
                            "available_values": ["true", "false"]},
                        {"name": "git_path", "type": "textbox"},
                        {"name": "distribution_list", "type": "email"},
                        {"name": "type", \
                         "type": "dropdown", "available_values": ["interval", "scheduled"]},
                        {"name": "hrs", "type": "number"},
                        {"name": "min", "type": "number"}
                        ]
    },               
    {
    "enable" : "false",
    "buildolderthandays" : 30,
    "olderthandays" : 30,
    "field_types" : [ 
        {
            "type" : "number",
            "name" : "intervalGiven"
        }, 
        {
            "type" : "dropdown",
            "name" : "enable",
            "available_values" : [ 
                "true", 
                "false"
            ]
        }, 
        {
            "type" : "dropdown",
            "name" : "RemoveActualArtifacts",
            "available_values" : [ 
                "true", 
                "false"
            ]
        }, 
        {
            "type" : "number",
            "name" : "buildcount"
        }, 
        {
            "type" : "number",
            "name" : "olderthandays"
        }, 
        {
            "type" : "dropdown",
            "name" : "type",
            "available_values" : [ 
                "interval", 
                "scheduled"
            ]
        }, 
        {
            "type" : "number",
            "name" : "hrs"
        }, 
        {
            "type" : "number",
            "name" : "min"
        }, 
        {
            "type" : "number",
            "name" : "buildolderthandays"
        }, 
        {
            "type" : "checkbox",
            "name" : "EntitiesToHandle",
            "available_values" : [ 
                "Logos", 
                "MediaFiles", 
                "Emails", 
                "GuestUsers", 
                "GitPush", 
                "Sync", 
                "Distribition", 
                "InactiveBuild", 
                "ActiveBuild", 
                "DeployementRequestlogs", 
                "CloneRequestLogs", 
                "OldData",
                "Auditing"
            ]
        }
    ],
    "EntitiesToHandle" : {
        "12" : True,
        "11" : True,
        "10" : True,
        "1" : True,
        "0" : True,
        "3" : True,
        "2" : True,
        "5" : True,
        "4" : True,
        "7" : True,
        "6" : True,
        "9" : True,
        "8" : True
    },
    "intervalGiven" : 10,
    "name" : "CleanerServices",
    "min" : 0,
    "RemoveActualArtifacts" : "false",
    "hrs" : 0,
    "configid" : 15,
    "type" : "scheduled",
    "buildcount" : 30
    },
    {
        "name": "AuditingServices",
        "olderthandays": "30",
        "enable": "true",
        "configid": 19,
        "field_types": [{"name": "enable", "type": "dropdown",
                            "available_values": ["true", "false"]},
                        {"name": "olderthandays", "type": "number"}]
    },
    {
        "name": "ProposedToolService",
        "support_details": "vpadmin@amdocs.com",
        "gitpath": base_path + "git",
        "jenkinspath": base_path + "jenkins",
        "package": "amdocs.aio",
        "reponame": "vp_builds",
        "configid": 20,
        "enable": "true",
        "field_types": [{"name": "support_details", "type": "textbox"},
                        {"name": "gitpath", "type": "textbox"},
                        {"name": "jenkinspath", "type": "textbox"},
                        {"name": "package", "type": "textbox"},
                        {"name": "reponame", "type": "textbox"},
                        {"name": "enable", "type": "dropdown",
                            "available_values": ["true", "false"]}]
    },
    {
        "name": "FabricService",
        "configid": 21,
        "command_timeout": 60*60,
        "field_types": [{"name": "command_timeout", "type": "number"}]
    },
    {
        "name": "Deployment",
        "configid": 22,
        "entity_exposed_attributes": "name",
        "machine_exposed_attributes": "machine_name",
        "field_types": [{"name": "entity_exposed_attributes", "type": "textbox"},
                        {"name": "machine_exposed_attributes", "type": "textbox"}]
    },
    {
        "name": "MachineGroup",
        "configid": 23,
        "deployment_details_count_to_display": 30,
        "field_types": [{"name": "deployment_details_count_to_display", "type": "textbox"}]   
                        }
]


EXITPOINTPLUGINS = [
    {
        "repo_provider": "Yum",
        "plugin_name": "YumSyncPlugin",
        "type": "sync",
        "repo_user": "admin",
        "repo_password": "admin123",
        "repo_url": "http://"+default_nexus_container_name+":8081/nexus/service/local/artifact/maven/content"
    },
    {
        "repo_provider": "Docker",
        "plugin_name": "DockerSyncPlugin",
        "type": "sync"
    },
    {
        "plugin_name": "DefaultDeploymentPlugin",
        "type": "deployment"
    },
    {
        "plugin_name": "DirectNexusDeploymentPlugin",
        "type": "deployment"
    },
    {
        "plugin_name": "WindowsDeploymentPlugin",
        "type": "deployment"
    },
	{
        "plugin_name": "DefaultSudoDeploymentPlugin",
        "type": "deployment"
    },
    {
        "plugin_name": "DefaultNexus2RepositoryPlugin",
        "type": "repository"
    },
    {
        "plugin_name": "SWPPPCustomNexus2RepositoryPlugin",
        "type": "repository"
    },
    {
        "plugin_name": "DefaultNexus3RepositoryPlugin",
        "type": "repository"
    },
    {
        "plugin_name": "DummyRepositoryPlugin",
        "type": "repository"
    },
    {
        "plugin_name": "JfrogArtifactoryRepositoryPlugin",
        "type": "repository"
    },
    {
        "plugin_name": "SWPPPCustomDeploymentPlugin",
        "type": "deployment"
    }
]

REPOSITORY_DATA=[
                 {
        "name":"DefaultNexus2Repository",        
        "repo_user": "admin",
        "repo_pass": "admin123",
        "upload_protocol": "http", #"http", "mvn","filesystem"
        "upload_type": "single", # "single","bulk"
        "base_url": "http://"+default_nexus_container_name+":8081/nexus/repository",
        "file_path_url": "http://"+default_nexus_container_name+":8081/nexus/content/repositories",
        "http_url": "http://"+default_nexus_container_name+":8081/nexus/service/local/artifact/maven/content",
        "mvn_url": "http://"+default_nexus_container_name+":8081/nexus/content/repositories/",
        "list_all_repositories_url": "http://"+default_nexus_container_name+":8081/nexus/service/local/repositories",
        "create_repo_url": "http://"+default_nexus_container_name+":8081/nexus/service/local/repositories",        
        "repo_path": base_path+"nexus/storage",
        "force_upload":"false", #"true","false"
        "additional_artifacts_upload":"true", #"true","false"
        "handler" : "DefaultNexus2RepositoryPlugin",
        "is_default_repo_ind": "true"
    },
    {
        "name":"DefaultNexus3Repository",
        "repo_user": "admin",
        "repo_pass": "admin123",
        "upload_protocol": "http", #"http", "mvn"
        "upload_type": "single",# "single"
        "base_url": "http://"+default_nexus_container_name+":8081/repository",
        "file_path_url": "http://"+default_nexus_container_name+":8081/repository",
        "mvn_url": "http://"+default_nexus_container_name+":8081/repository/",
        "list_all_repositories_url": "http://"+default_nexus_container_name+":8081/service/rest/beta/repositories",
        "add_script_url": "http://"+default_nexus_container_name+":8081/service/rest/v1/script",
        "run_script_url": "http://"+default_nexus_container_name+":8081/service/rest/v1/script/~/run",
        "remove_script_url": "http://"+default_nexus_container_name+":8081/service/rest/v1/script/~",        
        "force_upload":"false", #"true","false"
        "additional_artifacts_upload":"true", #"true","false"
        "handler" : "DefaultNexus3RepositoryPlugin",
        "is_default_repo_ind": "false"
    },
    {
        "name":"JfrogArtifactoryRepository",
        "repo_user": "admin",
        "repo_pass": "password",
        "base_url": "http://vp_jfrog_artifactory:9045/artifactory",
        "additional_artifacts_upload":"true", #"true","false"        
        "handler" : "JfrogArtifactoryRepositoryPlugin",
        "is_default_repo_ind": "false"
    },
    {
        "name":"SWPPPKeyStoreRepository",
        "host": "kvstore",
        "port": "6379",
        "user": "redisadmin",
        "pass": "Unix11!",
        "additional_artifacts_upload":"false", #"true","false"        
        "handler" : "DummyRepositoryPlugin",
        "is_default_repo_ind": "false"
    }
    ]