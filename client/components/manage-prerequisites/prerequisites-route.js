require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['managePrerequisitesControllerApp', 'addNewPrerequisiteControllerApp', 'editPrerequisiteController']
});

define(['angular', 'uiRouter', 'managePrerequisitesControllerApp', 'addNewPrerequisiteControllerApp', 'editPrerequisiteController'],function (app) {
  'use strict';

var prerequisitesRoutesApp = angular.module('prerequisitesRoutesApp', ['ui.router', 'managePrerequisitesControllerApp', 'addNewPrerequisiteControllerApp', 'editPrerequisiteController']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('managePrerequisites', {
        url: '/manage/prerequisites',
        views: {
            "main": {
                templateUrl: 'static/partials/manage-prerequisites/manage-prerequisites.partial.html',
                controller: 'ManagePrerequisitesController'
            }
        },
        data: {
            pageTitle: 'Manage Prerequisites'
        }
    }).state('editPrerequisites', {
        url: '/prerequisite/update',
        views: {
            "main": {
                templateUrl: 'static/partials/manage-prerequisites/manage-prerequisites.partial.html',
                controller: 'EditPrerequisiteController'
            }
        },
        data: {
            pageTitle: 'Manage Prerequisites'
        }
    }).state('createPrerequisite', {
        url: '/add/new/prerequisite',
        views: {
            "main": {
                templateUrl: 'static/partials/manage-prerequisites/manage-prerequisites.partial.html',
                controller: 'CreateNewPrerequisiteController'
            }
        },
        data: {
            pageTitle: 'Manage Prerequisites'
        }
    });
});

});