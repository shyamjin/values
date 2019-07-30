/*
Author - nlate
Description -
    1. Controller that handles with the togling between version tabs of the tool
Methods -
    1. showVersionDetailsTab(index) - Sets a version index as active selected version and resets the defalt build details
    2. getActiveTab(index) - Returns the Active tab CSS class
    3. deployTool(version_id, build_id) - function to redirect to deploy tool page
Uses -
    1. Show New Tool - components/tools/show-new-tool/tabs/verticaltabs.component.js
*/

define(['angular', 'showNewToolPartialControllerApp'],function (app) {
  'use strict';

var showNewToolVerticalTabComponentControllerApp = angular.module('showNewToolVerticalTabComponentControllerApp', ['showNewToolPartialControllerApp']);

showNewToolVerticalTabComponentControllerApp.controller('ShowNewToolVerticalTabController', function ($scope, $state, $rootScope) {
    $rootScope.displayTab = 0;
    $rootScope.build = {
        selected : ''
    };

    $scope.deployTool = function(version_id, build_number)
    {
        if(build_number === '' || build_number === null || build_number === undefined)
        {
            $rootScope.handleResponse("Unable to deploy as selected version of this tool either does not have a valid build or you have not selected the build");
            return false;
        }
        else
        {
            $state.go('deployTool', {id:version_id, build_number: build_number});
        }
    };

    $scope.getActiveTab = function(index)
    {
        if($rootScope.displayTab === index)
        {
             return "vp-tabsvertical__tab--active";
        }
    };

    $scope.showVersionDetailsTab = function(version_index)
    {
        $rootScope.displayTab = version_index;
        if($scope.versionData[version_index].build)
        {
            $rootScope.buildDetails = $scope.versionData[version_index].build[0];
            $rootScope.buildToDeploy = $scope.versionData[version_index].build[0];
            $rootScope.buildFilePath = $scope.versionData[version_index].build[0].file_path;
        }
        else
        {
            delete $rootScope.buildDetails;
            delete $rootScope.buildFilePath;
            delete $rootScope.buildToDeploy;
        }
        $scope.startPoint = 0;
    };

    $scope.versionData = $rootScope.toolDetailsFactory.getVersionList();
    $scope.activeVersionData = $rootScope.toolDetailsFactory.getActiveVersionData();

});

});