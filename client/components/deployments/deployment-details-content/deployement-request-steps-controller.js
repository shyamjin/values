define(['angular', 'uiRouter', 'ngCookies', 'moment', 'humanizeDuration', 'angularTimer', 'jquery', 'toolTips', 'authenticationServicesApp', 'toolServicesApp', 'machineServicesApp', 'deploymentServicesApp','deploymentPartialControllerApp'],function (app) {
  'use strict';

var deployementRequestStepsControllerApp = angular.module('deployementRequestStepsControllerApp', ['ui.router', '720kb.tooltips', 'authenticationServicesApp', 'toolServicesApp', 'machineServicesApp', 'deploymentServicesApp', 'timer','deploymentPartialControllerApp']);

deployementRequestStepsControllerApp.controller('DeployementRequestStepsController', function ($timeout, $scope, $rootScope, $state, $stateParams, DeploymentRequestView, OneDeploymentRequestView, SingleDeploymentRequestDetails,$interval){
    $scope.DeployementRequestDetail={};
    $scope.DeployementRequestDetail=SingleDeploymentRequestDetails.get({
        id:$stateParams.id
    },
    function(response)
    {
        $scope.NestedStepDetails = [];
        var stepDetails =[];
        stepDetails=response.data.step_details;
        var stepCountFlag = 0;
        for(var i=0;i<stepDetails.length;i++)
        {
           if(stepDetails[i].step_name==='checkIfValidUpgrade' || stepDetails[i].step_name==='authenticateAndDeploy')
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
    $scope.requestId=$stateParams.id;

});
});