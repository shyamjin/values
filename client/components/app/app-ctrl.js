define(['angular', 'ngResource', 'uiRouter', 'authenticationRoutesApp', 'applicationRoutesApp', 'deploymentRoutesApp', 'deploymentUnitsRoutesApp', 'machineRoutesApp', 'cloneRoutesApp', 'settingsRoutesApp', 'userRoutesApp', 'deploymentUnitsRoutesApp', 'tagsRoutesApp', 'pluginRoutesApp', 'monitoringRoutesApp', 'prerequisitesRoutesApp', 'statesRoutesApp', 'loginControllerApp', 'changePasswordControllerApp', 'forgotPasswordControllerApp', 'resetPasswordControllerApp', 'navsideComponentControllerApp', 'headerMessageComponentControllerApp', 'flaxAttributeRoutesApp', 'deploymentPluginRoutesApp','auditingRoutesApp','repositoryRoutesApp'], function (app) {

var appControllersApp = angular.module('appControllersApp', ['ngResource', 'ui.router',
 'authenticationRoutesApp',
 'applicationRoutesApp',
 'deploymentRoutesApp',
 'deploymentUnitsRoutesApp',
 'machineRoutesApp',
 'cloneRoutesApp',
 'settingsRoutesApp',
 'userRoutesApp',
 'deploymentUnitsRoutesApp',
 'tagsRoutesApp',
 'pluginRoutesApp',
 'monitoringRoutesApp',
 'prerequisitesRoutesApp',
 'statesRoutesApp',
 'appServices',
 'loginControllerApp',
 'changePasswordControllerApp',
 'forgotPasswordControllerApp',
 'resetPasswordControllerApp',
 'navsideComponentControllerApp',
 'headerMessageComponentControllerApp',
 'flaxAttributeRoutesApp',
 'deploymentPluginRoutesApp',
 'auditingRoutesApp',
 'repositoryRoutesApp']);


appControllersApp.controller('AppCtrl', function AppCtrl($scope, $location, $state, $cookieStore, $rootScope, VerifyToken, Logout, SystemData) {
    $rootScope.handleResponse = function(response)
    {
        $rootScope.$emit("handleResponse", {'response' : response});
    };

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

    $scope.closeAllOpenPopups = function(e)
    {
        console.log("testing clicks on screen ");
//        e = e || window.event;
//        e = e.target || e.srcElement;
        console.log(e);
        // Get all <div> elements in the document
        var allElements = document.querySelectorAll("div");
        for(var i=0; i<allElements.length; i++)
        {
            for(var j=0; j<allElements[i].classList.length; j++)
            {
                if(allElements[i].style.display)
                {
                    // Set the display property none of the that element
                    allElements[i].style.display = 'none';
                }
            }
        }
    };

    window.onclick=function ()
    {
        if(event.target.classList.contains('skip_slideup'))
        {
        }
        else
        {
            var allElements = document.getElementsByClassName('filter_popup');
            if (allElements.length > 0)
            {
                for(var i = 0; i < allElements.length; i++)
                {
                    $(allElements[i]).slideUp();
                }
            }
        }
    };

    function remaining_up()
    {
        var allElements = document.getElementsByClassName('filter_popup');
        for(var i = 0; i < allElements.length; i++)
        {
            $(allElements[i]).slideUp();
        }
    }

    $rootScope.logout = function () {
        sessionStorage.empty();
        $rootScope.isNavbarVisible = false;
        $rootScope.userProfile.userData.username = null;
        $rootScope.userProfile.userData.role = null;
        $rootScope.userProfile.permitted_routes = null;
        event.preventDefault();
        window.history.forward();
        for (i = 0; i < $rootScope.restrictedRoutes.length; i++)
        {
            $rootScope.restrictedRoutes[i] = null;
        }
        $rootScope.initialiseRoutes();
        $rootScope.userAuthentication = false;
        $state.go('login');

        Logout.save(function (response) {
            $http.defaults.headers.common['token'] = response.data.Token;
        });
    };

    $scope.$on('$stateChangeSuccess', function (event, toState, toParams, fromState, fromParams) {
        $scope.searchToolKeyword = '';
        $scope.searchDUKeyword = '';
        $scope.searchStateKeyword ='';
        $scope.searchStateSetKeyword = '';
        $rootScope.showResultPane = false;
        if (angular.isDefined(toState.data.pageTitle)) {
            $scope.pageTitle = toState.data.pageTitle;
        }
        if (sessionStorage.getItem('token'))
        {
            var tokenData = {};
            tokenData.token = sessionStorage.getItem('token');
            VerifyToken.save(tokenData,function(verifyTokenSuccessResponse) {
            },
            function(verifyTokenErrorResponse)
            {
                $rootScope.logout();
            });
        }

    });

    $rootScope.closeThis = function()
    {
        $state.go('dashboard');
    };

    $rootScope.discardChanges = function()
    {
        if(($location.path().indexOf('deploymentunit') >=1) || ($location.path().indexOf('deploymentunitset') >=1) || ($location.path().indexOf('du') >=1))
        {
            $rootScope.currentStatus = "";
            $state.go('duDashboard');
        }
        else if(($location.path().indexOf('machines') >=1) || ($location.path().indexOf('editmachine') >=1))
        {
            $rootScope.currentStatus = "";
            $state.go('manageMachines');
        }
        else
        {
            $rootScope.currentStatus = "";
            $state.go('dashboard');
        }
    };

});

});