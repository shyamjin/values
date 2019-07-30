define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

  var deleteUserControllerApp = angular.module('deleteUserControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
  deleteUserControllerApp.controller('DeleteUserController', function ($scope,$rootScope, $stateParams, Machine, $window, $state,UserDelete) {
     $scope.deletedUserStatus = "User is deleted";
     $scope.accountDeletion = UserDelete.remove({
          id : $stateParams.id
     },
     function(userDeleteRequest)
     {
        $rootScope.handleResponse(userDeleteRequest);
     },
     function(userDeleteResponseError)
     {
        $rootScope.handleResponse(userDeleteResponseError);
     });

 });
});
