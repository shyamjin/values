define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var manageUsersControllerApp = angular.module('manageUsersControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
manageUsersControllerApp.controller('ManageUsersController', function ($scope, $state, $rootScope, $location, $stateParams) {
    $scope.displayTab = "/users";
    $scope.displayOtherTab = '';

    $scope.showActiveUserTab = function(tab)
    {
        $rootScope.importResult = '';
        $rootScope.resultPane = false;
        $rootScope.preLoader = false;

        $scope.displayTab = $location.path().substring(0, $location.path().length);
        $scope.displayOtherTab = '';
    };

    $scope.getActiveUserTab = function(tab)
    {
        $scope.displayOtherTab = '';
        $scope.displayTab = $location.path().substring(0, $location.path().length);
        if($location.path().indexOf('edit/user/group')>=0)
        {
            $scope.displayTab = '/manage/users/groups';
            $scope.displayOtherTab = '/edit/user/group';
        }
        else if($location.path().indexOf('create/user/group')>=0)
        {
            $scope.displayTab = '/manage/users/groups';
            $scope.displayOtherTab = '/create/user/group';
        }
        if(tab === $scope.displayTab)
        {
            return 'vp-tabs__tab vp-tabs__tab--active pointer pr--sm pl--sm left';
        }
        else
        {
            return 'vp-tabs__tab pointer pr--sm pl--sm left';
        }
    };
});
});
