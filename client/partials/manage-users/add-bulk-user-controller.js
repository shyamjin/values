define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';

var addBulkUsersControllerApp = angular.module('addBulkUsersControllerApp', ['ui.router', '720kb.tooltips', 'userServicesApp']);
addBulkUsersControllerApp.controller('AddBulkUsersController', function ($scope, $state, $rootScope, $stateParams, $window, $http, $interval, $timeout, bulkUserUpload, GetAccount, Role){
    $scope.sampleUserData = {
            'accountData' : [],
            'Roles' : []
    };
    $scope.bulkUsersUpload = function(fileToUpload)
    {
        if(fileToUpload === undefined || fileToUpload === null)
        {
            $rootScope.handleResponse('Please select the bulk file to upload');
            return false;
        }

        $scope.isResultVisible = true;
        $rootScope.preLoader = true;
        $rootScope.result = false;

        var file = fileToUpload;
        if(file)
        {
            var uploadUserUrl = "/user/import";
            bulkUserUpload.uploadUsersFile(file, uploadUserUrl, function(resp){
            });
        }
    };
    GetAccount.get({
    },
    function(successResponse)
    {
        for(var a=0; a<successResponse.data.length; a++)
        {
            $scope.sampleUserData.accountData.push(successResponse.data[a].name);
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });
    Role.get({
        id:"all"
    },
    function(successResponse)
    {
        for(var a=0; a<successResponse.data.length; a++)
        {
            $scope.sampleUserData.Roles.push(successResponse.data[a].name);
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });
});
});
