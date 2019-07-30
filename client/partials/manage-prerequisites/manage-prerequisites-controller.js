define(['angular', 'prerequisitesRoutesApp', 'prerequisitesServicesApp'],function (app) {
  'use strict';

var managePrerequisitesControllerApp = angular.module('managePrerequisitesControllerApp', ['ui.router', '720kb.tooltips', 'prerequisitesRoutesApp', 'prerequisitesServicesApp']);

managePrerequisitesControllerApp.controller('ManagePrerequisitesController', function ($scope, $stateParams, $location) {
    $scope.displayTab = '/manage/prerequisites';
    $scope.showActiveTab = function(tab)
    {
        $scope.displayTab = $location.path().substring(0, $location.path().length);
    };

    $scope.getActiveTab = function(tab)
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