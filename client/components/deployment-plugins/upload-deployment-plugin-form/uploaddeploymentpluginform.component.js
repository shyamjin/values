/*
Author - nlate
Description -
    1. Controller that handles with the file and validations of uploaded for the operation of deployment plugin upload
Methods -
    1. $rootScope.$on('UploadDeploymentPlugin') - event to get the uploaded plugin file in the controller of UploadDeploymentPluginsContentController to be used by uploadPlugin(pluginFile)
Uses -
    1. Manage Deployment Plugins - components/deployment-plugins/upload-deployment-plugin-content/uploaddeploymentplugincontent.component.html
*/

require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['deploymentPluginDirectiveApp']
});

define(['angular', 'deploymentPluginDirectiveApp'],function (app) {
  'use strict';

var uploadDeploymentPluginFormComponentApp = angular.module('uploadDeploymentPluginFormComponentApp', ['deploymentPluginDirectiveApp']);

uploadDeploymentPluginFormComponentApp.controller("UploadDeploymentPluginsFormController",function($scope, $state, ExitPoint, UploadDeploymentPlugin, $rootScope, $http, GetPluginData, ExitPointUpdate){
    $rootScope.$on("newPluginData", function (event, args) {
        $scope.pluginFileSelected = '';
        $rootScope.pluginFileToUpload = null;
    });
    $rootScope.preLoader = false;
    if(!$rootScope.pluginData)
    {
        $rootScope.pluginOperation = 'new';
        $rootScope.pluginData = {
            type : 'repository',
            additional_parameters : []
        };
    }

    $scope.additional_parameters = [];

    $scope.addParameter = function()
    {
        if($rootScope.pluginData.additional_parameters)
        {
            $rootScope.pluginData.additional_parameters.push({"key" : "", "value" : ""});
        }
        else
        {
            $rootScope.pluginData.additional_parameters = [];
            $rootScope.pluginData.additional_parameters.push({"key" : "", "value" : ""});
        }

    };

    $scope.removeParameter = function(index)
    {
        $rootScope.pluginData.additional_parameters.splice(index, 1);
    };

    $scope.uploadDeploymentPlugin = function(file)
    {
        // prepare plugin data
        var jsonData = {};
        if($rootScope.pluginData.repo_provider)
        {
            jsonData.repo_provider = $rootScope.pluginData.repo_provider;
        }

        if($rootScope.pluginData.type === 'Sync' && ($rootScope.pluginData.repo_provider === '' || $rootScope.pluginData.repo_provider === null || $rootScope.pluginData.repo_provider === undefined))
        {
            $rootScope.handleResponse("Please enter repo provider");
            return false;
        }

        if($rootScope.pluginData.additional_parameters)
        {
            for(var i=0; i<$rootScope.pluginData.additional_parameters.length; i++)
            {
                if(($rootScope.pluginData.additional_parameters[i].key !== "" || $rootScope.pluginData.additional_parameters[i].key !== null || $rootScope.pluginData.additional_parameters[i].key !== undefined) && ($rootScope.pluginData.additional_parameters[i].value !== "" || $rootScope.pluginData.additional_parameters[i].value !== null || $rootScope.pluginData.additional_parameters[i].value !== undefined))
                {
                    jsonData[$rootScope.pluginData.additional_parameters[i].key] = $rootScope.pluginData.additional_parameters[i].value;
                }
                else
                {
                    $rootScope.handleResponse("Key or Value can not be empty for additional parameters");
                    return false;
                }
            }
        }
        jsonData.type = $rootScope.pluginData.type;

        if(file)
        {
            jsonData.plugin_name = file.name.substring(0, (file.name.length - 3));
            var substr = $rootScope.pluginData.type.charAt(0).toUpperCase()+$rootScope.pluginData.type.substring(1, $rootScope.pluginData.type.length)+"Plugin";
            if(!jsonData.plugin_name.includes(substr))
            {
                $rootScope.handleResponse("Invalid file name.File should have name including "+substr+" in it");
                return false;
            }
            else
            {
//                $rootScope.preLoader = true;
                // Upload deployment plugin code goes
                var uploadResponse = undefined;
                var uploadUrl = "/plugin/file/upload";
        //        uploadResponse = UploadDeploymentPlugin.uploadDeploymentPlugin(file, uploadUrl);
                var fd = new FormData();
                fd.append('file', file);
                fd.append('type', $rootScope.pluginOperation);

                $http.post(uploadUrl, fd, {
                    transformRequest: angular.identity,
                    headers: {'Content-Type': undefined}
                })

                .success(function(successResponse){
//                    $rootScope.preLoader = false;
//                    $rootScope.resultPane = true;
//                    $rootScope.response = {
//                        "message" : successResponse.message,
//                         "status" : 200,
//                         "result" : successResponse.result
//                    };
                    if($rootScope.pluginOperation === 'update')
                    {
                        jsonData._id = {
                            oid : $rootScope.pluginData._id.oid
                        };
                        ExitPointUpdate.update(jsonData, function(successResponse){
                            $rootScope.handleResponse(successResponse);
                            $state.go('manageDeploymentPlugin');
                            delete $rootScope.pluginData;
                            delete $rootScope.pluginOperation;
                            $rootScope.resultPane = false;
                            delete $rootScope.response;
                        },
                        function(errorResponse)
                        {
                            $rootScope.handleResponse(errorResponse);
                        });
                    }
                    else
                    {
                        ExitPoint.save(jsonData, function(successResponse){
                            $rootScope.handleResponse(successResponse);
                            $state.go('manageDeploymentPlugin');
                            delete $rootScope.pluginData;
                            delete $rootScope.pluginOperation;
                            $rootScope.resultPane = false;
                            delete $rootScope.response;
                            $scope.pluginFileSelected = '';
                            $rootScope.pluginFileToUpload = null;
                            $scope.pluginFileToUpload = null;

                        },
                        function(errorResponse)
                        {
                            $rootScope.handleResponse(errorResponse);
                        });
                    }

               })

               .error(function(errorResponse){
                    $rootScope.preLoader = false;
                    $rootScope.resultPane = true;
                    $rootScope.response = {
                        "message" : errorResponse.message,
                         "status" : 404,
                         "result" : "failed"
                    };
                    $rootScope.handleResponse($rootScope.response);
                    delete $rootScope.pluginOperation;
                });
            }
        }
        else if($rootScope.pluginOperation === 'update')
        {
            jsonData._id = {
                oid : $rootScope.pluginData._id.oid
            };
            jsonData.plugin_name = $rootScope.pluginData.plugin_name;
            ExitPointUpdate.update(jsonData, function(successResponse){
                delete $rootScope.pluginData;
                delete $rootScope.pluginOperation;
                $rootScope.handleResponse(successResponse);
                $rootScope.resultPane = false;
                delete $rootScope.response;
                $state.go('manageDeploymentPlugin');
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        }
        else
        {
            $rootScope.handleResponse("Please select plugin file");
            return false;
        }
    };

    $scope.discardPluginChanges = function()
    {
        $state.go('manageDeploymentPlugin')
    };
});

});