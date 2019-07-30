define(['angular', 'ngResource'], function (app) {
  'use strict';

var deploymentUnitsServicesApp = angular.module('deploymentUnitsServicesApp', []);

deploymentUnitsServicesApp.directive('logoModel', ['$parse', '$rootScope', function ($parse, $rootScope) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            element.bind('change', function (evt) {
                scope.$apply(function () {
                    var srcId = null;
                    var files = evt.target.files;
                    if(files[0].type==='image/jpeg' || files[0].type==='image/png' || files[0].type==='image/jpg' || files[0].type==='image/bmp' || files[0].type==='image/gif')
                    {
                        modelSetter(scope, element[0].files[0]);
                        return true;
                    }
                    else
                    {
                        model = $parse(attrs.fileModel);
                        modelSetter = model.assign;
                        delete scope.logoFileSelected;
                        delete scope.logoFile;
                        $rootScope.handleResponse('Please select image file for logo!');
                        return false;
                    }
                });
            });
        }
    };
}]);

deploymentUnitsServicesApp.service('duLogoFileUpload', ['$http', function ($http) {
    this.uploadDuSetLogoFileToUrl = function (file, uploadUrl) {
        var fd = new FormData();
        fd.append('logo', file);
        fd.append('duset_id',file.duset_id);
               $http.post(uploadUrl, fd, {
                  transformRequest: angular.identity,
                  headers: {'Content-Type': undefined}
               })

               .success(function(){
               })

               .error(function(){
               });
    };
       this.uploadeditDuSetLogoFileToUrl = function (file, uploadUrl) {
        var fd = new FormData();
        fd.append('logo', file);
        fd.append('duset_id',file.duset_id);
               $http.post(uploadUrl, fd, {
                  transformRequest: angular.identity,
                  headers: {'Content-Type': undefined}
               })

               .success(function(){
               })

               .error(function(){
               });
    };
}]);

deploymentUnitsServicesApp.factory('DeploymentUnitAll', function($resource) {
    return $resource('/deploymentunit/all', {
    },
    {
        get : {
            method: 'GET',
            isArray:false,
            interceptor: {
                response: function (response) {
                    return response.data.data;
                }
            }
        },
        query : {
            method: 'GET',
            isArray:false
        }
    });
}).factory('CreateDU', function ($resource) {
    return $resource('/deploymentunit/new', {
    },
    {

    });
}).factory('ApprovalStatusAll', function($resource) {
    return $resource('/deploymentunitapprovalstatus/all', {
    },
    {
        get : {
            method: 'GET',
            isArray:true,
            transformResponse : function(fulldata, headers) {
                var jsonData = JSON.parse(fulldata);
                return jsonData.data;
            }
        }
    });
}).factory('DUTypesAll', function($resource) {
    return $resource('/deploymentunittype/all', {
    },
    {
    });
}).factory('ViewDU', function($resource) {
    return $resource('/deploymentunit/view/:id', {
        id : '@_id'
    },
    {
    });
}).factory('EditDU', function ($resource) {
    return $resource('/deploymentunit/update', {
    },
    {
        update : {
            method : 'PUT'
        }
    });
}).factory('DUDelete', function($resource, $http,$rootScope){
    return $resource('/deploymentunit/delete/:id',{
        id:'@_id'
    },
    {
        remove : {
                method : 'DELETE'
        }
    });
  }).factory('CreateDUSet', function ($resource) {
    return $resource('/deploymentunitset/new', {
    }, {

    });
}).factory('DUSetAll', function($resource) {
    return $resource('/deploymentunitset/all', {
    },
    {
        get : {
            method: 'GET',
            isArray:false,
            transformResponse : function(fulldata, headers) {
                var jsonData = JSON.parse(fulldata);
                return jsonData;
            }
        }
    });
}).factory('ViewDUSet', function($resource) {
    return $resource('/deploymentunitset/view/:id', {
        id : '@_id'
    },
    {
    });
}).factory('EditDUSet', function ($resource) {
    return $resource('/deploymentunitset/update', {
    },
    {
        update : {
            method : 'PUT'
        }
    });
}).factory('GetAllDUBuildData', function ($resource) {
    return $resource('/deploymentunitset/view/getbuilds/:id', {
        id: '@_id'
    },
    {
        update : {
            method : 'PUT'
        }
    });
}).factory('GetDULatestBuildData', function ($resource) {
    return $resource('/deploymentunitset/view/getbuilds/:id', {
        id: '@_id'
    },
    {
        update : {
            method : 'PUT'
        }
    });
}).factory('GetDUStateData', function ($resource) {
    return $resource('/deploymentunitset/view/du/state/:id', {
        id: '@_id'
    },
    {
        update : {
            method : 'PUT'
        }
    });
}).factory('GetDUSetStateData', function ($resource) {
    return $resource('/state/all', {
        id: '@_id'
    },
    {
        update : {
            method : 'PUT'
        }
    });
}).factory('GetDUSetStateByID', function ($resource) {
    return $resource('/deploymentunitset/view/states/:parent_entity_id', {
        parent_entity_id: '@_parent_entity_id'
    },
    {
        update : {
            method : 'PUT'
        }
    });
});

});