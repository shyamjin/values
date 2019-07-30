define(['angular', 'ngResource'],function (app) {
  'use strict';

var monitoringServicesApp = angular.module('monitoringServicesApp', []);

monitoringServicesApp.factory('GetAllReports', function($resource, $http,$rootScope){
    return $resource('/reports/all',{
        id:'@_id'
    },
    {
    });
  });
});