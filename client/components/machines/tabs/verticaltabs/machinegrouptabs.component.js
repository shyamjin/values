define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';
var machineGroupsDetailsTabsControllerApp = angular.module('machineGroupsDetailsTabsControllerApp', ['ui.router']);
machineGroupsDetailsTabsControllerApp.controller('MachineGroupsDetailsTabController', function ($scope, $rootScope) {
    $rootScope.machineGroupDisplayDetailsTab = 0;
    $scope.showActiveMachineGroupsDetailsTab = function(tab)
    {
        $rootScope.machineGroupDisplayDetailsTab = tab;
    };

    $scope.getActiveMachineGroupsDetailsTab = function(tab)
    {
        if($rootScope.machineGroupDisplayDetailsTab === tab)
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