define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var deleteUserGroupControllerApp = angular.module('deleteUserGroupControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
deleteUserGroupControllerApp.controller('DeleteUserGroupController', function ($scope, $stateParams,$rootScope, $window, $state,UserGroupDelete) {
     $scope.deletedUserStatus = UserGroupDelete.remove({
          id :   $stateParams.id
     }, function (groupDeleteRequest){
        $state.go('manageUserGroups');
        $rootScope.handleResponse(groupDeleteRequest);
     },
     function (groupDeleteResponseError){
        $rootScope.handleResponse(groupDeleteResponseError);
     });
 });
});
