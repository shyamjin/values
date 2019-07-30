/*
Author - nlate
Description -
    1. Controller that handles with the upload operation of deployment plugin
Methods -
    1. uploadDeploymentPlugin(pluginFile) - Uploads a new deployment plugin
Uses -
    1. Manage Deployment Plugins - components/deployment-plugins/upload-deployment-plugin-content/uploaddeploymentplugincontent.component.html
*/

require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['uploadDeploymentPluginFormComponentApp']
});

define(['angular', 'uiRouter', 'uploadDeploymentPluginFormComponentApp'],function (app) {
  'use strict';

var uploadDeploymentPluginContentComponentApp = angular.module('uploadDeploymentPluginContentComponentApp', ['ui.router', 'uploadDeploymentPluginFormComponentApp']);

uploadDeploymentPluginContentComponentApp.controller("UploadDeploymentPluginsContentController",function($scope, $http, $state, $stateParams){
    $scope.validateDeploymentPluginFile = function(pluginFile)
    {
        // validate deployment plugin code goes
    };
});

});