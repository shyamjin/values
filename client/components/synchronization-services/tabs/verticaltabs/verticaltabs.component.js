define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';
var syncDetailsTabsComponent = angular.module('syncDetailsTabsComponent', ['ui.router']);
syncDetailsTabsComponent.controller('SyncDetailsTabController', function ($scope, $state, $rootScope, $location) {
    $scope.displayDetailsTab = $location.path().substring(0, $location.path().length);
    $scope.showActiveMachineDetailsTab = function(tab)
    {
        $scope.displayDetailsTab = $location.path().substring(0, $location.path().length);
    };

    $scope.getActiveMachineDetailsTab = function(tab)
    {
        if($scope.displayDetailsTab === tab)
        {
            return 'vp-tabsvertical__tab--active';
        }
        else
        {
            return '';
        }
    };
});

});

