require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var saveExportControllerApp = angular.module('saveExportControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

saveExportControllerApp.controller('SaveExportController', function ($timeout, $scope, $rootScope, $state, $stateParams, $http,SaveExports) {
    SaveExports.get({
    },
    function(successResponse)
    {
        $scope.saveExports = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.selectSaveExports = function(saveExports_id)
    {
        for(var i=0; i<$scope.saveExports.data.length; i++)
        {
            if($scope.saveExports.data[i]._id.$oid === saveExports_id)
            {
                $scope.saveExportsData = $scope.saveExports.data[i];
            }
        }
    };

    $scope.showToolNotExported = function()
    {
        $('#show_tools_not_exported_modal').show(700);
    };

    $scope.hideToolNotExported = function()
    {
        $('#show_tools_not_exported_modal').hide(700);
    };

    $scope.showToolExported = function()
    {
        $('#show_tools_exported_modal').show(700);
    };

    $scope.hideToolExported = function()
    {
        $('#show_tools_exported_modal').hide(700);
    };

});
});