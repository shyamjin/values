require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var resendDistributionServiceControllerApp = angular.module('resendDistributionServiceControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

resendDistributionServiceControllerApp.controller('ResendDistributionServiceController', function ($scope, $stateParams, $state, ResendDistributionService) {
     $scope.requestResendDistribution = ResendDistributionService.get({
        id :   $stateParams.id
     },
     function (DistributionResendSuccessResponse)
     {
        $state.go('distribution');
        $rootScope.handleResponse(DistributionResendSuccessResponse);
     },
     function (DistributionResendErrorResponse)
     {
        $state.go('distribution');
        $rootScope.handleResponse(DistributionResendErrorResponse);
     });

 });
 });