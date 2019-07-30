define(['angular', 'ngResource', 'uiRouter', 'ngCookies','toolTips', 'jquery', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp'], function (app) {
  'use strict';

var deploymentUnitDashboardControllerApp = angular.module('deploymentUnitDashboardControllerApp', ['ui.router','720kb.tooltips', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp']);

deploymentUnitDashboardControllerApp.controller('DeploymentUnitDashboardController', function ($scope, $rootScope, $state, $stateParams, $location, $interval, TicketStatus) {
    $scope.displayTab = '/dashboard/du';
    var promise = null;
    $scope.requestStatusMessages = [];

    $scope.searchDUWithName = function(keyword)
    {
        if($rootScope.currentState === 'duDashboard')
        {
            $rootScope.$emit("searchDUEvent", {'keyword' : keyword});
        }
        else if($rootScope.currentState === 'duSetDashboard')
        {
            $rootScope.$emit("searchDUSetEvent", {'keyword' : keyword});
        }
    };

    $scope.showActiveTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
    };

    $scope.getActiveTab = function(tab)
        {
            $scope.displayTab = $location.path().substring(0, $location.path().length);
            if(tab === $scope.displayTab)
            {
                return 'vp-tabs__tab--active';
            }
            else
            {
                return '';
            }
        };
    $scope.setBackground = function(type)
    {
        if(type === 'Fast Track')
        {
            return 'bg--cs17';
        }
        else if(type === 'Hot Fix')
        {
            return 'bg--cs13';
        }
        else
        {
            return 'bg--cs01';
        }
    };

    if($stateParams.request_id)
    {
        $scope.loadingStatus = true;
        $scope.requestID = 'group/view/'+$stateParams.request_id;
        $('#show_deployment_progress_modal').show(700);
        $scope.getRequestStatus = function ()
        {
            TicketStatus.get({
                id : $scope.requestID
            },
            function (response)
            {
                if(response.data.status=='Failed')
                {
                    $scope.loadingStatus = false;
                    $scope.requestStatusMessages.push(response.data.status_message);
                    $scope.stopRequestStatus();
                }
                else if(response.data.status=='Done')
                {
                    $scope.requestStatusMessages.push(response.data.status_message);
                    $scope.loadingStatus = false;
                    $scope.stopRequestStatus();
                }
                else
                {
                    $scope.toolDeploymentRequestStatus= response.data.status_message;
                    if($scope.requestStatusMessages.indexOf(response.data.status_message)<=-1)
                    {
                        $scope.requestStatusMessages.push(response.data.status_message);
                        if(response.data.status_message === 'The request has completed')
                        {
                            $scope.loadingStatus = false;
                        }
                    }
                }
            },
            function(errorResponse)
            {
                $interval.cancel(promise);
                promise = undefined;
                $rootScope.handleResponse(errorResponse);
            });
        };

        $scope.stopRequestStatus = function()
        {
            $scope.loadingStatus = false;
            $interval.cancel(promise);
            promise = undefined;
        };
        promise = $interval( function(){ $scope.getRequestStatus(); }, 3000);
    }

    $scope.closeRequestStatusModal = function()
    {
        $state.go('duDashboard');
        $('#show_deployment_progress_modal').hide(700);
    };

});
});