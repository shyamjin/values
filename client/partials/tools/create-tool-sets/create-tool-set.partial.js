/*
Author - nlate
Description -
    1. Controller that handles with the common operations required in create tool set
Methods -
    1.
Uses -
    1. Create Tool Set - partials/tools/create-tool-sets/create-tool-sets.partial.html
*/

define(['angular', 'toolSetServicesApp', 'createToolSetInfoComponentControllerApp', 'createToolSetBarComponentControllerApp', 'createToolSetAddToolComponentControllerApp', 'createToolSetToolSearchComponentControllerApp'],function (app) {
  'use strict';

var createToolSetPartialControllerApp = angular.module('createToolSetPartialControllerApp', ['toolSetServicesApp', 'createToolSetInfoComponentControllerApp', 'createToolSetBarComponentControllerApp', 'createToolSetAddToolComponentControllerApp', 'createToolSetToolSearchComponentControllerApp']);

createToolSetPartialControllerApp.controller("CreateToolSetPartialController",function($scope, $stateParams) {

});

});