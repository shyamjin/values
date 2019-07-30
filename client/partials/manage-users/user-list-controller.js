define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

  var userListControllerApp = angular.module('userListControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
  userListControllerApp.controller('UserListController', function($scope,$rootScope,$stateParams,$http,$state,$timeout, popupService,$window, Users, Role,GetAccount,UserUpdate,PasswordUpdate,UserGroup){

   $scope.getRole = function(role, href)
   {
        var ref = document.getElementById(href); //or grab it by tagname etc

        if($rootScope.userProfile.userData.rolename==='SuperAdmin' || role===$rootScope.userProfile.userData.rolename)
        {
            return '';
        }
        else if($rootScope.userProfile.userData.rolename==='Admin' && role==='SuperAdmin')
        {
            document.getElementById(href).removeAttribute("href");
            return 'disabled';
        }
        else if(($rootScope.userProfile.userData.rolename==='Admin' && role==='Operator') || ($rootScope.userProfile.userData.rolename==='Admin' && role==='Guest'))
        {
            return '';
        }
        else
        {
            document.getElementById(href).removeAttribute("href");
            return 'disabled';
        }
    };

    $scope.users = Users.get({
        id:"all"
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

});
});
