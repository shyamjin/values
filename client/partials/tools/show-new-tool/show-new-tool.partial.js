/*
Author - nlate
Description -
    1. Fetches the details of the tool selected
    2. Controller that handles with the seperations of data per controller present in the show tool components
Methods -
    1.
Uses -
    1. Show Tool - partials/tools/show-tool/show-tool.partial.html
*/

define(['angular', 'settingsServicesApp', 'showNewToolHeaderComponentControllerApp', 'showNewToolInfoComponentControllerApp', 'showNewToolVerticalTabComponentControllerApp', 'showNewToolVersionComponentControllerApp', 'showNewToolScreenshotBrowserComponentControllerApp'],function (app) {
  'use strict';

var showNewToolPartialControllerApp = angular.module('showNewToolPartialControllerApp', ['showNewToolHeaderComponentControllerApp', 'showNewToolInfoComponentControllerApp', 'showNewToolVerticalTabComponentControllerApp', 'showNewToolVersionComponentControllerApp', 'showNewToolScreenshotBrowserComponentControllerApp']);

showNewToolPartialControllerApp.controller('ShowNewToolPartialController', function ($scope, $stateParams, $rootScope, GetToolByID) {
    NewToolByID.get({
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