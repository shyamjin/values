require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageMachineControllerApp', 'bulkMachineUploadControllerApp', 'addNewMachineControllerApp', 'editMachineControllerApp',
    'addNewMachineGroupControllerApp', 'editMachineGroupControllerApp', 'manageMachineGroupsControllerApp', 'deleteMachineGroupControllerApp']
});

define(['angular', 'ngResource', 'uiRouter',
'manageMachineControllerApp', 'bulkMachineUploadControllerApp', 'addNewMachineControllerApp', 'editMachineControllerApp',
'addNewMachineGroupControllerApp', 'editMachineGroupControllerApp', 'manageMachineGroupsControllerApp', 'deleteMachineGroupControllerApp'],
function (app) {
  'use strict';

var machineRoutesApp = angular.module('machineRoutesApp', ['ui.router',
'manageMachineControllerApp', 'bulkMachineUploadControllerApp', 'addNewMachineControllerApp', 'editMachineControllerApp',
'addNewMachineGroupControllerApp', 'editMachineGroupControllerApp', 'manageMachineGroupsControllerApp', 'deleteMachineGroupControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('manageMachines', {
        url: '/machines',
        views: {
            "main": {
                templateUrl: 'static/partials/machines/machines.partial.html',
                controller: 'MachineController'
            }
        },
        data: {
            pageTitle: 'Manage Machines'
        }
    }).state('editmachine', {
        url: '/editmachine/:id',
        views: {
            "main": {
                 templateUrl: 'static/partials/machines/machines.partial.html',
                controller: 'EditMachineController'


            }
        },
        data: {
            pageTitle: 'Manage Machines'

        }
    }).state('AddNewMachine', {
        url: '/AddNewMachine',
        views: {
            "main": {
                 templateUrl: 'static/components/machines/create-anew-machine-content/createanewmachinecontent.component.html',
                controller: 'AddMachineController'
            }
        },
        data: {
            pageTitle: 'Manage Machines'

        }
    }).state('bulkMachineUpload', {
        url: '/bulk/machines',
        views: {
            "main": {
                templateUrl: 'static/components/machines/create-machines-bulk-content/createbulkcontent.component.html',
                controller: 'BulkMachineUploadController'
            }
        },
        data: {
            pageTitle: 'Manage Machines'
        }
    }).state('reDeployTool', {
        url: '/redeploy/version/:version_id/build_number/:build_number/build_id/:build_id/machine/:machine_id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/deploy-tools/deploy-tools.partial.html',
                controller: 'DeployToolController'
            }
        },
        data: {
            pageTitle: 'Re-deploy Tool'
        }
    }).state('unDeployTool', {
        url: '/undeploy/version/:version_id/build_number/:build_number/build_id/:build_id/machine/:machine_id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/deploy-tools/deploy-tools.partial.html',
                controller: 'DeployToolController'
            }
        },
        data: {
            pageTitle: 'Un-deploy Tool'
        }
    }).state('reDeployDU', {
        url: '/redeploy/du/:du_id/build_number/:build_number/build_id/:build_id/machine/:machine_id',
        views: {
            "main": {
                templateUrl: 'static/partials/deploy-du/deploy-du.partial.html',
                controller: 'DeployDUController'
            }
        },
        data: {
            pageTitle: 'Re-deploy DU'
        }
    }).state('unDeployDU', {
        url: '/undeploy/du/:du_id/build_number/:build_number/build_id/:build_id/machine/:machine_id',
        views: {
            "main": {
                templateUrl: 'static/partials/deploy-du/deploy-du.partial.html',
                controller: 'DeployDUController'
            }
        },
        data: {
            pageTitle: 'Un-deploy DU'
        }
    }).state('revertDU', {
        url: '/revert/du/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/deploy-du/deploy-du.partial.html',
                controller: 'DeployDUController'
            }
        },
        data: {
            pageTitle: 'Revert DU'
        }
    }).state('upgradeTool', {
        url: '/upgrade/oldversion/:old_version_id/newversion/:new_version_id/machine/:machine_id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/deploy-tools/deploy-tools.partial.html',
                controller: 'DeployToolController'
            }
        },
        data: {
            pageTitle: 'Upgrade Tool'
        }
    }).state('manageMachineGroups', {
        url: '/manage/machine/groups',
        views: {
            "main": {
                templateUrl: 'static/components/machines/manage-machine-groups-content/managemachinegroupscontent.component.html',
                controller: 'ManageMachineGroupsController'
            }
        },
        data: {
            pageTitle: 'Manage Machines'
        }
    }).state('createMachineGroup', {
        url: '/add/machine/group',
        views: {
            "main": {
                templateUrl: 'static/components/machines/create-anew-machine-group-content/createanewmachinegroupcontent.component.html',
                controller: 'CreateMachineGroupController'
            }
        },
        data: {
            pageTitle: 'Manage Machines'
        }
    }).state('editMachineGroup', {
        url: '/edit/machine/group/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/machines/machines.partial.html',
                controller: 'EditMachineGroupController'
            }
        },
        data: {
            pageTitle: 'Manage Machines'
        }
    }).state('deleteMachineGroup', {
        url: '/delete/machine/group/:id',
        views: {
            "main": {
                templateUrl: 'machine/manage-machine-groups.tpl.html',
                controller: 'DeleteMachineGroupController'
            }
        },
        data: {
            pageTitle: 'Manage Machine Groups'
        }
    });

});

});