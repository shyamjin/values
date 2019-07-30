define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'toolTips'],function (app) {
  'use strict';

var prerequisitesServicesApp = angular.module('prerequisitesServicesApp', []);

prerequisitesServicesApp.factory('PrerequisitesViewAll', function ($resource) {
    return $resource('/prerequisites/view', {
    },
    {
    });
}).factory('PrerequisiteView', function($resource,$rootScope) {
    return $resource('/prerequisites/view/:id', {
        id:'@_id'
    }, {
      });
}).factory('PrerequisiteCreate', function($resource,$rootScope) {
    return $resource('/prerequisites/add', {
    }, {
      });
}).factory('PrerequisiteEdit', function($resource,$rootScope) {
    return $resource('/prerequisites/update', {
    },
    {
        update : {
            method : 'PUT'
        }
    });
}).factory('PrerequisiteDelete', function ($resource) {
    return $resource('/prerequisites/delete/:id', {
        id : '@_id'
    }, {
            remove :{
                    method : 'DELETE'
            }
    });
});

});