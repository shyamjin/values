require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : []
});

define(['angular'],function (app) {
  'use strict';

var toolDashboardHeaderComponentControllerApp = angular.module('toolDashboardHeaderComponentControllerApp', []);

toolDashboardHeaderComponentControllerApp.controller("ToolDashboardHeaderComponentController",function($scope, $rootScope, $timeout){
    $scope.searchToolWithName = function(keyword)
    {
        if($rootScope.currentState === 'dashboard' || $rootScope.currentState === 'applications')
        {
            $rootScope.$emit("searchToolEvent", {'keyword' : keyword});
        }
        else if($rootScope.currentState === 'viewAllToolSets')
        {
            $rootScope.$emit("searchToolSetEvent", {'keyword' : keyword});
        }
    };
});

});