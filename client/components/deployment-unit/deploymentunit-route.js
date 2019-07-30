require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['dashboardDUAllControllerApp', 'deploymentUnitDashboardControllerApp',
    'addNewDUControllerApp', 'editDUControllerApp', 'viewDUControllerApp', 'addNewDUSetControllerApp',
    'allDUSetControllerApp', 'editDUSetControllerApp', 'viewDUSetControllerApp']
});

define(['angular', 'uiRouter', 'dashboardDUAllControllerApp', 'deploymentUnitDashboardControllerApp',
'addNewDUControllerApp', 'editDUControllerApp', 'viewDUControllerApp', 'addNewDUSetControllerApp',
'allDUSetControllerApp', 'editDUSetControllerApp', 'viewDUSetControllerApp'], function (app) {
  'use strict';

var deploymentUnitsRoutesApp = angular.module('deploymentUnitsRoutesApp', ['ui.router', 'dashboardDUAllControllerApp',
'deploymentUnitDashboardControllerApp', 'addNewDUControllerApp', 'editDUControllerApp', 'viewDUControllerApp', 'addNewDUSetControllerApp',
'allDUSetControllerApp', 'editDUSetControllerApp', 'viewDUSetControllerApp']).config(function config($stateProvider){
    $stateProvider.state('duDashboard', {
        url: '/dashboard/du',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-unit/dashboardDU/dashboard-du.partial.html',
                controller:'DeploymentUnitDashboardController'
            }
        },
        data: {
            pageTitle: 'DU'
        }
    }).state('newDU', {
        url: '/deploymentunit/new',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-unit/create-du/create-du.partial.html',
                controller:'CreateNewDUController'
            }
        },
        data: {
            pageTitle: 'Create New DU'
        }
    }).state('editDU', {
        url: '/deploymentunit/edit/:id',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-unit/edit-du/edit-du.partial.html',
                controller:'EditDUController'
            }
        },
        data: {
            pageTitle: 'Edit DU'
        }
    }).state('viewDU', {
        url: '/deploymentunit/view/:id',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-unit/show-du/show-du.partial.html',
                controller:'ViewDUController'
            }
        },
        data: {
            pageTitle: 'DU Details'
        }
    }).state('createDUSet', {
        url: '/deploymentunitset/new',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-unit/create-du-sets/create-du-set.partial.html',
                controller:'CreateNewDUSetController'
            }
        },
        data: {
            pageTitle: 'Create New DU Package'
        }
    }).state('duSetDashboard', {
        url: '/deploymentunitset/all',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-unit/dashboardDU/dashboard-du.partial.html',
                controller:'AllDUSetController'
            }
        },
        data: {
            pageTitle: 'DU'
        }
    }).state('editDUSet', {
        url: '/deploymentunitset/edit/:id',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-unit/edit-du-set/edit-du-set.partial.html',
                controller:'EditDUSetController'
            }
        },
        data: {
            pageTitle: 'Edit DU Package'
        }
    }).state('viewDUSet', {
        url: '/deploymentunitset/view/:id',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-unit/show-du-set/show-du-set.partial.html',
                controller:'ViewDUSetController'
            }
        },
        data: {
            pageTitle: 'DU Package Details'
        }
    }).state('runningServiceDUDashboard', {
        url: '/dashboard/du/:request_id',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-unit/dashboardDU/dashboard-du.partial.html',
                controller:'DeploymentUnitDashboardController'
            }
        },
        data: {
            pageTitle: 'DU'
        }
    });
});

});