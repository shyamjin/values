require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['createAccountControllerApp', 'cloneRequestGridControllerApp','cloneRequestStepsControllerApp']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'jquery', 'createAccountControllerApp', 'cloneRequestGridControllerApp','cloneRequestStepsControllerApp'],function (app) {
  'use strict';

var cloneRoutesApp = angular.module('cloneRoutesApp', ['ui.router', 'createAccountControllerApp', 'cloneRequestGridControllerApp','cloneRequestStepsControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('createclone', {
        url: '/createclone',
        views: {
            "main": {
                templateUrl: 'static/partials/clonerequests/create-clone-request/createclonerequest.partial.html',
                controller: 'CreateAccountController'
            }
        },
        data: {
            pageTitle: 'Create Clone Request'
        }
    }).state('clonerequests', {
        url: '/clonerequests',
        views: {
            "main": {
                templateUrl: 'static/partials/clonerequests/clonerequests.partial.html',
                controller: 'CloneRequestGridController'
            }
        },
        data: {
            pageTitle: 'Clone Requests'
        }
    });
});

});