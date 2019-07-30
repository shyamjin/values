/*
Author - nlate
Description -
    1. Controller that handles with the common operations required in create tool
Methods -
    1. showActiveTab(tab) - Sets the specified tab as an active tab
Uses -
    1. Create Tool - partials/tools/create-tools//create-tools.partial.html
*/

define(['angular', 'createToolInfoComponentControllerApp', 'createToolBarComponentControllerApp', 'createToolVerticalTabComponentControllerApp', 'createToolVersionComponentControllerApp'],function (app) {
  'use strict';

var createToolsPartialControllerApp = angular.module('createToolsPartialControllerApp', ['ui.router', 'createToolInfoComponentControllerApp', 'createToolBarComponentControllerApp', 'createToolVerticalTabComponentControllerApp', 'createToolVersionComponentControllerApp']);

createToolsPartialControllerApp.controller("CreateToolPartialController",function($scope, $stateParams, GetAllTools, $window, $state, CreateTool, toolFileUpload, $timeout, $rootScope, PrerequisitesViewAll, TagsAll, GetAllDeploymentPlugins) {
    $scope.application = {
        data : {
            name : '',
            tag : [],
            description : '',
            support_details : '',
            is_tool_cloneable : 'false',
            artifacts_only : 'false',
            all_versions : [{
                version_number : null,
                version_name : '',
                version_date : null,
                pre_requiests : [],
                gitlab_repo : '',
                gitlab_branch : '',
                jenkins_job : '',
                backward_compatible : 'no',
                mps_certified : [],
                release_notes : '',
                document : {
                    documents : []
                },
                deployment_field : {
                    fields : []
                },
                deployer_to_use : 'DefaultDeploymentPlugin'
            }]
        }
    };
});

});