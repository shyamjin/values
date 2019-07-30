define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';
var stateTabsComponent = angular.module('stateTabsComponent', ['ui.router']);
stateTabsComponent.controller('ManageStatesTabsController', function ($scope, $state, $location, $rootScope) {
    $scope.displayTab = '/view/du/state';
    $scope.showActiveTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
    };

    $scope.getActiveTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
        if($location.path().indexOf('editmachine')>=0)
        {
            $scope.displayTab = '/view/du/state';
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

