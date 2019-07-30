/*
Author - nlate
Description -
    1. Fetches the details of the tool selected
    2. Controller that handles with the seperations of data per controller present in the show tool components
Methods -
    1.
Uses -
    1. Show Proposed Tool - partials/tools/show-proposed-tool/show-proposed-tool.partial.html
*/

define(['angular', 'proposedToolServicesApp', 'showProposedToolHeaderComponentControllerApp', 'showProposedToolInfoComponentControllerApp'],function (app) {
  'use strict';

var showProposedToolPartialControllerApp = angular.module('showProposedToolPartialControllerApp', ['proposedToolServicesApp', 'showProposedToolHeaderComponentControllerApp', 'showProposedToolInfoComponentControllerApp']);

showProposedToolPartialControllerApp.controller('ShowProposedToolPartialController', function ($scope, $stateParams, $rootScope, GetProposedTool) {
    GetProposedTool.get({
       id: $stateParams.id
    },
    function(toolViewSuccessResponse)
    {
        $scope.application = toolViewSuccessResponse;
        $rootScope.proposedToolDetailsFactory.setProposedToolData(toolViewSuccessResponse.data);
    },
    function(toolViewErrorResponse)
    {
        $rootScope.handleResponse(toolViewErrorResponse);
    });

 });

});