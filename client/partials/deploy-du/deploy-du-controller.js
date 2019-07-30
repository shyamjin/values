define(['angular', 'uiRouter', 'ngCookies', 'moment', 'humanizeDuration', 'angularTimer', 'jquery', 'toolTips', 'authenticationServicesApp', 'toolServicesApp', 'machineServicesApp', 'deploymentServicesApp','deploymentPartialControllerApp'],function (app) {
  'use strict';

var deployDUControllerApp = angular.module('deployDUControllerApp', ['ui.router', '720kb.tooltips', 'authenticationServicesApp', 'toolServicesApp', 'machineServicesApp', 'deploymentServicesApp', 'timer','deploymentPartialControllerApp']);

deployDUControllerApp.controller('DeployDUController', function ($scope, $location,$rootScope, $state, $stateParams, Ticket, $interval, TicketStatus, $timeout, GetAllMachine, Machine, MachineGroup, GetCurrentServerTime, ViewDU, ViewDUSet, MachineGroupView, SaveDeploymentRequest, ViewSavedDeploymentRequest, deploymentFieldFileUpload, EditSavedDeploymentRequest, DeploymentUnitAll, SkipDeployment, IsBuildDeployedOnMachine) {
    GetCurrentServerTime.get({
    },
    function(getCurrentServerTimeSuccessResponse)
    {
       $scope.currentServerTime = getCurrentServerTimeSuccessResponse;
    },
    function(getCurrentServerTimeErrorResponse)
    {
      $rootScope.handleResponse(getCurrentServerTimeErrorResponse);
    });

    document.onclick=function ()
    {
        if(event.target.classList.contains('skip_slideup'))
        {
        }
        else
        {
            var allElements = document.getElementsByClassName('tag_popup');
            if (allElements.length > 0)
            {
                for(var i = 0; i < allElements.length; i++)
                {
                    $(allElements[i]).slideUp();
                }
            }
        }
    };

    function remaining_up()
    {
        var allElements = document.getElementsByClassName('tag_popup');
        for(var i = 0; i < allElements.length; i++)
        {
            $(allElements[i]).slideUp();
        }
    }

    $scope.current_time = new Date();
    $scope.scheduled_timestamp = $scope.current_time.toISOString();
    $rootScope.errorInd = false;
    var selectedDU = [];
    $scope.duList = [];
    $scope.deploy_on = 'machine';
    var deployment_type = 'dugroup';
    $scope.duSelectedToDeploy = [];
    $scope.selectedDU = {
        du_name : '',
        du_type : '',
        du_id : '',
        build_id : '',
        build_number : ''
    };
    $scope.selectedMachine = {
        machine_name : "",
        machine_id : ''
    };

    if($stateParams.dus)
    {
        selectedDU = JSON.parse($stateParams.dus);
        if(!angular.isArray(selectedDU))
        {
            selectedDU = selectedDU.split(",");

        }
    }

    MachineGroup.get({
    },
    function(successResponse){
       $scope.machineGroups = successResponse.data.data;
    },
    function(errorResponse){
        $rootScope.handleResponse(errorResponse);
    });

    SkipDeployment.get({
    },
    function(successResponse){
       $scope.skip_deployment = JSON.parse(successResponse.data.skipDeploymentInd);
       $scope.machine_matching_ind = JSON.parse(successResponse.data.machineMatchingInd);
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.selectMachineGroup = function(group_id, tool_name, entity)
    {
        $scope.machineGroupData = {
            group_id : '',
            group_name : '',
            description : '',
            machine_id_list : []
        };

        MachineGroupView.get({
            id : group_id,
            deploymentgroupdetails : false
        },
        function(successResponse){
            $scope.machineGroupData.group_id = successResponse.data._id.$oid;
            $scope.machineGroupData.group_name = successResponse.data.group_name;
            $scope.machineGroupData.description = successResponse.data.description;
            $scope.tempMachine ={};
            $scope.deploymentCount = 0;
            for(var a=0; a<successResponse.data.machine_id_list.length; a++)
            {
                for(var b=0; b<$scope.allMachines.length; b++)
                {
                    if(successResponse.data.machine_id_list[a] === $scope.allMachines[b]._id.$oid)
                    {
                        $scope.machineGroupData.machine_id_list.push($scope.allMachines[b]);
                        $scope.machineNoCount = successResponse.data.machine_id_list.length;
                        $scope.addMachine($scope.allMachines[b], tool_name, entity,$scope.machineGroupData.group_id, $scope.skip_deployment, $scope.is_build_already_deployed);
                    }
                }
            }

        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.setDeployOnValue = function(value)
    {
        $scope.deploy_on = value;
    };

    $scope.setFieldTypeCSS = function(param, isFieldUploaded)
    {
        if(param === 'label')
        {
            if(isFieldUploaded === true)
            {
                return 'field_uploaded_label';
            }
            else
            {
                return '';
            }
        }
        else
        {
            if(isFieldUploaded === true)
            {
                return 'field_uploaded_input';
            }
            else
            {
                return '';
            }
        }
    };

    DeploymentUnitAll.get({
        page: 0,
        perpage: 0
    },
    function(successResponse)
    {
        for(var i=0; i<successResponse.data.length; i++)
        {
            for(var j=0; j<successResponse.data[i].data.length; j++)
            {
                $scope.duList.push(successResponse.data[i].data[j]);
            }
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.isDUSelected = function(du)
    {
        var flag = 0;
        for(var j=0; j<$scope.duSelectedToDeploy.length; j++)
        {
            if(du.name === $scope.duSelectedToDeploy[j].du_name)
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

    $scope.addMoreDU = function(du)
    {
        var elementId = '';
        var du_flag = 0;
        var ind = 0;
        if(du.build_number)
        {
            for(var k=0; k<$scope.duSelectedToDeploy.length; k++)
            {
                if(du.name === $scope.duSelectedToDeploy[k].du_name)
                {
                    du_flag ++;
                    ind = k;
                }
            }

            if(du_flag === 0)
            {
                $scope.getDUDetails(du._id.$oid,du.build_number,du.build_id);
            }
            else
            {
                $scope.duSelectedToDeploy.splice(ind, 1);
            }
        }
        else
        {
            $rootScope.handleResponse(" Unable to select "+du.name+" as it does not have a valid build");
            elementId = document.getElementById("select_check_"+du.name);
            elementId.checked = false;
            return false;
        }

    };

    $scope.getDUDetails = function(du_id, build_number, build_id)
    {
        $scope.duDetails = ViewDU.get({
            id : du_id
        },
        function(response)
        {
            $scope.duData = response.data;
            var du = response.data;
            $scope.deployment_field_value = response.data.deployment_field;
            $scope.buildSelectedToDeploy = {
                build_id : build_id,
                build_number : build_number
            };
             var duData = {
                        du_id : du._id.$oid,
                        du_name: du.name,
                        du_type: du.type,
                        build_number : $scope.buildSelectedToDeploy.build_number,
                        build_id : $scope.buildSelectedToDeploy.build_id,
                        deployment_field_value :$scope.deployment_field_value,
                        du_dependent : du.dependent,
                        du_order : du.order,
                        flexible_attributes : du.flexible_attributes
             };
            $rootScope.deployDUFactory.addDU(duData);
            $scope.duSelectedToDeploy = [];
            $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
            $scope.selectedDU.du_name = $scope.duSelectedToDeploy[0].du_name;
            $scope.selectedDU.du_id = $scope.duSelectedToDeploy[0].du_id;
            $scope.selectedDU.build_id = $scope.duSelectedToDeploy[0].build_id;
            $scope.selectedDU.build_number = $scope.duSelectedToDeploy[0].build_number;
            $scope.selectedDU.du_type = $scope.duSelectedToDeploy[0].type;
            $scope.selectedDU.flexible_attributes = $scope.duSelectedToDeploy[0].flexible_attributes;
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    if ($location.path().indexOf('/deploy/duset/') >= 0)
    {
        $scope.request_type = 'deploy';
        deployment_type = 'dugroup';
        var du_set_extra_details = JSON.parse($stateParams.id);
        if(du_set_extra_details.duDataList.length > 0)
        {
            for(var t2=0; t2<du_set_extra_details.duDataList.length; t2++)
            {
                var duDataSet = {
                    du_id : du_set_extra_details.duDataList[t2].du_id,
                    du_name: du_set_extra_details.duDataList[t2].name,
                    du_type: du_set_extra_details.duDataList[t2].type,
                    build_number : du_set_extra_details.duDataList[t2].build_number,
                    build_id : du_set_extra_details.duDataList[t2].build_id,
                    state_id : du_set_extra_details.duDataList[t2].state_id,
                    deployment_field_value :du_set_extra_details.duDataList[t2].deployment_field,
                    du_dependent : du_set_extra_details.duDataList[t2].dependent,
                    package_state_id:du_set_extra_details.duDataList[t2].package_state_id,
                    parent_entity_set_id:du_set_extra_details.duset_id,
                    du_order : du_set_extra_details.duDataList[t2].order,
                    flexible_attributes : du_set_extra_details.duDataList[t2].flexible_attributes
                };
               // $rootScope.deployDUFactory.addDU(du._id.$oid, du.name, du.type, $scope.buildSelectedToDeploy.build_number, $scope.buildSelectedToDeploy.build_id, $scope.deployment_field_value, du.dependent, du.order);
                $rootScope.deployDUFactory.addDU(duDataSet);
                $scope.duSelectedToDeploy = [];
                $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
                $scope.selectedDU.du_name = $scope.duSelectedToDeploy[0].du_name;
                $scope.selectedDU.du_id = $scope.duSelectedToDeploy[0].du_id;
                $scope.selectedDU.build_id = $scope.duSelectedToDeploy[0].build_id;
                $scope.selectedDU.build_number = $scope.duSelectedToDeploy[0].build_number;
                $scope.selectedDU.du_type = $scope.duSelectedToDeploy[0].type;
                $scope.selectedDU.flexible_attributes = $scope.duSelectedToDeploy[0].flexible_attributes;

            }
        }

       /* $scope.duSetDetails = ViewDUSet.get({

            id : du_set_extra_details.duset_id
        },
        function(dusetSuccessResponse)
        {
            for(var t1=0; t1<dusetSuccessResponse.data.du_set_details.length; t1++)
            {
                if(du_set_extra_details.duDataList.length>0)
                {
                    for(var t2=0; t2<du_set_extra_details.duDataList.length; t2++)
                    {
                        if(dusetSuccessResponse.data.du_set_details[t1]._id.$oid === du_set_extra_details.duDataList[t2].du_id)
                        {
                            $scope.duData = dusetSuccessResponse.data.du_set_details[t1];
                            var du = dusetSuccessResponse.data.du_set_details[t1];
                            var duId= du._id.$oid;
                            var duData = du_set_extra_details.duDataList[t2];
                            if(duId === duData.du_id && duData.build_id && duData.state_id)
                            {
                                $scope.buildSelectedToDeploy = {
                                    build_id : duData.build_id,
                                    build_number : duData.build_number,
                                    state_id:duData.state_id
                                };
                                $scope.deployment_field_value = duData.deployment_field;
                                if(duData.package_state_id)
                                {
                                    $scope.package_state_id = duData.package_state_id;
                                }

                            }
                            else if (duId === duData.du_id && duData.build_id && !duData.state_id)
                            {
                                $scope.buildSelectedToDeploy = {
                                    build_id : duData.build_id,
                                    build_number : duData.build_number
                                };
                                $scope.deployment_field_value = dusetSuccessResponse.data.du_set_details[t1].deployment_field;
                            }

                            var duDataSet = {
                                du_id : du._id.$oid,
                                du_name: du.name,
                                du_type: du.type,
                                build_number : $scope.buildSelectedToDeploy.build_number,
                                build_id : $scope.buildSelectedToDeploy.build_id,
                                state_id : $scope.buildSelectedToDeploy.state_id,
                                deployment_field_value :$scope.deployment_field_value,
                                du_dependent : du.dependent,
                                package_state_id:$scope.package_state_id,
                                parent_entity_set_id:du_set_extra_details.duset_id,
                                du_order : du.order,
                                flexible_attributes : du.flexible_attributes
                            };
                           // $rootScope.deployDUFactory.addDU(du._id.$oid, du.name, du.type, $scope.buildSelectedToDeploy.build_number, $scope.buildSelectedToDeploy.build_id, $scope.deployment_field_value, du.dependent, du.order);
                            $rootScope.deployDUFactory.addDU(duDataSet);
                            $scope.duSelectedToDeploy = [];
                            $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
                            $scope.selectedDU.du_name = $scope.duSelectedToDeploy[0].du_name;
                            $scope.selectedDU.du_id = $scope.duSelectedToDeploy[0].du_id;
                            $scope.selectedDU.build_id = $scope.duSelectedToDeploy[0].build_id;
                            $scope.selectedDU.build_number = $scope.duSelectedToDeploy[0].build_number;
                            $scope.selectedDU.du_type = $scope.duSelectedToDeploy[0].type;
                            $scope.selectedDU.flexible_attributes = $scope.duSelectedToDeploy[0].flexible_attributes;
                        }
                    }
                }
            }
        },
        function(errorResponse) {
            $rootScope.handleResponse(errorResponse);
        });*/
    }

    $scope.setMachineTypeCSS = function(machine_type, machine_id)
    {
        var styles = "";
        for(var du=0; du<$scope.duSelectedToDeploy.length; du++)
        {
            if($scope.duSelectedToDeploy[du].du_name === $scope.selectedDU.du_name)
            {
                for(var mac=0; mac<$scope.duSelectedToDeploy[du].requests.length; mac++)
                {
                    if(machine_id === $scope.duSelectedToDeploy[du].requests[mac].machine_id)
                    {
                        styles = styles + "vp-search__item--selected";
                    }
                }
            }
        }
        return styles;
    };

    $scope.removeDU = function(id)
    {
        if($scope.duSelectedToDeploy.length>1)
        {
            $rootScope.deployDUFactory.removeDU(id);
            $scope.selectedDU.du_name = $scope.duSelectedToDeploy[0].du_name;
            $scope.selectedDU.du_id = $scope.duSelectedToDeploy[0].du_id;
            $scope.selectedDU.build_id = $scope.duSelectedToDeploy[0].build_id;
            $scope.selectedDU.build_number = $scope.duSelectedToDeploy[0].build_number;
            if($scope.duSelectedToDeploy[0].requests.length>0)
            {
                $scope.selectedMachine.machine_name = $scope.duSelectedToDeploy[0].requests[0].machine_name;
                $scope.selectedMachine.machine_id = $scope.duSelectedToDeploy[0].requests[0]._id.$oid;
            }
            else
            {
                $scope.selectedMachine.machine_name = '';
            }
        }
        else
        {
            $rootScope.handleResponse('Atleast one DU should be selected for the deployment');
        }
    };

    $scope.getSelectedMachine = function(machine)
    {
        $scope.selectedMachine.machine_name = machine;
    };

    $scope.getSelectedDU = function(du)
    {
        $scope.selectedDU.du_name = $scope.duSelectedToDeploy[du].du_name;
        $scope.selectedDU.du_id = $scope.duSelectedToDeploy[du].du_id;
        $scope.selectedDU.build_id = $scope.duSelectedToDeploy[du].build_id;
        $scope.selectedDU.build_number = $scope.duSelectedToDeploy[du].build_number;
        $scope.selectedDU.flexible_attributes = $scope.duSelectedToDeploy[du].flexible_attributes;
        if($scope.duSelectedToDeploy[du].requests[0])
        {
            $scope.selectedMachine.machine_name = $scope.duSelectedToDeploy[du].requests[0].machine_name;
            $scope.selectedMachine.machine_id = $scope.duSelectedToDeploy[du].requests[0].machine_id;
        }
    };

    $scope.previousMachine = function(machine)
    {
        for(var m1=0;m1<$scope.toolsSelectedToDeploy.length;m1++)
        {
            if($scope.toolsSelectedToDeploy[m1].machine_name===machine)
            {
                if($scope.toolsSelectedToDeploy[m1-1])
                {
                    $scope.selectedMachine.machine_name = $scope.toolsSelectedToDeploy[m1-1].machine_name;
                    $scope.selectedMachine.machine_id = $scope.toolsSelectedToDeploy[m1-1]._id.$oid;
                }
            }
       }
    };

    $scope.nextMachine = function(machine)
    {
        for(var m1=0;m1<$scope.toolsSelectedToDeploy.length;m1++)
        {
            if($scope.toolsSelectedToDeploy[m1].machine_name===machine)
            {
                if($scope.toolsSelectedToDeploy[m1+1])
                {
                    $scope.selectedMachine.machine_name = $scope.toolsSelectedToDeploy[m1+1].machine_name;
                    $scope.selectedMachine.machine_id = $scope.toolsSelectedToDeploy[m1+1]._id.$oid;
                }
            }
       }
    };

    $scope.getFormValidated = function(du, machine)
    {
        var validation_flag = 0;
        var machine_validation_flag = 0;
        for(var d=0; d<$scope.duSelectedToDeploy.length; d++)
        {
            if(du === $scope.duSelectedToDeploy[d].du_name)
            {
                if($scope.duSelectedToDeploy[d].requests.length>0)
                {
                    for(var e=0; e<$scope.duSelectedToDeploy[d].requests.length; e++)
                    {
                        if(machine === $scope.duSelectedToDeploy[d].requests[e].machine_name)
                        {
                            if($scope.duSelectedToDeploy[d].requests[e].du_deployment_value.length>0)
                            {
                                for(var f=0; f<$scope.duSelectedToDeploy[d].requests[e].du_deployment_value.length; f++)
                                {
                                    if($scope.duSelectedToDeploy[d].requests[e].du_deployment_value[f].is_mandatory && $scope.duSelectedToDeploy[d].requests[e].du_deployment_value[f].default_value==='' || $scope.duSelectedToDeploy[d].requests[e].du_deployment_value[f].default_value===undefined)
                                    {
                                        validation_flag++;
                                    }
                                }
                            }
                        }

                    }
                }
                else
                {
                    validation_flag = -1;
                }
            }
        }

        if(validation_flag === -1)
        {
            return 'vp-uielement__toolitem--unknown';
        }
        else if(validation_flag === 0)
        {
            return 'vp-uielement__toolitem--ready';
        }
        else
        {
            return 'vp-uielement__toolitem--error';
        }
    };

    $scope.getDUValidated = function(du, machine)
    {
        var validation_flag = 0;
        var duIndex = 0;
        var requestIndex = 0;
        if($scope.duSelectedToDeploy.length>0)
        {
            for(var d=0; d<$scope.duSelectedToDeploy.length; d++)
            {
                if(du === $scope.duSelectedToDeploy[d].du_name)
                {
                    duIndex = d;
                }
            }

            for(var e=0; e<$scope.duSelectedToDeploy[duIndex].requests.length; e++)
            {
                if(machine === $scope.duSelectedToDeploy[duIndex].requests[e].machine_name)
                {
                    requestIndex = e;
                }
            }

            if($scope.duSelectedToDeploy[duIndex].requests.length>0)
            {
                for(var f=0; f<$scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value.length; f++)
                {
                    if($scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value[f].is_mandatory && $scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value[f].default_value==='' || $scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value[f].default_value===undefined)
                    {
                        validation_flag++;
                    }
                }
            }
            else
            {
                validation_flag = -1;
            }

            if(validation_flag === -1)
            {
                return 'vp-uielement__toolitem--unknown';
            }
            else if(validation_flag === 0)
            {
                return 'vp-uielement__toolitem--ready';
            }
            else
            {
                return 'vp-uielement__toolitem--error';
            }
        }
        else
        {
            return '';
        }
    };

    $scope.showMoreMachines = function()
    {
        if(document.getElementById("more_machine_popup_include").style.display === "none" || document.getElementById("more_machine_popup_include").style.display === "")
        {
            document.getElementById("more_machine_popup_include").style.display = "block";
        }
        else
        {
           document.getElementById("more_machine_popup_include").style.display = "none";
        }
    };

    $scope.showMoreDU = function()
    {
        if(document.getElementById("more_du_popup_include").style.display === "none" || document.getElementById("more_du_popup_include").style.display === "")
        {
            remaining_up();
            $('#more_du_popup_include').slideDown();
        }
        else
        {
           $('#more_du_popup_include').slideUp();
        }
    };

    $scope.showMoreDUToAdd = function()
    {
        if(document.getElementById("more_du_add_popup").style.display === "none" || document.getElementById("more_du_add_popup").style.display === "")
        {
            remaining_up();
            $('#more_du_add_popup').slideDown();
        }
        else
        {
           $('#more_du_add_popup').slideUp();
        }
    };

    $scope.closeDeploymentScheduler = function()
    {
        document.getElementById("deployment_scheduler").style.display = "none";
    };

    $scope.setScheduleType = function(type)
    {
        $scope.deploy_at = type;
    };

    $scope.removeMachine = function(du_name, machine)
    {
        for(var a=0; a<$scope.allMachines.length; a++)
        {
            if($scope.allMachines[a].machine_name === machine)
            {
                $scope.allMachines[a].isSelected = false;
            }
            if(machine==='all')
            {
                $scope.allMachines[a].isSelected = false;
            }
        }

        $rootScope.deployDUFactory.removeMachine(du_name, machine);
        $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
        if(machine==='all')
        {
            $scope.selectedMachine = {
                machine_name : "",
                machine_id : ''
            };
        }
        for(var tIndex=0; tIndex<$scope.duSelectedToDeploy.length; tIndex++)
        {
            if($scope.duSelectedToDeploy[tIndex].du_name === du_name)
            {
                if($scope.duSelectedToDeploy[tIndex].requests.length>0)
                {
                    $scope.selectedMachine.machine_name = $scope.duSelectedToDeploy[tIndex].requests[0].machine_name;
                    $scope.selectedMachine.machine_id = $scope.duSelectedToDeploy[tIndex].requests[0].machine_id;
                }
                else
                {
                    $scope.selectedMachine = {
                        machine_name : "",
                        machine_id : ''
                    };
                }
            }
        }
    };

    $scope.dataDuCountInd = false;

    $scope.addMachine = function(machine, singleSelectedDU, entity,machineGroupData)
    {
        $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
        $scope.duCount = $scope.duSelectedToDeploy.length;
        $rootScope.errorInd = false;
        angular.forEach($scope.duSelectedToDeploy, function(selectedDUValue, key) {

           	if ($scope.skip_deployment === true)
            {
                IsBuildDeployedOnMachine.get({
                    parent_entity_id : selectedDUValue.du_id,
                    machine_id : machine._id.$oid,
                    build_id :  selectedDUValue.build_id
               },
               function(successResponse){
                   if(successResponse.data == null)
                   {
                       $scope.is_build_already_deployed = false;
                       $scope.loadingSymbol(machine,machineGroupData);
                       $scope.addMachineBasedOnBuildAlreadyDeployed($scope.is_build_already_deployed,machine, singleSelectedDU,entity,machineGroupData, selectedDUValue);
                   }
                   else
                   {
                       $scope.is_build_already_deployed = true;
                       $scope.loadingSymbol(machine,machineGroupData);
                       $scope.addMachineBasedOnBuildAlreadyDeployed($scope.is_build_already_deployed,machine, singleSelectedDU,entity,machineGroupData, selectedDUValue);
                   }

               },
               function(errorResponse)
               {
                   $rootScope.handleResponse(errorResponse, selectedDUValue);
               });
            }
        	else
            {
                  $scope.is_build_already_deployed = false;
                  $scope.loadingSymbol(machine,machineGroupData);
                  $scope.addMachineBasedOnBuildAlreadyDeployed($scope.is_build_already_deployed,machine, singleSelectedDU,entity,machineGroupData, selectedDUValue);
            }
          //calling a factory method for FA Matching


        });

        for(var mIndex=0; mIndex<$scope.allMachines.length; mIndex++)
        {
            if($scope.allMachines[mIndex].machine_name === machine.machine_name)
            {
                $scope.allMachines[mIndex].isSelected = true;
            }
        }
    };


    $scope.addMachineBasedOnBuildAlreadyDeployed = function(isBuildDeployed, machine, singleSelectedDU,entity,machineGroupData, selectedDUValue)
    {
        var duMachineMatchInd = false;
        if($scope.machine_matching_ind === true)
        {
            if( $scope.request_type ==="deploy")
            {
                if(entity === 'all')
                {
                    duMachineMatchInd =  $rootScope.faFactory.checkMachineMatch(selectedDUValue,machine);
                }
                else
                {
                    duMachineMatchInd =  $rootScope.faFactory.checkMachineMatch(singleSelectedDU,machine);
                }

                if(duMachineMatchInd === false)
                {
                    $rootScope.errorInd = true;
                }
            }
            else
            {
                duMachineMatchInd = true;
            }

        }
        if($scope.machine_matching_ind === false || duMachineMatchInd === true)
        {
            var machineData = {
               machines : machine,
               du : singleSelectedDU.du_name,
               entity :  entity,
               skip_deployment : false,
               is_build_already_deployed :isBuildDeployed,
               machine_group_id : machineGroupData,
               machineMatchingInd: $scope.machine_matching_ind

            };

            if(isBuildDeployed ===  true)
            {
                if(entity === 'all')
                {
                    machineData.du = selectedDUValue.du_name;
                    machineData.skip_deployment = $scope.skip_deployment;
                    $rootScope.deployDUFactory.addMachine(machineData);

                }
                else
                {
                    machineData.skip_deployment = $scope.skip_deployment;
                    $rootScope.deployDUFactory.addMachine(machineData);
                }
            }
            else
            {
                if(entity === 'all')
                {
                    machineData.du = selectedDUValue.du_name;
                    $rootScope.deployDUFactory.addMachine(machineData);
                }
                else
                {
                    $rootScope.deployDUFactory.addMachine(machineData);
                }
            }
            $scope.selectedMachine.machine_name = machine.machine_name;
            $scope.selectedMachine.machine_id = machine._id.$oid;
        }

    };

    $scope.loadingSymbol = function(machine,getMachineGroupData)
    {
        $scope.duCount --;
        if(getMachineGroupData)
        {
            $scope.tempMachine[machine._id.$oid]=machine._id.$oid;
            if(Object.keys($scope.tempMachine).length < $scope.machineNoCount)
            {
                 $scope.dataDuCountInd = true;
            }
            else if (Object.keys($scope.tempMachine).length === $scope.machineNoCount)
            {
                $scope.dataDuCountInd = true;
                $scope.deploymentCount ++;

                if($scope.deploymentCount === $scope.duSelectedToDeploy.length  )
                {
                    $scope.dataDuCountInd = false;
                    if($rootScope.errorInd === true)
                    {
                        $rootScope.handleResponse('Some machines were not selected as criteria of matching was not fulfilled');
                    }
                }
            }
        }
        else
        {
            if($scope.duCount > 0 )
            {
                 $scope.dataDuCountInd = true;
            }
            else
            {
                $scope.dataDuCountInd = false;
                if($rootScope.errorInd === true)
                {
                    $rootScope.handleResponse('Some machines were not selected as criteria of matching was not fulfilled');
                }
            }
        }

    };

    $scope.setActiveMachineTab = function(machine)
    {
        if(machine === $scope.selectedMachine.machine_name)
        {
            return 'vp-dttabs__tab--active';
        }
        else
        {
            return '';
        }
    };

    if(selectedDU.length>0)
    {
        $scope.request_type = 'deploy';
        deployment_type = 'dugroup';
        /*SkipDeployment.get({
        },
        function(successResponse){
           $scope.skip_deployment = JSON.parse(successResponse.data.skipDeploymentInd);
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });*/

        for(var id_1=0; id_1<selectedDU.length; id_1++)
        {
            var du_id = selectedDU[id_1].id;
            var build_number = selectedDU[id_1].build_number;
            var build_id = selectedDU[id_1].build_id;
            $scope.getDUDetails(du_id, build_number, build_id);
        }
    }

    $scope.showCopySettingsAttention = function()
    {
        if(document.getElementById("copy_attenation_popup").style.display === "none" || document.getElementById("copy_attenation_popup").style.display === "")
        {
            document.getElementById("copy_attenation_popup").style.display = "block";
        }
        else
        {
           document.getElementById("copy_attenation_popup").style.display = "none";
        }
    };

    $scope.closeCopySettingsAttention = function()
    {
        document.getElementById("copy_attenation_popup").style.display = "none";
    };

    $scope.copyToAllMachines = function(du, machine)
    {
        $rootScope.deployDUFactory.copyToAllMachines(du, machine);
        document.getElementById("copy_attenation_popup").style.display = "none";
    };

    $scope.cancelCopy = function()
    {
        document.getElementById("copy_attenation_popup").style.display = "none";
    };

    $scope.restoreDefaultValues = function(du, machine)
    {
        $rootScope.deployDUFactory.restoreDefaultValues(du, machine);
    };

    $scope.copyfieldValueToAllMachines = function(du, machine, fieldIndex)
    {
        $rootScope.deployDUFactory.copyfieldValueToAllMachines(du, machine, fieldIndex);
    };

    $scope.checkIfCopied = function(copyState)
    {
        if(copyState === true)
        {
            return 'vp-machinesform__copyallbtnwrap--done';
        }
        else
        {
            return '';
        }
    };

    $scope.checkIfFieldCopied = function(copyState)
    {
        if(copyState === true)
        {
            return 'vp-machinesform__fieldbtnwrap--done ';
        }
        else
        {
            return '';
        }
    };

    $scope.cancelDeploymentRequest = function()
    {
        $state.go('duDashboard');
    };

    $scope.deploy_on = 'machines';
    $scope.machines = GetAllMachine.get({
    },
    function(machineSucessResponse)
    {
        $scope.allMachines = machineSucessResponse.data.data;
        $scope.machines = machineSucessResponse.data;
        for(var mIndx=0; mIndx<$scope.allMachines.length; mIndx++)
        {
            if($stateParams.machine_id===$scope.allMachines[mIndx]._id.$oid)
            {
                $scope.machines.selected = $scope.allMachines[mIndx];
            }
            $scope.allMachines[mIndx].isSelected = false;
        }

        if($location.path().indexOf('/deploy/du/') >= 0)
        {
                var du_set_extra_details = JSON.parse($stateParams.id);
                selectedDU.push(du_set_extra_details.du_id);
                $scope.request_type="deploy";
                deployment_type = 'dugroup';

                $scope.duDetails = ViewDU.get({
                    id : du_set_extra_details.du_id
                },
                function(response)
                {
                    $scope.duData = response.data;
                    var du = response.data;
                    var du_list_details =[];
                    for (var i=0; i< du_set_extra_details.duDataList.length; i++)
                    {
                        if(du_set_extra_details.duDataList[i].state)
                        {
                            du_list_details.build_number = du_set_extra_details.duDataList[i].build_number;
                            du_list_details.build_id = du_set_extra_details.duDataList[i].build_id;
                            du_list_details.state_id = du_set_extra_details.duDataList[i].state;
                            du_list_details.deployment_field = du_set_extra_details.duDataList[i].deployment_field;

                        }
                        else
                        {
                            du_list_details.build_number = du_set_extra_details.duDataList[i].build_number;
                            du_list_details.build_id = du_set_extra_details.duDataList[i].build_id;
                            du_list_details.deployment_field = response.data.deployment_field;
                        }

                    }
                    var duData = {
                        du_id : du._id.$oid,
                        du_name: du.name,
                        du_type: du.type,
                        build_number : du_list_details.build_number,
                        build_id : du_list_details.build_id,
                        state_id : du_list_details.state_id,
                        deployment_field_value :du_list_details.deployment_field,
                        du_dependent : du.dependent,
                        du_order : du.order,
                        flexible_attributes : du.flexible_attributes
                    };

                    $rootScope.deployDUFactory.addDU(duData);
                    $scope.duSelectedToDeploy = [];
                    $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
                    $scope.selectedDU.du_name = $scope.duSelectedToDeploy[0].du_name;
                    $scope.selectedDU.du_id = $scope.duSelectedToDeploy[0].du_id;
                    $scope.selectedDU.build_id = $scope.duSelectedToDeploy[0].build_id;
                    $scope.selectedDU.build_number = $scope.duSelectedToDeploy[0].build_number;
                    $scope.selectedDU.du_type = $scope.duSelectedToDeploy[0].type;
                    $scope.selectedDU.flexible_attributes = $scope.duSelectedToDeploy[0].flexible_attributes;
                    SkipDeployment.get({
                    },
                    function(successResponse){
                       $scope.skip_deployment = JSON.parse(successResponse.data.skipDeploymentInd);
                    },
                    function(errorResponse)
                    {
                        $rootScope.handleResponse(errorResponse);
                    });

                },
                function(errorResponse)
                {
                    $rootScope.handleResponse(errorResponse);
                });
        }
        else if($stateParams.du_id && $stateParams.machine_id)
        {
            if(($location.path()).indexOf("redeploy") >= 1)
            {
                $scope.request_type="redeploy";
                deployment_type = 'dugroup';
                deployment_type = 'dugroup';
                $scope.duDetails = ViewDU.get({
                    id : $stateParams.du_id+'/machine/'+$stateParams.machine_id
                },
                function(response)
                {
                    $scope.duData = response.data;
                    var du = response.data;
                    $scope.deployment_field_value = response.data.deployment_field;
                    if($stateParams.build_id && $stateParams.build_number)
                    {
                        $scope.buildSelectedToDeploy = {
                            build_id : $stateParams.build_id,
                            build_number : $stateParams.build_number
                        };
                    }
                    else
                    {
                        $scope.buildSelectedToDeploy = {
                            build_id : 0,
                            build_number : 0
                        };
                    }

                     var duData = {
                        du_id : du._id.$oid,
                        du_name: du.name,
                        du_type: du.type,
                        build_number : $scope.buildSelectedToDeploy.build_number,
                        build_id : $scope.buildSelectedToDeploy.build_id,
                        deployment_field_value :$scope.deployment_field_value,
                        du_dependent : du.dependent,
                        du_order : du.order
                    };
                    $rootScope.deployDUFactory.addDU(duData);

                    $scope.duSelectedToDeploy = [];
                    $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
                    $scope.selectedDU.du_name = $scope.duSelectedToDeploy[0].du_name;
                    $scope.selectedDU.du_id = $scope.duSelectedToDeploy[0].du_di;
                    $scope.selectedDU.build_id = $scope.duSelectedToDeploy[0].build_id;
                    $scope.selectedDU.build_number = $scope.duSelectedToDeploy[0].build_number;
                    $scope.selectedDU.du_type = $scope.duSelectedToDeploy[0].type;
                    for(var c=0; c<$scope.allMachines.length; c++)
                    {
                            if($stateParams.machine_id === $scope.allMachines[c]._id.$oid)
                            {
                                $scope.selectedMachine.machine_name = $scope.allMachines[c].machine_name;
                                $scope.selectedMachine.machine_id = $scope.allMachines[c]._id.$oid;
                                $scope.addMachine($scope.allMachines[c], $scope.selectedDU, 'current',undefined, $scope.skip_deployment, $scope.is_build_already_deployed);
                            }
                    }
                },
                function(errorResponse) {
                    $rootScope.handleResponse(errorResponse);
                });
            }
            else if(($location.path()).indexOf("undeploy") >= 1)
            {
                $scope.request_type="undeploy";
                deployment_type = 'dugroup';
                deployment_type = 'dugroup';
                $scope.duDetails = ViewDU.get({
                    id : $stateParams.du_id+'/machine/'+$stateParams.machine_id
                },
                function(response)
                {
                    $scope.duData = response.data;
                    var du = response.data;
                    $scope.deployment_field_value = response.data.deployment_field;
                    if($stateParams.build_id && $stateParams.build_number)
                    {
                        $scope.buildSelectedToDeploy = {
                            build_id : $stateParams.build_id,
                            build_number : $stateParams.build_number
                        };
                    }
                    else
                    {
                        $scope.buildSelectedToDeploy = {
                            build_id : 0,
                            build_number : 0
                        };
                    }
                    var duData = {
                        du_id : du._id.$oid,
                        du_name: du.name,
                        du_type: du.type,
                        build_number : $scope.buildSelectedToDeploy.build_number,
                        build_id : $scope.buildSelectedToDeploy.build_id,
                        deployment_field_value :$scope.deployment_field_value,
                        du_dependent : du.dependent,
                        du_order : du.order
                    };
                    $rootScope.deployDUFactory.addDU(duData);

                    //$rootScope.deployDUFactory.addDU(du._id.$oid, du.name, du.type, $scope.buildSelectedToDeploy.build_number, $scope.buildSelectedToDeploy.build_id, $scope.deployment_field_value, du.dependent, du.order);

                    $scope.duSelectedToDeploy = [];
                    $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
                    $scope.selectedDU.du_name = $scope.duSelectedToDeploy[0].du_name;
                    $scope.selectedDU.du_id = $scope.duSelectedToDeploy[0].du_id;
                    $scope.selectedDU.build_id = $scope.duSelectedToDeploy[0].build_id;
                    $scope.selectedDU.build_number = $scope.duSelectedToDeploy[0].build_number;
                    $scope.selectedDU.du_type = $scope.duSelectedToDeploy[0].type;
                    for(var c=0; c<$scope.allMachines.length; c++)
                    {
                            if($stateParams.machine_id === $scope.allMachines[c]._id.$oid)
                            {
                                $scope.selectedMachine.machine_name = $scope.allMachines[c].machine_name;
                                $scope.selectedMachine.machine_id = $scope.allMachines[c]._id.$oid;
                                $scope.addMachine($scope.allMachines[c], $scope.selectedDU, "current", undefined, $scope.skip_deployment, $scope.is_build_already_deployed);
                            }
                    }
                },
                function(errorResponse) {
                    $rootScope.handleResponse(errorResponse);
                });
            }
        }

        if($location.path().indexOf('/revert/du/') >= 0)
        {
            var du_revert_details = JSON.parse($stateParams.id);
            $scope.request_type="revert";
            deployment_type = 'dugroup';
            angular.forEach(du_revert_details.duDataList, function(selectedDUValue, key)
            {
                $scope.duDetails = ViewDU.get({
                id : selectedDUValue.du_id,
                machine : selectedDUValue.machine_id
                },
                function(successResponse)
                {
                    if(selectedDUValue.du_id === successResponse.data._id.$oid)
                    {
                        $scope.duSuccessfulData = successResponse.data;
                        var duId= $scope.duSuccessfulData._id.$oid;
                        var duPassedRevertedData = selectedDUValue;
                        if(duId === duPassedRevertedData.du_id && duPassedRevertedData.new_build_id && duPassedRevertedData.new_state_id)
                        {
                            $scope.buildSelectedToDeploy = {
                                build_id : duPassedRevertedData.new_build_id,
                                build_number : duPassedRevertedData.new_build_number,
                                state_id:duPassedRevertedData.new_state_id
                            };
                            $scope.deployment_field_value = duPassedRevertedData.deployment_field;
                            if(duPassedRevertedData.package_state_id)
                            {
                                $scope.package_state_id = duPassedRevertedData.package_state_id;
                            }
                        }
                        else if(duId === duPassedRevertedData.du_id && duPassedRevertedData.new_build_id && !duPassedRevertedData.new_state_id)
                        {
                            $scope.buildSelectedToDeploy = {
                                build_id : duPassedRevertedData.new_build_id,
                                build_number : duPassedRevertedData.new_build_number
                            };
                            $scope.deployment_field_value = $scope.duSuccessfulData.deployment_field;
                        }
                        var duData = {
                            du_id : $scope.duSuccessfulData._id.$oid,
                            du_name: $scope.duSuccessfulData.name,
                            du_type: $scope.duSuccessfulData.type,
                            build_number : $scope.buildSelectedToDeploy.build_number,
                            build_id : $scope.buildSelectedToDeploy.build_id,
                            state_id : $scope.buildSelectedToDeploy.state_id,
                            deployment_field_value :$scope.deployment_field_value,
                            package_state_id:$scope.package_state_id,
                            du_dependent : $scope.duSuccessfulData.dependent,
                            du_order : $scope.duSuccessfulData.order,
                            old_build_id : duPassedRevertedData.previous_build_id,
                            old_build_number : duPassedRevertedData.previous_build_number,
                            parent_entity_set_id : duPassedRevertedData.parent_entity_set_id
                        };
                        $rootScope.deployDUFactory.addDU(duData);
                        $scope.duSelectedToDeploy = [];
                        $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
                        var index = $scope.duSelectedToDeploy.length-1;
                        $scope.selectedDU.du_name = $scope.duSelectedToDeploy[index].du_name;
                        $scope.selectedDU.du_id = $scope.duSelectedToDeploy[index].du_id;
                        $scope.selectedDU.build_id = $scope.duSelectedToDeploy[index].build_id;
                        $scope.selectedDU.build_number = $scope.duSelectedToDeploy[index].build_number;
                        $scope.selectedDU.du_type = $scope.duSelectedToDeploy[index].type;
                        for(var c=0; c<$scope.allMachines.length; c++)
                        {
                            for (var d=0; d<duPassedRevertedData.machine_id.length; d++)
                            {
                                if(duPassedRevertedData.machine_id[d] === $scope.allMachines[c]._id.$oid)
                                {
                                    $scope.selectedMachine.machine_name = $scope.allMachines[c].machine_name;
                                    $scope.selectedMachine.machine_id = $scope.allMachines[c]._id.$oid;
                                    var machineData = {
                                       machines : $scope.allMachines[c],
                                       du : $scope.selectedDU.du_name,
                                       entity :  "current"
                                    };
                                    $rootScope.deployDUFactory.addMachine(machineData);
                                    //$scope.addMachine($scope.allMachines[c], $scope.selectedDU, "current",undefined, $scope.skip_deployment, $scope.is_build_already_deployed);
                                }
                            }
                        }
                    }
                },
                function(errorResponse) {
                   $rootScope.handleResponse(errorResponse);
                });
            });

        }

        if($stateParams.request_id)
        {
            $scope.request_type="deploy";
            deployment_type = 'dugroup';
            ViewSavedDeploymentRequest.get({
                id : $stateParams.request_id
            },
            function(viewSavedDeploymentRequestsSuccessReponse)
            {
                $scope.savedRequestData = viewSavedDeploymentRequestsSuccessReponse.data.data;
                $rootScope.deployDUFactory.cloneRequestObject($scope.savedRequestData);
                $scope.toolsSelectedToDeploy = [];
                $scope.allVersions = [];
                $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
                $scope.selectedDU.du_name = $scope.duSelectedToDeploy[0].du_name;
                $scope.selectedDU.du_id = $scope.duSelectedToDeploy[0].du_id;
                $scope.selectedDU.build_id = $scope.duSelectedToDeploy[0].build_id;
                $scope.selectedDU.build_number = $scope.duSelectedToDeploy[0].build_number;
                var du_name = $scope.selectedDU.du_name;
                $scope.selectedMachine.machine_name = $scope.duSelectedToDeploy[0].requests[0].machine_name;
                $scope.selectedMachine.machine_id = $scope.duSelectedToDeploy[0].requests[0]._id.$oid;

            },
            function(viewSavedDeploymentRequestsErrorReponse)
            {
                $rootScope.handleResponse(viewSavedDeploymentRequestsErrorReponse);
            });
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.warning_flag = true;
    $scope.start_status=false;
    $scope.stop_status=true;
    $scope.isFormVisible = false;
    $scope.isStatusVisible = false;
    $scope.dropdown = [];
    $scope.machine_group = {
        selected : ''
    };
    var promise;

    $scope.requestForm=true;
    $scope.requestStatusMessages=[];
    $scope.ticket = new Ticket();
    $scope.requestSubmitted=false;
    $scope.responseRec= false;
    $scope.deploy_at = 'now';

    $scope.showScheduleDeployment = function()
    {
        if(document.getElementById("deployment_scheduler").style.display === "none" || document.getElementById("deployment_scheduler").style.display === "")
        {
            document.getElementById("deployment_scheduler").style.display = "block";
        }
        else
        {
           document.getElementById("deployment_scheduler").style.display = "none";
        }
    };

    $scope.scheduleDeployment = function(time)
    {
        document.getElementById("deployment_scheduler").style.display = "none";
        if($scope.deploy_at === 'now')
        {
            $scope.scheduledDateISO = $scope.currentServerTime.CurrentTime;
        }
        else
        {
            $scope.scheduled_time = new Date(time);
            $scope.scheduled_timestamp = $scope.scheduled_time.toISOString();
        }
    };

    $scope.testConnection = function(form)
    {
        var testMachineData = {};
        if($scope.request_type==='deploy')
        {
            $scope.machine = $scope.deployReqForm.target_machine.$viewValue;
            for(var m=0; m<$scope.machine.length; m++)
            {
                $scope.result = "";
                testMachineData.machine_name = $scope.machine[m].machine_name;
                testMachineData.machine_id = $scope.machine[m].machine_id;
                testMachineData.host = $scope.machine[m].host;
                testMachineData.username = $scope.machine[m].username;
                testMachineData.password = $scope.machine[m].password;
                testMachineData.ip = $scope.machine[m].ip;
                testMachineData.machine_type = $scope.machine[m].machine_type;
                $scope.result = $scope.testMachineConnection(testMachineData);
                if($scope.result==='failed')
                {
                    break;
                }
            }
        }
        else
        {
            testMachineData = $scope.machines.selected;
            $scope.result = $scope.testMachineConnection(testMachineData);
        }
    };

    $scope.testMachineConnection = function(testMachineData)
    {
        TestMachine.save (testMachineData, function (testMachineSuccessResponse){
            $scope.connectionResponse = testMachineSuccessResponse.result;
            $rootScope.handleResponse(testMachineSuccessResponse);
        },
        function(testMachineErrorResponse){
            $scope.connectionResponse = testMachineErrorResponse.data.result;
            $rootScope.handleResponse(testMachineErrorResponse);
        });
        return $scope.connectionResponse;
    };

    $scope.MachineGroups = MachineGroup.get({
    },
    function(successResponse){
        $scope.MachineGroups = successResponse.data.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.uploadDeploymentFields = function(du, machine)
    {
        var file = $scope.fileToImport;
        if(file)
        {
            var uploadUrl = "/deploymentrequest/deploymentfield/upload";
            deploymentFieldFileUpload.uploadFileToUrl(file, uploadUrl, 'du', du, machine, function(){
            });
            $scope.duSelectedToDeploy = $rootScope.deployDUFactory.getDU();
        }
    };

    $scope.addToInputValue = function(input_name, value)
    {
        var duIndex = 0;
        var requestIndex = 0;
        var fieldIndex = 0;
        for(var d=0;  d<$scope.duSelectedToDeploy.length; d++)
        {
            if($scope.duSelectedToDeploy[d].du_name === $scope.selectedDU.du_name)
            {
                duIndex = d;
                for(var e=0;  e<$scope.duSelectedToDeploy[d].requests.length; e++)
                {
                    if($scope.duSelectedToDeploy[d].requests[e].machine_name === $scope.selectedMachine.machine_name)
                    {
                        requestIndex = e;
                        for(var f=0;  f<$scope.duSelectedToDeploy[d].requests[e].du_deployment_value.length; f++)
                        {
                            if($scope.duSelectedToDeploy[d].requests[e].du_deployment_value[f].input_name === input_name)
                            {
                                fieldIndex = f;
                            }
                        }
                    }
                }
            }
        }

        if($scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value[fieldIndex].input_value)
        {
            var result = $.inArray(value, $scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value[fieldIndex].input_value);
            if(result < 0)
            {
                $scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value[fieldIndex].input_value.push(value);
            }
            else
            {
                $scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value[fieldIndex].input_value.splice(result, 1);
            }
        }
    };

    $scope.isFieldSelected = function(fieldName, fieldValue)
    {
        var duIndex = 0;
        var requestIndex = 0;
        var fieldIndex = 0;
        for(var d=0;  d<$scope.duSelectedToDeploy.length; d++)
        {
            if($scope.duSelectedToDeploy[d].du_name === $scope.selectedDU.du_name)
            {
                duIndex = d;
                for(var e=0;  e<$scope.duSelectedToDeploy[d].requests.length; e++)
                {
                    if($scope.duSelectedToDeploy[d].requests[e].machine_name === $scope.selectedMachine.machine_name)
                    {
                        requestIndex = e;
                        for(var f=0;  f<$scope.duSelectedToDeploy[d].requests[e].du_deployment_value.length; f++)
                        {
                            if($scope.duSelectedToDeploy[d].requests[e].du_deployment_value[f].input_name === fieldName)
                            {
                                fieldIndex = f;
                            }
                        }
                    }
                }
            }
        }

        if($scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value[fieldIndex].default_value)
        {
            var result = $.inArray(fieldValue, $scope.duSelectedToDeploy[duIndex].requests[requestIndex].du_deployment_value[fieldIndex].default_value);
            if(result < 0)
            {
                return false;
            }
            else
            {
                return true;
            }
        }
    };

    $scope.sendDeploymentRequest = function(form, deploymentParam)
    {
        if($scope.deploy_at === 'now')
        {
            $scope.scheduledDateISO = $scope.currentServerTime.CurrentTime;
            console.log($scope.scheduledDateISO);
        }
        else
        {
            $scope.scheduledDateISO = $scope.scheduled_timestamp;
        }
        $scope.isFormVisible=true;
        $scope.isStatusVisible=true;
        $scope.requestSubmitted=true;
        $scope.responseRec= false;
        $scope.requestSubmissionStatus= "Request is being sent to Server";
        $scope.requestForm=true;
        $scope.userData = $rootScope.userFactory.getUserDetails();
        console.log($scope.userData.user);
        var jsonData = {
            deployment_requests : []
        };
        var formData = $("form").serializeArray();
        var du_deployment_value =[];

        for(var a=0; a<$scope.duSelectedToDeploy.length; a++)
        {
            var du_name = $scope.duSelectedToDeploy[a].du_name;
            var du_id = $scope.duSelectedToDeploy[a].du_id;
            var dependent = $scope.duSelectedToDeploy[a].dependent;
            var order = $scope.duSelectedToDeploy[a].order;
            var deployment_field_values = [];
            var requests = [];
            if($scope.duSelectedToDeploy[a].requests.length === 0)
            {
                $rootScope.handleResponse("Please select machine for DU "+$scope.duSelectedToDeploy[a].du_name);
                return false;
            }
            else
            {
                for(var b=0; b<$scope.duSelectedToDeploy[a].requests.length; b++)
                {
                    var deployment_fields = [];
                    deployment_field_values = [];
                    angular.copy($scope.duSelectedToDeploy[a].requests[b].du_deployment_value, deployment_fields);
                    if($scope.request_type!== 'deploy')
                    {
                        $scope.duSelectedToDeploy[a].requests[b].skip_deployment = false;
                    }
                    if($scope.request_type!=='undeploy')
                    {
                        if(deployment_fields.length > 0)
                        {
                            for(var c=0; c<deployment_fields.length; c++)
                            {
                                if((deployment_fields[c].is_mandatory === true || deployment_fields[c].is_mandatory === 'true') && (deployment_fields[c].input_type === 'email'))
                                {
                                    if(deployment_fields[c].default_value)
                                    {
                                        var support = deployment_fields[c].default_value;
                                        var atpos = support.indexOf("@");
                                        var dotpos = support.lastIndexOf(".");
                                        if (atpos<1 || dotpos<atpos+2 || dotpos+2>=support.length) {
                                            $rootScope.handleResponse('Please enter valid email address!');
                                            return false;
                                        }
                                    }
                                }
                                else if((deployment_fields[c].is_mandatory === true || deployment_fields[c].is_mandatory === 'true') && (deployment_fields[c].input_type !== 'checkbox') && (deployment_fields[c].default_value === null || deployment_fields[c].default_value === undefined || deployment_fields[c].default_value === '' || (!deployment_fields[c].default_value)) && ($scope.request_type!=='undeploy'))
                                {
                                    $rootScope.handleResponse('Field '+deployment_fields[c].input_name+' in du '+$scope.duSelectedToDeploy[a].requests[b].du_name+' for machine '+$scope.duSelectedToDeploy[a].requests[b].machine_name+' can not be empty!');
                                    return false;
                                }
                                else if((deployment_fields[c].is_mandatory === true || deployment_fields[c].is_mandatory === 'true') && (deployment_fields[c].input_type === 'checkbox') && (deployment_fields[c].input_value === null || deployment_fields[c].input_value === undefined || deployment_fields[c].input_value === '' || deployment_fields[c].input_value.length === 0 || (!deployment_fields[c].input_value)) && ($scope.request_type!=='undeploy'))
                                {
                                    $rootScope.handleResponse('Field '+deployment_fields[c].input_name+' in du '+$scope.duSelectedToDeploy[a].requests[b].du_name+' for machine '+$scope.duSelectedToDeploy[a].requests[b].machine_name+' can not be empty!');
                                    return false;
                                }
                                else if((deployment_fields[c].is_mandatory === true || deployment_fields[c].is_mandatory === 'true') && (deployment_fields[c].input_type === 'date') && (deployment_fields[c].default_value === null || deployment_fields[c].default_value === undefined || deployment_fields[c].default_value === '' || (!deployment_fields[c].default_value) || (isNaN(deployment_fields[c].default_value.getTime()))) && ($scope.request_type!=='undeploy'))
                                {
                                    $rootScope.handleResponse('Field '+deployment_fields[c].input_name+' in du '+$scope.duSelectedToDeploy[a].requests[b].du_name+' for machine '+$scope.duSelectedToDeploy[a].requests[b].machine_name+' can not be empty!');
                                    return false;
                                }
                             }

                            for(var d=0; d<deployment_fields.length; d++)
                            {
                            if(((!deployment_fields[d].is_mandatory) || deployment_fields[d].is_mandatory === false || deployment_fields[d].is_mandatory === 'false') && (deployment_fields[d].input_type === 'checkbox') && (deployment_fields[d].input_value === null || deployment_fields[d].input_value === undefined || deployment_fields[d].input_value === '' || deployment_fields[d].input_value.length === 0 || (!deployment_fields[d].input_value)) && ($scope.request_type!=='undeploy'))
                            {
                                deployment_fields.splice(d, 1);
                                if(d > 0)
                                {
                                    d = d-1;
                                }
                                else
                                {
                                    d = 0;
                                }
                            }
                            if(((!deployment_fields[d].is_mandatory) || deployment_fields[d].is_mandatory === false || deployment_fields[d].is_mandatory === 'false') && (deployment_fields[d].input_type !== 'checkbox') && (deployment_fields[d].default_value === null || deployment_fields[d].default_value === undefined || deployment_fields[d].default_value === '' || (!deployment_fields[d].default_value)) && ($scope.request_type!=='undeploy'))
                            {
                                deployment_fields.splice(d, 1);
                                if(d > 0)
                                {
                                    d = d-1;
                                }
                                else
                                {
                                    d = 0;
                                }
                            }
                            if(((!deployment_fields[d].is_mandatory) || deployment_fields[d].is_mandatory === false || deployment_fields[d].is_mandatory === 'false') && (deployment_fields[d].input_type === 'date') && (deployment_fields[d].default_value === null || deployment_fields[d].default_value === undefined || deployment_fields[d].default_value === '' || (!deployment_fields[d].default_value) || (isNaN(deployment_fields[d].default_value.getTime()))) && ($scope.request_type!=='undeploy'))
                            {
                                deployment_fields.splice(d, 1);
                                if(d > 0)
                                {
                                    d = d-1;
                                }
                                else
                                {
                                    d = 0;
                                }
                            }
                        }

                            for(var e=0; e<deployment_fields.length; e++)
                            {
                            if(deployment_fields[e].input_type === 'checkbox')
                            {
                                deployment_field_values.push({"input_name":deployment_fields[e].input_name, "input_type":deployment_fields[e].input_type, "input_value":deployment_fields[e].input_value.toString(), "order_id":deployment_fields[e].order_id});
                            }
                            else
                            {
                                deployment_field_values.push({"input_name":deployment_fields[e].input_name, "input_type":deployment_fields[e].input_type, "input_value":deployment_fields[e].default_value, "order_id":deployment_fields[e].order_id});
                            }
                        }
                        }
                    }
                    requests.push({'machine_id' : $scope.duSelectedToDeploy[a].requests[b].machine_id, 'tool_deployment_value' : deployment_field_values, 'warning_flag' : $scope.duSelectedToDeploy[a].requests[b].warning_flag, 'skip_dep_ind' : $scope.duSelectedToDeploy[a].requests[b].skip_deployment,'check_matching_ind' :$scope.duSelectedToDeploy[a].requests[b].machineMatchingInd,'machine_group_id':$scope.duSelectedToDeploy[a].requests[b].machine_group_id }); //eitan added skip deployment ind to the json request
                }
                if($scope.request_type === 'revert')
                {
                    jsonData.deployment_requests.push({'parent_entity_id' : du_id, 'requested_by' : $rootScope.userProfile.userData.user, 'request_type' : $scope.request_type, 'deployment_type' : deployment_type, 'requests' : requests, 'dependent' : dependent, 'deployment_order' : order, 'scheduled_date' : $scope.scheduledDateISO, 'previous_build_id' : $scope.duSelectedToDeploy[a].old_build_id, 'previous_build_number' : $scope.duSelectedToDeploy[a].old_build_number, 'build_number' : $scope.duSelectedToDeploy[a].build_number, 'build_id' : $scope.duSelectedToDeploy[a].build_id,
                    'state_id' : $scope.duSelectedToDeploy[a].state_id,'package_state_id' : $scope.duSelectedToDeploy[a].package_state_id,'parent_entity_set_id' : $scope.duSelectedToDeploy[a].parent_entity_set_id});
                }
                else
                {
                    /*if(($scope.duSelectedToDeploy.length===1) && ($scope.duSelectedToDeploy[a].build_id !==0))
                    {
                        jsonData.deployment_requests.push({'parent_entity_id' : du_id, 'requested_by' : $rootScope.userProfile.userData.user, 'request_type' : $scope.request_type, 'deployment_type' : deployment_type, 'requests' : requests, 'dependent' : dependent, 'deployment_order' : order, 'scheduled_date' : $scope.scheduledDateISO, 'build_number' : $scope.duSelectedToDeploy[a].build_number, 'build_id' : $scope.duSelectedToDeploy[a].build_id});
                    }*/
                    if ($scope.duSelectedToDeploy[a].build_id && $scope.duSelectedToDeploy[a].build_number)
                    {
                        jsonData.deployment_requests.push({'parent_entity_id' : du_id, 'requested_by' : $rootScope.userProfile.userData.user, 'request_type' : $scope.request_type, 'deployment_type' : deployment_type, 'requests' : requests, 'dependent' : dependent, 'deployment_order' : order, 'scheduled_date' : $scope.scheduledDateISO, 'build_number' : $scope.duSelectedToDeploy[a].build_number, 'build_id' : $scope.duSelectedToDeploy[a].build_id,'state_id' : $scope.duSelectedToDeploy[a].state_id,'package_state_id' : $scope.duSelectedToDeploy[a].package_state_id,'parent_entity_set_id' : $scope.duSelectedToDeploy[a].parent_entity_set_id});
                    }/*
                    else
                    {
                    jsonData.deployment_requests.push({'parent_entity_id' : du_id, 'requested_by' : $rootScope.userProfile.userData.user, 'request_type' : $scope.request_type, 'deployment_type' : deployment_type, 'requests' : requests, 'dependent' : dependent, 'deployment_order' : order, 'scheduled_date' : $scope.scheduledDateISO});
                    }*/
                }
            }
        }

        $scope.requestSubmitted = true;
        $scope.responseRec = false;
        if(deploymentParam === 'deploy')
        {
            $scope.requestSubmissionStatus =  Ticket.save (jsonData, function (response) {
                $scope.responseID = response.data.id;
                $state.go('runningServiceDUDashboard', {'request_id' : response.data.id});
                $rootScope.handleResponse(response);
                $rootScope.selectedDU = [];
                selectedDU = [];
                $scope.selectedDU = {
                    du_name : '',
                    du_type : '',
                    du_id : '',
                    build_id : '',
                    build_number : ''
                };
                $scope.duSelectedToDeploy = [];
                $scope.selectedMachine = {
                    machine_name : "",
                    machine_id : ''
                };
            },
            function(errorResponse) {
                $scope.errorAdd="true";
                $rootScope.handleResponse(errorResponse);
            });
        }
        else
        {
            var savedData = {
                _id : {
                    oid : ''
                },
                status : 'saved',
                deployment_type : 'dugroup',
                    data : []
            };
            savedData.data = $scope.duSelectedToDeploy;
            if($stateParams.request_id)
            {
                savedData._id.oid = $stateParams.request_id;
                EditSavedDeploymentRequest.update (savedData, function (response) {
                    $scope.responseMessage = response;
                    $scope.responseRec= true;
                    $scope.requestForm = false;
                    $scope.requestStatusMessages.push(response.message);
                    $state.go('duDashboard');
                    $rootScope.handleResponse(response);
                    $rootScope.selectedDU = [];
                    selectedDU = [];
                    $scope.selectedDU = {
                        du_name : '',
                        du_type : '',
                        du_id : ''
                    };
                    $scope.duSelectedToDeploy = [];
                    $scope.selectedMachine = {
                        machine_name : "",
                        machine_id : ''
                    };
                },
                function(errorResponse) {
                    $scope.errorAdd="true";
                    $rootScope.handleResponse(errorResponse);
                });
            }
            else
            {
                delete savedData.status;
                delete savedData._id;
                SaveDeploymentRequest.save(savedData, function (response) {
                    $scope.responseMessage = response;
                    $scope.responseRec= true;
                    $scope.requestForm = false;
                    $scope.requestStatusMessages.push(response.message);
                    $state.go('duDashboard');
                    $rootScope.handleResponse(response);
                    $rootScope.selectedDU = [];
                    selectedDU = [];
                    $scope.selectedDU = {
                        du_name : '',
                        du_type : '',
                        du_id: ''
                    };
                    $scope.duSelectedToDeploy = [];
                    $scope.selectedMachine = {
                        machine_name : "",
                        machine_id : ''
                    };
                },
                function(errorResponse) {
                    $scope.errorAdd="true";
                    $rootScope.handleResponse(errorResponse);
                });
            }
        }
    };
});
});