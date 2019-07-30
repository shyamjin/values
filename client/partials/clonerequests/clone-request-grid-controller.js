/* Created by Nilesh Late */
require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['cloneServicesApp']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'jquery', 'cloneServicesApp'],function (app) {
  'use strict';

var cloneRequestGridControllerApp = angular.module('cloneRequestGridControllerApp', ['ui.router', 'cloneServicesApp']);

cloneRequestGridControllerApp.controller('CloneRequestGridController', function ($scope, $state, $stateParams, $window, $http, $interval, CloneRequestStatusAll, $rootScope, CloneRequestStatus, RetryCloneRequest){
      $scope.toolSteps = false;
      $scope.cloneRequestsAll = CloneRequestStatusAll.get({
      },
      function(errorResponse)
      {
        $rootScope.handleResponse(errorResponse);
      });

      $scope.selectCloneRequest = function (requestid)
      {
        $('html, body').animate({
            scrollTop: $("#requestDetailsSection").offset().top - 50
        }, 1000);
        $scope.cloneRequest = CloneRequestStatus.get({
            id: requestid
        },
        function (response)
        {
            $scope.GroupData = response.data;
            $scope.SingleData = response.data;
            if(response.data.logs)
            {
                $scope.allCloneLogs = response.data.logs;
            }
            $scope.selectedIndex=-1;
        });
      };

    $scope.retry = function(requestId)
    {
        var jsonData = {
            _id : {
                oid : ''
            }
        };
        jsonData._id.oid = requestId;
        $scope.retryCloneRequest = RetryCloneRequest.update(jsonData,function(retryCloneRequestSuccessResponse){
            $rootScope.handleResponse(retryCloneRequestSuccessResponse);
            $scope.cloneRequestsAll=CloneRequestStatusAll.get({
            },
            function(successResponse) {
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            $scope.selectCloneRequest(jsonData._id.oid);
        },
        function(retryCloneRequestErrorResponse){
            $rootScope.handleResponse(retryCloneRequestErrorResponse);
        });
     };

    $scope.showToolStepsDetails = function(requestID)
    {
        CloneRequestStatus.get({
            id : requestID
        },
        function(response)
        {
            $scope.toolSteps = true;
            $scope.toolStepDetails = [];
            var stepDetails =[];
            stepDetails=response.data.step_details;
            var stepCountFlag = 0;
            for(var i=0;i<stepDetails.length;i++)
            {
                if(stepDetails[i].step_name==='clone_tools' || stepDetails[i].step_name==='import_tools' || stepDetails[i].step_name==='update_tools')
                {
                       for(var key_1 in stepDetails[i].tool_step_details)
                       {
                           for(var key_2 in stepDetails[i].tool_step_details[key_1])
                           {
                               $scope.toolStepDetails.push(stepDetails[i].tool_step_details[key_1][key_2]);
                           }
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
        $scope.toolSteps = false;
     };

     $scope.showLog = function()
     {
        jQuery(".log-modal").addClass("active");
        jQuery(".log-overlay").addClass("active");
     };
     $scope.hideLog = function() {
        jQuery(".log-modal").removeClass("active");
        jQuery(".log-overlay").removeClass("active");
     };

});
});