define(['angular','deploymentRequestGridControllerApp'],function (app) {
  'use strict';

var deploymentDetailsContentControllerApp = angular.module('deploymentDetailsContentControllerApp', ['deploymentRequestGridControllerApp']);

deploymentDetailsContentControllerApp.controller('deploymentDetailContentController', function ($scope,  $rootScope,$interval,SingleDeploymentRequestDetails, RetryDeploymentRequest,DeploymentRequestView) {
   var promise;
   var jsonData={};

   jsonData._id={
        oid:""
   };

   $rootScope.$on("setGroupData", function (event, args) {
        $scope.GroupData = args;
   });

   $scope.getDeploymentRequestLog = function (index)
   {
        $scope.SingleData = $scope.GroupData.details[index];
        $scope.selectedIndex=index;
        $scope.deploymentRequestDetails = SingleDeploymentRequestDetails.get({
            id: $scope.SingleData._id.$oid
        },
        function (response)
        {
            jQuery(".log-modal").addClass("active");
            jQuery(".log-overlay").addClass("active");
            $scope.CurrentDeployment = response.data;
            $scope.CurrentDeploymentlogs = response.data.logs;
        },
        function (errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
   };

   $scope.showLog = function()
   {
        $scope.showLogIndicator = true;
        if($scope.CurrentDeployment.status === 'Processing')
        {
            promise = $interval( function(){ $scope.getDeploymentRequestLog($scope.reqIndex); }, 7000);
        }
        else
        {
            jQuery(".log-modal").addClass("active");
            jQuery(".log-overlay").addClass("active");
        }
   };

   $scope.hideLog = function()
   {
        $interval.cancel(promise);
        jQuery(".log-modal").removeClass("active");
        jQuery(".log-overlay").removeClass("active");
   };

   $scope.retry = function(requestId)
   {
        jsonData._id.oid=requestId;
        $scope.retryDeploymentRequest=RetryDeploymentRequest.update(jsonData,function(retryDeploymentRequestResponse){
            $rootScope.handleResponse(retryDeploymentRequestResponse);
            DeploymentRequestView.get({
                page: 0
            },
            function(response){
                $scope.deployments = response;
                $scope.currentPage = response.data.page;
                $scope.totalCount = response.data.total;
            }, 
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(retryDeploymentRequestErrorResponse)
        {
            $rootScope.handleResponse(retryDeploymentRequestErrorResponse);
        });
        $rootScope.$emit('setDeploymentGroup',$scope.selectedGroupID);
        $rootScope.$emit('setIndexOfFirstTab',0);
   };

   $scope.showNestedStepsDetails = function(requestID)
   {
        SingleDeploymentRequestDetails.get({
            id : requestID
        },
        function(response)
        {
            $scope.NestedSteps = true;
            $scope.NestedStepDetails = [];
            var stepDetails =[];
            stepDetails=response.data.step_details;
            var stepCountFlag = 0;
            for(var i=0;i<stepDetails.length;i++)
            {
                if(stepDetails[i].step_name==='checkIfValidUpgrade' || stepDetails[i].step_name==='validate_mandatory_details' || stepDetails[i].step_name==='authenticateAndDeploy' || stepDetails[i].step_name==='check_tunneling_and_deploy')
                {
                       for(var key_1 in stepDetails[i].nested_step_details)
                       {

                               $scope.NestedStepDetails.push(stepDetails[i].nested_step_details[key_1]);

                       }
    //                        var key = Object.keys(stepDetails[i].tool_step_details);
                }
           }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };


    $scope.showSteps = function()
    {
        $scope.NestedSteps = false;
    };
 });

});