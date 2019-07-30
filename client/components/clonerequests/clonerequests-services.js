define(['angular', 'ngResource'],function (app) {
  'use strict';

var cloneServicesApp = angular.module('cloneServicesApp', []);

cloneServicesApp.factory('Account', function($resource) {
    return $resource('/account/new', {
    }, {

      });
    }).factory('AccountDelete', function($resource,$location) {
        return $resource('/account/delete/:id', {
            id : '@_id'
        }, {
                remove :{
                        method : 'DELETE'
                }
          });
    }).factory('CloneRequest', function($resource) {
        return $resource('/clonerequest/add', {
        }, {

          });
    }).factory('CloneRequestStatus', function($resource,$rootScope) {
        return $resource('/clonerequest/view/:id', {
        id:'@_id'
        }, {
         query : {
                    method: 'GET',
                    isArray: true,
                    transformResponse : function(response, headers) {
                        var jsonData = JSON.parse(response);
                        return jsonData;
                      }
                  }
          });
    }).factory('CloneRequestStatusAll', function($resource,$rootScope) {
        return $resource('/clonerequest/all', {
        }, {
         query : {
                    method: 'GET',
                    isArray: true,
                    transformResponse : function(response, headers) {

                       console.log('Clone Response in json format');
                        var jsonData = JSON.parse(response);
                            console.log(jsonData);
                            return jsonData;
                      }
                  }
          });
    }).factory('RetryCloneRequest', function($resource,$rootScope) {
    return $resource('/clonerequest/retry', {
     }, {
        update : {
                  method: 'PUT'
                  }
         });
    });

    cloneServicesApp.directive('validAccount', function() {
      return {
        require: '?ngModel',
        link: function(scope, element, attrs, ngModelCtrl) {
          if(!ngModelCtrl) {
            return;
          }
          element.bind('keypress', function(event) {
            if(event.keyCode === 32) {
              event.preventDefault();
            }
          });
        }
      };
    });

});