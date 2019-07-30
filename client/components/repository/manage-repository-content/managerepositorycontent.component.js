define(['angular', 'ngResource', 'uiRouter', 'toolTips','ngCookies','ngFocus','repositoryPartialControllerApp','repositoryServicesApp','deploymentPluginServicesApp'],function (app) {
  'use strict';

var EditRepositoryControllerApp = angular.module('EditRepositoryControllerApp', ['ui.router','720kb.tooltips','focus-if','repositoryPartialControllerApp','repositoryServicesApp','deploymentPluginServicesApp']);

EditRepositoryControllerApp.controller('EditRepositoryController', function($scope, $state, $stateParams, $rootScope, repositoryViewAll,repositoryViewById, GetAllDeploymentPlugins, updateRepository)
{
    $scope.repositorySelected = false;
    $scope.additional_artifacts_upload = [
        "true",
        "false"
    ];

    $scope.additional_parameters = [];
    repositoryViewAll.get({
    },
    function(successResponse)
    {
        $scope.repositoryAll = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.getRepoUlClass = function()
    {
        if($scope.repositorySelected === true)
        {
            if($scope.displayTab!='/view/repository')
            {
                $scope.repositorySelected = false;
            }
            return "vp-userform__fieldslist text--cs03 pr--lg";
        }
         else
         {
            return "vp-userform__fieldslist text--cs03 pr--lg hidden";
         }
    };

    $scope.getRepoFormClass = function()
    {
        if($scope.repositorySelected === true)
        {
            if($scope.displayTab!='/view/repository')
            {
                $scope.repositorySelected = false;
            }
            return "vp-selectedrepoform--active vp-userform vp-control max";
        }
        else
        {
            return "vp-selectedrepoform vp-userform vp-control max";
        }
    };

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

    $scope.isRepositorySelected = function(repo)
    {
        repositoryViewById.get({
            id:repo._id.$oid
        },
        function(viewRepoSuccessResponse)
        {
            $scope.repositorySelected = true;
            $scope.additional_parameters = [];
            $scope.repositoryViewIdData = viewRepoSuccessResponse;
            var val = $scope.repositoryViewIdData.data;
            for(var j in val)
            {
               if(j !=="_id" && j !== "name" && j!== "additional_artifacts_upload" && j!== "handler")
               {
                    $scope.additional_parameters.push({"key" :j, "value" : val[j]});
               }
            }
            GetAllDeploymentPlugins.get({
                value:"repository"
            },
            function(successResponse)
            {
                $scope.allRepositoryPlugins = successResponse.data;
                for(var i=0; i<$scope.allRepositoryPlugins.length; i++)
                {
                    if($scope.allRepositoryPlugins[i].plugin_name === $scope.repositoryViewIdData.data.handler)
                    {
                        $scope.repositoryViewIdData.data.handler = $scope.allRepositoryPlugins[i].plugin_name;
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(viewRepoErrorResponse)
        {
           $rootScope.handleResponse(viewRepoErrorResponse);
        });
    };

    $scope.discardChanges = function()
    {
        $scope.repositorySelected = false;
        delete $scope.repositoryViewIdData;
        $state.go('viewRepository');
    };

    $scope.createNewHandler = function()
    {
        $state.go('uploadDeploymentPlugin');
    };
    $scope.editRepository = function(repoData)
    {
        var jsonData = {
         _id : {
                oid : ''
            }
        };

        if($scope.additional_parameters)
        {
            for(var i=0; i<$scope.additional_parameters.length; i++)
            {
                if($scope.additional_parameters[i].key !== "" || $scope.additional_parameters[i].key !== null || $scope.additional_parameters[i].key !== undefined)
                {
                    jsonData[$scope.additional_parameters[i].key] = $scope.additional_parameters[i].value;
                }
                else
                {
                    $rootScope.handleResponse("Key can not be empty for additional parameters");
                    return false;
                }
            }
        }
        jsonData.additional_artifacts_upload = repoData.data.additional_artifacts_upload;
        jsonData.handler = repoData.data.handler;
        jsonData.name= repoData.data.name;
        jsonData._id.oid= repoData.data._id.$oid;

        updateRepository.update(jsonData, function(repoSuccessResponse)
        {
            $scope.repositorySelected = false;
            $state.go('viewRepository');
            $rootScope.handleResponse(repoSuccessResponse);
        },
        function(repoErrorResponse)
        {
            $rootScope.handleResponse(repoErrorResponse);
        });

    };

});
});