define(['angular', 'ngResource'], function (app) {
  'use strict';

var flexAttributeServicesApp = angular.module('flexAttributeServicesApp', []);

flexAttributeServicesApp.factory('flexAttributeByEntity', function($resource) {
    return $resource('/flexattributes/view/entity/:entity', {
    entity: '@_entity'
    }
    );
}).factory('flexAttributeViewAll', function($resource) {
    return $resource('/flexattributes/view/all', {
    });
}).factory('createNewFlexAttributes', function($resource) {
    return $resource('/flexattributes/new', {
    });
}).factory('FlexAttributesById', function($resource) {
    return $resource('/flexattributes/view/:id', {
    id:'@_id'
    });
}).factory('editFlxibleAttribute', function($resource) {
    return $resource('/flexattributes/update', {
    },
    {
        update : {
            method : 'PUT'
        }
    });
});
});