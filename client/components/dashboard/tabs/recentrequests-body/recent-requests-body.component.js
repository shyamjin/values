/*
Author and refactored by - nlate
Description -
    1. Controller that fetches the deployment requests from server and shows in the form of single deployment request on Dashboard screen
Methods -
    1. getAllRequeests() - Fetches all deployment requests
    2. retry(id) - re-submits the deployment request that was failed
Uses -
    1. Tool Dashboard / DU Dashboard - components/dashboard/tabs/recentrequests-body/recent-requests-body.component.html
*/

require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['moment', 'humanizeDuration',  'angularTimer', 'deploymentServicesApp']
});

define(['angular'],function (app) {
  'use strict';

var recentRequestsComponentControllerApp = angular.module('recentRequestsComponentControllerApp', ['deploymentServicesApp']);

recentRequestsComponentControllerApp.controller('RecentDeploymentRequestsController', function ($scope, $rootScope, $interval, $state, DeploymentRequestAll, RetryDeploymentRequest, RequestStatus) {
    var jsonData={};
    $scope.showLogIndicator = false;
    jsonData._id={
        oid:""
    };
    var promise;
    var interval;
    $scope.showRequestDetails = false;

    function getAllRequeests()
    {
        DeploymentRequestAll.get({
//            startdate: startDate,
            perpage: 100,
            page: 0
        },
        function(response)
        {
            $scope.requestsAll =  response;
            if($scope.requestsAll.data.requests_count.inprogress > 0)
            {
                angular.forEach($scope.requestsAll.data.list, function(value, key) {
                    for(var i=0; i<value.length; i++)
                    {
                       if (value[i].status === 'Processing')
                       {
                        var currentTime = new Date(value[i].current_time);
                        var startTime = new Date(value[i].start_time);
                        var timeDifference = Math.abs(currentTime - startTime);

                        var hours = Math.floor(timeDifference / (60 * 60));

                        var divisor_for_minutes = timeDifference % (60 * 60);
                        var minutes = Math.floor(divisor_for_minutes / 60);

                        var divisor_for_seconds = divisor_for_minutes % 60;
                        var seconds = Math.ceil(divisor_for_seconds);
                        if (hours < 10)   { hours    = "0" + hours; }
                        if (minutes < 10) { minutes = "0" + minutes; }
                        if (seconds < 10)  { seconds  = "0" + seconds; }
                        if (hours)            { hours   = "00"; }
                        var obj = {
                            "hh": hours,
                            "mm": minutes,
                            "ss": seconds
                        };
                        value[i].deployment_run_time = obj;
                        }
                    }
                });
            }
            else
            {
                $interval.cancel(interval);
                interval = undefined;
            }
        }, 
        function(errorResponse)
        {
            $interval.cancel(interval);
            interval = undefined;

            $rootScope.handleResponse(errorResponse);
        });
    }

    //run call every 5 seconds
    interval = $interval(getAllRequeests,5000);

    $scope.retry = function(requestId)
    {
        jsonData._id.oid=requestId;
        RetryDeploymentRequest.update(jsonData,function(retryDeploymentRequestResponse){
            $scope.showLogIndicator = false;
            document.getElementById("show_deployment_request").style.display = "none";
            $rootScope.handleResponse(retryDeploymentRequestResponse);
        },
        function(retryDeploymentRequestErrorResponse)
        {
            $scope.showLogIndicator = false;
            document.getElementById("show_deployment_request").style.display = "none";
            $rootScope.handleResponse(retryDeploymentRequestErrorResponse);
        });
    };

    $scope.isExpanded = function(flag)
    {
        if(flag === true)
        {
            return 'vp-treeview__dateitem--expanded';
        }
        else
        {
            return '';
        }
    };

    $scope.$on('$stateChangeStart', function (event, toState, toParams, fromState, fromParams) {
        $interval.cancel(interval);
        interval = undefined;
    });

});

});