define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

  var deleteRoleControllerApp = angular.module('deleteRoleControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
  deleteRoleControllerApp.controller('DeleteRoleController', function ($scope, $stateParams, $rootScope, $state, RoleDelete) {
     var id = $stateParams.id ;
     var roleData = {};
     roleData._id = {
        oid : ""
     };
     roleData._id.oid = id;
     RoleDelete.remove(roleData,function(response){
        $rootScope.handleResponse(response);
     },
     function(errorResponse) {
        $rootScope.handleResponse(errorResponse);
     });
 });
});
