require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var updateToolControllerApp = angular.module('updateToolControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

updateToolControllerApp.controller('UpdateToolController', function ($scope, $state, $stateParams, ImportUpdate, $rootScope) {
    var jsonData = {};
    jsonData.ids = [];
    jsonData.ids.push(id);
    jsonData.type = 'updatetool';

    ImportUpdate.save(jsonData, function(updateToolSuccessResponse){
        $scope.responseMessage = updateToolSuccessResponse;
        $state.go('toolImportUpdateStatus', {'request_id' : jsonData.ids});
        $rootScope.handleResponse(updateToolSuccessResponse);
    },
    function(updateToolErrorResponse)
    {
        $rootScope.handleResponse(updateToolErrorResponse);
    });
});
});