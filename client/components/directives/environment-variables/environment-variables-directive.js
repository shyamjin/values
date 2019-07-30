define(['angular', 'ngResource'], function (app) {
  'use strict';
var environmentVariablesDirectiveApp = angular.module('environmentVariablesDirectiveApp', []);

environmentVariablesDirectiveApp.directive('environmentVariables', function () {
    return {
        restrict: 'E',
        templateUrl :'static/components/directives/environment-variables/environment-variables-directive.html',
        scope:{
            envVars: '=',
            onLoad: '&',
            disabled: '@'
        },
        controller: function($scope, $rootScope){
            $scope.addEntry= function() {
                $scope.envVars.push({name: "", value: ""});
            };

            $scope.removeEntry= function(index) {
                $scope.envVars.splice(index, 1);
            }
        }
    };
});
});