require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var manageSynchronizationServiceControllerApp = angular.module('manageSynchronizationServiceControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

manageSynchronizationServiceControllerApp.controller('ManageSynchronizationServiceController', function ($scope, $stateParams, $location, $state, $timeout, $rootScope) {
    $scope.displayTab = '/manage/synchronization/services';
    $scope.showActiveSyncTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
    };

    $scope.getActiveSyncTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
        if(tab === $scope.displayTab)
        {
            return 'vp-tabs__tab--active';
        }
        else
        {
            return '';
        }
    };
    $scope.closeRunningRequestDetails = function()
    {
        $('#show_request_progress_modal').hide(700);
    };
 });
 });