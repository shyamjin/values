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

define(['angular'],function (app) {
  'use strict';

var createToolBarComponentControllerApp = angular.module('createToolBarComponentControllerApp', []);

createToolBarComponentControllerApp.controller('CreateToolBarController', function ($scope, $state, $rootScope, TagsAll, CreateTool, toolFileUpload) {
    $scope.createNewTool = function(form)
    {
        $rootScope.$emit('setToolData', {});
        $rootScope.$emit('setVersionData', {});
        $rootScope.$emit('setToolLogo', {});
        $rootScope.$emit('setMediaFiles', {});
        // Get tool general data and version data
        $scope.toolData = $rootScope.toolDetailsFactory.getToolData();
        $scope.versionData = $rootScope.toolDetailsFactory.getVersionList();

        // Validate tool general data and all version data
        var toolValidationResponse = $rootScope.toolDataValidatorFactory.validateToolData($scope.toolData);
        if(toolValidationResponse.result === "failed")
        {
            $rootScope.handleResponse(toolValidationResponse);
            return false;
        }

        var versionValidationResponse = $rootScope.toolDataValidatorFactory.validateVersionData($scope.versionData);
        if(versionValidationResponse.result === "failed")
        {
            $rootScope.version_errors = versionValidationResponse.version_errors;
            $rootScope.displayTab = versionValidationResponse.display_tab;
            return false;
        }

        var toolData = {};
        var versionData = {};
        var version_date = '';
        var vdate = '';
        var vdateISO = '';
        var full_version_date = '';
        toolData.name = $scope.toolData.name;
        toolData.tag = $scope.toolData.tag;
        toolData.support_details = $scope.toolData.support_details;
        toolData.logo = $scope.toolData.logo;
        toolData.description = $scope.toolData.description;

//        toolData.is_tool_cloneable = $scope.application.data.is_tool_cloneable;
//        toolData.artifacts_only = $scope.application.data.artifacts_only;

        versionData.version_name = $scope.versionData[0].version_name;
        if($scope.versionData[0].version_date)
        {
            version_date =  $scope.versionData[0].version_date;
            vdate = new Date(version_date);
            vdateISO = vdate.toISOString();
            full_version_date = vdateISO.replace('T',' ');
            full_version_date = full_version_date.replace('Z',' ');
        }
        else
        {
            version_date =  $scope.version_date;
            vdate = new Date(version_date);
            vdateISO = vdate.toISOString();
            full_version_date = vdateISO.replace('T',' ');
            full_version_date = full_version_date.replace('Z',' ');
        }
        versionData.version_date = full_version_date;
        versionData.version_number = $scope.versionData[0].version_number;
        versionData.pre_requiests = $scope.versionData[0].pre_requiests;
        versionData.branch_tag = $scope.versionData[0].branch_tag;
        versionData.gitlab_repo = $scope.versionData[0].gitlab_repo;
        versionData.gitlab_branch = $scope.versionData[0].gitlab_branch;
        versionData.jenkins_job = $scope.versionData[0].jenkins_job;
        versionData.document = $scope.versionData[0].document;
        versionData.backward_compatible = $scope.versionData[0].backward_compatible;
        versionData.release_notes = $scope.versionData[0].release_notes;
        versionData.mps_certified = $scope.versionData[0].mps_certified;
        versionData.deployment_field = $scope.versionData[0].deployment_field;
        versionData.deployer_to_use = $scope.versionData[0].deployer_to_use;
        versionData.repository_to_use = $scope.versionData[0].repository_to_use;

        var version_length = versionData.length;

        if($scope.versionData[0].dependent_tools)
        {
            for(var dt=0; dt<$scope.versionData[0].dependent_tools.length; dt++)
            {
                if(!$scope.versionData[0].dependent_tools[dt].is_mandatory)
                {
                    $scope.versionData[0].dependent_tools[dt].is_mandatory = false;
                }
            }
            versionData.dependent_tools = $scope.versionData[0].dependent_tools;
        }

        toolData.version = versionData;

        $scope.toolStatus = CreateTool.save(toolData, function(toolAddResponse)
        {
            $scope.logo = $rootScope.toolDetailsFactory.getToolLogo();
            var file = $scope.logo;
            if(file)
            {
                file.tool_id= toolAddResponse.data.tool_id;
                var uploadUrl = "/tool/upload/logo";
                toolFileUpload.uploadFileToUrl(file, uploadUrl);
            }

            var screenshot = [];
            for(var l=0;l<$rootScope.screenshotFiles.length;l++)
            {
                screenshot = $rootScope.screenshotFiles[l];
                if(screenshot)
                {
                      screenshot.version_id= toolAddResponse.data.version_id;
                      var uploadScreenshotUrl = "/tool/versions/uploadScreenshot";
                      toolFileUpload.uploadScreenShotToUrl(screenshot, uploadScreenshotUrl);
                }
            }

            $state.go('viewApplication',{"id":toolAddResponse.data._id});
            $rootScope.handleResponse(toolAddResponse);
        },
        function(toolAddErrorResponse)
        {
            $rootScope.handleResponse(toolAddErrorResponse);
        });
   };
});

});