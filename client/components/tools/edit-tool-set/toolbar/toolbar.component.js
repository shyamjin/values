/*
Author - nlate
Description -
    1. Shows the toolbar with create and discard button
    2. Controller that handles with the operations to create new tool set and discard all changes
Methods -
    1. createNewToolSet() - Creates a new tool set
    2. discardChanges() - Discards all changes and redirects user to tool dashboard
Uses -
    1. Create Tool Set - components/tools/create-tool-set/toolbar/toolbar.component.html
*/

define(['angular'],function (app) {
  'use strict';

var editToolSetBarComponentControllerApp = angular.module('editToolSetBarComponentControllerApp', []);

editToolSetBarComponentControllerApp.controller('EditToolSetBarController', function ($scope, $state, $rootScope, ToolSetEdit, toolFileUpload) {
    $scope.editToolSet = function(form)
    {
        var jsonData = {
            _id : {
                oid : ''
            }
        };
        $rootScope.$emit('setToolSetData', {});
        $rootScope.$emit('setToolListData', {});
        $rootScope.$emit('setToolSetLogo', {});

        // Get tool set general data and tool list
        $scope.toolSetData = $rootScope.toolSetDetailsFactory.getToolSetData();
        $scope.toolListData = $rootScope.toolSetDetailsFactory.getToolList();

        // Validate tool general data and all version data
        var toolSetValidationResponse = $rootScope.toolSetDataValidatorFactory.validateToolSetData($scope.toolSetData);
        if(toolSetValidationResponse.result === "failed")
        {
            $rootScope.handleResponse(toolSetValidationResponse);
            return false;
        }

        var toolListValidationResponse = $rootScope.toolSetDataValidatorFactory.validateToolListData($scope.toolListData);
        if(toolListValidationResponse.result === "failed")
        {
            $rootScope.handleResponse(toolListValidationResponse);
            return false;
        }

        jsonData._id.oid = $scope.toolSetData.toolset_id;
        jsonData.name = $scope.toolSetData.name;
        jsonData.description = $scope.toolSetData.description;
        jsonData.tag = $scope.toolSetData.tag;
        jsonData.logo = $scope.toolSetData.logo;
        jsonData.tool_set = $scope.toolListData;

        ToolSetEdit.update(jsonData, function(toolSetUpdateSuccessResponse){
            $rootScope.handleResponse(toolSetUpdateSuccessResponse);
            $scope.logo = $rootScope.toolSetDetailsFactory.getToolSetLogo();
            var file = $scope.logo;
            if(file)
            {   file.toolset_id= $scope.toolSetData.toolset_id;
                var uploadUrl = "/toolset/upload/logo";
                toolFileUpload.uploadToolSetLogoFileToUrl(file, uploadUrl);
            }
            $state.go('viewAllToolSets');
        },
        function(toolSetUpdateErrorResponse)
        {
            $rootScope.handleResponse(toolSetUpdateErrorResponse);
        });
    };
});

});