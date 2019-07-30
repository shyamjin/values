/*
Author - nlate
Description -
    1. Controller that handles with the operations of Update and discard the selected plugin
Methods -
    1. editPlugin(form) - Fetches deployment requests by request id - dep
    2. discardPluginChanges() - re-submits the deployment request that was failed - dep
Uses -
    1. Manage Deployment Plugins - components/deployment-plugins/manage-deployment-plugins-content/managedeploymentpluginscontent.component.html
*/

require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['pluginListSearchComponentApp']
});

define(['angular', 'pluginListSearchComponentApp'],function (app) {
  'use strict';

var manageDeploymentPluginContentComponentApp = angular.module('manageDeploymentPluginContentComponentApp', ['pluginListSearchComponentApp']);

manageDeploymentPluginContentComponentApp.controller("ManageDeploymentPluginContentController",function($scope,$rootScope, $http, $state, $stateParams){
    $rootScope.showResultPane = false;
    $scope.editPlugin = function(editPluginForm)
    {
        // code for edit plugin goes here
    };

    $scope.discardPluginChanges = function()
    {
        // code for discard plugin changes goes here
    };
});

});