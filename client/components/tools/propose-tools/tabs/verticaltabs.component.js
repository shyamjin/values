/*
Author - nlate
Description -
    1. Controller that handles with the toggling between version tabs of the tool
Methods -
    1. showVersionDetailsTab(index) - Sets a version index as active selected version and resets the defalt build details
    2. getActiveTab(index) - Returns the Active tab CSS class
    3. deployTool(version_id, build_id) - function to redirect to deploy tool page
Uses -
    1. Show Tool - components/tools/show-tool/tabs/verticaltabs.component.js
*/

define(['angular'],function (app) {
  'use strict';

var proposeToolVerticalTabComponentControllerApp = angular.module('proposeToolVerticalTabComponentControllerApp', []);

proposeToolVerticalTabComponentControllerApp.controller('ProposeToolVerticalTabController', function ($scope, $state, $rootScope) {
    $rootScope.displayTab = 0;
    $rootScope.versionData = [{
        version_number : null,
        version_name : ''        
    }];

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
    };

});

});