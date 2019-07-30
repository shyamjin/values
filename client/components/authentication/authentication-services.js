define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var authenticationServicesApp = angular.module('authenticationServicesApp', []);

angular.module('authenticationServicesApp', []).factory('Authentication', function($resource) {
    return $resource('/user/basicauth', {
    },
    {
    });
}).factory('Registeration', function($resource,$rootScope) {
    return $resource('/user/signup', {
    },
    {
        register: {
            method: 'POST',
            transformResponse : function(response, headers) {
                return response;
            }
         }
      });
}).factory('UserProfile', function ($resource) {
    return $resource('/user/name/:username', {
        username: '@_username'
    },
    {
    });
}).factory('GuiPermissions', function ($resource) {
    return $resource('/guipermissions', {
    },
    {
        get : {
            method: 'GET',
            headers:{'detail':'false'}
        }
   });
 }).factory('ChangePassword', function ($resource) {
     return $resource('/user/change/password', {
     },
     {
        update : {
            method: 'PUT'
        }
     });
 }).factory('forgotPassword', function ($resource) {
     return $resource('/user/forgotPassword', {
     },
     {
     });
 }).factory('VerifyToken', function ($resource) {
     return $resource('/user/auth/verify', {
     },
     {
        get : {
            method: 'GET',
            isArray: false,
            transformResponse : function(fulldata, headers) {
                var jsonData = JSON.parse(fulldata);
                return jsonData;
            }
        }
     });
 }).factory('AccountLogoView', function ($resource) {
     return $resource('/systemdetails/get_logo', {
     },
     {
     });
 }).factory('UserDetails', function()  {
    var userProfile = {
        userData : {},
        guiPermissions : []
    };

    return {
    setUserDetails : function(userData)
    {
        userProfile.userData = userData;
    },
    getUserDetails : function()
    {
        return userProfile.userData;
    },
    setGUIPermissions : function(guiPermissions)
    {
        userProfile.guiPermissions = guiPermissions;
    },
    getGUIPermissions : function()
    {
        return userProfile.guiPermissions;
    }
    };
}).factory('Logout', function ($resource) {
        return $resource('/user/logout', {
        }, {});
});

});