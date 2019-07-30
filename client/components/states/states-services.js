define(['angular', 'ngResource'],function (app) {
  'use strict';

var statesServicesApp = angular.module('statesServicesApp', []);

statesServicesApp.factory('createState', function ($resource, $rootScope) {
    return $resource('/state/add', {

        }, {

            });
    }).factory('GetAllDuState', function($resource, $http,$rootScope){
    return $resource('/state/all',{
    },
        {
        get : {
            method: 'GET',
            isArray:false,
            transformResponse : function(fulldata, headers) {
                var jsonData = JSON.parse(fulldata);
                return jsonData.data;
            }
        }
    });
    }).factory('DUStateViewById', function($resource) {
    return $resource('/state/view/:id', {
        id : '@_id'
    },
    {
    });
    }).factory('editDuState', function ($resource) {
    return $resource('/state/update', {
    },
    {
        update : {
            method : 'PUT'
        }
    });
    }).factory('StateDelete', function($resource, $http,$rootScope){
        return $resource('/state/delete/:id',{
            id:'@_id'
        },
        {
            remove : {
                    method : 'DELETE'
            }
        });
    });
});