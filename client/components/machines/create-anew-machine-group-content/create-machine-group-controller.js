define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'toolTips'],function (app) {
  'use strict';

    var addNewMachineGroupControllerApp = angular.module('addNewMachineGroupControllerApp', ['ui.router', '720kb.tooltips']);

    addNewMachineGroupControllerApp.controller('CreateMachineGroupController', function ($scope, $stateParams, GetAllMachine, Machine, $window, $state, $timeout, $rootScope, MachineGroupCreate) {
    $scope.newMachineGroupData = {
        group_name : '',
        description : '',
        machine_id_list : []
    };

    $scope.faNameValueMap = {};

    $scope.showAddMachine = function()
    {
        if(document.getElementById("add_machine").style.display === "none" || document.getElementById("add_machine").style.display === "")
        {
            document.getElementById("add_machine").style.display = "block";
        }
        else
        {
           document.getElementById("add_machine").style.display = "none";
        }
    };

    $scope.closeAddMachine = function()
    {
        document.getElementById("add_machine").style.display = "none";
    };

    $scope.addMachine = function(machine)
    {
        var tag_flag = 0;
        var ind = 0;
        if($scope.newMachineGroupData.machine_id_list.length>0)
        {
            for(var c=0;  c<$scope.newMachineGroupData.machine_id_list.length; c++)
            {
                if(machine.machine_name===$scope.newMachineGroupData.machine_id_list[c].machine_name)
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $scope.newMachineGroupData.machine_id_list.push(machine);
            }
            else
            {
                $scope.newMachineGroupData.machine_id_list.splice(ind, 1);
            }
        }
        else
        {
            $scope.newMachineGroupData.machine_id_list = [];
            $scope.newMachineGroupData.machine_id_list.push(machine);
        }
    };

    $scope.isMachineSelected = function(machine)
    {
        var flag = 0;
        if(!$scope.newMachineGroupData.machine_id_list)
        {
            $scope.newMachineGroupData.machine_id_list = [];
        }
        for(var j=0; j<$scope.newMachineGroupData.machine_id_list.length; j++)
        {
            if(machine === $scope.newMachineGroupData.machine_id_list[j].machine_name)
            {
                flag++;
            }
        }
        if(flag>0)
        {
            return true;
        }
        else
        {
            return false;
        }
    };

    GetAllMachine.get({
    },
    function(successResponse)
    {
        $scope.allMachines = successResponse.data.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.createNewMachineGroup = function(form)
    {
        var jsonData = {
            group_name : '',
            description : '',
            machine_id_list : [],
            flexible_attributes: ''
        };

        jsonData.group_name = $scope.newMachineGroupData.group_name;
        jsonData.description = $scope.newMachineGroupData.description;
        jsonData.flexible_attributes = $scope.faNameValueMap;
        for(var j=0; j<$scope.newMachineGroupData.machine_id_list.length; j++)
        {
            jsonData.machine_id_list.push($scope.newMachineGroupData.machine_id_list[j]._id.$oid);
        }

        if (jsonData.machine_id_list.length<1)
        {
            $rootScope.handleResponse('Please select atleast one machines to add in group!');
            return false;
        }

        $scope.MachineGroupStatus = MachineGroupCreate.save(jsonData, function(machineGroupSuccessAddResponse){
            $state.go('manageMachineGroups');
            $rootScope.handleResponse(machineGroupSuccessAddResponse);
        },
        function(machineGroupErrorAddResponse){
            $rootScope.handleResponse(machineGroupErrorAddResponse);
        });
    };
    $scope.discardMachineGroupsChanges = function()
    {
        $state.go('manageMachineGroups');
    };
});
});