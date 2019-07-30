define(['angular', 'ngResource', 'uiRouter', 'personalizeControllerApp',
'settingsViewControllerApp', 'importExportControllerApp', 'deleteConfigurationControllerApp', 'manageSynchronizationServiceControllerApp',
'synchronizationServiceControllerApp', 'editSynchronizationServiceControllerApp', 'distributionServiceControllerApp', 'deleteDistributionServiceControllerApp',
'resendDistributionServiceControllerApp', 'importToolControllerApp', 'updateToolControllerApp',
'newToolsComponentControllerApp', 'updatedToolsComponentControllerApp', 'syncRequestReportsComponentApp', 'viewSyncRequestComponentApp','saveExportControllerApp'],function (app) {
  'use strict';

var settingsRoutesApp = angular.module('settingsRoutesApp', ['ui.router', 'personalizeControllerApp',
'settingsViewControllerApp', 'importExportControllerApp', 'deleteConfigurationControllerApp', 'manageSynchronizationServiceControllerApp',
'synchronizationServiceControllerApp', 'editSynchronizationServiceControllerApp', 'distributionServiceControllerApp', 'deleteDistributionServiceControllerApp',
'resendDistributionServiceControllerApp', 'importToolControllerApp', 'updateToolControllerApp',
'newToolsComponentControllerApp', 'updatedToolsComponentControllerApp', 'syncRequestReportsComponentApp', 'viewSyncRequestComponentApp','saveExportControllerApp']).config(function($stateProvider, $httpProvider) {
    $stateProvider.state('settings', {
        url: '/settings',
        views: {
            "main": {
                templateUrl: 'static/partials/settings/settings.partial.html',
                controller: 'SettingsViewController'
            }
        },
        data: {
            pageTitle: 'Value Pack Settings'
        }
    }).state('deleteconfig', {
        url: '/delete/config/:id',
        views: {
            "main": {
                 templateUrl: 'Settings/view-settings.tpl.html',
                controller: 'DeleteConfigurationController'
            }
        },
        data: {
            pageTitle: 'Value Pack Settings'

        }
    }).state('manageSynchronization', {
        url: '/manage/synchronization/services',
        views: {
            "main": {
                 templateUrl: 'static/partials/synchronization-services/synchronization-service.partial.html',
                 controller: 'ManageSynchronizationServiceController'
            }
        },
        data: {
            pageTitle: 'Synchronization Services'

        }
    }).state('synchronization', {
        url: '/synchronization',
        views: {
            "main": {
                 templateUrl: 'static/partials/synchronization-services/synchronization-service.partial.html',
                 controller: 'synchronizationServiceController'
            }
        },
        data: {
            pageTitle: 'Synchronization Services'

        }
    }).state('editSynchronization', {
        url: '/edit/sync/:id',
        views: {
            "main": {
                 templateUrl: 'static/partials/synchronization-services/synchronization-service.partial.html',
                controller: 'EditSynchronizationServiceController'
            }
        },
        data: {
            pageTitle: 'Edit Synchronization Request'

        }
    }).state('distribution', {
        url: '/distribution',
        views: {
            "main": {
                 templateUrl: 'static/partials/distribution/distribution.partial.html',
            controller: 'DistributionServiceController'
            }
        },
        data: {
            pageTitle: 'Distribution Service'

        }
    }).state('importexport', {
        url: '/importexport',
        views: {
            "main": {
                 templateUrl: 'static/partials/import-export/importexport.partial.html',
            controller: 'ImportExportController'
            }
        },
        data: {
            pageTitle: 'Import Export Data'

        }
    }).state('distributionDelete', {
        url: '/distribution/cancel/:id',
        views: {
            "main": {
                 templateUrl: 'Settings/distribution-service.tpl.html',
            controller: 'DeleteDistributionServiceController'
            }
        },
        data: {
            pageTitle: 'Distribution Service'

        }
    }).state('distributionResend', {
        url: '/distribution/resend/:id',
        views: {
            "main": {
                 templateUrl: 'static/partials/distribution/distribution.partial.html',
                 controller: 'ResendDistributionServiceController'
            }
        },
        data: {
            pageTitle: 'Distribution Service1'

        }
    }).state('newTools', {
        url: '/tools/new',
        views: {
            "main": {
                 templateUrl: 'static/partials/dashboard/dashboard.partial.html',
                 controller: 'NewToolListController'
            }
        },
        data: {
            pageTitle: 'Dashboard'

        }
    }).state('ToolsUpdates', {
        url: '/tools/updates',
        views: {
            "main": {
                 templateUrl: 'static/partials/dashboard/dashboard.partial.html',
                 controller: 'UpdatedToolListController'
            }
        },
        data: {
            pageTitle: 'Dashboard'

        }
    }).state('importTool', {
        url: '/import/tool/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/show-new-tool/show-new-tool.partial.html',
                controller: 'ImportToolController'
            }
        },
        data: {
            pageTitle: 'New Tool Details'
        }
    }).state('updateTool', {
        url: '/update/tool/:id',
        views: {
            "main": {
                templateUrl: 'static/partials/tools/show-updated-tool/show-updated-tool.partial.html',
                controller: 'UpdateToolController'
            }
        },
        data: {
            pageTitle: 'Updated Tool Details'
        }
    }).state('viewSyncRequestReports', {
        url: '/view/sync/requests',
        views: {
            "main": {
                templateUrl: 'static/components/synchronization-services/sync-request-reports/syncrequestreports.component.html',
                controller: 'SyncRequestReportsController'
            }
        },
        data: {
            pageTitle: 'Synchronization Services'
        }
    }).state('viewSyncRequestReportByID', {
        url: '/view/sync/request/:id',
        views: {
            "main": {
                templateUrl: 'static/components/synchronization-services/sync-request-reports/syncrequestreports.component.html',
                controller: 'ViewSyncRequestDataController'
            }
        },
        data: {
            pageTitle: 'Synchronization Services'
        }
    });
});

});