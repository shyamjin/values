require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var importToolControllerApp = angular.module('importToolControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

importToolControllerApp.controller('ImportToolController', function ($scope, $state, $stateParams, ImportUpdate, $rootScope) {
    var jsonData = {};
    jsonData.ids = [];
    jsonData.ids.push(id);
    jsonData.type = 'importtool';

    $scope.importToolStatus = ImportUpdate.save(jsonData, function(importSuccessResponse){
        $scope.responseMessage = importSuccessResponse;
        $state.go('toolImportUpdateStatus', {'request_id' : jsonData.ids});
        $rootScope.handleResponse(importSuccessResponse);
    },
    function(importErrorResponse)
    {
        $rootScope.handleResponse(importErrorResponse);
    });

});
});