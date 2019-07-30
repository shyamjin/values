/*
Author - nlate
Description -
    1. Controller that handles with the seperations of data and the operations in tool dashboard
Methods -
    1. showActiveTab(tab) - Sets the specified tab as an active tab
    2. getActiveTab(tab) - Returns a CSS class whether the specified tab is active or not
    3. getRequestStatus() - Gets the status of the deployment request
    4. getImportUpdateRequestStatus() - Gets the status of the import/update request of the tool
    5. stopRequestStatus() - Stops the status tracking of the deployment request
    6. stopImportUpdateRequestStatus() - Stops the status tracking of the import/update request
    7. closeRequestStatusModal() - Closes the popup of the request status modal and stops the timers for all processes
Uses -
    1. Show Tool - partials/dashboard/dashboard.partial.html
*/

define(['angular', 'uiRouter', 'settingsServicesApp', 'toolDashboardHeaderComponentControllerApp'],function (app) {
  'use strict';

var dashboardControllerApp = angular.module('dashboardControllerApp', ['ui.router', 'settingsServicesApp', 'toolDashboardHeaderComponentControllerApp']);

dashboardControllerApp.controller('DashboardController', function ($scope, $state, $stateParams, $rootScope, $location, $interval, TicketStatus, ImportUpdateStatus, $window) {
    var toolDeploymentPromise = null;
    var toolImportUpdatePromise = null;
    $scope.requestStatusMessages = [];
    if($rootScope.userProfile.token){
         $scope.displayTab = '/dashboard';
    }
    else{
        $state.go('login');
        return;
    }


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
        if($scope.displayTab === '/dashboard' && tab === '/tools/all')
        {
            return 'vp-tabs__tab--active';
        }
        else
        {
            return '';
        }
    };

    $scope.getRequestStatus = function ()
    {
        TicketStatus.get({
            id : $scope.requestID
        },
        function (response)
        {
            if(response.data.status=='Failed')
            {
                $scope.requestStatusMessages.push(response.data.status_message);
                $scope.loadingStatus = false;
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
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.getImportUpdateRequestStatus = function (request_id)
    {
        ImportUpdateStatus.get({
            id : request_id
        },
        function (response)
        {
            if(response.data.master_clone_request_status === 'Failed')
            {
                $scope.requestStatusMessages.push(response.data.status_message);
                $rootScope.handleResponse(response.data.status_message);
                $scope.stopImportUpdateRequestStatus();
                $scope.loadingStatus = false;
            }
            else
            {
                $scope.toolDeploymentRequestStatus = response.data.status_message;
                if($scope.requestStatusMessages.indexOf(response.data.status_message)<=-1)
                {
                    $scope.requestStatusMessages.push(response.data.status_message);
                }
                if(response.data.master_clone_request_status === 'Completed')
                {
                    $scope.requestStatusMessages.push(response.data.status_message);
                    $scope.loadingStatus = false;
                }
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    if($stateParams.request_id)
    {
        if($location.path().indexOf('/deployment')>=1)
        {
            $scope.loadingStatus = true;
            $scope.runningServicesPageTitle = 'Deployment';
            $scope.requestID = 'group/view/'+$stateParams.request_id;
            $('#show_deployment_progress_modal').show(700);
            toolDeploymentPromise = $interval( function(){ $scope.getRequestStatus(); }, 3000);
        }

        if($location.path().indexOf('/importupdate')>=1)
        {
            var request_ids = $stateParams.request_id.split(",");
            $scope.loadingStatus = true;
            $scope.runningServicesPageTitle = 'Request';
            $scope.requestID = $stateParams.request_id;
            $('#show_deployment_progress_modal').show(700);
            toolImportUpdatePromise = $interval( function(){ $scope.getImportUpdateRequestStatus(request_ids[0]); }, 3000);
//            for(var i=0; I<request_ids.length; i++)
//            {
//
//            }
        }
    }

    $scope.stopRequestStatus = function()
    {
        $scope.loadingStatus = false;
        $interval.cancel(toolDeploymentPromise);
        $interval.cancel(toolImportUpdatePromise);
        toolDeploymentPromise = undefined;
        toolImportUpdatePromise = undefined;
    };

    $scope.stopImportUpdateRequestStatus = function()
    {
        $scope.loadingStatus = false;
        $interval.cancel(toolDeploymentPromise);
        $interval.cancel(toolImportUpdatePromise);
        toolDeploymentPromise = undefined;
        toolImportUpdatePromise = undefined;
    };

    $scope.closeRequestStatusModal = function()
    {
        $state.go('dashboard');
        $('#show_deployment_progress_modal').hide(700);
        $interval.cancel(toolDeploymentPromise);
        $interval.cancel(toolImportUpdatePromise);
        toolDeploymentPromise = undefined;
        toolImportUpdatePromise = undefined;
    };

    $window.onclick = function ()
    {
        if(event.target.classList.contains('skip_slideup'))
        {
        }
        else
        {
            var allElements = document.querySelectorAll( 'body *' );
            if (allElements.length > 0)
            {
                for(var i = 0; i < allElements.length; i++)
                {
                    $(allElements[i]).slideUp();
                }
            }
        }
    };

    function remaining_up()
    {
        var allElements = document.getElementsByClassName('tag_popup');
        for(var i = 0; i < allElements.length; i++)
        {
            $(allElements[i]).slideUp();
        }
    }

});

});