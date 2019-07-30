define(['angular', 'uiRouter', 'ngCookies', 'applicationRoutesApp', 'authenticationServicesApp'],function (app) {
  'use strict';

var resetPasswordControllerApp = angular.module('resetPasswordControllerApp', ['ui.router', 'ngCookies', 'authenticationRoutesApp', 'authenticationServicesApp', 'applicationRoutesApp']);

resetPasswordControllerApp.controller('ResetPasswordController',function($scope, $state, $stateParams, $rootScope, $cookies, $cookieStore, $http, $timeout, ChangePassword, Authentication, UserProfile, GuiPermissions){
    var authenticateUserData = {};
    var resetPasswordData = {
        _id : {
            oid : ''
        }
    };

    $scope.resetPassword = function(form)
    {
        delete $scope.errorMessage;
        $scope.username = $stateParams.user;
        if($scope.newPassword === $scope.confirmNewPassword)
        {
            authenticateUserData.user = $scope.username;
            authenticateUserData.password = $scope.oldPassword;
            $http.defaults.headers.common['Authorization'] = 'Basic ' + btoa(authenticateUserData.user + ':' + authenticateUserData.password);
            Authentication.save(undefined,function (authenticationSuccessResponse) {

                $rootScope.userAuthentication = authenticationSuccessResponse.result;
                $rootScope.userProfile.token = authenticationSuccessResponse.data.Token;
                $http.defaults.headers.common['token'] = $rootScope.userProfile.token;
                sessionStorage.setItem('token',$rootScope.userProfile.token);
                sessionStorage.setItem('ga_userprofile',JSON.stringify($rootScope.userProfile.userData));

                $scope.getUserProfile = UserProfile.get({
                    username : $stateParams.user
                },
                function(userProfileResponse){
                    resetPasswordData._id.oid = userProfileResponse.data._id.$oid;
                    resetPasswordData.password = $scope.newPassword;
                    ChangePassword.update(resetPasswordData,function(changePasswordSuccessResponse){
                        $rootScope.handleResponse(changePasswordSuccessResponse.message);
                        $scope.guiPermissions=GuiPermissions.get({
                        },
                        function(guiPermissionsResponse)
                        {
                            $rootScope.userProfile.permitted_routes = guiPermissionsResponse.data;
                            $rootScope.userFactory.setGUIPermissions(guiPermissionsResponse.data);
                            sessionStorage.setItem('ga_permissions',$rootScope.userProfile.permitted_routes);
                            var permitted_routes = [];
                            permitted_routes = $rootScope.userProfile.permitted_routes;
                            for(i=0;i<$rootScope.userProfile.permitted_routes.length;i++)
                            {
                                if($rootScope.userProfile.permitted_routes[i].indexOf('#')===0)
                                {
                                    $rootScope.restrictedRoutes[i]=$rootScope.userProfile.permitted_routes[i].substr(1);
                                }
                                else
                                {
                                    $rootScope.restrictedRoutes[i]=$rootScope.userProfile.permitted_routes[i];
                                }
                            }
                            for(var i=0;i<$rootScope.restrictedRoutes.length;i++)
                            {
                                if($rootScope.restrictedRoutes[i]==$rootScope.allPaths[$rootScope.restrictedRoutes[i]])
                                {
                                    $rootScope.isallowed[$rootScope.restrictedRoutes[i]] = true;
                                }
                            }
                            $rootScope.isNavbarVisible = true;
                            if($rootScope.userProfile.token && $rootScope.userAuthentication==="success")
                            {
                                $state.go('dashboard');
                            }
                        },
                        function(errorResponse)
                        {
                            $scope.errorMessage = errorResponse.data.message;
                            if(errorResponse.data.message==='Unexpected token < in JSON at position 0')
                            {
                                $state.go('login');
                            }
                        });
                    },
                    function(changePasswordErrorResponse)
                    {
                        $scope.errorMessage = changePasswordErrorResponse.data.message;
                    });
                    $rootScope.userProfile.userData = userProfileResponse.data;
                    sessionStorage.setItem('ga_userdata',JSON.stringify($rootScope.userProfile.userData));
                    sessionStorage.setItem('ga_userprofile',JSON.stringify($rootScope.userProfile.userData));
                    $rootScope.userFactory.setUserDetails(userProfileResponse.data);
                });
            },
            function(authErrorResponse)
            {
                $scope.errorMessage = authErrorResponse.data.message;
                $scope.username="";
                $scope.password="";
            });
        }
        else
        {
            $scope.errorMessage = 'New password and confirm password does not match!';
        }
    };
});

});