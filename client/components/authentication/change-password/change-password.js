define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'authenticationServicesApp'],function (app) {
  'use strict';

var changePasswordControllerApp = angular.module('changePasswordControllerApp', ['ui.router', 'ngCookies', 'authenticationRoutesApp', 'authenticationServicesApp']);

changePasswordControllerApp.controller('ChangePasswordController',function($scope, $state, $stateParams, $rootScope, $cookies, $cookieStore, $http, $timeout, ChangePassword, UserProfile, UserUpdate){
    $scope.username = $stateParams.user;
    var resetPasswordData = {
        _id : {
            oid : ''
        }
    };

    $scope.changePassword = function(form)
    {
        if($scope.newPassword === $scope.confirmNewPassword)
        {
            UserProfile.get({
                username : $stateParams.user
            },
            function(userProfileSuccessResponse)
            {
                resetPasswordData._id.oid = userProfileSuccessResponse.data._id.$oid;
                resetPasswordData.password = $scope.newPassword;
                ChangePassword.update(resetPasswordData,function(changePasswordSuccessResponse){
                    $rootScope.handleResponse(changePasswordSuccessResponse.message);
                    $state.go('login');
                },
                function(changePasswordErrorResponse)
                {
                    $scope.errorMessage = changePasswordErrorResponse.data.message;
                });
            },
            function(userProfileErrorResponse)
            {
                $scope.errorMessage = changePasswordErrorResponse.data.message;
            });
        }
        else
        {
            $scope.errorMessage = "Password and confirm password should be same";
        }
    };
});

});