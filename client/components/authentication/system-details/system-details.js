define(['angular', 'ngResource', 'uiRouter', 'applicationRoutesApp', 'authenticationServicesApp'],function (app) {
  'use strict';

var forgotPasswordControllerApp = angular.module('systemDetailsControllerApp', ['ui.router', 'authenticationRoutesApp', 'authenticationServicesApp', 'applicationRoutesApp']);

forgotPasswordControllerApp.controller('SystemDetailsController',function($scope, forgotPassword){        
});

});