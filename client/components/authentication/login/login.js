define(['angular', 'uiRouter', 'ngCookies', 'applicationRoutesApp', 'authenticationServicesApp'],function (app) {
  'use strict';

var loginControllerApp = angular.module('loginControllerApp', ['ui.router', 'ngCookies', 'authenticationRoutesApp', 'authenticationServicesApp', 'applicationRoutesApp']);

loginControllerApp.controller("UserLoginController",function($scope, $http, $state, $stateParams, $timeout, $rootScope, Authentication, $location, UserProfile, $cookies, $cookieStore, GuiPermissions, UserDetails){
    $scope.invalidLogin = true;
    $scope.loadingBar = true;
    $scope.errorMessage = "";
    $scope.validateUser = function(form)
    {
        $scope.loadingBar = false;
        $scope.errorMessage ='';
        $scope.user = new Authentication();
        var userName = {};
        userName = $scope.username;
        var passWord = {};
        passWord = $scope.password;

        var jsonData = {};
        jsonData.user = userName;
        jsonData.password = passWord;    
        $http.defaults.headers.common['Authorization'] = 'Basic ' + btoa(userName + ':' + passWord);
        $scope.userdata = Authentication.save(undefined,function (authenticationResponse) {
            $rootScope.userAuthentication=authenticationResponse.result;
            $rootScope.userProfile.token=authenticationResponse.data.Token;
            $http.defaults.headers.common['token'] = $rootScope.userProfile.token;
            $scope.defaultHomeState = authenticationResponse.data.homepage;
            sessionStorage.setItem("token", $rootScope.userProfile.token);
            sessionStorage.setItem("ga_userprofile", JSON.stringify($rootScope.userProfile.userData));
            //$cookieStore.put('ga_userprofile',$rootScope.userProfile);
            if((!authenticationResponse.data.isfirstlogin) || (authenticationResponse.data.isfirstlogin === true) || (authenticationResponse.data.isfirstlogin === 'true'))
            {
                $state.go('changePassword', {'user' : jsonData.user});
            }
            else
            {
                $scope.getUserProfile = UserProfile.get({
                username : jsonData.user
                },
                function(userProfileResponse){
                    $scope.loadingBar = true;
                    $rootScope.userProfile.userData = userProfileResponse.data;
                    $rootScope.userProfile.homepage=authenticationResponse.data.homepage;
                    sessionStorage.setItem("ga_userdata", JSON.stringify($rootScope.userProfile.userData));
                    sessionStorage.setItem("ga_userprofile", JSON.stringify($rootScope.userProfile.userData));
                    //$cookieStore.put('ga_userdata',userProfileResponse.data);
                    //$cookieStore.put('ga_userprofile',userProfileResponse.data);
                    $rootScope.userFactory.setUserDetails(userProfileResponse.data);
                });

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
                        $state.go($scope.defaultHomeState);
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
            }
        },
        function(authErrorResponse)
        {
            $scope.errorMessage=authErrorResponse.data.message;
            $scope.username="";
            $scope.password="";
            $scope.loadingBar = true;
        });
    };
    
    $scope.showSystemDetails = function()
    {
    	 if(document.getElementById("view_system_details").style.display === "none" || document.getElementById("view_system_details").style.display === "")
         {
             $('#view_system_details').slideDown();
         }
         else
         {
            $('#view_system_details').slideUp();
         }
    	
    }; 
    $scope.closeSysDetailModal = function()
    {
        $('#view_system_details').hide(700);
    };
});

});