/*
Author - nlate
Description -
    1. Fetches the details of the tool selected
    2. Controller that handles with the seperations of data per controller present in the show tool components
Methods -
    1.
Uses -
    1. Show Updated Tool - partials/tools/show-updated-tool/show-updated-tool.partial.html
*/

define(['angular', 'settingsServicesApp', 'showUpdatedToolScreenshotBrowserComponentControllerApp', 'showUpdatedToolHeaderComponentControllerApp', 'showUpdatedToolInfoComponentControllerApp', 'showUpdatedToolVerticalTabComponentControllerApp', 'showUpdatedToolVersionComponentControllerApp'],function (app) {
  'use strict';

var showUpdatedToolPartialControllerApp = angular.module('showUpdatedToolPartialControllerApp', ['settingsServicesApp',
    'showUpdatedToolScreenshotBrowserComponentControllerApp',
    'showUpdatedToolHeaderComponentControllerApp',
    'showUpdatedToolInfoComponentControllerApp',
    'showUpdatedToolVerticalTabComponentControllerApp',
    'showUpdatedToolVersionComponentControllerApp'
]);

showUpdatedToolPartialControllerApp.controller('ShowUpdatedToolPartialController', function ($scope, $stateParams, $rootScope, GetDistributedTool) {
    GetDistributedTool.get({
       id: $stateParams.id
    },
    function(toolViewSuccessResponse)
    {
        $scope.application = toolViewSuccessResponse;
        $rootScope.toolDetailsFactory.setVersionList(toolViewSuccessResponse.data.all_versions);
        $rootScope.toolDetailsFactory.setToolData(toolViewSuccessResponse.data);
        $rootScope.toolDetailsFactory.setActiveVersionData(toolViewSuccessResponse.data.version);
    },
    function(toolViewErrorResponse)
    {
        $rootScope.handleResponse(toolViewErrorResponse);
    });

 });

});