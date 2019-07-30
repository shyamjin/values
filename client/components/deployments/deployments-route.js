define(['angular', 'uiRouter', 'deployToolControllerApp', 'deployDUControllerApp', 'deployementRequestStepsControllerApp',
'recentRequestsComponentControllerApp', 'savedRequestsComponentControllerApp', 'requestDetailsComponentControllerApp'],function (app) {
  'use strict';

var deploymentRoutesApp = angular.module('deploymentRoutesApp', ['ui.router', 'deployToolControllerApp', 'deployDUControllerApp', 'deployementRequestStepsControllerApp',
'recentRequestsComponentControllerApp', 'savedRequestsComponentControllerApp', 'requestDetailsComponentControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('deployTool', {
        url: '/deploy/tool/:id/:build_number',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/deploy-tools/deploy-tools.partial.html',
                controller: 'DeployToolController'
            }
        },
        data: {
            pageTitle: 'Deploy Tool'
        }
    }).state('deployMultipleTools', {
        url: '/deploy/tools/:tools',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/deploy-tools/deploy-tools.partial.html',
                controller: 'DeployToolController'
            }
        },
        data: {
            pageTitle: 'Deploy Tool'
        }
    }).state('deploymentrequests', {
        url: '/deploymentrequests',
        views: {
            "main": {
                templateUrl: 'static/partials/deployments/deployments.partial.html',
                controller: 'deploymentPartialController'
            }
        },
        data: {
            pageTitle: 'Deployments'
        }
    }).state('deploymentrequestsbyid', {
        url: '/deploymentrequest/view/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/deployments/deployments.partial.html',
                controller: 'DeploymentRequestsGridController'
            }
        },
        data: {
            pageTitle: 'Deployments'
        }
    }).state('deployToolSet', {
        url: '/deploy/toolset/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/deploy-tools/deploy-tools.partial.html',
                controller: 'DeployToolController'
            }
        },
        data: {
            pageTitle: 'Deploy Tool Set'
        }
    }).state('recentRequests', {
        url: '/deploymentrequests',
        views: {
            "main": {
                templateUrl: 'static/partials/deployments/deployments.partial.html',
                controller: 'RecentDeploymentRequestsController'
            }
        },
        data: {
            pageTitle: 'Recent Deployments'
        }
    }).state('savedRequests', {
        url: '/saved/requests',
        views: {
            "main": {
                templateUrl: 'static/partials/deployments/deployments.partial.html',
                controller: 'SavedDeployementRequestsController'
            }
        },
        data: {
            pageTitle: 'Saved Deployments'
        }
    }).state('deployDU', {
        url: '/deploy/du/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/deploy-du/deploy-du.partial.html',
                controller: 'DeployDUController'
            }
        },
        data: {
            pageTitle: 'Deploy DU'
        }
    }).state('deployDUSet', {
        url: '/deploy/duset/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/deploy-du/deploy-du.partial.html',
                controller: 'DeployDUController'
            }
        },
        data: {
            pageTitle: 'Deploy DU Package'
        }
    }).state('editSavedToolDeploymentRequest', {
        url: '/edit/saved/deployment/tool/:request_id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/deploy-tools/deploy-tools.partial.html',
                controller: 'DeployToolController'
            }
        },
        data: {
            pageTitle: 'Deploy Tool'
        }
    }).state('editSavedDUDeploymentRequest', {
        url: '/edit/saved/deployment/du/:request_id',
        views: {
            "main": {
                templateUrl: 'static/partials/deploy-du/deploy-du.partial.html',
                controller: 'DeployDUController'
            }
        },
        data: {
            pageTitle: 'Deploy DU'
        }
    }).state('deployMultipleDus', {
        url: '/deploy/dus/:dus',
        views: {
            "main": {
                templateUrl: 'static/partials/deploy-du/deploy-du.partial.html',
                controller: 'DeployDUController'
            }
        },
        data: {
            pageTitle: 'Deploy DU'
        }
    });
});

});