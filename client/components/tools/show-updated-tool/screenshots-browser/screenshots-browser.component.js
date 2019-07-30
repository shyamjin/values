/*
Author - nlate
Description -
    1. Shows screenshot of the selected index in popup
    2. Controller that handles with the navigation of screenshots in version if any
Methods -
    1. showPreviousOne() - Shows the previous screenshot image in popup
    2. showNextOne() - Shows the next screenshot image in popup
    3. closeScreenshotBrowser() - closes the current window and redirects the user to tool dashboard
Uses -
    1. Show Tool - components/tools/show-tool/header/header.component.html
*/

define(['angular', 'showUpdatedToolPartialControllerApp'],function (app) {
  'use strict';

var showUpdatedToolScreenshotBrowserComponentControllerApp = angular.module('showUpdatedToolScreenshotBrowserComponentControllerApp', ['showUpdatedToolPartialControllerApp']);

showUpdatedToolScreenshotBrowserComponentControllerApp.controller('ShowUpdatedToolScreenshotBrowserController', function ($scope, $state, $rootScope) {
    $scope.versionData = $rootScope.toolDetailsFactory.getVersionList();
    $scope.showNextOne = function()
    {
        if($rootScope.currentScreenshotURLIndex < $scope.versionData[$rootScope.displayTab].media_file.media_files.length)
        {
            $rootScope.currentScreenshotURLIndex = $scope.currentScreenshotURLIndex + 1;
            $rootScope.screenshotURL = $scope.versionData[$rootScope.displayTab].media_file.media_files[$rootScope.currentScreenshotURLIndex].url;
        }
        else
        {
            $rootScope.currentScreenshotURLIndex = 0;
            $rootScope.screenshotURL = $scope.versionData[$rootScope.displayTab].media_file.media_files[0].url;
        }
    };

    $scope.showPreviousOne = function()
    {
        if($rootScope.currentScreenshotURLIndex > 0)
        {
            $rootScope.currentScreenshotURLIndex = $scope.currentScreenshotURLIndex - 1;
            $rootScope.screenshotURL = $scope.versionData[$rootScope.displayTab].media_file.media_files[$rootScope.currentScreenshotURLIndex].url;
        }
        else
        {
            $rootScope.currentScreenshotURLIndex = $scope.versionData[$rootScope.displayTab].media_file.media_files.length - 1;
            $rootScope.screenshotURL = $scope.versionData[$rootScope.displayTab].media_file.media_files[$rootScope.currentScreenshotURLIndex].url;
        }
    };

    $scope.closeScreenshotBrowser = function()
    {
        $('#view_screenshot').hide(700);
    };
});

});