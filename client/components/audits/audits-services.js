define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var auditServicesApp = angular.module('auditServicesApp', []);

auditServicesApp.factory('auditsViewAll', function ($resource) {
    return $resource('/auditing/view/all', {
    },
    {
    });
}).factory('auditsViewById', function($resource) {
    return $resource('/auditing/view/id/:id', {
        id : '@_id'
    },
    {
    });
});

});