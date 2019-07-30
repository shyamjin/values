/* Created By - Nilesh Late -  Directive and Service created for import file */

define(['angular', 'ngResource'],function (app) {
  'use strict';

var settingsServicesApp = angular.module('settingsServicesApp', []);

    settingsServicesApp.directive('importModel', ['$parse', function ($parse) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                var model = $parse(attrs.importModel);
                var modelSetter = model.assign;
                element.bind('change', function (evt) {
                    scope.$apply(function () {
                    var files = evt.target.files;
                    scope.importFileSelected = files[0].name;
                        modelSetter(scope, element[0].files[0]);
                    });
                });
            }
        };
    }]);

    settingsServicesApp.directive('accountlogoModel', ['$parse','$rootScope', function ($parse,$rootScope ) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                var model = $parse(attrs.accountlogoModel);
                var modelSetter = model.assign;
                element.bind('change', function (evt) {
                    scope.$apply(function () {
                    var files = evt.target.files;
                    if(files[0].type==='image/jpeg' || files[0].type==='image/png' || files[0].type==='image/jpg' || files[0].type==='image/bmp' || files[0].type==='image/gif')
                    {
                        scope.accountLogoSelected = files[0];
                        scope.personalizeFileSelected = files[0].name;
                        modelSetter(scope, element[0].files[0]);
                    }
                    else
                    {
                        $rootScope.handleResponse('Invalid file format... Please select either jpeg / png /jpg / bmp or gif');
                        return false;
                    }
                    });
                });
            }
        };
    }]);

    settingsServicesApp.service('logoFileUpload', ['$http','$rootScope', function ($http, $rootScope) {
        this.uploadAccountFileToUrl = function (file, uploadUrl) {
            var fd = new FormData();
            fd.append('file', file);
            $http.post(uploadUrl, fd, {
                      transformRequest: angular.identity,
                      headers: {'Content-Type': undefined}
                   })

                   .success(function(successResponse){
                        $rootScope.handleResponse(successResponse);
                   })

                   .error(function(errorResponse){
                        $rootScope.handleResponse(errorResponse);
                   });
        };
    }]);

    settingsServicesApp.service('fileUpload', ['$http','$rootScope', function ($http, $rootScope) {
        this.uploadFileToUrl = function (file, uploadUrl) {

                      var fd = new FormData();
                      fd.append('file', file);
                      $http.post(uploadUrl, fd, {
                      transformRequest: angular.identity,
                      headers: {'Content-Type': undefined}
                   })

                   .success(function(successResponse){
                        $rootScope.resultPane = true;
                        $rootScope.preLoader = false;
                        $rootScope.result = successResponse;
                        $rootScope.handleResponse(successResponse);
                   })

                   .error(function(errorResponse){
                        $rootScope.resultPane = true;
                        $rootScope.preLoader = false;
                        $rootScope.result = errorResponse;
                        $rootScope.handleResponse(errorResponse);
                   });
        };
    }]);

    settingsServicesApp.factory('ExportData', function($resource, $http,$rootScope){
        return $resource('/sync/manual/export',{
        },
        {
            save : {
                    method : 'POST'
                    }
            }
        );
    }).factory('SaveExports', function($resource, $http,$rootScope){
        return $resource('/sync/savedexports',{
        },
        {
        });
    }).factory('Settings', function ($resource, $http) {
        return $resource('/config/:id', {
            id: '@_id'
        }, {
             query : {
                    method: 'GET',
                    isArray:true,
                    transformResponse : function(fullconfigdata, headers) {
                        var jsonconfigdata = JSON.parse(fullconfigdata);
                        return fullconfigdata;
                      }
                  },
             save: {
                    method: 'POST',
                    transformRequest: function (data, headers) {
                        var fd = new FormData();
                        for (var key in data) {
                            fd.append(key, data[key]);
                        }
                        return fd;
                    },
                    headers: {
                        'Content-Type': undefined
                    }
                }

            });
    }).factory('ConfigDelete', function($resource, $http,$rootScope){
        return $resource('config/delete/:id',{
              id:'@_id'
        },
        {
            remove : {
                    method : 'DELETE'
            }
        });
    }).factory('ConfigEdit', function($resource, $http,$rootScope){
        return $resource('config/update',{
        },
        {
            update: {
                method:'PUT'
            }
        });
    }).factory('CreateNewSync', function($resource, $http){
        return $resource('/syncrequest/add',{

        },
        {
        });
    }).factory('ViewSyncRequest', function($resource, $http){
        return $resource('/syncrequest/:id',{
            id:'@_id'

        },
        {

        });
    }).factory('UpdateSyncRequest', function($resource, $http,$rootScope){
        return $resource('syncrequest/update',{
        },
        {
            update: {
                        method:'PUT'
                    }
        });
    }).factory('DeleteSyncRequest', function($resource, $http,$rootScope){
        return $resource('/syncrequest/delete/:id',{
            id : '@_id'
        },
        {
            remove : {
                method : 'DELETE'
            }
        });
    }).factory('SyncOnDemand', function($resource, $http,$rootScope){
        return $resource('syncrequest/run/:id',{
        id: '@_id'
        },{
        });
    }).factory('SkipDeployment', function($resource, $http,$rootScope){
        return $resource('config/view/configid/:id',{
        id: '3'
        },{
        });
    }).factory('GetConfigSchedule', function($http, $resource){
        return $resource('/config/distribution/schedule',{
        });
    }).factory('DistributionService', function($http, $resource){
        return $resource('/clonerequest/distribution/all',{
        });
    }).factory('UpdateConfigDistribution', function($resource, $http,$rootScope){
        return $resource('/config/distribution/schedule/update',{
        },
        {
            update: {
                method:'PUT'
            }
        });
    }).factory('AddCloneDistribution', function($resource, $http,$rootScope){
        return $resource('/clonerequest/distribution/add',{
        },
        {
        });
    }).factory('UpdateCloneDistribution', function($resource, $http,$rootScope){
        return $resource('/clonerequest/distribution/update',{
        },
        {
            update: {
                method:'PUT'
            }
        });
    }).factory('DeleteDistributionService', function($resource, $http,$rootScope){
        return $resource('/clonerequest/distribution/cancel/:id',{
            id : '@_id'
        },
        {
            remove : {
                method : 'DELETE'
            }
        });
    }).factory('ResendDistributionService', function($resource, $http,$rootScope){
        return $resource('/clonerequest/distribution/run/:id',{
            id : '@_id'
        },
        {
        });
    }).factory('RunAllDistributionService', function($resource, $http,$rootScope){
        return $resource('/clonerequest/distribution/run/all',{
        },
        {

        });
    }).factory('NewTools', function ($resource) {
        return $resource('/clonerequest/distribution/view/all ', {
        },
        {
            query : {
                method: 'GET',
                isArray:true,
                transformResponse : function(fulldata, headers) {
                    var jsonData = JSON.parse(fulldata);
                    return jsonData.data.ImportTool;
                  }
            }
        });
    }).factory('UpdatedTools', function ($resource) {
        return $resource('/clonerequest/distribution/view/all ', {
        },
        {
            query : {
                method: 'GET',
                isArray:true,
                transformResponse : function(fulldata, headers) {
                    var jsonData = JSON.parse(fulldata);
                    return jsonData.data.UpdateTool;
                }
            }
        });
    }).factory('GetDistributedTool', function ($resource) {
        return $resource('/clonerequest/distribution/view/tool/:id', {
           id: '@_id'
        }, {

        });
    }).factory('ImportUpdate', function ($resource) {
    return $resource('/clonerequest/distribution/tool', {
    }, {
            update : {
                method : 'PUT'
            }
         });
    }).factory('ImportUpdateStatus', function ($resource) {
        return $resource('/clonerequest/distribution/tool/status/:id', {
        id:'@_id'
        },
        {
            update : {
                method : 'PUT'
            }
         });
    }).factory('SyncRequestsAll', function ($resource) {
        return $resource('/sync/view/all', {
            page: '@_page',
            perpage: '@_perpage'
        },
        {
        });
    }).factory('GetSyncRequestByID', function ($resource) {
        return $resource('/sync/view/syncid/:id', {
            id: '@_id',
            page: '@_page',
            perpage: '@_perpage'
        },
        {
        });
    }).factory('RetrySyncRequest', function ($resource) {
        return $resource('/sync/retry', {
        },
        {
            update : {
                method : 'PUT'
            }
        });
    });

    });