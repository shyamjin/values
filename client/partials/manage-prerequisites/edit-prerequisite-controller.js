define(['angular', 'prerequisitesRoutesApp', 'prerequisitesServicesApp'],function (app) {
  'use strict';

var editPrerequisiteController = angular.module('editPrerequisiteController', ['ui.router', '720kb.tooltips', 'prerequisitesRoutesApp', 'prerequisitesServicesApp']);

editPrerequisiteController.controller('EditPrerequisiteController', function ($scope, $stateParams, $state, $rootScope, PrerequisiteView, PrerequisiteEdit, PrerequisitesViewAll, PrerequisiteDelete) {
    PrerequisitesViewAll.get({
    },
    function(prerequisiteSuccessResponse)
    {
        $scope.prerequisitesAll = prerequisiteSuccessResponse.data;
    },
    function(prerequisiteErrorResponse)
    {
        $rootScope.handleResponse(prerequisiteErrorResponse);
    });

    var jsonData = {
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

    $scope.selectPrerequisite = function(id)
    {
        $scope.prerequisiteData = {
            prerequisite_name : '',
            display_name : '',
            version_command : '',
            parse_version : '',
            prerequisites_status : '',
            version_list : []
        };
        $scope.Prerequisite = PrerequisiteView.get({
            id : id
        },
        function(prerequisiteViewSuccessResponse)
        {
            $scope.prerequisiteData.prerequisite_name = prerequisiteViewSuccessResponse.data.prerequisites_name;
            $scope.prerequisiteData.display_name = prerequisiteViewSuccessResponse.data.display_name;
            $scope.prerequisiteData.version_command = prerequisiteViewSuccessResponse.data.version_command;
            $scope.prerequisiteData.parse_version = prerequisiteViewSuccessResponse.data.parse_version;
            $scope.prerequisiteData.prerequisites_status = prerequisiteViewSuccessResponse.data.prerequisites_status;
            for(var i=0; i<prerequisiteViewSuccessResponse.data.version_list.length; i++)
            {
                $scope.prerequisiteData.version_list.push({'number' : prerequisiteViewSuccessResponse.data.version_list[i]});
            }
        },
        function(prerequisiteViewErrorResponse)
        {
            $rootScope.handleResponse(prerequisiteViewErrorResponse);
        });
    };

    $scope.editPrerequisite = function(form)
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

        PrerequisiteEdit.update(jsonData, function(prerequisiteEditSuccessResponse){
            delete $scope.prerequisiteData;
            $state.go('managePrerequisites');
            $rootScope.handleResponse(prerequisiteEditSuccessResponse);
        },
        function(prerequisiteEditErrorResponse)
        {
            $rootScope.handleResponse(prerequisiteEditErrorResponse);
        });
    };

    $scope.openDeletePrerequisiteConfirmationPopup = function(id)
    {
        $scope.prerequisite_id = id;
        $('#show_delete_prerequisite_confirmation_popup').show(700);
    };

    $scope.closeDeletePrerequisiteConfirmationPopup = function()
    {
        delete $scope.prerequisite_id;
        $('#show_delete_prerequisite_confirmation_popup').hide(700);
    };

    $scope.deletePrerequisite = function(id)
    {
        PrerequisiteDelete.remove({
            id : $scope.prerequisite_id
        },
        function(prerequisiteDeleteSuccessResponse)
        {
            delete $scope.prerequisitesAll;
            $('#show_delete_prerequisite_confirmation_popup').hide(700);
            PrerequisitesViewAll.get({
            },
            function(prerequisiteSuccessResponse)
            {
                $scope.prerequisitesAll = prerequisiteSuccessResponse.data;
            },
            function(prerequisiteErrorResponse)
            {
                $rootScope.handleResponse(prerequisiteErrorResponse);
            });

            $state.go('managePrerequisites');
            $rootScope.handleResponse(prerequisiteDeleteSuccessResponse);
        },
        function (prerequisiteDeleteErrorResponse)
        {
            $('#show_delete_prerequisite_confirmation_popup').hide(700);
            $rootScope.handleResponse(prerequisiteDeleteErrorResponse);
        });
    };

    $scope.discardPrerequisiteChanges = function()
    {
        delete $scope.prerequisiteData;
        $state.go('managePrerequisites');
    };

});
});