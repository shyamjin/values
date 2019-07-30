/*
Author - nlate
Description -
    1. Shows Logo and name of the tool set selected
    2. Controller that handles with the operations allowed in the header of show tool set component
Methods -
    1. addToolToFavourites(id) - adds tool to favourite tool list - dep
    2. closeThis() - closes the current window and redirects the user to tool dashboard
Uses -
    1. Show Tool Set - components/tools/show-tool-set/header/header.component.html
*/

define(['angular', 'showToolSetPartialControllerApp'],function (app) {
  'use strict';

var showToolSetHeaderComponentControllerApp = angular.module('showToolSetHeaderComponentControllerApp', ['showToolSetPartialControllerApp']);

showToolSetHeaderComponentControllerApp.controller('ShowToolSetHeaderController', function ($scope, $rootScope, $state) {
    $scope.generalToolSetData = $rootScope.toolSetDetailsFactory.getToolSetData();
    $scope.addToolToFavourites = function(tool_id)
    {
        // code for add this tool to favourite tool - deprecated
    };

    $scope.closeThis = function()
    {
        // code for close this window
        $state.go("viewAllToolSets");
    };
});

});