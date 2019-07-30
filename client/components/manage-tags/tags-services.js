define(['angular', 'ngResource'],function (app) {
  'use strict';

var tagsServicesApp = angular.module('tagsServicesApp', []);

tagsServicesApp.factory('TagsAll', function($resource) {
    return $resource('/tag/all', {
    },
    {
        get : {
            method: 'GET',
            isArray: true,
            transformResponse : function(fulldata, headers) {
                var jsonData = JSON.parse(fulldata);
                return jsonData.data;
            }
        }
    });
}).factory('CreateTag', function ($resource) {
    return $resource('/tag/new', {
    }, {

    });
}).factory('ViewTag', function($resource) {
    return $resource('/tag/view/:id', {
        id : '@_id'
    },
    {
    });
}).factory('EditTag', function ($resource) {
    return $resource('/tag/update', {
    },
    {
        update : {
            method : 'PUT'
        }
    });
}).factory('DeleteTag', function($resource, $http,$rootScope){
    return $resource('/tag/delete/:id',{
        id:'@_id'
    },
    {
        remove : {
                method : 'DELETE'
        }
    });
});

});