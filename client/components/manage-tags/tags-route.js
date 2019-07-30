require.config({
    baseUrl: "",
    waitSeconds: 0
});

define(['angular', 'ngResource', 'uiRouter', 'editTagControllerApp',
    'manageTagsControllerApp',
    'createNewTagControllerApp'],function (app) {
  'use strict';

var tagsRoutesApp = angular.module('tagsRoutesApp', ['ui.router','editTagControllerApp',
    'manageTagsControllerApp',
    'createNewTagControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('manageTags', {
        url: '/manage/tags',
        views: {
            "main": {
                templateUrl: 'static/partials/manage-tags/manage-tags.partial.html',
                controller: 'ManageTagsController'
            }
        },
        data: {
            pageTitle: 'Manage Tags'
        }
    }).state('editTags', {
        url: '/tag/update',
        views: {
            "main": {
                templateUrl: 'static/partials/manage-tags/manage-tags.partial.html',
                controller: 'EditTagController'
            }
        },
        data: {
            pageTitle: 'Manage Tags'
        }
    }).state('createTag', {
        url: '/tag/new',
        views: {
            "main": {
                templateUrl: 'static/partials/manage-tags/manage-tags.partial.html',
                controller: 'CreateNewTagController'
            }
        },
        data: {
            pageTitle: 'Manage Tags'
        }
    });
});

});