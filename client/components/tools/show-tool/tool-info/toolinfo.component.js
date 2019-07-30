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

define(['angular', 'showToolPartialControllerApp','retainBuildDirectiveApp','toolServicesApp'],function (app) {
  'use strict';

var toolInfoComponentControllerApp = angular.module('toolInfoComponentControllerApp', ['showToolPartialControllerApp','retainBuildDirectiveApp','toolServicesApp']);

toolInfoComponentControllerApp.controller('ToolInfoController', function ($scope, $state, $rootScope,BuildMarkup) {
    $scope.toolData = $rootScope.toolDetailsFactory.getToolData();
    $scope.toolVersionData = $rootScope.toolDetailsFactory.getVersionList();
    $scope.toolVersionSelectedBuild=[];
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

    //    Retain Build markup popup screen
    $scope.showRetainBuild = function(toolId)
    {   $scope.selectedToolId =toolId;
        if(document.getElementById("retain_build_popup_screen").style.display === "none" || document.getElementById("retain_build_popup_screen").style.display === '')
        {
            document.getElementById("retain_build_popup_screen").style.display = "block";

             $scope.preLoader = true;
        }
        else
        {
           document.getElementById("retain_build_popup_screen").style.display = "none";
       }
    };
    $scope.closeRetainBuild = function()
    {
        document.getElementById("retain_build_popup_screen").style.display = "none";
    };

     $scope.addBuildAsMarkup = function(toolVersionSelectedBuild)
    {
        $scope.toolVersionSelectedBuild = toolVersionSelectedBuild
        $scope.parameter ={
            updateMarkupBuild: $scope.toolVersionSelectedBuild
        }
        BuildMarkup.save($scope.parameter, function(updateBuildMarkupSuccessResponse){

                $rootScope.handleResponse(updateBuildMarkupSuccessResponse);
                document.getElementById("retain_build_popup_screen").style.display = "none";
            },
            function(updateBuildMarkupErrorResponse)
            {
                $rootScope.handleResponse(updateBuildMarkupErrorResponse);
                return false;
            });
    };

});

});