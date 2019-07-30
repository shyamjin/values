/*
Author - nlate
Description -
    1. Shows Logo and name of the tool selected
    2. Controller that handles with the operations allowed in the header of show tool component
Methods -
    1. addToolToFavourites(id) - adds tool to favourite tool list - dep
    2. closeThis() - closes the current window and redirects the user to tool dashboard
Uses -
    1. Show Updated Tool - components/tools/show-updated-tool/header/header.component.html
*/

define(['angular', 'showUpdatedToolPartialControllerApp'],function (app) {
  'use strict';

var showUpdatedToolHeaderComponentControllerApp = angular.module('showUpdatedToolHeaderComponentControllerApp', ['showUpdatedToolPartialControllerApp']);

showUpdatedToolHeaderComponentControllerApp.controller('ShowUpdatedToolHeaderController', function ($scope, $rootScope, $state) {
    $scope.toolData = $rootScope.toolDetailsFactory.getToolData();
    $scope.addToolToFavourites = function(tool_id)
    {
        // code for add this tool to favourite tool
    };

    $scope.closeThis = function()
    {
        // code for close this window
        $state.go("dashboard");
    };
});

});