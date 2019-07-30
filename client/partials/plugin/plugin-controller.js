require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['pluginServicesApp']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'pluginServicesApp'],function (app) {
  'use strict';

var pluginControllersApp = angular.module('pluginControllersApp', ['ui.router','pluginServicesApp']);

pluginControllersApp.controller('PluginController', function($timeout, $scope, $rootScope, $state, $stateParams, $http,PluginView,PluginViewById,PluginActive,PluginInActive,PluginInstall,PluginUnInstall,PluginReload){
    PluginView.get({
    },
    function(successResponse)
    {
        $scope.plugin = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });



    $scope.selectPlugin = function (plugin_id)
    {
        $scope.pluginID = plugin_id;
        $scope.PluginData= PluginViewById.get({
            id:plugin_id
        },
        function(successResponse)
        {

            $scope.PluginData = successResponse.data;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.active = function (name)
    {
        var Name = name;
        PluginActive.get({
            Name: name
        },
        function(successResponse)
        {
            $rootScope.handleResponse(successResponse);
            delete $scope.plugin;
            $scope.selectPlugin($scope.pluginID);
            PluginView.get({
            },
            function(successResponse)
            {
                $scope.plugin = successResponse;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.inactive = function (name)
    {
        var Name = name;
        PluginInActive.get({
            Name: name
        },
        function(successResponse)
        {
            $rootScope.handleResponse(successResponse);
            delete $scope.plugin;
            $scope.selectPlugin($scope.pluginID);
            PluginView.get({
            },
            function(successResponse)
            {
                $scope.plugin = successResponse;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.install = function (name)
    {
        var Name = name;
        PluginInstall.get({
            Name: name
        },
        function(successResponse)
        {
            $rootScope.handleResponse(successResponse);
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.uninstall = function (name)
    {
        var Name = name;
        PluginUnInstall.get({
            Name: name
        },
        function(successResponse)
        {
            $rootScope.handleResponse(successResponse);
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.reload = function ()
    {
        PluginReload.get({
        },
        function(successResponse)
        {
            $rootScope.handleResponse(successResponse);
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };
});
});