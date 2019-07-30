define(['angular', 'ngResource', 'uiRouter', 'appServices'], function (app) {

var systemDataControllerApp = angular.module('systemDataControllerApp', ['ngResource', 'ui.router','appServices']);


systemDataControllerApp.controller('SystemDataController', function($scope, $rootScope, SystemData) {
    $scope.application = SystemData.get({
    },
    function(SystemDataSuccessResponse)
    {
    },
    function(SystemDataErrorResponse)
    {
        $rootScope.handleResponse(SystemDataErrorResponse);
    });
});
});