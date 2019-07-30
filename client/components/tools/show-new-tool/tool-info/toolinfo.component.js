/*
Author - nlate
Description -
    1. Shows the tool general details
    2. Controller that handles with the routing for edit tool operation
Methods -
    1. showLessToolReleaseNotesContent() - show less content function for description
    2. showMoreToolReleaseNotesContent - show more content function for description
Uses -
    1. Show New Tool - components/tools/show-new-tool/tool-info/toolinfo.component.html
*/

define(['angular', 'showNewToolPartialControllerApp'],function (app) {
  'use strict';

var showNewToolInfoComponentControllerApp = angular.module('showNewToolInfoComponentControllerApp', ['showNewToolPartialControllerApp']);

showNewToolInfoComponentControllerApp.controller('ShowNewToolInfoController', function ($scope, $state, $rootScope) {
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
});

});