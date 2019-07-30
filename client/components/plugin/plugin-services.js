define(['angular', 'ngResource'],function (app) {
  'use strict';

var pluginServicesApp = angular.module('pluginServicesApp', []);

pluginServicesApp.factory('PluginView', function ($resource, $rootScope) {
        return $resource('/plugin/all', {
        },
        {

        });
    }).factory('PluginViewById', function ($resource, $rootScope) {
        return $resource('/plugin/view/:id', {
            id: '@_id'
        },
        {

        });
    }).factory('PluginActive', function ($resource, $rootScope) {
        return $resource('/plugin/active/:Name', {
        },
        {

        });
    }).factory('PluginInActive', function ($resource, $rootScope) {
        return $resource('/plugin/inactive/:Name', {
        },
        {

        });
    }).factory('PluginInstall', function ($resource, $rootScope) {
        return $resource('/plugin/install/:Name', {
        },
        {

        });
    }).factory('PluginUnInstall', function ($resource, $rootScope) {
        return $resource('/plugin/uninstall/:Name', {
        },
        {

        });
    }).factory('PluginReload', function ($resource, $rootScope) {
        return $resource('/plugin/reload', {
        },
        {

        });
    });
});