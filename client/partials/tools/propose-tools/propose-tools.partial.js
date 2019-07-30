/*
Author - nlate
Description -
    1. Controller that handles with the common operations required in create tool
Methods -
    
Uses -
    1. Propose Tool - partials/tools/propose-tools/propose-tools.partial.html
*/

define(['angular', 'proposeToolHeaderComponentControllerApp', 'proposeToolInfoComponentControllerApp', 'proposeToolBarComponentControllerApp'],function (app) {
  'use strict';

var proposeToolsPartialControllerApp = angular.module('proposeToolsPartialControllerApp', ['proposeToolHeaderComponentControllerApp', 'proposeToolInfoComponentControllerApp', 'proposeToolBarComponentControllerApp']);

proposeToolsPartialControllerApp.controller("ProposeToolPartialController",function($scope, $cookieStore, $rootScope) {
    $scope.isUserLoggedIn = function()
    {
        if(sessionStorage.getItem('token'))
        {
            return true;
        }
        else
        {
            return false;
        }
    };
});

});