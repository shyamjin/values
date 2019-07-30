/*
Author - nlate
Description -
    1. Controller that handles with the operations allowed in the tool set info component of show tool set
Methods -
    1. editToolSet(id) - Redirects the user to edit tool set page
    2. deployToolSet(id) - Validates the associated builds in the tools included in tool sets and redirects to deploy tool page if data is valid
Uses -
    1. Show Tool Set - components/tools/show-tool-set/tool-set-info/toolsetinfo.component.html
*/

define(['angular', 'showToolSetPartialControllerApp','toolTips'],function (app) {
  'use strict';

var showToolSetInfoComponentControllerApp = angular.module('showToolSetInfoComponentControllerApp', ['showToolSetPartialControllerApp', 'deploymentRoutesApp','720kb.tooltips']);

showToolSetInfoComponentControllerApp.controller('ShowToolSetInfoController', function ($scope, $rootScope, $state, ToolSetByID) {
    $scope.generalToolSetData = $rootScope.toolSetDetailsFactory.getToolSetData();
    $rootScope.$on('updateToolList', function(event, args){
        $scope.toolList = args.selectedTools;
    });
    $scope.toolList = $rootScope.toolSetDetailsFactory.getToolList();
    $scope.toolsSelectedToDeploy = [];
    $scope.addToolToFavourites = function(tool_id)
    {
        // code for add this tool to favourite tool - deprecated
    };

    $scope.closeThis = function()
    {
        // code for close this window
        $state.go("viewAllToolSets");
    };

    $scope.selectToolSet = function(toolset_id)
    {
        ToolSetByID.get({
            id : toolset_id
        },
        function(toolsetSuccessResponse)
        {
            for(var t1=0; t1<toolsetSuccessResponse.data.tool_set.length; t1++)
            {
                if(toolsetSuccessResponse.data.tool_set[t1].build_number === undefined || toolsetSuccessResponse.data.tool_set[t1].build_number === null || toolsetSuccessResponse.data.tool_set[t1].build_number === '')
                {
                    $rootScope.handleResponse("Unable to deploy as latest version of the tool "+toolsetSuccessResponse.data.tool_set[t1].tool_name+" does not have a valid build");
                    return false;
                }
                else
                {
                    $scope.toolsSelectedToDeploy.push({"version_id": toolsetSuccessResponse.data.tool_set[t1].version_id, "build_number": toolsetSuccessResponse.data.tool_set[t1].build_number, "build_id": toolsetSuccessResponse.data.tool_set[t1].build_id});
                }
            }
            if($scope.toolsSelectedToDeploy.length>0)
            {
                $state.go('deployMultipleTools', {tools: JSON.stringify($scope.toolsSelectedToDeploy)});
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };
});

});