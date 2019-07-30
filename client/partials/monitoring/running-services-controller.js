require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['monitoringServicesApp']
});

define(['angular', 'ngResource', 'uiRouter', 'monitoringServicesApp','settingsServicesApp'],function (app) {
  'use strict';

var runningServicesControllerApp = angular.module('runningServicesControllerApp', ['ui.router', 'monitoringServicesApp','settingsServicesApp']);

runningServicesControllerApp.controller('RunningServicesController', function($timeout, $interval, $scope, $rootScope, $state, $stateParams, $http, Settings){
    var promise;
    var interval;
    $scope.runningServicesInd = false;
    function getAllRunningServices()
    {
        Settings.get({
            id : 'all'
        },
        function(successResponse)
        {
            $scope.runningServices = successResponse;
            $scope.runningServicesCount = 0;
            for(var i=0; i<$scope.runningServices.data.length; i++)
            {
               if($scope.runningServices.data[i].run_status === 'Running')
               {
                $scope.runningServicesInd = true;
                $scope.runningServicesCount++;
                var obj ={};
                var currentTime = new Date($scope.runningServices.data[i].utc_current_time);
                var startTime = new Date($scope.runningServices.data[i].utc_start_time);
                var timeDifference = Math.abs(currentTime - startTime);
                var hours = Math.floor(timeDifference / (60 * 60));
                var divisor_for_minutes = timeDifference % (60 * 60);
                var minutes = Math.floor(divisor_for_minutes / 60);
                var divisor_for_seconds = divisor_for_minutes % 60;
                var seconds = Math.ceil(divisor_for_seconds);
                if (hours < 10)   { hours    = "0" + hours; }
                if (minutes < 10) { minutes = "0" + minutes; }
                if (seconds < 10)  { seconds  = "0" + seconds; }
                if (hours)            { hours   = "00"; }
                obj = {
                    "hh": hours,
                    "mm": minutes,
                    "ss": seconds
                };
                $scope.runningServices.data[i].runningservices_run_time = obj;
               }
            }
            },
            function(errorResponse)
            {
                $interval.cancel(interval);
                interval = undefined;
                $rootScope.handleResponse(errorResponse);
            });
    }
     interval = $interval(getAllRunningServices,5000);
     $scope.$on('$stateChangeStart', function (event, toState, toParams, fromState, fromParams) {
     $interval.cancel(interval);
     interval = undefined;
    });

});
});