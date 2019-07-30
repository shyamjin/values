require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var deleteDistributionServiceControllerApp = angular.module('deleteDistributionServiceControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

deleteDistributionServiceControllerApp.controller('DeleteDistributionServiceController', function ($scope, $stateParams, $state, DeleteDistributionService) {
     $scope.requestDeletion = DeleteDistributionService.remove({
        id :   $stateParams.id
     },
     function (DistributionDeleteSuccessResponse)
     {
        $state.go('distribution');
        $rootScope.handleResponse(DistributionDeleteSuccessResponse);
     },
     function (DistributionDeleteErrorResponse)
     {
        $state.go('distribution');
        $rootScope.handleResponse(DistributionDeleteErrorResponse);
     });

 });
 });