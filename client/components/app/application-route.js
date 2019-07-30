define(['angular',
    'uiRouter',
    'dashboardControllerApp',
    'createToolsPartialControllerApp',
    'editToolsPartialControllerApp',
    'allToolsComponentControllerApp',
    'showToolPartialControllerApp',
    'proposeToolsPartialControllerApp',
    'proposedToolsComponentControllerApp',
    'showProposedToolPartialControllerApp',
    'showUpdatedToolPartialControllerApp',
    'createToolSetPartialControllerApp',
    'editToolSetPartialControllerApp',
    'showToolSetPartialControllerApp',
    'toolSetListComponentControllerApp',
    'systemDataControllerApp',
    'accountLogoControllerApp'],function (app) {
  'use strict';

var applicationRoutesApp = angular.module('applicationRoutesApp', ['ui.router',
    'dashboardControllerApp',
    'createToolsPartialControllerApp',
    'editToolsPartialControllerApp',
    'allToolsComponentControllerApp',
    'showToolPartialControllerApp',
    'proposeToolsPartialControllerApp',
    'proposedToolsComponentControllerApp',
    'showProposedToolPartialControllerApp',
    'showUpdatedToolPartialControllerApp',
    'createToolSetPartialControllerApp',
    'editToolSetPartialControllerApp',
    'showToolSetPartialControllerApp',
    'toolSetListComponentControllerApp',
    'systemDataControllerApp',
    'accountLogoControllerApp']).config(function config($stateProvider, $urlRouterProvider) {

    var $cookies;
    angular.injector(['ngCookies']).invoke(['$cookies', function (_$cookies_) {
        $cookies = _$cookies_;
    }]);

    if ($cookies.get('token')) {
        $urlRouterProvider.when('', '/dashboard');
    }
    else {
        $urlRouterProvider.otherwise('/login');
    }
        
    $stateProvider.state('dashboard', {
        url: '/dashboard',
        views: {
            "main": {
                templateUrl: 'static/partials/dashboard/dashboard.partial.html',
                controller:'DashboardController'
            }
        },
        data: {
            pageTitle: 'Dashboard'
        }
    }).state('systemdata', {
        url: '/systemdata',
        views: {
            "main": {
                controller: 'SystemDataController',
                templateUrl: 'static/components/app/about-dpm/about-dpm.partial.html'
            }
        },
        data: {
            pageTitle: 'About DPM'
        }
    }).state('runningToolDeploymentStatus', {
        url: '/dashboard/deployment/:request_id',
        views: {
            "main": {
                templateUrl: 'static/partials/dashboard/dashboard.partial.html',
                controller:'DashboardController'
            }
        },
        data: {
            pageTitle: 'Dashboard'
        }
    }).state('toolImportUpdateStatus', {
        url: '/dashboard/importupdate/:request_id',
        views: {
            "main": {
                templateUrl: 'static/partials/dashboard/dashboard.partial.html',
                controller:'DashboardController'
            }
        },
        data: {
            pageTitle: 'Dashboard'
        }
    }).state('applications', {
        url: '/tools/all',
        views: {
            "main": {
                templateUrl: 'static/partials/dashboard/dashboard.partial.html',
                controller: 'ToolListController'
            }
        },
        data: {
            pageTitle: 'Dashboard'

        }
    }).state('viewApplication', {
        url: '/tool/view/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/show-tool/show-tool.partial.html',
                controller: 'ShowToolPartialController'
            }
        },
        data: {
            pageTitle: 'Tool Details'
        }
    }).state('createNewTool', {
        url: '/tool/new',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/create-tools//create-tools.partial.html',
                controller: 'CreateNewToolController'
            }
        },
        data: {
            pageTitle: 'Create New Tool'
        }
    }).state('viewAllToolSets', {
        url: '/toolset/all',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/show-tool/show-tool.partial.html',
                controller: 'AllToolSetController'
            }
        },
        data: {
            pageTitle: 'Dashboard'
        }
    }).state('editTool', {
        url: '/edit/tool/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/edit-tools/edit-tools.partial.html',
                controller: 'EditToolController'
            }
        },
        data: {
            pageTitle: 'Edit Tool'
        }
    }).state('viewNewApplication', {
        url: '/tool/new/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/show-new-tool/show-new-tool.partial.html',
                controller: 'DistributedToolViewController'
            }
        },
        data: {
            pageTitle: 'New Tool Details'
        }
    }).state('viewUpdatedApplication', {
        url: '/tool/updated/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/show-updated-tool/show-updated-tool.partial.html',
                controller: 'DistributedToolViewController'
            }
        },
        data: {
            pageTitle: 'Updated Tool Details'
        }
    }).state('newToolSet', {
        url: '/toolset/new',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/create-tool-sets/create-tool-set.partial.html',
                controller: 'AddNewToolSetController'
            }
        },
        data: {
            pageTitle: 'Create New Tool Set'
        }
    }).state('viewToolSet', {
        url: '/toolset/view/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/show-tool-set/show-tool-set.partial.html'
            }
        },
        data: {
            pageTitle: 'View Tool Set'
        }
    }).state('editToolSet', {
        url: '/edit/toolset/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/edit-tool-set/edit-tool-set.partial.html'
            }
        },
        data: {
            pageTitle: 'Edit Tool Set'
        }
    }).state('proposeNewTool', {
        url: '/propose/tool',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/propose-tools/propose-tools.partial.html',
                controller: 'ProposeToolPartialController'
            }
        },
        data: {
            pageTitle: 'Propose New Tool'
        }
    }).state('viewProposedTools', {
        url: '/proposed/tools/all',
        views: {
            "main": {
                templateUrl: 'static/partials/dashboard/dashboard.partial.html',
                controller: 'ProposedToolListController'
            }
        },
        data: {
            pageTitle: 'Dashboard'
        }
    }).state('viewProposedTool', {
        url: '/view/proposed/tool/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/show-proposed-tool/show-proposed-tool.partial.html',
                controller: 'ShowProposedToolPartialController'
            }
        },
        data: {
            pageTitle: 'View Proposed Tool'
        }
    }).state('editProposedTools', {
        url: '/edit/tool/proposed/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/edit-proposed-tools/edit-proposed-tools.partial.html',
                controller: 'EditProposedToolController'
            }
        },
        data: {
            pageTitle: 'Edit Proposed Tool'
        }
    });
});

});