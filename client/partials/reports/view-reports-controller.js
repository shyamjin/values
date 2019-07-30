require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['monitoringServicesApp']
});

define(['angular', 'ngResource', 'uiRouter', 'monitoringServicesApp','settingsServicesApp'],function (app) {
  'use strict';

var viewReportsControllerApp = angular.module('viewReportsControllerApp', ['ui.router', 'monitoringServicesApp','settingsServicesApp']);

viewReportsControllerApp.controller('ViewReportsController', function($timeout, $interval, $scope, $rootScope,$window, $state, $stateParams, $http,Settings ,GetAllReports){
    GetAllReports.get({
    },
    function(getReportsSuccessResponse)
    {
        $rootScope.reportURL = [];
        $rootScope.reportsData = getReportsSuccessResponse.data;
        for(var t1=0; t1<getReportsSuccessResponse.data.length; t1++)
        {
            $rootScope.reportURL.push({'name' : getReportsSuccessResponse.data[t1].name, 'url' : getReportsSuccessResponse.data[t1].url});
        }
    },
    function(getReportsErrorResponse)
    {
        $rootScope.handleResponse(getReportsErrorResponse);
    });

    $scope.redirectToSlamDataReports = function(link)
    {
      $window.open(link, '_blank');
    };

});
});