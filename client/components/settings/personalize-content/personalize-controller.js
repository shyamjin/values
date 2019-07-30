require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var personalizeControllerApp = angular.module('personalizeControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

personalizeControllerApp.controller('PersonalizeController', function ($scope, $state, $stateParams, logoFileUpload, $rootScope)
    {
     $scope.uploadAccountLogo = function(form)
    {
        if($scope.accountLogoSelected)
        {
            var jsonData = {};
            var file = $scope.accountLogoSelected;
            if(file)
            {
                var uploadUrl = "/systemdetails/logoupload";
                logoFileUpload.uploadAccountFileToUrl(file, uploadUrl, function(){
                });
            }
        }
        else
        {
            $rootScope.handleResponse('Please select a file to upload');
            return false;
        }
    };
});
});