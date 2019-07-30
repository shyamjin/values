require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var deleteConfigurationControllerApp = angular.module('deleteConfigurationControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

deleteConfigurationControllerApp.controller('DeleteConfigurationController', function ($scope, $stateParams, $window, $state,ConfigDelete) {
    $scope.configDeletion = ConfigDelete.remove({
          id :   $stateParams.id
     },
     function (configDeleteRequest)
     {
        $rootScope.handleResponse(configDeleteRequest);
     },
     function (configDeleteResponseError){
        $rootScope.handleResponse(configDeleteResponseError);
     });
 });
 });