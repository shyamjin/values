/*
Author - nlate
Description -
    1. Controller that handles with the tabs in manage deployment plugins
Methods -
    1. showActiveTab(tab) - Sets the CSS class to active tab
    2. getActiveTab(tab) - Gets the Active tab url and sets to the variable
Uses -
    1. Manage Deployment Plugins - components/deployment-plugins/tabs/tabs.component.html
*/

require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageDeploymentPluginContentComponentApp', 'uploadDeploymentPluginContentComponentApp']
});

define(['angular', 'uiRouter', 'manageDeploymentPluginContentComponentApp', 'uploadDeploymentPluginContentComponentApp'],function (app) {
  'use strict';

var manageDeploymentPluginsTabComponentApp = angular.module('manageDeploymentPluginsTabComponentApp', ['ui.router', 'manageDeploymentPluginContentComponentApp', 'uploadDeploymentPluginContentComponentApp']);

manageDeploymentPluginsTabComponentApp.controller("ManageDeploymentPluginsTabController",function($scope, $http, $state, $stateParams, $location, $rootScope){
    $scope.activeTab = "/manage/plugins/deployment";
    $scope.showActiveTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
        delete $rootScope.pluginData;
        delete $rootScope.pluginOperation;
        $rootScope.resultPane = false;
        delete $rootScope.response;
        if(tab === '/plugin/deployment/upload')
        {
            $rootScope.pluginOperation = 'new';
        }
        else
        {
            $rootScope.pluginOperation = 'update';
        }
    };

    $scope.getActiveTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
        if($scope.displayTab===tab)
        {
            return 'vp-tabs__tab--active';
        }
        else
        {
            return '';
        }
    };
});

});