define(['angular', 'ngResource'], function (app) {
  'use strict';

var repositoryServicesApp = angular.module('repositoryServicesApp', []);

repositoryServicesApp.factory('repositoryViewAll', function($resource) {
    return $resource('/repository/view/all', {
    });
}).factory('repositoryViewById', function($resource) {
    return $resource('/repository/view/:id', {
    id: '@_id'
    },{

    });
}).factory('updateRepository', function($resource) {
    return $resource('/repository/update', {
     },{
           update : {
            method : 'PUT'
        }
    });
}).factory('createNewRepository', function($resource) {
    return $resource('/repository/add', {
     },{

    });
});
});