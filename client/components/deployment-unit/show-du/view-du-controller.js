define(['angular', 'ngResource', 'uiRouter', 'ngCookies','toolTips', 'jquery', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp'], function (app) {
  'use strict';

var viewDUControllerApp = angular.module('viewDUControllerApp', ['ui.router','720kb.tooltips', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp']);

viewDUControllerApp.controller('ViewDUController', function ($scope, $stateParams, $rootScope, $state, PrerequisitesViewAll, ApprovalStatusAll, DUTypesAll, UserDetails, ViewDU) {

    $scope.closeDUDetailsModal = function()
    {
        $('#show_du_details').hide(700);
        $state.go('duDashboard');
    };

    $scope.deploymentTypeToSelect ={
        type :""
    };
    $scope.showAllReleaseNotes = true;
    $scope.showAllDUReleaseNotes = true;
    $scope.showLessDUReleaseNotes = false;
    $scope.BuildFlag = false;
    $scope.StateFlag= false;
    $scope.selectedBuild = '';
    $scope.showAllChecksum = true;

    $scope.showMoreReleaseNotes = function()
    {
        $scope.showAllReleaseNotes = false;
        $('#release_notes_build').removeClass('text--ellipsis');
    };

    $scope.showLessReleaseNotes = function()
    {
        $scope.showAllReleaseNotes = true;
        $('#release_notes_build').addClass('text--ellipsis');
    };

    $scope.showMoreReleaseNotesContent = function()
    {
        $scope.showAllDUReleaseNotes = false;
        $scope.showLessDUReleaseNotes = true;
        $('#release_notes_du').removeClass('text--ellipsis');
    };

    $scope.showLessReleaseNotesContent = function()
    {
        $scope.showAllDUReleaseNotes = true;
        $scope.showLessDUReleaseNotes = false;
        $('#release_notes_du').addClass('text--ellipsis');
    };

    $scope.showMoreChecksum = function()
    {
        $scope.showAllChecksum = false;
    };

    $scope.showLessChecksum = function()
    {
        $scope.showAllChecksum = true;
    };

    $scope.setDUDeployType = function(value)
    {
        $scope.deploymentTypeToSelect.type = value;
        $scope.deployDUSetData.duDataList = [];
        $scope.BuildFlag = false;
        $scope.StateFlag= false;
        $scope.buildDetails = '';
        if($scope.deploymentTypeToSelect.type === "Build")
        {
            if($scope.application.data.build.length > 0)
            {
                $scope.StateFlag= false;
                $scope.BuildFlag = true;
                $scope.buildDetails ='';
            }
        }
        if($scope.deploymentTypeToSelect.type === "State")
        {
            if($scope.application.data.state.length > 0)
            {
                $scope.BuildFlag = false;
                $scope.StateFlag= true;
                $scope.buildDetails ='';
            }
        }
        if ($scope.deploymentTypeToSelect.type === "")
        {
            $scope.BuildFlag = false;
            $scope.StateFlag= false;
            $scope.buildDetails ='';
        }

    };

    $scope.flexibleAttributes = {};
    $scope.faNameValueMap = {};
    $scope.faDefLoaded = function(faDef){
        $scope.flexibleAttributes = faDef;

        ViewDU.get({
        id : $stateParams.id
        },
        function(viewDUSuccessResponse)
        {
            $('#show_du_details').show(700);
            $scope.application = viewDUSuccessResponse;
             $scope.deployDUSetData = {
                'du_id' : $scope.application.data._id.$oid,
                'duDataList' : []
            };
            var approval_status = $scope.application.data.approval_status;
            var du_type = $scope.application.data.type;
            if($scope.application.data.build && $scope.application.data.build.length>0)
            {
                $scope.selectedBuild = parseInt($scope.application.data.build[0].build_number, 10);
            }
            ApprovalStatusAll.get({
            },
            function(successResponse)
            {
                $scope.approvalStatusAll = successResponse;
                for(var i=0; i<$scope.approvalStatusAll.length; i++)
                {
                    if($scope.approvalStatusAll[i]._id.$oid === approval_status)
                    {
                        $scope.application.data.approval_status = $scope.approvalStatusAll[i].name;
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            DUTypesAll.get({
            },
            function(successResponse)
            {
                $scope.DUTypes = successResponse;
                for(var j=0; j<$scope.DUTypes.length; j++)
                {
                    if($scope.DUTypes[j]._id.$oid === du_type)
                    {
                        $scope.application.data.type = $scope.DUTypes[j].name;
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });

            if ($scope.application.data.flexible_attributes){
                for(var k in $scope.application.data.flexible_attributes){
                    $scope.faNameValueMap[k]=$scope.application.data.flexible_attributes[k];
                }
            }
        },
        function(viewDUErrorResponse)
        {
            $rootScope.handleResponse(viewDUErrorResponse);
        });
    };

    $scope.showBuildDetails = function(value)
    {
        var build = value;
        $scope.selectedBuildToDeploy = JSON.parse(value);
        $scope.deployDUSetData.duDataList = [];
        $scope.deployDUSetData.duDataList.push({'build_id' :$scope.selectedBuildToDeploy._id.$oid,'build_number':$scope.selectedBuildToDeploy.build_number}) ;
        $scope.buildDetails = JSON.parse(value);
    };
    $scope.showStateDetails = function(value)
    {
        $scope.selectedStateToDeploy = JSON.parse(value);
        $scope.deployDUSetData.duDataList = [];
        $scope.deployDUSetData.duDataList.push({'state': $scope.selectedStateToDeploy._id.$oid,'build_id':$scope.selectedStateToDeploy.build._id.$oid,'build_number':$scope.selectedStateToDeploy.build.build_number,'deployment_field':$scope.selectedStateToDeploy.deployment_field}) ;
        $scope.StateDetails = JSON.parse(value);
        $scope.buildDetails = $scope.StateDetails.build;
    };

    $scope.duSetDeploy = function(value)
    {
        if($scope.deploymentTypeToSelect.type)
        {
            if($scope.deploymentTypeToSelect.type === 'Build')
            {
                if ($scope.deployDUSetData.duDataList.length === 0)
                {
                    $rootScope.handleResponse('Please select build for du');
                    return false;
                }
            }
            if($scope.deploymentTypeToSelect.type === 'State')
            {
                if ($scope.deployDUSetData.duDataList.length === 0)
                {
                    $rootScope.handleResponse('Please select state for du');
                    return false;
                }
            }
        }
        else
        {

            $scope.deployDUSetData.duDataList = [];
            if($scope.application.data.build !== null && $scope.application.data.build !== undefined)
            {
                 $scope.deployDUSetData.duDataList.push({'build_id' :$scope.application.data.build[0]._id.$oid,'build_number':$scope.application.data.build[0].build_number});
                 $state.go('deployDU',{id : JSON.stringify($scope.deployDUSetData)});
            }
            else
            {
                $rootScope.handleResponse('Valid Build is not available for this DU');
                return false;
            }
        }
        $state.go('deployDU',{id : JSON.stringify(value)});

    };

});
});