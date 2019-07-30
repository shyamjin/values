define(['angular', 'ngResource'],function (app) {
  'use strict';

var deploymentPluginServicesApp = angular.module('deploymentPluginServicesApp', []);

deploymentPluginServicesApp.factory('GetAllDeploymentPlugins', function ($resource, $rootScope) {
    return $resource('/plugin/file/list/:value', {
    },
    {

    });
}).factory('RemoveDeploymentPlugin', function ($resource, $rootScope) {
    return $resource('/plugin/file/remove/:name', {
        name: '@_name'
    },
    {

    });
}).factory('ReadDeploymentPlugin', function ($resource, $rootScope) {
    return $resource('/plugin/file/read/:path', {
        path: '@_path'
    },
    {

    });
}).factory('ExitPoint', function($resource) {
    return $resource('/plugin/exitpoint/new', {
    },
    {

    });
}).factory('GetPluginData', function($resource) {
    return $resource('/plugin/file/view/:id', {
        id: '@_id'
    },
    {

    });
}).factory('ExitPointUpdate', function($resource) {
    return $resource('/plugin/exitpoint/update', {
    },
    {
        update : {
            method : 'PUT'
        }
    });
});

deploymentPluginServicesApp.service('UploadDeploymentPlugin', ['$http','$rootScope', function ($http, $rootScope) {
    this.uploadDeploymentPlugin = function (file, uploadDeploymentPluginUrl) {
          var fd = new FormData();
          fd.append('file', file);
          $http.post(uploadDeploymentPluginUrl, fd, {
          transformRequest: angular.identity,
          headers: {'Content-Type': undefined}
       })

       .success(function(successResponse){
            $rootScope.preLoader = false;
            $rootScope.resultPane = true;
            $rootScope.response = {
                "message" : successResponse.message,
                 "status" : 200,
                 "result" : successResponse.result
            };
            $rootScope.handleResponse($rootScope.response);
            return $rootScope.response;
       })

       .error(function(errorResponse){
            $rootScope.preLoader = false;
            $rootScope.resultPane = true;
            $rootScope.response = {
                "message" : errorResponse.message,
                 "status" : 404,
                 "result" : "failed"
            };
            $rootScope.handleResponse($rootScope.response);
            return $rootScope.response;
       });
    };
}]);

});