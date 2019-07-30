define(['angular','deploymentPartialControllerApp'],function (app) {
  'use strict';

var deploymentVerticalTabsControllerApp = angular.module('deploymentVerticalTabsControllerApp', ['deploymentPartialControllerApp']);

deploymentVerticalTabsControllerApp.controller('DeploymentVerticalTabsController', function ($scope,  $rootScope) {

    $rootScope.$on("setGroupData", function (event, args) {
        $scope.GroupData = args;
    });

    $rootScope.$on("setVerticalTabIndex", function (event, args) {
        $scope.selectedIndex  = args;
    });

    $scope.selectDeployment = function (index)
    {
       $rootScope.$emit('setIndexOfFirstTab',index);
    };

 });

});