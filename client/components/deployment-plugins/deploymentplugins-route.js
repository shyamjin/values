require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageDeploymentPluginsControllerApp', 'manageDeploymentPluginsTabComponentApp']
});

define(['angular', 'ngResource', 'uiRouter', 'manageDeploymentPluginsControllerApp', 'manageDeploymentPluginsTabComponentApp'],function (app) {
  'use strict';

var deploymentPluginRoutesApp = angular.module('deploymentPluginRoutesApp', ['ui.router','manageDeploymentPluginsControllerApp', 'manageDeploymentPluginsTabComponentApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('manageDeploymentPlugin', {
        url: '/manage/plugins/deployment',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-plugins/manage-deployment-plugins.partial.html',
                controller: 'ManageDeploymentPluginsController'
            }
        },
        data: {
            pageTitle: 'Manage Deployment Plugins'
        }
    }).state('uploadDeploymentPlugin', {
        url: '/plugin/deployment/upload',
        views: {
            "main": {
                templateUrl: 'static/components/deployment-plugins/manage-deployment-plugins.partial.html',
                controller: 'UploadDeploymentPluginsContentController'
            }
        },
        data: {
            pageTitle: 'Manage Deployment Plugins'
        }
    });
});

});