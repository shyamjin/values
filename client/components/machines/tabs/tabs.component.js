define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';
var machineTabsComponent = angular.module('machineTabsComponent', ['ui.router']);
machineTabsComponent.controller('ManageMachineTabController', function ($scope, $state, $location, $rootScope) {
    $scope.displayTab = '/machines';
    $scope.showActiveMachineTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
    };

    $scope.getActiveMachineTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
        if($location.path().indexOf('editmachine')>=0)
        {
            $scope.displayTab = '/machines';
        }
        if($location.path().indexOf('/edit/machine/group')>=0)
        {
            $scope.displayTab = '/manage/machine/groups';
        }
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

