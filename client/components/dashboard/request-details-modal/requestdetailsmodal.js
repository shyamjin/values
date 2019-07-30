/*
Author and refactored by - nlate
Description -
    1. Controller that fetches the deployment request by using request id from server and shows in the form of single deployment request on Dashboard screen as a modal popup
Methods -
    1. showDeploymentRequestDetails(id) - Fetches deployment requests by request id
    2. retry(id) - re-submits the deployment request that was failed
Uses -
    1. Tool Dashboard / DU Dashboard - components/dashboard/request-details-modal/requestdetailsmodal.html
*/

require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['moment', 'humanizeDuration',  'angularTimer', 'deploymentServicesApp']
});

define(['angular'],function (app) {
  'use strict';

var requestDetailsComponentControllerApp = angular.module('requestDetailsComponentControllerApp', ['deploymentServicesApp']);

requestDetailsComponentControllerApp.controller('DeploymentRequestDetailsController', function ($scope, $rootScope, $interval, $state, DeploymentRequestAll, RetryDeploymentRequest, RequestStatus) {
    var jsonData={};
    var promise;
    $scope.showLogIndicator = false;
    jsonData._id={
        oid:""
    };
    $scope.showRequestDetails = false;

    $scope.retry = function(requestId)
    {
        jsonData._id.oid=requestId;
        $scope.retryDeploymentRequest=RetryDeploymentRequest.update(jsonData,function(retryDeploymentRequestResponse){
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

    $scope.showDeploymentRequestDetails = function(request_id)
    {
        $scope.requestID = request_id;
        document.getElementById("show_deployment_request").style.display = "block";
        $scope.requestDetails = RequestStatus.get({
            id:request_id
        },
        function(response)
        {
            if(response.data.tool_deployment_value.length===0)
            {
               $scope.toolDeplValueVisible=false;
            }
            else{
                $scope.toolDeplValueVisible=true;
            }
            $scope.CurrentDeploymentlogs = response.data.logs;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.getDeploymentRequestLog = function(request_id)
    {
        $scope.requestID = request_id;
        $scope.requestDetails = RequestStatus.get({
            id:request_id
        },
        function(response)
        {
            jQuery(".log-modal").addClass("active");
            jQuery(".log-overlay").addClass("active");
            if(response.data.tool_deployment_value.length===0)
            {
               $scope.toolDeplValueVisible=false;
            }
            else
            {
                $scope.toolDeplValueVisible=true;
            }
            $scope.CurrentDeploymentlogs = response.data.logs;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.showLog = function()
    {
        $scope.showLogIndicator = true;
        jQuery(".log-modal").addClass("active");
        jQuery(".log-overlay").addClass("active");
        if($scope.requestDetails.data.status === 'Processing')
        {
            promise = $interval( function(){ $scope.getDeploymentRequestLog($scope.requestID); }, 7000);
        }
    };

    $scope.hideLog = function()
    {
        $interval.cancel(promise);
        $scope.showLogIndicator = false;
        jQuery(".log-modal").removeClass("active");
        jQuery(".log-overlay").removeClass("active");
    };

    $scope.closeDeploymentRequestDetails = function()
    {
        $scope.showLogIndicator = false;
        document.getElementById("show_deployment_request").style.display = "none";
        $interval.cancel(promise);
    };

    $scope.viewDeploymentRequestDetails = function(id)
    {
        $state.go('deploymentrequestsbyid', {id : id});
    };
});

});