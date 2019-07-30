/*
Author - nlate
Description -
    1. Shows the tool general details
    2. Controller that handles with the routing for edit tool operation
Methods -
    1. showLessToolReleaseNotesContent() - show less content function for description
    2. showMoreToolReleaseNotesContent - show more content function for description
Uses -
    1. Show Tool - components/tools/show-tool/tool-info/toolinfo.component.html
*/

define(['angular', 'showProposedToolPartialControllerApp'],function (app) {
  'use strict';

var showProposedToolInfoComponentControllerApp = angular.module('showProposedToolInfoComponentControllerApp', ['showProposedToolPartialControllerApp']);

showProposedToolInfoComponentControllerApp.controller('ShowProposedToolInfoController', function ($scope, $state, $rootScope, ApproveProposedTool, RejectProposedTool) {
    $rootScope.toolData = $rootScope.proposedToolDetailsFactory.getProposedToolData();
    $scope.showLessBuildReleaseNotes = false;
    $scope.showAllToolReleaseNotes = true;
    $scope.showAllToolRequestReason = true;

    $scope.showMoreToolReleaseNotesContent = function()
    {
        $scope.showAllToolReleaseNotes = false;
        $scope.showLessToolReleaseNotes = true;
        $('#release_notes_tool').removeClass('text--ellipsis');
    };

    $scope.showLessToolReleaseNotesContent = function()
    {
        $scope.showAllToolReleaseNotes = true;
        $scope.showLessToolReleaseNotes = false;
        $('#release_notes_tool').addClass('text--ellipsis');
    };

    $scope.showMoreToolRequestReasonContent = function()
    {
        $scope.showAllToolRequestReason = false;
        $scope.showLessToolRequestReason = true;
        $('#request_reason_tool').removeClass('text--ellipsis');
    };

    $scope.showLessToolRequestReasonContent = function()
    {
        $scope.showAllToolRequestReason = true;
        $scope.showLessToolRequestReason = false;
        $('#request_reason_tool').addClass('text--ellipsis');
    };

    $rootScope.approveTool = function(tool_data)
    {
        var jsonData = {
            _id : ''
        }
        jsonData._id = tool_data.tool_id;
        jsonData.name = tool_data.name;
        jsonData.description = tool_data.description;
        jsonData.support_details = tool_data.support_details;
        jsonData.version = tool_data.version;
        ApproveProposedTool.save(jsonData, function(approveProposedToolSuccessResponse){
            $state.go('viewProposedTools');
            $rootScope.handleResponse(approveProposedToolSuccessResponse);
        },
        function(approveProposedToolErrorResponse){
            $rootScope.handleResponse(approveProposedToolErrorResponse);
        });
    };

    $rootScope.rejectTool = function(tool_id)
    {
        RejectProposedTool.remove({
            id: tool_id
        },
        function(approveProposedToolSuccessResponse){
            $state.go('viewProposedTools');
            $rootScope.handleResponse(approveProposedToolSuccessResponse);
        },
        function(approveProposedToolErrorResponse){
            $rootScope.handleResponse(approveProposedToolErrorResponse);
        });
    };
});

});