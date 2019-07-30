require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['requestTabComponent', 'proposedToolServicesApp']
});

define(['angular'],function (app) {
  'use strict';

var proposedToolsComponentControllerApp = angular.module('proposedToolsComponentControllerApp', ['requestTabComponent', 'proposedToolServicesApp']);

proposedToolsComponentControllerApp.controller('ProposedToolListController', function ($scope, $state, $rootScope, GetAllProposedTools, ApproveProposedTool) {
    $rootScope.$on("searchToolEvent", function (event, args) {
        var keyword = args.keyword;
        $scope.searchToolWithName(keyword);
    });

    $scope.getReleaseNotesLineCount = function()
    {
        var paraHeight = document.getElementById('release_notes_content').offsetHeight;
        var lineHeight = parseInt(document.getElementById('release_notes_content').style.lineHeight, 10);
        $scope.lines = (divHeight / lineHeight);
        return '';
    };

    GetAllProposedTools.get({
    },
    function(successResponse)
    {
        $scope.applications = successResponse.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $rootScope.approveTool = function(tool_data)
    {
        var jsonData = {
            _id : ''
        }
        jsonData._id = tool_data._id;
        jsonData.name = tool_data.name;
        jsonData.description = tool_data.description;
        jsonData.support_details = tool_data.support_details;
        jsonData.version = tool_data.version;
        ApproveProposedTool.save(jsonData, function(approveProposedToolSuccessResponse){
            $rootScope.handleResponse(approveProposedToolSuccessResponse);
            delete $scope.applications;
            GetAllProposedTools.get({
            },
            function(successResponse)
            {
                $scope.applications = successResponse.data;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(approveProposedToolErrorResponse){
            $rootScope.handleResponse(approveProposedToolErrorResponse);
        });
    };

});

});