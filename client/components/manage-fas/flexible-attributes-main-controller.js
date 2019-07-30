define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var manageFlexAttributesControllerApp = angular.module('manageFlexAttributesControllerApp', ['ui.router']);

manageFlexAttributesControllerApp.controller('ManageFlexAttributesController', function($scope, $state, $stateParams,$location, $rootScope){
    $scope.displayTab = '/manage/flexibleattributes';
    $scope.showActiveTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
    };

    $scope.getActiveTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
        if($scope.displayTab===tab)
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