/*
Author - nlate
Description -
    1. Controller that handles with the common operations required in create tool
Methods -
    1. showActiveTab(tab) - Sets the specified tab as an active tab
Uses -
    1. Create Tool - partials/tools/create-tools//create-tools.partial.html
*/

define(['angular', 'editToolInfoComponentControllerApp', 'editToolBarComponentControllerApp', 'editToolVerticalTabComponentControllerApp', 'editToolVersionComponentControllerApp'],function (app) {
  'use strict';

var editToolsPartialControllerApp = angular.module('editToolsPartialControllerApp', ['ui.router', 'editToolInfoComponentControllerApp', 'editToolBarComponentControllerApp', 'editToolVerticalTabComponentControllerApp', 'editToolVersionComponentControllerApp']);

editToolsPartialControllerApp.controller("EditToolPartialController",function($scope, $stateParams, GetAllTools, $window, $state, GetToolByID , $rootScope, GetAllDeploymentPlugins) {


    GetToolByID.get({
       id: $stateParams.id
    },
    function(toolViewSuccessResponse)
    {
        $scope.application = toolViewSuccessResponse;
        for(var id_app=0; id_app<$scope.application.data.all_versions.length; id_app++)
        {
            if($scope.application.data.all_versions[id_app].deployment_field)
            {
                if($scope.application.data.all_versions[id_app].deployment_field.fields && $scope.application.data.all_versions[id_app].deployment_field.fields.length>0)
                {
                    for(var df=0;df<$scope.application.data.all_versions[id_app].deployment_field.fields.length;df++)
                    {
                        if($scope.application.data.all_versions[id_app].deployment_field.fields[df].input_type==='date' && $scope.application.data.all_versions[id_app].deployment_field.fields[df].default_value)
                        {
                            var fieldDate =  $scope.application.data.all_versions[id_app].deployment_field.fields[df].default_value;
                            var dateFormat = new Date(fieldDate);
                            delete $scope.application.data.all_versions[id_app].deployment_field.fields[df].default_value;
                            $scope.application.data.all_versions[id_app].deployment_field.fields[df].default_value = dateFormat;
                        }
                        $scope.application.data.all_versions[id_app].deployment_field.fields[df].is_existing = true;
                    }
                }
            }
            if(!$scope.application.data.all_versions[id_app].deployer_to_use)
            {
                GetAllDeploymentPlugins.get({
                },
                function(successResponse)
                {
                    $scope.allDeploymentPlugins = successResponse.data;
                    $scope.application.data.all_versions[id_app].deployer_to_use = $scope.allDeploymentPlugins[0].plugin_name;
                },
                function(errorResponse)
                {
                    $rootScope.handleResponse(errorResponse);
                });
            }
        }

        if(toolViewSuccessResponse.data.status==='1')
        {
            $scope.application.data.status = "Active";
        }
        else if(toolViewSuccessResponse.data.status==='2')
        {
            $scope.application.data.status = "In Development";
        }
        else
        {
            $scope.application.data.status = "Deprecated";
        }

        if(toolViewSuccessResponse.data.artifacts_only === true || toolViewSuccessResponse.data.artifacts_only === 'true')
        {
            $scope.application.data.artifacts_only = "true";
        }
        else
        {
            $scope.application.data.artifacts_only = "false";
        }

        if(toolViewSuccessResponse.data.is_tool_cloneable === true || toolViewSuccessResponse.data.is_tool_cloneable === 'true')
        {
            $scope.application.data.is_tool_cloneable = "true";
        }
        else
        {
            $scope.application.data.is_tool_cloneable = "false";
        }

        for(var a=0; a<toolViewSuccessResponse.data.all_versions.length;a++)
        {
            if(toolViewSuccessResponse.data.all_versions[a].status==='1')
            {
                $scope.application.data.all_versions[a].status = "Active";
            }
            else
            {
                $scope.application.data.all_versions[a].status = "Deprecated";
            }

            var vDate = $scope.application.data.all_versions[a].version_date.$date;
            delete $scope.application.data.all_versions[a].version_date.$date;
            $scope.application.data.all_versions[a].version_date = new Date(vDate);

        }

        if(toolViewSuccessResponse.data.allow_build_download==='true')
        {
            $scope.application.data.allow_build_download = "Yes";
        }
        else
        {
            $scope.application.data.allow_build_download = "No";
        }

        $rootScope.toolDetailsFactory.setToolData(toolViewSuccessResponse.data);
        $rootScope.toolDetailsFactory.setVersionList(toolViewSuccessResponse.data.all_versions);
        $rootScope.toolDetailsFactory.setActiveVersionData(toolViewSuccessResponse.data.version);
    },
    function(toolViewErrorResponse)
    {
        $rootScope.handleResponse(toolViewErrorResponse);
    });
});

});