define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'toolTips'],function (app) {
  'use strict';

    var editMachineGroupControllerApp = angular.module('editMachineGroupControllerApp', ['ui.router', '720kb.tooltips']);

    editMachineGroupControllerApp.controller('EditMachineGroupController', function ($scope, $stateParams, GetAllMachine, Machine, $window, $state, $timeout, $rootScope, MachineGroup, MachineGroupView, MachineGroupEdit, MachineGroupDelete) {
    $scope.hideMachineGroupdData = false;
    $scope.hideShowMoreMachineGroup = false;
    $scope.machineGroupNameFilterFlag = true;
    $scope.machineListFilterFlag = false;
    $scope.faNameValueMap = {};
    var machineGroupNameFilter = "";
    var machineListFilter = [];
    MachineGroup.getAll({
    },
    function(successResponse){
        $scope.machineGroups = successResponse.data.data;
        $scope.currentPage = successResponse.data.page;
        $scope.totalCount = successResponse.data.total;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

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
    $scope.isFilterApplied = false;
    $scope.openFilter = function()
    {
        if(document.getElementById("open_filter").style.display === "none" || document.getElementById("open_filter").style.display === "")
        {
            $('#open_filter').show();
            $scope.open_filter = true;
        }
        else
        {
            $('#open_filter').hide();
            $scope.open_filter = false;
        }
    };

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
    $scope.cancleFilter = function()
    {
        $('#open_filter').hide(700);
    };

    $scope.showGroupNameFilter = function()
    {
        if($scope.machineGroupNameFilterFlag === true)
        {
            $scope.machineGroupNameFilterFlag = false;
        }
        else
        {
            $scope.machineGroupNameFilterFlag = true;
        }
    };
    $scope.showMachineListFilter = function()
    {
        if($scope.machineListFilterFlag === true)
        {
            $scope.machineListFilterFlag = false;
        }
        else
        {
            $scope.machineListFilterFlag = true;
        }
    };
    $scope.setGroupNameFilterCSS = function(flag)
    {
        if(flag === false)
        {
            return '';
        }
        else
        {
            return 'vp-filterelement__filterrowlvlone--expanded';
        }
    };
    $scope.setMachineListFilterCSS = function(flag)
    {
        if(flag === false)
        {
            return '';
        }
        else
        {
            return 'vp-filterelement__filterrowlvlone--expanded';
        }
    };
    $scope.showMachineTypeFilter = function()
    {
        if($scope.machineTypeFilterFlag === true)
        {
            $scope.machineTypeFilterFlag = false;
        }
        else
        {
            $scope.machineTypeFilterFlag = true;
        }
    };

    $scope.setMachineListFilter = function(list)
    {
        var listFlag = 0;
        var ind = 0;
        var machineListFilterLen = machineListFilter.length;
        if(machineListFilterLen>0)
        {
            for(var a=0; a<machineListFilterLen; a++)
            {
                if(machineListFilter[a] === list)
                {
                    ind = a;
                }
                else
                {
                    listFlag++;
                }
            }

            if(listFlag === machineListFilterLen)
            {
                machineListFilter.push(list);
            }
            else
            {
                machineListFilter.splice(ind, 1);
            }
        }
        else
        {
            machineListFilter.push(list);
        }
    };
    $scope.setGroupNameFilter = function(name)
    {
        machineGroupNameFilter = name;
    };

    $scope.applyMachineGroupFilters = function()
    {
        var machine_group_name = "";
        var machine_id_list = "";
        var perpage = 0;

        if(machineGroupNameFilter !== null && machineGroupNameFilter!== undefined && machineGroupNameFilter !== '')
        {
            machine_group_name = machineGroupNameFilter;
        }
        else
        {
           machine_group_name =null;
        }


        if(machineListFilter.length>0)
        {
            machine_id_list = machineListFilter.toString();
        }
        else
        {
            machine_id_list = null;
        }


        if(machine_group_name === null && machine_id_list === null)
        {
            perpage = null;
            $scope.hideShowMoreMachineGroup = false;
            $scope.isFilterApplied = false;
        }
        else
        {
            $scope.hideShowMoreMachineGroup = true;
            $scope.isFilterApplied = true;
        }
        var jsonData={
            machine_group_name : machine_group_name,
            machine_id_list : machine_id_list,
            page : 0,
            perpage : perpage
        };
        $('#open_filter').hide(700);
        MachineGroup.get({
            machine_group_name : machine_group_name,
            machine_id_list : machine_id_list,
            page : 0,
            perpage : perpage
        },
        function(successResponse)
        {
            delete $scope.machineGroups;
            delete $scope.machineGroupData;
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
            $scope.machineGroups = successResponse.data.data;
            $scope.$watch(function(scope) {
                return scope.machineGroups;
            },
            function(newValue, oldValue) {
            });
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.closeFilter = function(form)
    {
        machineGroupNameFilter = "";
        machineListFilter = [];
        $('#open_filter').hide(700);
        $scope.open_filter = false;
        $scope.hideShowMoreMachineGroup = false;
        $scope.isFilterApplied = false;
        MachineGroup.getAll({
        },
        function(successResponse)
        {
            delete $scope.machineGroupData;
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
            $scope.machineGroups = successResponse.data.data;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.showMoreMachineGroup = function()
    {
        $scope.currentPage = $scope.currentPage+1;
        $scope.tempMachines = [];
        angular.copy($scope.machineGroups, $scope.tempMachines);
        delete $scope.machineGroups;
        MachineGroup.get({
           page:$scope.currentPage
        },
        function(successResponse)
        {
            $scope.machineGroups = [];
            $scope.currentPage = successResponse.data.page;
            $scope.totalCount = successResponse.data.total;
            for(var a=0; a<successResponse.data.data.length; a++)
            {
                $scope.tempMachines.push(successResponse.data.data[a]);
            }
            for(var b=0; b<$scope.tempMachines.length; b++)
            {
                $scope.machineGroups.push($scope.tempMachines[b]);
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });

    };

    $scope.discardMachineGroupChanges = function()
    {
        $state.go('manageMachineGroups');
        delete $scope.machineGroupData;
    };

    $scope.removeThisMachineGroup = function(group_id)
    {
        MachineGroupDelete.remove({
            id :   group_id
        },
        function (groupDeleteRequest)
        {
            $state.go('manageMachineGroups');
            delete $scope.machineGroupData;
            MachineGroup.get({
            },
            function(successResponse){
               $scope.machineGroups = successResponse.data.data;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            $rootScope.handleResponse(groupDeleteRequest);
        },
        function (groupDeleteResponseError)
        {
            $rootScope.handleResponse(groupDeleteResponseError);
        });
    };

    $scope.closeAddMachine = function()
    {
        document.getElementById("add_machine").style.display = "none";
    };

    $scope.addMachine = function(machine)
    {
        var tag_flag = 0;
        var ind = 0;
        if($scope.machineGroupData.machine_id_list.length>0)
        {
            for(var c=0;  c<$scope.machineGroupData.machine_id_list.length; c++)
            {
                if(machine.machine_name===$scope.machineGroupData.machine_id_list[c].machine_name)
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $scope.machineGroupData.machine_id_list.push(machine);
            }
            else
            {
                $scope.machineGroupData.machine_id_list.splice(ind, 1);
            }
        }
        else
        {
            $scope.machineGroupData.machine_id_list = [];
            $scope.machineGroupData.machine_id_list.push(machine);
        }
    };

    $scope.isMachineSelected = function(machine)
    {
        var flag = 0;
        if(!$scope.machineGroupData.machine_id_list)
        {
            $scope.machineGroupData.machine_id_list = [];
        }
        for(var j=0; j<$scope.machineGroupData.machine_id_list.length; j++)
        {
            if(machine === $scope.machineGroupData.machine_id_list[j].machine_name)
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

    $scope.selectMachineGroup = function(group_id)
    {
        $scope.machineGroupData = {
            group_id : '',
            group_name : '',
            description : '',
            machine_id_list : []
        };
        $rootScope.machineGroupDisplayDetailsTab = 0;
        MachineGroupView.get({
            id : group_id
        },
        function(successResponse){
            $scope.hideMachineGroupdData = true;
            $scope.machineGroupDetails = successResponse.data;
            $scope.machineGroupData.group_id = successResponse.data._id.$oid;
            $scope.machineGroupData.group_name = successResponse.data.group_name;
            $scope.machineGroupData.description = successResponse.data.description;
            for(var a=0; a<successResponse.data.machine_id_list.length; a++)
            {
                for(var b=0; b<$scope.allMachines.length; b++)
                {
                    if(successResponse.data.machine_id_list[a] === $scope.allMachines[b]._id.$oid)
                    {
                        $scope.machineGroupData.machine_id_list.push($scope.allMachines[b]);
                    }
                }
            }
            if (successResponse.data.flexible_attributes){
                for(var fa in successResponse.data.flexible_attributes){
                    $scope.faNameValueMap[fa] = successResponse.data.flexible_attributes[fa];
                }
            } else {
                for(var k in $scope.faNameValueMap) {
                    $scope.faNameValueMap[k] = '';
                }
            }
            $rootScope.$emit('setMachineGroupsDetails',$scope.machineGroupDetails);
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    if($stateParams.id)
    {
        $scope.selectMachineGroup($stateParams.id);
    }


    $scope.editMachineGroup = function(form)
    {
        var jsonData = {
            _id : {
                oid : ''
            },
            group_name : '',
            description : '',
            machine_id_list : [],
            flexible_attributes: ''
        };

        jsonData._id.oid = $scope.machineGroupData.group_id;
        jsonData.group_name = $scope.machineGroupData.group_name;
        jsonData.description = $scope.machineGroupData.description;
        jsonData.flexible_attributes = $scope.faNameValueMap;

        for(var j=0; j<$scope.machineGroupData.machine_id_list.length; j++)
        {
            jsonData.machine_id_list.push($scope.machineGroupData.machine_id_list[j]._id.$oid);
        }

        if (jsonData.machine_id_list.length<1)
        {
            $rootScope.handleResponse('Please select atleast one machine to add in group!');
            return false;
        }

        $scope.MachineGroupStatus = MachineGroupEdit.update(jsonData, function(machineGroupSuccessAddResponse){
            $state.go('manageMachineGroups');
            $scope.hideMachineGroupdData = false;
            delete $scope.machineGroups;
            MachineGroup.get({
            },
            function(successResponse){
               $scope.machineGroups = successResponse.data.data;
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            $rootScope.handleResponse(machineGroupSuccessAddResponse);
        },
        function(machineGroupErrorAddResponse){
            $rootScope.handleResponse(machineGroupErrorAddResponse);
        });
    };
    $scope.machineDeploymentGroupDetails = function(groupId)
    {
        $state.go('deploymentrequestsbyid', {id : groupId});
    };

    $scope.selectMachineToView = function(selectedMachine)
    {
        $state.go('editmachine', {id : selectedMachine});
    };
});
});