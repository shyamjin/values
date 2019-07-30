require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['editDUSetStateControllerApp', 'manageStatesControllerApp', 'addNewDUStateControllerApp', 'addNewDUSetStateControllerApp']
});

define(['angular', 'ngResource', 'uiRouter', 'editDUSetStateControllerApp', 'manageStatesControllerApp', 'addNewDUStateControllerApp', 'addNewDUSetStateControllerApp'],function (app) {
  'use strict';

var statesRoutesApp = angular.module('statesRoutesApp', ['ui.router','editDUSetStateControllerApp', 'manageStatesControllerApp', 'addNewDUStateControllerApp', 'addNewDUSetStateControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('manageStates', {
        url: '/view/du/state',
        views: {
            "main": {
                templateUrl: 'static/partials/states/states.partial.html',
                controller: 'ManageStatesController'
            }
        },
        data: {
            pageTitle: 'Manage States'
        }
    }).state('viwDUSetState', {
        url: '/view/duset/state',
        views: {
            "main": {
                templateUrl: 'static/components/states/manage-duset-state-content/managedusetstatecontent.component.html',
                controller: 'editDUSetStateController'
            }
        },
        data: {
            pageTitle: 'Manage States'
        }
}).state('createDUState', {
        url: '/create/du/state',
        views: {
            "main": {
                templateUrl: 'static/components/states/create-du-state-content/createdustatecontent.component.html',
                controller: 'CreateNewDUStateController'
            }
        },
        data: {
            pageTitle: 'Manage States'
        }
}).state('createDUSetState', {
        url: '/create/duset/state',
        views: {
            "main": {
                templateUrl: 'static/components/states/create-duset-state-content/createdusetstatecontent.component.html',
                controller: 'CreateNewDUSetStateController'
            }
        },
        data: {
            pageTitle: 'Manage States'
        }
});
});

});