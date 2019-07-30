require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['auditPartialControllerApp']
});

define(['angular', 'ngResource', 'uiRouter','auditPartialControllerApp'],function (app) {
  'use strict';

var auditingRoutesApp = angular.module('auditingRoutesApp', ['ui.router','auditPartialControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('viewauditings', {
        url: '/view/audits',
        views: {
            "main": {
                templateUrl: 'static/partials/audits/audits.partial.html',
                controller: 'auditPartialController'
            }
        },
        data: {
            pageTitle: 'View Audits'
        }
    });
});

});