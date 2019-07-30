define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';
var manageSyncServicesComponent = angular.module('manageSyncServicesComponent', ['ui.router']);
manageSyncServicesComponent.controller('ManageSyncServicesTabController', function ($scope, $state, $rootScope, $location) {
    $scope.displayTab = '/manage/synchronization/services';
    $scope.showActiveSyncTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
        delete $rootScope.selectedSyncID;
        delete $rootScope.SyncData;
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
});

});

