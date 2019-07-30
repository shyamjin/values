require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['loginControllerApp']
});

define(['angular', 'ngResource', 'uiRouter', 'loginControllerApp'],function (app) {
  'use strict';

var authenticationRoutesApp = angular.module('authenticationRoutesApp', ['ui.router', 'loginControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('login', {
            url: '/login',
        views: {
            "main": {
                templateUrl: 'static/components/authentication/login/login.html',
                controller: 'UserLoginController'
            }
        },
        data: {
            pageTitle: 'Login'
        }
    }).state('error', {
            url: '/error',
        views: {
            "main": {
                templateUrl: 'static/partials/error-handling/error.html',
                controller: 'UserLoginController'
            }
        },
        data: {
            pageTitle: 'Error'
        }
    }).state('resetNewUserPassword', {
            url: '/newuser/:user',
        views: {
            "main": {
                templateUrl: 'static/components/authentication/reset-password/reset-password.html',
                controller: 'ResetPasswordController'
            }
        },
        data: {
            pageTitle: 'Reset Password'
        }
    }).state('resetOldUserPassword', {
            url: '/user/:user',
        views: {
            "main": {
                templateUrl: 'static/components/authentication/reset-password/reset-password.html',
                controller: 'ResetPasswordController'
            }
        },
        data: {
            pageTitle: 'Reset Password'
        }
    }).state('forgotpassword',{
        url: '/forgotpassword',
        views: {
            "main":{
                templateUrl: 'static/components/authentication/forgot-password/forgot-password.html',
                controller: 'ForgotPasswordController'
            }
        },
        data: {
            pageTitle: 'Forgot Password'
        }
    }).state('changePassword',{
        url: '/change/password/:user',
        views: {
            "main":{
                templateUrl: 'static/components/authentication/change-password/change-password.html',
                controller: 'ChangePasswordController'
            }
        },
        data: {
            pageTitle: 'Change Password'
        }
    })
});

});