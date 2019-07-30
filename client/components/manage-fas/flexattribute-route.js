require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageFlexAttributesControllerApp',
    'editFlexAttributesControllerApp',
    'addNewFlexAttributesControllerApp']
});

define(['angular', 'ngResource', 'uiRouter', 'manageFlexAttributesControllerApp',
    'editFlexAttributesControllerApp',
    'addNewFlexAttributesControllerApp'],function (app) {
  'use strict';

var flaxAttributeRoutesApp = angular.module('flaxAttributeRoutesApp', ['ui.router','manageFlexAttributesControllerApp',
    'editFlexAttributesControllerApp',
    'addNewFlexAttributesControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('manageflexattribute', {
        url: '/manage/flexibleattributes',
        views: {
            "main": {
                templateUrl: 'static/components/manage-fas/manage-fas.partial.html',
                controller: 'ManageFlexAttributesController'
            }
        },
        data: {
            pageTitle: 'Manage FA'
        }
    }).state('createFA', {
        url: '/new/flexibleattributes',
        views: {
            "main": {
                templateUrl: 'static/components/manage-fas/add-new-fa/addnewfascontent.component.html',
                controller: 'AddNewFlexAttributesController'
            }
        },
        data: {
            pageTitle: 'Manage FA'
        }
    });
});

});