/*
Author - nlate
Description -
    1. Shows Logo and name of the tool selected
    2. Controller that handles with the operations allowed in the header of show tool component
Methods -
    1. addToolToFavourites(id) - adds tool to favourite tool list - dep
    2. closeThis() - closes the current window and redirects the user to tool dashboard
Uses -
    1. Show Proposed Tool - components/tools/show-proposed-tool/header/header.component.html
*/

define(['angular'],function (app) {
  'use strict';

var proposeToolHeaderComponentControllerApp = angular.module('proposeToolHeaderComponentControllerApp', []);

proposeToolHeaderComponentControllerApp.controller('ProposeToolHeaderController', function ($scope, $rootScope, $state, $cookieStore) {

    $scope.closeThis = function()
    {
        // code for close this window
        if(sessionStorage.getItem('token'))
        {
            $state.go("dashboard");
        }
        else
        {
            $state.go("login");
        }
    };
});

});