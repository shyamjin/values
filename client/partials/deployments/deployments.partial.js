/*
Author - shyamjin
Description -
    1. Controller that handles with the common operations required in deployment view
Methods -

Uses -
    1. Deployment - partials/deployments/deployments.partial.html
*/


define(['angular','deploymentRequestGridControllerApp','deploymentVerticalTabsControllerApp','deploymentDetailsContentControllerApp','DeploymentRequestsFilterControllerApp','revertDeploymentGroupControllerApp'],function (app) {
  'use strict';

var deploymentPartialControllerApp = angular.module('deploymentPartialControllerApp', ['deploymentRequestGridControllerApp','deploymentVerticalTabsControllerApp','deploymentDetailsContentControllerApp','DeploymentRequestsFilterControllerApp','revertDeploymentGroupControllerApp']);

deploymentPartialControllerApp.controller('deploymentPartialController', function ($scope,  $rootScope) {


 });

});