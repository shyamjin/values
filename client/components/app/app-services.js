define(['angular', 'ngResource'], function (app) {

    var appServices = angular.module('appServices', ['ngResource']);

    appServices.factory('AuthenticationService', function ($http, SessionService, $cookies, $cookieStore, $rootScope) {
        return {

            login: function (user) {
                // this method could be used to call the API and set the user instead of taking it in the function params
                SessionService.currentUser = user;
            },

            isLoggedIn: function () {
                if (sessionStorage.getItem('token') == null) {
                    return false;
                }
                else if (sessionStorage.getItem('token')) {
                    return true;
                }
                else if ($rootScope.userProfile.token != null) {
                    return true;
                }
                else {
                    return false;
                }
            }
        };
    }).factory('SessionService', function () {

        return {
            currentUser: null
        };
    }).factory('RoleService', function ($http) {

        var adminRoles = ['admin', 'editor'];
        var otherRoles = ['user'];

        return {
            validateRoleAdmin: function (currentUser) {
                return currentUser ? _.contains(adminRoles, currentUser.role) : false;
            },

            validateRoleOther: function (currentUser) {
                return currentUser ? _.contains(otherRoles, currentUser.role) : false;
            }
        };
    }).factory('SystemData', function($resource) {
        return $resource('/systemdetails/all', {
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
    });

});