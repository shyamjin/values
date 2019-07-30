/*
Author - nlate
Description -
    1. Shows the toolbar with create and discard button
    2. Controller that handles with the operations to create new tool and discard all changes
Methods -
    1. createNewTool() - Creates a new tool
    2. discardChanges() - Discards all changes and redirects user to tool dashboard
Uses -
    1. Create Tool - components/tools/edit-tools/toolbar/toolbar.component.html
*/

define(['angular', 'toolServicesApp'],function (app) {
  'use strict';

var proposeToolBarComponentControllerApp = angular.module('proposeToolBarComponentControllerApp', ['toolServicesApp']);

proposeToolBarComponentControllerApp.controller('ProposeToolBarController', function ($scope, $state, $rootScope, ProposeTool, $cookieStore) {
    $scope.proposeNewTool = function(form)
    {
        $rootScope.$emit('setProposedToolData', {});
        // Get tool general data and version data
        $scope.toolData = $rootScope.proposedToolDetailsFactory.getProposedToolData();

        var toolValidationResponse = $rootScope.toolDataValidatorFactory.validateToolData($scope.toolData);
        if(toolValidationResponse.result === "failed")
        {
            $rootScope.handleResponse(toolValidationResponse);
            return false;
        }

        var toolData = {};
        var versionData = {};

        toolData.name = $scope.toolData.name;
        toolData.support_details = $scope.toolData.support_details;
        toolData.description = $scope.toolData.description;
        toolData.request_reason = $scope.toolData.request_reason;
        versionData.version_name = $scope.toolData.version.version_name;
        versionData.version_number = $scope.toolData.version.version_number;
        toolData.version = versionData;

        ProposeTool.save(toolData, function(proposeToolSuccessReponse)
        {
            $rootScope.handleResponse(proposeToolSuccessReponse);
            if(sessionStorage.getItem('token'))
            {
                $state.go("dashboard");
            }
            else
            {
                $state.go("login")
            }
        },
        function(proposeToolErrorReponse)
        {
            $rootScope.handleResponse(proposeToolErrorReponse);
        });
    };

    $scope.discardProposedToolChanges = function()
    {
        $state.go("login");
    };

});

});