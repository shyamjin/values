define(['angular', 'ngResource', 'uiRouter', 'authenticationServicesApp'], function (app) {

var accountLogoControllerApp = angular.module('accountLogoControllerApp', ['ngResource', 'ui.router', 'authenticationServicesApp']);

accountLogoControllerApp.controller('AccountLogoController',function($scope, $state, $stateParams, $rootScope ,AccountLogoView ){
    AccountLogoView.get({
    },
    function(successResponse)
    {
        $scope.AccountLogo = successResponse.data;
    },
    function(errorResponse)
    {
    });
});
});