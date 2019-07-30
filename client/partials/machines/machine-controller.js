require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : [ 'machineServicesApp',  'machineTabsComponent', 'machineDetailsTabsComponent','machineGroupsDetailsTabsControllerApp']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'toolTips', 'machineServicesApp', 'machineTabsComponent', 'machineDetailsTabsComponent','flexAttributeDirectiveApp','machineGroupsDetailsTabsControllerApp', 'environmentVariablesDirectiveApp','attentionModelDirectiveApp'],function (app) {
  'use strict';

    var manageMachineControllerApp = angular.module('manageMachineControllerApp', ['ui.router', '720kb.tooltips', 'machineServicesApp', 'machineTabsComponent', 'machineDetailsTabsComponent','flexAttributeDirectiveApp','machineGroupsDetailsTabsControllerApp', 'environmentVariablesDirectiveApp','attentionModelDirectiveApp']);

    manageMachineControllerApp.controller('MachineController', function ($scope, $state, $rootScope, GetAllMachine) {
    $scope.isResultVisible = false;
    $rootScope.resultPane = false;
    $rootScope.result = false;
    $rootScope.preLoader = false;
    var selectedMachine = '';

    $scope.showSearchResults = function(keyword)
    {
        if(keyword === '' || keyword === null || keyword === undefined)
        {
            document.getElementById("search_autocomplete_machines_dashbaord").style.display = "none";
        }
        else
        {
            document.getElementById("search_autocomplete_machines_dashbaord").style.display = "block";
            $scope.searchMachineKeyword = keyword;
        }
    };

    $scope.selectSearchMachine = function(machine)
    {
        selectedMachine = machine._id.$oid;
        $scope.searchMachineKeyword = machine.machine_name;
        document.getElementById("search_autocomplete_machines_dashbaord").style.display = "none";
    };

    $scope.searchMachine = function()
    {
        $rootScope.searchProgress = true;
        $state.go('editmachine', {id : selectedMachine});
    };

    GetAllMachine.get({
    },
    function(successResponse)
    {
        $scope.machines = successResponse.data.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

});
});