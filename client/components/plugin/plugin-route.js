require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['pluginControllersApp']
});

define(['angular', 'ngResource', 'uiRouter', 'pluginControllersApp'],function (app) {
  'use strict';

var pluginRoutesApp = angular.module('pluginRoutesApp', ['ui.router','pluginControllersApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('Plugin', {
        url: '/plugin',
        views: {
            "main": {
                templateUrl: 'static/partials/plugin/plugin.partial.html',
                controller: 'PluginController'
            }
        },
        data: {
            pageTitle: 'Plugin'
        }
    });
});

});