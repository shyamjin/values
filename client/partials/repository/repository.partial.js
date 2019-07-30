/*
Author - shyamjin
Description -
    1. Controller that handles with the common operations required in repository view
Methods -

Uses -
    1. repository - partials/repository/repository.partial.html
*/


define(['angular','EditRepositoryControllerApp','AddNewRepositoryControllerApp'],function (app) {
  'use strict';

var repositoryPartialControllerApp = angular.module('repositoryPartialControllerApp', ['EditRepositoryControllerApp','AddNewRepositoryControllerApp']);

repositoryPartialControllerApp.controller('ManageRepositoryController', function ($scope, $location, $rootScope) {
    $scope.displayTab = '/view/repository';
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