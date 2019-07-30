define(['angular', 'ngResource', 'uiRouter', 'applicationRoutesApp', 'authenticationServicesApp'],function (app) {
  'use strict';

var forgotPasswordControllerApp = angular.module('forgotPasswordControllerApp', ['ui.router', 'authenticationRoutesApp', 'authenticationServicesApp', 'applicationRoutesApp']);

forgotPasswordControllerApp.controller('ForgotPasswordController',function($scope, forgotPassword){
        $scope.forgotPassword = function(form)
        {
            var jsonData={};
            jsonData.user = $scope.username;
            forgotPassword.save(jsonData,function(response){
                $scope.forgotPasswordSuccessResponse = response.message;
            },
            function(errorResponse)
            {
                $scope.forgotPasswordErrorResponse = errorResponse.data.message;
            });
        };
});

});