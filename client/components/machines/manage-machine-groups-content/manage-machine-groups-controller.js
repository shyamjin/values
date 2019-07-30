define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'toolTips'],function (app) {
  'use strict';

    var manageMachineGroupsControllerApp = angular.module('manageMachineGroupsControllerApp', ['ui.router', '720kb.tooltips']);

    manageMachineGroupsControllerApp.controller('ManageMachineGroupsController', function ($scope, $stateParams, $window, $state, $timeout, $rootScope, MachineGroup) {
       MachineGroup.get({
       },
       function(successResponse){
            $scope.MachineGroups = successResponse.data.data;
       },
       function(errorResponse)
       {
            $rootScope.handleResponse(errorResponse);
       });
});
});