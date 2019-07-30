/*
Author - nlate
Description -
    1. Controller that handles with the details of each version in tool
Methods -
    1. 
Uses -
    1. Propose Tool - components/tools/propose-tools/version-form/versionsform.component.html
*/

define(['angular'],function (app) {
  'use strict';

var proposeToolVersionComponentControllerApp = angular.module('proposeToolVersionComponentControllerApp', []);

proposeToolVersionComponentControllerApp.controller('ProposeToolVersionController', function ($scope, $state, $rootScope) {    
    $rootScope.displayTab = 0;
    $rootScope.vIndex  = 0;
    $rootScope.version_errors = {        
        version_number : '',
        version_name : ''        
    };

});

});