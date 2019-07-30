require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['runningServicesControllerApp', 'viewReportsControllerApp']
});

define(['angular', 'ngResource', 'uiRouter', 'runningServicesControllerApp', 'viewReportsControllerApp'],function (app) {
  'use strict';

var monitoringRoutesApp = angular.module('monitoringRoutesApp', ['ui.router', 'runningServicesControllerApp', 'viewReportsControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('runningservices', {
        url: '/view/monitoring/runningservices',
        views: {
            "main": {
                templateUrl: 'static/partials/monitoring/runningservices.partial.html',
                controller: 'RunningServicesController'
            }
        },
        data: {
            pageTitle: 'Running Services'
        }
    }).state('viewreports', {
        url: '/view/reports',
        views: {
            "main": {
                templateUrl: 'static/partials/reports/reports.partial.html',
                controller: 'ViewReportsController'
            }
        },
        data: {
            pageTitle: 'View Reports'
        }
    });
});

});