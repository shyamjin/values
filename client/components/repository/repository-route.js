require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['repositoryPartialControllerApp']
});

define(['angular', 'ngResource', 'uiRouter','repositoryPartialControllerApp'],function (app) {
  'use strict';

var repositoryRoutesApp = angular.module('repositoryRoutesApp', ['ui.router','repositoryPartialControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('viewRepository', {
        url: '/view/repository',
        views: {
            "main": {
                templateUrl: 'static/partials/repository/repository.partial.html',
                controller: 'ManageRepositoryController'
            }
        },
        data: {
            pageTitle: 'View Repository'
        }
    }).state('newRepository', {
        url: '/new/repository',
        views: {
            "main": {
                templateUrl: 'static/components/repository/add-new-repository/addnewrepositorycontent.component.html',
                controller: 'AddNewRepositoryController'
            }
        },
        data: {
            pageTitle: 'View Repository'
        }
    });
});

});