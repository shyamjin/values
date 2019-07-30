define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';
var machineDetailsTabsComponent = angular.module('machineDetailsTabsComponent', ['ui.router']);
machineDetailsTabsComponent.controller('EditMachineDetailsTabController', function ($scope, $state, $rootScope) {
    $rootScope.displayDetailsTab = 0;
    $scope.showActiveMachineDetailsTab = function(tab)
    {
        $rootScope.displayDetailsTab = tab;
        if($rootScope.displayDetailsTab === 3 || $rootScope.displayDetailsTab === '3')
        {
            $rootScope.$emit('GetToolDeploymentHistory', {});
        }
        if($rootScope.displayDetailsTab === 4 || $rootScope.displayDetailsTab === '4')
        {
            $rootScope.$emit('GetDUDeploymentHistory', {});
        }
    };

    $scope.getActiveMachineDetailsTab = function(tab)
    {
        if($rootScope.displayDetailsTab === tab)
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

