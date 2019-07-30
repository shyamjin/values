/*
Author - nlate
Description -
    Controller that fetches the ;list of deployment plugins and shows it on the page
Methods -
    1. openDeletePluginConfirmationPopup(id) - Opens a plugin delete confirmation popup
    2. deletePlugin(id) - deletes plugin
    3. closeDeletePluginConfirmationPopup() - Closes the Delete Plugin Confirmation Popup and cancels the delete operation
Uses -
    1. Manage Deployment Plugins - components/deployment-plugins/plugin-list-search/pluginlistsearch.component.html
*/

require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['deploymentPluginServicesApp']
});

define(['angular', 'uiRouter', 'deploymentPluginServicesApp'],function (app) {
  'use strict';

var pluginListSearchComponentApp = angular.module('pluginListSearchComponentApp', ['ui.router', 'deploymentPluginServicesApp']);

pluginListSearchComponentApp.controller("PluginListSearchController",function($scope, $rootScope, $state, $stateParams, $window, GetAllDeploymentPlugins, RemoveDeploymentPlugin, ReadDeploymentPlugin, GetPluginData){
    $rootScope.showResultPane = false;
    GetAllDeploymentPlugins.get({
        value:"all"
    },
    function(successResponse)
    {
        $scope.allDeploymentPlugins = successResponse.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });


    $scope.openDeletePluginConfirmationPopup = function(plugin_name)
    {
        // code for open delete plugin confirmation popup goes here
        $scope.plugin_name = plugin_name;
        $('#show_delete_plugin_confirmation_popup').show(700);
    };

    $scope.closeDeletePluginConfirmationPopup = function(plugin_id)
    {
        // code for close delete plugin confirmation popup and cancel delete operation goes here
        $('#show_delete_plugin_confirmation_popup').hide(700);
    };

    $scope.deletePlugin = function()
    {
        // code for open delete plugin goes here
        RemoveDeploymentPlugin.remove({
            name : $scope.plugin_name
        },
        function(successResponse)
        {
            $('#show_delete_plugin_confirmation_popup').hide(700);
            $rootScope.handleResponse(successResponse);
            $state.go('manageDeploymentPlugin');
            delete $scope.plugin_name;
            delete $scope.allDeploymentPlugins;
            GetAllDeploymentPlugins.get({
                value:"all"
            },
            function(successResponse)
            {
                $scope.allDeploymentPlugins = successResponse.data;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        },
        function(errorResponse)
        {
            $('#show_delete_plugin_confirmation_popup').hide(700);
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.viewPlugin = function(plugin_id)
    {
        GetPluginData.get({
            id: plugin_id
        },
        function(pluginDataSuccessResponse){
            $rootScope.pluginData = pluginDataSuccessResponse.data;
        },
        function(pluginDataErrorResponse){
            $rootScope.handleResponse(pluginDataErrorResponse);
        });

        $('#show_plugin_data_popup').show(700);
    };

    $scope.closePluginDetailsModal = function()
    {
        $('#show_plugin_data_popup').hide(700);
        delete $rootScope.pluginData;
    };

    $scope.setInitClass = function(line)
    {
        if(line.substring(0, 6).includes('class') || line.substring(0, 7).includes('def'))
        {
            return 'text--semibold';
        }
        else
        {
            return 'text--regular';
        }
    };

    $scope.selectPlugin = function(plugin_id)
    {
        $rootScope.$emit('newPluginData', {});
        $rootScope.resultPane = false;
        delete $rootScope.response;
        $rootScope.pluginOperation = 'update';
        $rootScope.showResultPane = true;
        GetPluginData.get({
            id: plugin_id
        },
        function(pluginDataSuccessResponse){
            $rootScope.pluginData = {
                _id : {
                    oid : ''
                },
                repo_provider : '',
                type : '',
                additional_parameters : [],
                plugin_name : ''
            };
            $rootScope.pluginData.plugin_name = pluginDataSuccessResponse.data.plugin_name;
            $rootScope.pluginData.type = pluginDataSuccessResponse.data.type;
            $rootScope.pluginData._id.oid = pluginDataSuccessResponse.data._id;
            if(pluginDataSuccessResponse.data.repo_provider)
            {
                $rootScope.pluginData.repo_provider = pluginDataSuccessResponse.data.repo_provider;
            }

            for (var key in pluginDataSuccessResponse.data)
            {
                if (key !== 'plugin_name' && key !== 'repo_provider' && key !== 'type' && key !== 'additional_parameters' && key !== '_id' && key !== 'file_contents')
                {
                    var val = pluginDataSuccessResponse.data[key];
                    $rootScope.pluginData.additional_parameters.push({"key" : key, "value" : val});
                }
            }
        },
        function(pluginDataErrorResponse){
            $rootScope.handleResponse(pluginDataErrorResponse);
        });
    };

    $scope.downloadPlugin = function(file_path)
    {
        window.open(file_path,'_blank');
    };

});

});