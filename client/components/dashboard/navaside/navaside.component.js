require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['appServices', 'headerMessageComponentControllerApp', 'authenticationServicesApp','changePasswordDirectiveApp']
});

define(['angular', 'uiRouter', 'appServices', 'headerMessageComponentControllerApp', 'authenticationServicesApp','changePasswordDirectiveApp'],function (app) {
  'use strict';

var navsideComponentControllerApp = angular.module('navsideComponentControllerApp', ['ui.router', 'appServices', 'headerMessageComponentControllerApp', 'authenticationServicesApp','changePasswordDirectiveApp']);

navsideComponentControllerApp.controller("NavsideController",function($scope,$http, $rootScope, $state, $cookies, $cookieStore, SystemData, AccountLogoView, Logout){
    $scope.showMonitoringSection =false;
    $scope.selectedData=[];
    $scope.useredit_errors=[];
    SystemData.get({
    },
    function(SystemDataSuccessResponse)
    {
        $scope.host = SystemDataSuccessResponse.data.hostname;
        $rootScope.systemDetails = SystemDataSuccessResponse.data;
    },
    function(SystemDataErrorResponse)
    {
        $rootScope.handleResponse(SystemDataErrorResponse);
    });

    AccountLogoView.get({
    },
    function(successResponse)
    {
        $scope.AccountLogo = successResponse.data;
    },
    function(errorResponse)
    {

    });

    $scope.showMonitoringSection = function()
    {
        if(document.getElementById("monitoring_section").style.display === "none" || document.getElementById("monitoring_section").style.display === "")
        {
            $('#monitoring_section').slideDown();
        }
        else
        {
           $('#monitoring_section').slideUp();
        }
    };

    $scope.showPluginsSection = function()
    {
        if(document.getElementById("plugins_section").style.display === "none" || document.getElementById("plugins_section").style.display === "")
        {
            $('#plugins_section').slideDown();
        }
        else
        {
           $('#plugins_section').slideUp();
        }
    };

    window.onclick=function ()
    {
        if( !event.target.classList.contains('button_toggle'))
        {
            var elements = document.getElementsByClassName("side-nav");
            if (elements.length > 0)
            {
                for(var i = 0; i < elements.length; i++)
                {
                    if (document.getElementById("side-nav-toggle").style.width == "320px" )
                    {
                        document.getElementById("side-nav-toggle").style.width = "0";
                    }
                }
            }
        }
    };

    $scope.toggleSideNav = function ()
    {
        var nav = document.getElementById("side-nav-toggle");

        if (document.getElementById("side-nav-toggle").style.width == "320px" )
        {
            document.getElementById("side-nav-toggle").style.width = "0";
        }
        else
        {
            document.getElementById("side-nav-toggle").style.width = "320px";
        }

    };

    $scope.getURL = function (path) {
        return $location.path();

    };

    $scope.defaultRoute = function()
    {
        $state.go($rootScope.userProfile.homepage);
    };

    $scope.logout = function () {
        $cookieStore.remove("token");
        $scope.isNavbarVisible = false;
        $rootScope.userProfile.userData.username = null;
        $rootScope.userProfile.userData.role = null;
        $rootScope.userProfile.permitted_routes = null;
        event.preventDefault();
        window.history.forward();
        for (var i = 0; i < $rootScope.restrictedRoutes.length; i++) {
            $rootScope.restrictedRoutes[i] = null;
        }
        $rootScope.initialiseRoutes();
        $rootScope.userAuthentication = false;
        $state.go('login');

        $scope.logoutService = Logout.save(function (response) {
            $http.defaults.headers.common['token'] = response.data.Token;
        });
    };
//    $scope.atPasswordId = $rootScope.userProfile.userData._id.$oid;
    $scope.showEditPassword = function()
    {
        if(document.getElementById("update_password_screen").style.display === "none" || document.getElementById("update_password_screen").style.display === '')
        {
            document.getElementById("update_password_screen").style.display = "block";
        }
        else
        {
           document.getElementById("update_password_screen").style.display = "none";
       }
    };
    $scope.closePassword = function()
    {
        document.getElementById("update_password_screen").style.display = "none";
    };
});

});