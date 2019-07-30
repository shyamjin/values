define(['angular', 'ngResource', 'uiRouter', 'toolTips','ngCookies','ngFocus','repositoryPartialControllerApp','repositoryServicesApp','deploymentPluginServicesApp'],function (app) {
  'use strict';

var AddNewRepositoryControllerApp = angular.module('AddNewRepositoryControllerApp', ['ui.router','720kb.tooltips','focus-if','repositoryPartialControllerApp','repositoryServicesApp','deploymentPluginServicesApp']);

AddNewRepositoryControllerApp.controller('AddNewRepositoryController', function($scope, $state, $stateParams, $rootScope, GetAllDeploymentPlugins,createNewRepository)
{
    $scope.repository = {
        data : {
            name : '',
            additional_artifacts_upload : 'true',
            handler:''
        }
    };

    $scope.additional_artifacts_upload =
    [
        "true",
        "false"
    ];

    $scope.additional_parameters = [];

    GetAllDeploymentPlugins.get({
        value:"repository"
    },
    function(successResponse)
    {
        $scope.allRepositoryPlugins = successResponse.data;
        if($scope.allRepositoryPlugins.length > 0)
        {
            for(var i=0; i<$scope.allRepositoryPlugins.length; i++)
            {
                 $scope.repository.data.handler = $scope.allRepositoryPlugins[0].plugin_name;
            }
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.addRepoParameter = function()
    {
        if($scope.additional_parameters.length > 0)
        {
            $scope.additional_parameters.push({"key" : "", "value" : ""});
        }
        else
        {
            $scope.additional_parameters = [];
            $scope.additional_parameters.push({"key" : "", "value" : ""});
        }

    };
    $scope.removeRepoParameter = function(index)
    {
        $scope.additional_parameters.splice(index, 1);
    };

    $scope.createNewHandler = function()
    {
        $state.go('uploadDeploymentPlugin');
    };

    $scope.addNewRepository = function()
    {
        var repoData = {};
         if($scope.repository.data.name === undefined || $scope.repository.data.name === '')
        {
            $rootScope.handleResponse('Please enter repository name');
            return false;
        }
        if($scope.repository.data.additional_artifacts_upload === '' || $scope.repository.data.additional_artifacts_upload === undefined)
        {
            $rootScope.handleResponse('Please select Handle Additional Artifacts');
            return false;
        }
        if($scope.repository.data.handler === '' || $scope.repository.data.handler === undefined)
        {
            $rootScope.handleResponse('Please select handler');
            return false;
        }
        if($scope.additional_parameters)
        {
            for(var i=0; i<$scope.additional_parameters.length; i++)
            {
                if($scope.additional_parameters[i].key !== "" && $scope.additional_parameters[i].key !== undefined)
                {
                    repoData[$scope.additional_parameters[i].key] = $scope.additional_parameters[i].value;
                }
                else
                {
                    $rootScope.handleResponse("Key can not be empty for additional parameters");
                    return false;
                }
            }
        }
        repoData.additional_artifacts_upload = $scope.repository.data.additional_artifacts_upload;
        repoData.handler = $scope.repository.data.handler;
        repoData.name= $scope.repository.data.name;
        createNewRepository.save(repoData,function(SuccessResponse)
        {
            $state.go('viewRepository');
            $rootScope.handleResponse(SuccessResponse);
        },
        function(ErrorResponse)
        {
            $rootScope.handleResponse(ErrorResponse);
        });
    };

    $scope.discardNewRepoChanges = function()
    {
         delete $scope.repository ;
         $state.go('viewRepository');
    };
});
});