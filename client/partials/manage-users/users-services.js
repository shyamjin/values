define(['angular', 'ngResource'],function (app) {
  'use strict';

var userServicesApp = angular.module('userServicesApp', []);

   userServicesApp.directive('bulkUserModel', ['$parse', '$rootScope',  function ($parse, $rootScope) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                var model = $parse(attrs.bulkUserModel);
                var modelSetter = model.assign;
                element.bind('change', function (evt) {
                    scope.$apply(function () {
                        var files = evt.target.files;
                        if(files[0].type==='application/vnd.ms-excel')
                        {
                            scope.bulkUserFileSelected = files[0].name;
                            modelSetter(scope, element[0].files[0]);
                        }
                        else
                        {
                            $rootScope.handleResponse('Invalid file format... Please select .csv file');
                            return false;
                        }
                    });
                });
            }
        };
    }]);

   userServicesApp.service('bulkUserUpload', ['$http','$rootScope','$state', '$stateParams', function ($http, $rootScope, $state, $stateParams) {
        this.uploadUsersFile = function (file, uploadUserUrl) {

                      var fd = new FormData();
                      fd.append('file', file);
                      $http.post(uploadUserUrl, fd, {
                      transformRequest: angular.identity,
                      headers: {'Content-Type': undefined}
                   })

                   .success(function(successResponse){
                        $rootScope.preLoader = false;
                        $rootScope.resultPane = true;
                        $rootScope.importResult = successResponse;
                        $rootScope.handleResponse(successResponse);
                   })

                   .error(function(errorResponse){
                        $rootScope.preLoader = false;
                        $rootScope.resultPane = true;
                        $rootScope.importResult = errorResponse;
                        $rootScope.handleResponse(errorResponse);
                   });
        };
   }]);

userServicesApp.factory('Users', function($resource, $http,$rootScope){
    return $resource('user/:id',{
    id : '@_id'
    },
    {
        query : {
                method : 'GET',
                isArray : true,
                transformResponse : function(fullData){
                    var jsonData = JSON.parse(fullData);
                    return jsonData;
                }
        }
    });
}).factory('UserAdd', function($resource, $http){
    return $resource('user/new',{
    },
    {
    });
}).factory('UserUpdate', function($resource, $http,$rootScope){
    return $resource('user/update',{
    },
    {
        update: {
            method:'PUT'
        }
    });
}).factory('PasswordUpdate', function($resource, $http,$rootScope){
    return $resource('user/change/password',{
    },
    {
        update: {
            method:'PUT'
        }
    });
}).factory('UserDelete', function($resource, $http,$rootScope){
    return $resource('user/delete/:id',{
        id:'@_id'
    },
    {
        remove : {
            method : 'DELETE'
        }
    });
}).factory('GetAccount', function($resource, $http){
    return $resource('account/all',{

    },
    {

    });
}).factory('Role', function($resource, $http,$rootScope){
    return $resource('role/:id',{
    id : '@_id'
    },
    {
        query : {
                method : 'GET',
                isArray : true,
                transformResponse : function(fullData){
                    var jsonData = JSON.parse(fullData);
                    return jsonData;
                }
        }
    });
}).factory('RoleAdd', function($resource, $http,$rootScope){
    return $resource('role/new',{
    },
    {
        query : {
            method : 'GET',
            isArray : true,
            transformResponse : function(fullData){
                var jsonData = JSON.parse(fullData);
                return jsonData;
            }
        }
    });
}).factory('RoleEdit', function($resource, $http,$rootScope){
    return $resource('role/update',{
    },
    {
        update: {
            method:'PUT'
        }
    });
}).factory('RolePermissionEdit', function($resource, $http,$rootScope){
    return $resource('role/list/update',{
    },
    {
        update: {
            method:'PUT'
        }
    });
}).factory('RoleDelete', function($resource, $http,$rootScope){
    return $resource('role/delete',{
    },
    {
        remove : {
          method : 'DELETE'
        }
    });
}).factory('PermissionGroup', function($resource, $http,$rootScope){
    return $resource('grouppermissions/:id',{
    id : '@_id'
    },
    {
        query : {
                method : 'GET',
                isArray : true,
                transformResponse : function(fullData){
                    console.log(fullData);
                    var jsonData = JSON.parse(fullData);
                    console.log(jsonData);
                    return jsonData;
                }
        }
    });
}).factory('RemovePermissionGroup', function($resource, $http,$rootScope){
    return $resource('role/remove/permissiongroup',{
    },
    {
        update: {
            method:'PUT'
        }
    });
}).factory('createUserGroup', function($resource, $http){
    return $resource('/teams/add',{
    },
    {
    });
}).factory('UserGroupDelete', function($resource, $http,$rootScope){
    return $resource('/teams/delete/:id',{
    id:'@_id'
    },
    {
        remove : {
            method : 'DELETE'
        }
    });
}).factory('UserGroupView', function($resource,$rootScope) {
    return $resource('/teams/view/:id', {
        id:'@_id'
    },
    {
    });
}).factory('UserGroupEdit', function($resource,$rootScope) {
    return $resource('/teams/update',{
    },
    {
        update : {
            method: 'PUT'
        }
    });
 }).factory('UserGroup', function ($resource, $http) {
    return $resource('/teams/view', {
    });
}).factory('GenerateToken', function($resource, $http,$rootScope){
    return $resource('/user/generateaccesstoken',{
    },
    {
        update: {
            method:'PUT'
        }
    });
}).factory('DeleteToken', function($resource, $http,$rootScope){
    return $resource('/user/deleteaccesstoken/:id',{
    },
    {
        remove: {
            method:'DELETE'
        }
    });
});

});