/* Created by Nilesh Late */
require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['cloneServicesApp']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'jquery', 'cloneServicesApp'],function (app) {
  'use strict';

var cloneRequestStepsControllerApp = angular.module('cloneRequestStepsControllerApp', ['ui.router', 'cloneServicesApp']);

cloneRequestStepsControllerApp.controller('CloneRequestStepsController', function ($scope, $state, $stateParams, $window, $http, $interval, CloneRequestStatusAll, $rootScope, CloneRequestStatus){
    $scope.cloneRequestDetail={};
    $scope.cloneRequestDetail=CloneRequestStatus.get({
        id:$stateParams.id
    },
    function(response)
    {
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
    $scope.requestId=$stateParams.id;
});
});