require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : []
});

define(['angular'],function (app) {
  'use strict';

var headerMessageComponentControllerApp = angular.module('headerMessageComponentControllerApp', []);

headerMessageComponentControllerApp.controller("HeaderMessageComponentController",function($scope, $rootScope, $interval, $state){
    $rootScope.$on("handleResponse", function (event, args) {
        var response = args.response;
        $scope.handleResponse(response);
    });

    var promise = null;
    $scope.closeHeaderMessage = function ()
    {
        delete $scope.success_message;
        delete $scope.error_message;
        delete $scope.warning_message;
        $('#header_message').slideUp(700);
        $interval.cancel(promise);
        promise = undefined;
    };

    $scope.handleResponse = function(response)
    {
        $scope.success_message = "";
        $scope.error_message = "";
        $scope.warning_message = "";
        $('#header_message').slideDown(700);
        if(response.status === 200)
        {
            $scope.success_message = response.message;
        }
        else if(response.status === 404 || response.status === 400)
        {
            if(response.message)
            {
                $scope.error_message = response.message;
            }
            else if(response.data)
            {
                if(response.data.message)
                {
                    $scope.error_message = response.data.message;
                }
            }
        }        
        else if(response.status === 401)
        {
            $scope.error_message = "Unauthorized access";
        }
        else if(response.result)
        {
            if(response.result === 'success' && response.message)
            {
                $scope.success_message = response.message;
            }
            else
            {
                $scope.error_message = response.message;
            }
        }
        else
        {
            $scope.warning_message = response;
        }
        promise = $interval(function(){
            $scope.closeHeaderMessage();
        }, 7000);
    };
});

});