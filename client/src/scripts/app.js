define(['angular',
    'ngResource',
    'uiRouter',
    'ngCookies',
    'appControllersApp',
    'appServices',
    'authenticationServicesApp',
    'deploymentServicesApp',
    'headerMessageComponentControllerApp',
    'toolServicesApp',
    'proposedToolServicesApp',
    'toolSetServicesApp'], function (app) {

    var mainApp = angular.module('app',
        ['ngResource',
            'ui.router',
            'ngCookies',
            'authenticationServicesApp',
            'deploymentServicesApp',
            'appControllersApp',
            'appServices',
            'headerMessageComponentControllerApp',
            'toolServicesApp',
            'proposedToolServicesApp',
            'toolSetServicesApp'
            ]);

    mainApp.run(function run($rootScope, $location, $state, $http, $cookieStore, $cookies, AuthenticationService, SessionService, UserDetails, GuiPermissions) {
        'use strict';
        $rootScope.userToken = {};
        $rootScope.userAuthentication = {};
        $rootScope.userName = {};

        $rootScope.userProfile = {
            "token": "",
            "permitted_routes": [],
            "userData": {},
            "homepage":""
        };
        var td_injector = angular.injector(['ng', 'toolServicesApp']);
        $rootScope.toolDetailsFactory = td_injector.get('ToolDetailsFactory');

        $rootScope.toolDataValidatorFactory = td_injector.get('ToolDataValidatorFactory');

        var dt_injector = angular.injector(['ng', 'deploymentServicesApp']);
        $rootScope.deployToolFactory = dt_injector.get('DeployTool');

        var dt_du_injector = angular.injector(['ng', 'deploymentServicesApp']);
        $rootScope.deployDUFactory = dt_du_injector.get('DeployDUFactory');

        var dt_fa_injector = angular.injector(['ng', 'deploymentServicesApp']);
        $rootScope.faFactory = dt_fa_injector.get('FasMatchingFactory');

        var userDetails_injector = angular.injector(['ng', 'authenticationServicesApp']);
        $rootScope.userFactory = userDetails_injector.get('UserDetails');

        var dt_pt_injector = angular.injector(['ng', 'proposedToolServicesApp']);
        $rootScope.proposedToolDetailsFactory = dt_pt_injector.get('ToolDetailsFactory');

        var dt_ts_injector = angular.injector(['ng', 'toolSetServicesApp']);
        $rootScope.toolSetDetailsFactory = dt_ts_injector.get('ToolSetDetailsFactory');
        $rootScope.toolSetDataValidatorFactory = dt_ts_injector.get('ToolSetDataValidatorFactory');

        $rootScope.$on('$stateChangeSuccess', function (ev, to, toParams, from, fromParams) {
            $rootScope.selectedTools = [];
            $rootScope.deployToolFactory.cleanDeployFactoryObject();
            $rootScope.deployDUFactory.cleanDeployDUFactoryObject();
            $rootScope.toolDetailsFactory.cleanToolDataObject();
            $rootScope.toolSetDetailsFactory.cleanToolSetDataObject();
            $rootScope.previousState = from.name;
            $rootScope.currentState = to.name;
            delete $rootScope.searchProgress;
        });
        // check if current location matches route

        $rootScope.initialiseRoutes = function () {
            $rootScope.isallowed = {};
            $rootScope.allPaths = {};
            $rootScope.allPaths['/tools/all'] = "/tools/all";
            $rootScope.allPaths['/deploymentrequests'] = '/deploymentrequests';
            $rootScope.allPaths['/sanjay'] = '/sanjay';
            $rootScope.allPaths['/createclone'] = '/createclone';
            $rootScope.allPaths['/users'] = '/users';
            $rootScope.allPaths['/manageroles'] = '/manageroles';
            $rootScope.allPaths['/clonerequests'] = '/clonerequests';
            $rootScope.allPaths['/machines'] = '/machines';
            $rootScope.allPaths['/settings'] = '/settings';
            $rootScope.allPaths['/catalog'] = '/catalog';
            $rootScope.allPaths['/tool/new'] = '/tool/new';
            $rootScope.allPaths['/logout'] = '/logout';
            $rootScope.allPaths['/admin'] = '/admin';
            $rootScope.allPaths['/changepassword'] = '/changepassword';
            $rootScope.allPaths['/synchronization'] = '/synchronization';
            $rootScope.allPaths['/importexport'] = '/importexport';
            $rootScope.allPaths['/distribution'] = '/distribution';
            $rootScope.allPaths['/tools/new'] = '/tools/new';
            $rootScope.allPaths['/tools/updates'] = '/tools/updates';
            $rootScope.allPaths['/systemdata'] = '/systemdata';
            $rootScope.allPaths['/dashboard'] = '/dashboard';
            $rootScope.allPaths['/view/reports'] = '/view/reports';
            $rootScope.allPaths['/toolset/new'] = '/toolset/new';
            $rootScope.allPaths['/plugin'] = '/plugin';
            $rootScope.allPaths['/dashboard/du'] = '/dashboard/du';
            $rootScope.allPaths['/deploymentunit/new'] = '/deploymentunit/new';
            $rootScope.allPaths['/deploymentunitset/new'] = '/deploymentunitset/new';
            $rootScope.allPaths['/machine/remove/:id'] = '/machine/remove/:id';
            $rootScope.allPaths['/manage/synchronization/services'] = '/manage/synchronization/services';
            $rootScope.allPaths['/delete/machine/group/:id'] = '/delete/machine/group/:id';
            $rootScope.allPaths['/toolset/all'] = '/toolset/all';
            $rootScope.allPaths['/edit/tool/:id'] = '/edit/tool/:id';
            $rootScope.allPaths['/deploy/tool/:id/:build_number'] = '/deploy/tool/:id/:build_number';
            $rootScope.allPaths['/recent/requests'] = '/recent/requests';
            $rootScope.allPaths['/saved/requests'] = '/saved/requests';
            $rootScope.allPaths['/deploymentunitset/all'] = '/deploymentunitset/all';
            $rootScope.allPaths['/manage/tags'] = '/manage/tags';
            $rootScope.allPaths['/tag/update'] = '/tag/update';
            $rootScope.allPaths['/manage/prerequisites'] = '/manage/prerequisites';
            $rootScope.allPaths['/view/monitoring'] = '/view/monitoring';
            $rootScope.allPaths['/view/monitoring/runningservices'] = '/view/monitoring/runningservices';
            $rootScope.allPaths['/users'] = '/users';
            $rootScope.allPaths['/edit/user/:id'] = '/edit/user/:id';
            $rootScope.allPaths['/users/import'] = '/users/import';
            $rootScope.allPaths['/view/du/state'] = '/view/du/state';
            $rootScope.allPaths['/view/duset/state'] = '/view/duset/state';
            $rootScope.allPaths['/create/du/state'] = '/create/du/state';
            $rootScope.allPaths['/state/delete/:id'] = '/state/delete/:id';
            $rootScope.allPaths['/manage/flexibleattributes'] = '/manage/flexibleattributes';
            $rootScope.allPaths['/new/flexibleattributes'] = '/new/flexibleattributes';
            $rootScope.allPaths['/manage/plugins/deployment'] = '/manage/plugins/deployment';
            $rootScope.allPaths['/plugin/deployment/upload'] = '/plugin/deployment/upload';
            $rootScope.allPaths['/editmachine/:id'] = '/editmachine/:id';
            $rootScope.allPaths['/proposed/tools/all'] = '/proposed/tools/all';
            $rootScope.allPaths['/view/proposed/tool/:id'] = '/view/proposed/tool/:id';
            $rootScope.allPaths['/deploymentrequest/view/:id'] = '/deploymentrequest/view/:id';
            $rootScope.allPaths['/approve/tool/proposed/:id'] = '/approve/tool/proposed/:id';
            $rootScope.allPaths['/plugin/deployment/read/:path'] = '/plugin/deployment/read/:path';
            $rootScope.allPaths['/machine/view/deployment/history/entity/:entity/:id'] = '/machine/view/deployment/history/entity/:entity/:id';
            $rootScope.allPaths['/deploymentrequest/group/revert/:id'] = '/deploymentrequest/group/revert/:id';
            $rootScope.allPaths['/edit/machine/group/:id'] = '/edit/machine/group/:id';
            $rootScope.allPaths['/view/audits'] = '/view/audits';
            $rootScope.allPaths['/view/repository'] = '/view/repository';
            $rootScope.allPaths['/new/repository'] = '/new/repository';

            $rootScope.isallowed['/tools/all'] = false;
            $rootScope.isallowed['/deploymentrequests'] = false;
            $rootScope.isallowed['/createclone'] = false;
            $rootScope.isallowed['/users'] = false;
            $rootScope.isallowed['/manageroles'] = false;
            $rootScope.isallowed['/clonerequests'] = false;
            $rootScope.isallowed['/machines'] = false;
            $rootScope.isallowed['/settings'] = false;
            $rootScope.isallowed['/catalog'] = false;
            $rootScope.isallowed['/tool/new'] = false;
            $rootScope.isallowed['/notificationservice'] = false;
            $rootScope.isallowed['/logout'] = false;
            $rootScope.isallowed['/admin'] = false;
            $rootScope.isallowed['/synchronization'] = false;
            $rootScope.isallowed['/importexport'] = false;
            $rootScope.isallowed['/distribution'] = false;
            $rootScope.isallowed['/tools/new'] = false;
            $rootScope.isallowed['/systemdata'] = false;
            $rootScope.isallowed['/dashboard'] = false;
            $rootScope.isallowed['/view/reports'] = false;
            $rootScope.isallowed['/toolset/new'] = false;
            $rootScope.isallowed['/plugin'] = false;
            $rootScope.isallowed['/dashboard/du'] = false;
            $rootScope.isallowed['/deploymentunit/new'] = false;
            $rootScope.isallowed['/deploymentunitset/new'] = false;
            $rootScope.isallowed['/machine/remove/:id'] = false;
            $rootScope.isallowed['/manage/synchronization/services'] = false;
            $rootScope.isallowed['/delete/machine/group/:id'] = false;
            $rootScope.isallowed['/toolset/all'] = false;
            $rootScope.isallowed['/edit/tool/:id'] = false;
            $rootScope.isallowed['/deploy/tool/:id/:build_number'] = false;
            $rootScope.isallowed['/recent/requests'] = false;
            $rootScope.isallowed['/saved/requests'] = false;
            $rootScope.isallowed['/deploymentunitset/all'] = false;
            $rootScope.isallowed['/manage/tags'] = false;
            $rootScope.isallowed['/tag/update'] = false;
            $rootScope.isallowed['/manage/prerequisites'] = false;
            $rootScope.isallowed['/view/monitoring'] = false;
            $rootScope.isallowed['/view/monitoring/runningservices'] = false;
            $rootScope.isallowed['/users'] = false;
            $rootScope.isallowed['/edit/user/:id'] = false;
            $rootScope.isallowed['/users/import'] = false;
            $rootScope.isallowed['/view/du/state'] = false;
            $rootScope.isallowed['/view/duset/state'] = false;
            $rootScope.isallowed['/create/du/state'] = false;
            $rootScope.isallowed['/state/delete/:id'] = false;
            $rootScope.isallowed['/manage/flexibleattributes'] = false;
            $rootScope.isallowed['/new/flexibleattributes'] = false;
            $rootScope.isallowed['/manage/plugins/deployment'] = false;
            $rootScope.isallowed['/plugin/deployment/upload'] = false;
            $rootScope.isallowed['/editmachine/:id'] = false;
            $rootScope.isallowed['/proposed/tools/all'] = false;
            $rootScope.isallowed['/deploymentrequest/view/:id'] = false;
            $rootScope.isallowed['/view/proposed/tool/:id'] = false;
            $rootScope.isallowed['/approve/tool/proposed/:id'] = false;
            $rootScope.isallowed['/plugin/deployment/read/:path'] = false;
            $rootScope.isallowed['/machine/view/deployment/history/entity/:entity/:id'] = false;
            $rootScope.isallowed['/deploymentrequest/group/revert/:id'] = false;
            $rootScope.isallowed['/edit/machine/group/:id'] = false;
            $rootScope.isallowed['/view/audits'] = false;
            $rootScope.isallowed['/view/repository'] = false;
            $rootScope.isallowed['/new/repository'] = false;
        };

        $rootScope.initialiseRoutes();
        $rootScope.isNavbarVisible = false;
        $rootScope.restrictedRoutes = [];
        var cleanRoutes = ["/login", "/error", "/signup", "/changepassword", "/admin", "/forgotpassword", "/newuser/:user", "/user/:user", "/change/password/:user", "/propose/tool"];

        // check if current location matches route

        var routeClean = function (route) {
            var flag = false;
            for (var i = 0; i < cleanRoutes.length; i++) {
                if (route == cleanRoutes[i]) {
                    flag = true;
                    break;
                }
            }
            return flag;
        };

        var isRouteAllowed = function (route) {
            var flag = false;
            for (var i = 0; i < $rootScope.restrictedRoutes.length; i++) {
                if (route == $rootScope.restrictedRoutes[i]) {
                    flag = true;
                    break;
                }
            }
            return flag;
        };

        if (sessionStorage.getItem('token'))
        {
            $rootScope.userProfile.token = sessionStorage.getItem('token');
            $http.defaults.headers.common['token'] = $rootScope.userProfile.token;
            if($rootScope.userProfile.userData)
            {
                $rootScope.userProfile.userData = JSON.parse(sessionStorage.getItem('ga_userprofile'));
            }

            if($rootScope.userProfile.permitted_routes.length <= 0)
            {
                $rootScope.userProfile.permitted_routes = sessionStorage.getItem('ga_permissions');
                GuiPermissions.get({
                },
                function(guiPermissionsResponse)
                {
                    $rootScope.userProfile.permitted_routes = guiPermissionsResponse.data;
                    $rootScope.userFactory.setGUIPermissions(guiPermissionsResponse.data);
//                    sessionStorage.setItem('ga_permissions',$rootScope.userProfile.permitted_routes);
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
                    $rootScope.$on('$stateChangeStart', function (ev, to, toParams, from, fromParams) {
                        $rootScope.isChangePasswordFormVisible = true;

                        if (routeClean(to.url)) {
                        }
                        else if (!routeClean(to.url) && !AuthenticationService.isLoggedIn()) {
                            ev.preventDefault();
                            $rootScope.isNavbarVisible = false;
                            $state.go('login');
                        }
                        else if (!isRouteAllowed(to.url)) {
                            ev.preventDefault();
                            $state.go('error');
                        }
                    });
                },
                function(errorResponse)
                {
                    if(errorResponse.data.message==='Unexpected token < in JSON at position 0')
                    {
                        $state.go('login');
                    }
                });
            }
        }
    });

});