/*
Author - nlate
Description -
    1. Shows the tool general details
    2. Controller that handles with the routing for edit tool operation
Methods -
    1. showLessToolReleaseNotesContent() - show less content function for description
    2. showMoreToolReleaseNotesContent - show more content function for description
Uses -
    1. Show Updated Tool - components/tools/show-updated-tool/tool-info/toolinfo.component.html
*/

define(['angular', 'showUpdatedToolPartialControllerApp'],function (app) {
  'use strict';

var showUpdatedToolInfoComponentControllerApp = angular.module('showUpdatedToolInfoComponentControllerApp', ['showUpdatedToolPartialControllerApp', 'settingsServicesApp']);

showUpdatedToolInfoComponentControllerApp.controller('ShowUpdatedToolInfoController', function ($scope, $state, $rootScope, ImportUpdate) {
    $scope.toolData = $rootScope.toolDetailsFactory.getToolData();
    $scope.showLessBuildReleaseNotes = false;
    $scope.showAllToolReleaseNotes = true;

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

    $scope.updateTool = function(id)
    {
        var jsonData = {};
        jsonData.ids = [];
        jsonData.ids.push(id);
        jsonData.type = 'updatetool';

        $scope.importToolStatus = ImportUpdate.save(jsonData, function(importSuccessResponse){
            $scope.responseMessage = importSuccessResponse;
            $scope.requestID = jsonData._id.oid;
            $state.go('toolImportUpdateStatus', {'request_id' : jsonData._id.oid});
            $rootScope.handleResponse(importSuccessResponse);
        },
        function(importErrorResponse)
        {
            $rootScope.handleResponse(importErrorResponse);
        });
    };
});

});