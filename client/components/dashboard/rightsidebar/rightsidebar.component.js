define(['angular', 'ngResource', 'uiRouter', 'ngCookies'],function (app) {
  'use strict';
var rightSideBarComponent = angular.module('rightSideBarComponent', ['ui.router']);
rightSideBarComponent.controller('MachineSearchController', function ($scope, $state) {

    $scope.searchMachine = function(searchMachineKeyword)
    {
//        $state.go('machines', {});
//        /editmachine/:id
    };

});

});

