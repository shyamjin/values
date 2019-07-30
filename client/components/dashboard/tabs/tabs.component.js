define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';
var requestTabComponent = angular.module('requestTabComponent', ['ui.router']);
requestTabComponent.controller('RequestsTabController', function ($scope, $state, $location) {
    $scope.activeRequestTab = '0';
    $scope.showActiveRequestsTab = function(tab)
    {
        $scope.activeRequestTab = tab;
    };

    $scope.getActiveRequestsTab = function(tab)
    {
        if(tab === $scope.activeRequestTab)
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

