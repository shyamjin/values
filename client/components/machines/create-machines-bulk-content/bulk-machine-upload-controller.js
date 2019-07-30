define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'toolTips',
'machineServicesApp'],function (app) {
  'use strict';

    var bulkMachineUploadControllerApp = angular.module('bulkMachineUploadControllerApp', ['ui.router', '720kb.tooltips',
    'machineServicesApp']);

    bulkMachineUploadControllerApp.controller('BulkMachineUploadController', function ($scope, $state, $rootScope, $stateParams, $window, $http, $interval, $timeout, bulkFileUpload,GetAccount,GetAllMachineTypes) {
    $scope.isResultVisible = false;
    $rootScope.preLoader = false;
    $rootScope.resultPane = false;

    $scope.sampleMachineData = {
            'accountData' : [],
            'machineTypes' : [],
            'shell_type' : [
                        "/bin/bash -c",
                        "/bin/ksh -c",
                        "/bin/sh -c",
                        "/bin/csh -c"
            ],
            'reload_commands' : [
                ". ~/.profile",
                ". ~/.bash_profile",
                ". ~/.bashrc"
            ]
    };

    $scope.bulkMachineUpload = function(fileToUpload)
    {
        if(fileToUpload === undefined || fileToUpload === null)
        {
            $rootScope.handleResponse('Please select the bulk file to upload');
            return false;
        }

        $scope.isResultVisible = true;
        $rootScope.preLoader = true;
        $rootScope.resultPane = false;

        var file = fileToUpload;
        if(file)
        {
            var uploadMachineUrl = "/machine/import";
            bulkFileUpload.uploadMachineFile(file, uploadMachineUrl, function(resp){
            });
        }
    };

    GetAccount.get({
    },
    function(successResponse)
    {
        for(var a=0; a<successResponse.data.length; a++)
        {
            $scope.sampleMachineData.accountData.push(successResponse.data[a].name);
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.MachineTypes = GetAllMachineTypes.get({
    },
    function( types)
    {
        for(var b=0; b<types.data.length; b++)
        {
            $scope.sampleMachineData.machineTypes.push(types.data[b].type);
        }
    },
    function(errorResponse)
    {
       $rootScope.handleResponse(errorResponse);
    });

});
});