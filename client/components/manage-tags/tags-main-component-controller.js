define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var manageTagsControllerApp = angular.module('manageTagsControllerApp', ['ui.router','tagsServicesApp']);
manageTagsControllerApp.controller('ManageTagsController', function($scope, $location){
    $scope.activeTab = '/manage/tags';
    $scope.showActiveTab = function(tab)
    {
        $scope.activeTab = $location.path().substring(0, $location.path().length);
    };

    $scope.getActiveTab = function(tab)
    {
        $scope.activeTab = $location.path().substring(0, $location.path().length);
        if($scope.activeTab===tab)
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