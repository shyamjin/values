define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'toolTips'],function (app) {
  'use strict';

    var deleteMachineGroupControllerApp = angular.module('deleteMachineGroupControllerApp', ['ui.router', '720kb.tooltips']);

    deleteMachineGroupControllerApp.controller('DeleteMachineGroupController', function ($scope, $stateParams, $window, $state,MachineGroupDelete) {
     $scope.deletedUserStatus = MachineGroupDelete.remove({
          id :   $stateParams.id
     },
     function (groupDeleteRequest){
        $state.go('manageMachineGroups');
        $rootScope.handleResponse(groupDeleteRequest);
     },
     function (groupDeleteResponseError){
        $rootScope.handleResponse(groupDeleteResponseError);
     });

});
});