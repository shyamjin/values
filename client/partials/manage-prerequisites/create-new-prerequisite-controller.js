define(['angular', 'prerequisitesRoutesApp', 'prerequisitesServicesApp'],function (app) {
  'use strict';

var addNewPrerequisiteControllerApp = angular.module('addNewPrerequisiteControllerApp', ['ui.router', '720kb.tooltips', 'prerequisitesRoutesApp', 'prerequisitesServicesApp']);

addNewPrerequisiteControllerApp.controller('CreateNewPrerequisiteController', function ($scope, $stateParams, $state, $rootScope, PrerequisiteView, PrerequisiteCreate) {
        var jsonData = {};
        $scope.prerequisiteData = {
            prerequisite_name : '',
            display_name : '',
            version_command : '',
            parse_version : '',
            prerequisites_status : '',
            version_list : []
        };

        $scope.prerequisiteStatus = [
            "active",
            "deprecated"
        ];

        $scope.addVersion = function()
        {
            $scope.prerequisiteData.version_list.push({'number' : 0.0});
        };

        $scope.removeVersion = function(index)
        {
            $scope.prerequisiteData.version_list.splice(index, 1);
        };

        $scope.createNewPrerequisite = function(form)
        {
            jsonData.version_list = [];
            var version_list_length = $scope.prerequisiteData.version_list.length;
            for(var a=0; a<version_list_length; a++)
            {
                if($scope.prerequisiteData.version_list[a].number === undefined)
                {
                    $rootScope.handleResponse('Please enter a version number!');
                    return false;
                }
                else
                {
                    var number = parseFloat($scope.prerequisiteData.version_list[a].number);
                    jsonData.version_list.push(number);
                }
            }
            if(version_list_length>0)
            {
                for(var i=0; i<version_list_length; i++)
                {
                    var flag = 0;
                    var isNumberFlag = 0;
                    if(jsonData.version_list[i]<0.1 || jsonData.version_list[i]>99 || jsonData.version_list[i] === undefined || jsonData.version_list[i] === null)
                    {
                        $rootScope.handleResponse('Please enter a valid version number!');
                        return false;
                    }

                    for(var j=0; j<version_list_length; j++)
                    {
                        if(jsonData.version_list[i]===jsonData.version_list[j])
                        {
                            flag++;
                        }
                    }

                    if(flag>1)
                    {
                        $rootScope.handleResponse('Please enter the each version number only once!');
                        return false;
                    }
                }
            }
            else
            {
                $rootScope.handleResponse("Please enter at least one version");
                return false;
            }

            if($scope.prerequisiteData.prerequisite_name === null || $scope.prerequisiteData.prerequisite_name === undefined || $scope.prerequisiteData.prerequisite_name === '')
            {
                $rootScope.handleResponse("Please enter prerequisite name");
                return false;
            }

            if($scope.prerequisiteData.display_name === null || $scope.prerequisiteData.display_name === undefined || $scope.prerequisiteData.display_name === '')
            {
                $rootScope.handleResponse("Please enter display name");
                return false;
            }

            if($scope.prerequisiteData.prerequisites_status === null || $scope.prerequisiteData.prerequisites_status === undefined || $scope.prerequisiteData.prerequisites_status === '')
            {
                $rootScope.handleResponse("Please select prerequisites status");
                return false;
            }

            jsonData.prerequisites_name = $scope.prerequisiteData.prerequisite_name;
            jsonData.display_name = $scope.prerequisiteData.display_name;
            jsonData.version_command = $scope.prerequisiteData.version_command;
            jsonData.parse_version = $scope.prerequisiteData.parse_version;
            jsonData.prerequisites_status = $scope.prerequisiteData.prerequisites_status;

            PrerequisiteCreate.save(jsonData, function(prerequisiteCreateSuccessResponse){
                $state.go('managePrerequisites');
                $rootScope.handleResponse(prerequisiteCreateSuccessResponse);
            },
            function(prerequisiteCreateErrorResponse)
            {
                $rootScope.handleResponse(prerequisiteCreateErrorResponse);
            });
        };
 });
 });