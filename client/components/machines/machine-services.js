define(['angular', 'ngResource'],function (app) {
  'use strict';

var machineServicesApp = angular.module('machineServicesApp', []);

machineServicesApp.factory('GetAllMachine', function($resource, $http,$rootScope){
    return $resource('/machine/view/all',{
    page:0,
    perpage:0
    },
        {
        getAll:{
             params:{
            perpage: null
        }
        }

        });
    }).factory('MachineAdd', function ($resource) {
        return $resource('/machine/new', {  },{

        });
    }).factory('Machine', function ($resource, $http) {
        return $resource('/machine/view/:id', {
            id : '@_id'
        },
        {
            query : {
                method: 'GET',
                isArray:true,
                transformResponse : function(fullmachinedata, headers) {
                    var jsonmachineData = JSON.parse(fullmachinedata);
                    return jsonmachineData;
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
    }).factory('GetAllMachineTypes', function($resource, $http,$rootScope){
    return $resource('/machine/type/all',{
    },
        {
        });
    }).factory('UpdateMachine', function($resource,$rootScope) {
        return $resource('/machine/update',{
        },
         {
            update :
                    {
                            method: 'PUT'
                     }
          });
    }).factory('MachineDelete', function($resource, $http,$rootScope){
    return $resource('/machine/remove/:id',{
        id:'@_id'
    },
    {
        remove : {
                method : 'DELETE'
        }
    });
    }).factory('GetDeploymentHistory', function($resource, $http,$rootScope){
    return $resource('/machine/view/deployment/history/entity/:entity/:id',{
        entity: '@_entity',
        id: '@_id'
    },
    {
    });
  });
machineServicesApp.factory('AddFavouriteMachine', function($resource,$rootScope) {
    return $resource('/machine/fav/new', {
    },
        {
        });
    }).factory('ViewFavouriteMachine', function($resource,$rootScope) {
        return $resource('machine/fav/user/:id', {
        },
        {
            query :
            {
                method: 'GET',
                isArray: false,
                transformResponse : function(response, headers) {
                    var jsonData = JSON.parse(response);
                    return jsonData;
                }
            }
      });
    }).factory('ViewFavouriteMachineAll', function($resource,$rootScope) {
        return $resource('machine/all/fav', {
        },
        {
            query :
            {
                method: 'GET',
                isArray: false,
                transformResponse : function(response, headers) {
                    var jsonData = JSON.parse(response);
                    return jsonData;
                }
            }
        });
    }).factory('FavMachineDelete', function($resource, $http,$rootScope){
        return $resource('/machine/fav/delete/:id',{
        id:'@_id'
        },
            {
                remove : {
                    method : 'DELETE'
            }
        });
    }).factory('GetFavouriteMachine', function($resource,$rootScope) {
        return $resource('/machine/fav/machine/:m_id/user/:u_id', {
            m_id:'@_id',
            u_id:'@_uid'
        }, {

        });
    });

    machineServicesApp.directive('bulkFileModel', ['$parse', '$rootScope',  function ($parse, $rootScope) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                var model = $parse(attrs.bulkFileModel);
                var modelSetter = model.assign;
                element.bind('change', function (evt) {
                    scope.$apply(function () {
                        var files = evt.target.files;
                        if(files[0].type==='application/vnd.ms-excel')
                        {
                            scope.bulkFileSelected = files[0].name;
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

    machineServicesApp.service('bulkFileUpload', ['$http','$rootScope','$state', '$stateParams', function ($http, $rootScope, $state, $stateParams) {
        this.uploadMachineFile = function (file, uploadMachineUrl) {

                      var fd = new FormData();
                      fd.append('file', file);
                      $http.post(uploadMachineUrl, fd, {
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

    machineServicesApp.factory('TestMachine', function($resource,$rootScope) {
    return $resource('/machine/test', {
    }, {
      });
  });

  machineServicesApp.factory('MachineGroup', function ($resource, $http) {
    return $resource('/machinegroups/view', {
    page:0,
    perpage:0
    },
        {
        getAll:{
             params:{
                perpage: null
             }
        }

        });
  }).factory('MachineGroupCreate', function($resource,$rootScope) {
    return $resource('/machinegroups/add', {
    }, {
      });
  }).factory('MachineGroupDelete', function($resource, $http,$rootScope){
    return $resource('/machinegroups/delete/:id',{
        id:'@_id'
    },
    {
        remove : {
                method : 'DELETE'
        }
    });
  }).factory('MachineGroupView', function($resource,$rootScope) {
    return $resource('/machinegroups/view/:id', {
        id:'@_id'
    }, {

      });
  }).factory('MachineGroupEdit', function($resource,$rootScope) {
    return $resource('/machinegroups/update',{
    },
     {
        update :
                {
                        method: 'PUT'
                 }
      });
  });

});