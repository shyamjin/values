define(['angular', 'uiRouter', 'ngCookies', 'moment', 'humanizeDuration', 'angularTimer', 'jquery', 'toolTips', 'authenticationServicesApp', 'toolServicesApp', 'machineServicesApp', 'deploymentServicesApp','deploymentPartialControllerApp'],function (app) {
  'use strict';

var deployToolControllerApp = angular.module('deployToolControllerApp', ['ui.router', '720kb.tooltips', 'authenticationServicesApp', 'toolServicesApp', 'machineServicesApp', 'deploymentServicesApp', 'timer','deploymentPartialControllerApp']);

deployToolControllerApp.controller('DeployToolController', function ($scope, $location, $rootScope, $state, GetAllTools, GetToolByID, $stateParams, Ticket, $interval, TicketStatus, $timeout, DeployTool, GetAllMachine, Machine, MachineGroup, GetCurrentServerTime, ToolSetByID, MachineGroupView, SaveDeploymentRequest, ViewSavedDeploymentRequest, deploymentFieldFileUpload, EditSavedDeploymentRequest, SkipDeployment, IsBuildDeployedOnMachine) {
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
    $scope.scheduled_timestamp = new Date();
    var selectedTools = [];
    $scope.toolList = [];
    $scope.deploy_on = 'machine';
    $scope.toolsSelectedToDeploy = [];
    var deployment_type;
    $scope.deploy_on = 'machines';
    $scope.warning_flag = true;
    $scope.dropdown = [];
    $scope.machine_group = {
        selected : ''
    };
    var promise;
    $scope.requestStatusMessages = [];
    $scope.deploy_at = 'now';
    $scope.selectedTool = {
        tool_name : '',
        version_number : ''
    };
    $scope.selectedMachine = {
        machine_name : "",
        machine_id : ''
    };

    var toolData = {
        tool_id : '',
        tool_name : '',
        version_id : '',
        version_name : '',
        version_number : '',
        deployment_fields : [],
        build_id : '',
        build_number : ''
    };

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

    function remaining_up()
    {
        var allElements = document.getElementsByClassName('tag_popup');
        for(var i = 0; i < allElements.length; i++)
        {
            $(allElements[i]).slideUp();
        }
    }

    if($stateParams.tools)
    {
        selectedTools = JSON.parse($stateParams.tools);
        if(!angular.isArray(selectedTools))
        {
            selectedTools = selectedTools.split(",");
        }
    }

    if($stateParams.toolset_id)
    {
        deployment_type = 'toolsetgroup';
        $scope.toolSetDetails = ToolSetByID.get({
            id : $stateParams.toolset_id
        },
        function(toolsetSuccessResponse)
        {
            for(var t1=0; t1<toolsetSuccessResponse.data.tool_set.length; t1++)
            {
                selectedTools.push(toolsetSuccessResponse.data.tool_set[t1].version_id);
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    }

    SkipDeployment.get({
    },
    function(successResponse){
        $scope.skip_deployment = JSON.parse(successResponse.data.skipDeploymentInd);
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    MachineGroup.get({
    },
    function(successResponse)
    {
        $scope.machineGroups = successResponse.data.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.setDeployOnValue = function(value)
    {
        $scope.deploy_on = value;
    };

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
        function(successResponse)
        {
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
                        $scope.addMachine($scope.allMachines[b], tool_name, entity,$scope.machineGroupData.group_id, $scope.skip_deployment, $scope.is_build_already_deployed) ;
                    }
                }
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    GetAllTools.get({
        id: "all",
        status: "active,indevelopment,deprecated",
        page: 0,
        perpage: 0
    },
    function(toolViewSuccessResponse,headers)
    {
        $scope.applications = toolViewSuccessResponse.data.data;
        for(var t1=0; t1<toolViewSuccessResponse.data.data.length; t1++)
        {
            for(var t2=0; t2<toolViewSuccessResponse.data.data[t1].versions.length; t2++)
            {
                $scope.toolList.push({'tool_id' : toolViewSuccessResponse.data.data[t1]._id.$oid, 'tool_name' : toolViewSuccessResponse.data.data[t1].name, 'version_id' : toolViewSuccessResponse.data.data[t1].versions[t2].version_id, 'version_name' : toolViewSuccessResponse.data.data[t1].versions[t2].version_name, 'version_number' : toolViewSuccessResponse.data.data[t1].versions[t2].version_number, 'build_number' : toolViewSuccessResponse.data.data[t1].versions[t2].latest_build_number, 'build_id' : toolViewSuccessResponse.data.data[t1].versions[t2].latest_build_id});
            }
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.isToolSelected = function(tool)
    {
        var flag = 0;
        for(var j=0; j<$scope.toolsSelectedToDeploy.length; j++)
        {
            if(tool.version_id === $scope.toolsSelectedToDeploy[j].version_id)
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

    $scope.isMachineSelectedForThisTool = function(tool_name, machine_id)
    {
        for(var tool=0; tool<$scope.toolsSelectedToDeploy.length; tool++)
        {
            if(tool_name === $scope.toolsSelectedToDeploy[tool].tool_name)
            {
                for(var mac=0; mac<$scope.toolsSelectedToDeploy[tool].requests.length; mac++)
                {
                    if($scope.toolsSelectedToDeploy[tool].requests[mac].machine_id = machine_id)
                    {
                        return true;
                    }
                    else
                    {
                        return false;
                    }
                }
            }
            else
            {
                return false;
            }
        }
    };

    $scope.addMoreTools = function(tool)
    {
        for(var k=0; k<$scope.toolsSelectedToDeploy.length; k++)
        {
            if(tool.tool_name === $scope.toolsSelectedToDeploy[k].tool_name)
            {
                $scope.newVersionNumber = tool.version_number;
                $scope.newVersionName = tool.version_name;
                $scope.newVersionId = tool.version_id;
                $scope.changeToolIndex = k;
                $scope.oldToolVersion = $scope.toolsSelectedToDeploy[k].version_number;
                $scope.duplicateTool = $scope.toolsSelectedToDeploy[k].tool_name;
                $('#show_changeTool_version_warning').show(700);
            }
            else
            {
                $scope.getToolDetails(tool.version_id, tool.build_number, tool.build_id);
            }
        }
    };

    $scope.cancelToolSelection = function()
    {
        $('#show_changeTool_version_warning').hide(700);
    };

    $scope.changeToolVersion = function()
    {
        $('#show_changeTool_version_warning').hide(700);
        $scope.getToolDetails($scope.newVersionId);
        $scope.removeTool($scope.changeToolIndex);
    };

    $scope.removeTool = function(id)
    {
        if($scope.toolsSelectedToDeploy.length>1)
        {
            $rootScope.deployToolFactory.removeTool(id);
            $scope.selectedTool.tool_name = $scope.toolsSelectedToDeploy[0].tool_name;
            if($scope.toolsSelectedToDeploy[0].requests.length>0)
            {
                $scope.selectedMachine.machine_name = $scope.toolsSelectedToDeploy[0].requests[0].machine_name;
                $scope.selectedMachine.machine_id = $scope.toolsSelectedToDeploy[0].requests[0]._id.$oid;
            }
            else
            {
                $scope.selectedMachine.machine_name = '';
                $scope.selectedMachine.machine_id = '';
            }
        }
        else
        {
            $rootScope.handleResponse('Atleast one tool should be selected for the deployment');
        }
    };

    $scope.selectVersion = function(tool_name, version_id, version_name, version_number)
    {
        $rootScope.deployToolFactory.selectVersion(tool_name, version_id, version_name, version_number);
    };

    $scope.getSelectedMachine = function(machine)
    {
        $scope.selectedMachine.machine_name = machine;
    };

    $scope.getSelectedTool = function(tool, version)
    {
        $scope.selectedTool.tool_name = $scope.toolsSelectedToDeploy[tool].tool_name;
        $scope.selectedTool.version_number = $scope.toolsSelectedToDeploy[tool].version_number;
        $scope.selectedTool.build_id = $scope.toolsSelectedToDeploy[tool].build_id;
        $scope.selectedTool.build_number = $scope.toolsSelectedToDeploy[tool].build_number;
        if($scope.toolsSelectedToDeploy[tool].requests[0])
        {
            $scope.selectedMachine.machine_name = $scope.toolsSelectedToDeploy[tool].requests[0].machine_name;
            $scope.selectedMachine.machine_id = $scope.toolsSelectedToDeploy[tool].requests[0].machine_id;
        }
    };

    $scope.setMachineTypeCSS = function(machine_type, machine_id)
    {
        var styles = "";
        for(var tool=0; tool<$scope.toolsSelectedToDeploy.length; tool++)
        {
            if($scope.toolsSelectedToDeploy[tool].tool_name === $scope.selectedTool.tool_name)
            {
                for(var mac=0; mac<$scope.toolsSelectedToDeploy[tool].requests.length; mac++)
                {
                    if(machine_id === $scope.toolsSelectedToDeploy[tool].requests[mac].machine_id)
                    {
                        styles = styles + "vp-search__item--selected";
                    }
                }
            }
        }
        return styles;
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

    $scope.getFormValidated = function(tool, machine)
    {
        var validation_flag = 0;
        var machine_validation_flag = 0;
        for(var d=0; d<$scope.toolsSelectedToDeploy.length; d++)
        {
            if(tool === $scope.toolsSelectedToDeploy[d].tool_name)
            {
                if($scope.toolsSelectedToDeploy[d].requests.length>0)
                {
                    for(var e=0; e<$scope.toolsSelectedToDeploy[d].requests.length; e++)
                    {
                        if(machine === $scope.toolsSelectedToDeploy[d].requests[e].machine_name)
                        {
                            if($scope.toolsSelectedToDeploy[d].requests[e].tool_deployment_value.length>0)
                            {
                                for(var f=0; f<$scope.toolsSelectedToDeploy[d].requests[e].tool_deployment_value.length; f++)
                                {
                                    if($scope.toolsSelectedToDeploy[d].requests[e].tool_deployment_value[f].is_mandatory && $scope.toolsSelectedToDeploy[d].requests[e].tool_deployment_value[f].default_value==='' || $scope.toolsSelectedToDeploy[d].requests[e].tool_deployment_value[f].default_value===undefined)
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

    $scope.getToolValidated = function(tool, machine)
    {
        var validation_flag = 0;
        var toolIndex = 0;
        var requestIndex = 0;
        if($scope.toolsSelectedToDeploy.length>0)
        {
            for(var d=0; d<$scope.toolsSelectedToDeploy.length; d++)
            {
                if(tool === $scope.toolsSelectedToDeploy[d].tool_name)
                {
                    toolIndex = d;
                }
            }

            for(var e=0; e<$scope.toolsSelectedToDeploy[toolIndex].requests.length; e++)
            {
                if(machine === $scope.toolsSelectedToDeploy[toolIndex].requests[e].machine_name)
                {
                    requestIndex = e;
                }
            }

            if($scope.toolsSelectedToDeploy[toolIndex].requests.length>0)
            {
                for(var f=0; f<$scope.toolsSelectedToDeploy[toolIndex].requests[requestIndex].tool_deployment_value.length; f++)
                {
                    if($scope.toolsSelectedToDeploy[toolIndex].requests[requestIndex].tool_deployment_value[f].is_mandatory && $scope.toolsSelectedToDeploy[toolIndex].requests[requestIndex].tool_deployment_value[f].default_value==='' || $scope.toolsSelectedToDeploy[toolIndex].requests[requestIndex].tool_deployment_value[f].default_value===undefined)
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

    $scope.showMoreTools = function()
    {
        if(document.getElementById("more_tools_popup_include").style.display === "none" || document.getElementById("more_tools_popup_include").style.display === "")
        {
            remaining_up();
            $('#more_tools_popup_include').slideDown();
        }
        else
        {
            $('#more_tools_popup_include').slideUp();
        }
    };

    $scope.closeToolsToAdd = function()
    {
        $('#more_tools_popup_include').slideUp();
    };

    $scope.showMoreToolsToAdd = function()
    {
        if(document.getElementById("more_tools_add_popup").style.display === "none" || document.getElementById("more_tools_add_popup").style.display === "")
        {
            remaining_up();
            $('#more_tools_add_popup').slideDown();
        }
        else
        {
            $('#more_tools_add_popup').slideUp();
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

    $scope.removeMachine = function(tool_name, machine)
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
        $rootScope.deployToolFactory.removeMachine(tool_name, machine);
        $scope.toolsSelectedToDeploy = $rootScope.deployToolFactory.getTools();
        for(var tIndex=0; tIndex<$scope.toolsSelectedToDeploy.length; tIndex++)
        {
            if($scope.toolsSelectedToDeploy[tIndex].tool_name === tool_name)
            {
                if($scope.toolsSelectedToDeploy[tIndex].requests.length>0)
                {
                    $scope.selectedMachine.machine_name = $scope.toolsSelectedToDeploy[tIndex].requests[0].machine_name;
                    $scope.selectedMachine.machine_id = $scope.toolsSelectedToDeploy[tIndex].requests[0].machine_id;
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
        if(machine==='all')
        {
            $scope.selectedMachine = {
                    machine_name : "",
                    machine_id : ''
            };
        }
    };

    $scope.addMachine = function(machine, tool, entity,machineGroupData)
    {
        $scope.selectedMachine.machine_name = machine.machine_name;
        $scope.selectedMachine.machine_id = machine._id.$oid;
        $scope.toolsSelectedToDeploy = $rootScope.deployToolFactory.getTools();

        angular.forEach($scope.toolsSelectedToDeploy, function(value, key) {
            IsBuildDeployedOnMachine.get({
                parent_entity_id : value.version_id,
                machine_id : $scope.selectedMachine.machine_id,
                build_id :  value.build_id
            },
            function(successResponse){
                if(successResponse.data == null)
                {
                    $scope.is_build_already_deployed = false;
                }
                else
                {
                    $scope.is_build_already_deployed = true;
                }
                var machineData = {
                   machines : machine,
                   tool : tool,
                   entity :  entity,
                   skip_deployment : false,
                   is_build_already_deployed :$scope.is_build_already_deployed,
                   machine_group_id : machineGroupData
                };

                if($scope.is_build_already_deployed ===  true)
                {
                    if(entity === 'all')
                    {
                        machineData.tool = value.tool_name;
                        machineData.skip_deployment = $scope.skip_deployment;
                        //$rootScope.deployToolFactory.addMachine(machine, value.tool_name, entity, $scope.skip_deployment, $scope.is_build_already_deployed, $scope.machineGroupData.group_id);
                        $rootScope.deployToolFactory.addMachine(machineData);
                    }
                    else
                    {
                        machineData.skip_deployment = $scope.skip_deployment;
                        //$rootScope.deployToolFactory.addMachine(machine, tool, entity, $scope.skip_deployment, $scope.is_build_already_deployed,$scope.machineGroupData.group_id);
                        $rootScope.deployToolFactory.addMachine(machineData);
                    }
                }
                else
                {
                    if(entity === 'all')
                    {
                        machineData.tool = value.tool_name;
                        //$rootScope.deployToolFactory.addMachine(machine, value.tool_name, entity, false, $scope.is_build_already_deployed,$scope.machineGroupData.group_id);
                        $rootScope.deployToolFactory.addMachine(machineData);
                    }
                    else
                    {
                        //$rootScope.deployToolFactory.addMachine(machine, tool, entity, false, $scope.is_build_already_deployed,$scope.machineGroupData.group_id);
                        $rootScope.deployToolFactory.addMachine(machineData);
                    }
                }
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        });
        for(var mIndex=0; mIndex<$scope.allMachines.length; mIndex++)
        {
            if($scope.allMachines[mIndex].machine_name === machine.machine_name)
            {
                $scope.allMachines[mIndex].isSelected = true;
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

    $scope.getToolDetails = function(version_id, build_number, build_id)
    {
        $scope.applications = GetToolByID.get({
            id : 'version/'+version_id
        },
        function(response)
        {
            toolData.tool_id = response.data._id.$oid;
            toolData.tool_name = response.data.name;
            toolData.version_id = response.data.version._id.$oid;
            toolData.version_name = response.data.version.version_name;
            toolData.version_number = response.data.version.version_number;
            toolData.deployment_fields = response.data.version.deployment_field;
            toolData.build_id = build_id;
            toolData.build_number = build_number;
            $rootScope.deployToolFactory.addTool(toolData);
            $rootScope.deployToolFactory.addVersions(toolData);
            $scope.toolsSelectedToDeploy = [];
            $scope.allVersions = [];
            $scope.toolsSelectedToDeploy = $rootScope.deployToolFactory.getTools();
            $scope.selectedTool.tool_name = $scope.toolsSelectedToDeploy[0].tool_name;
            $scope.selectedTool.version_number = $scope.toolsSelectedToDeploy[0].version_number;
            $scope.selectedTool.build_id = $scope.toolsSelectedToDeploy[0].build_id;
            $scope.selectedTool.build_number = $scope.toolsSelectedToDeploy[0].build_number;
            $scope.selectedTool.version_id = $scope.toolsSelectedToDeploy[0].version_id;
            $scope.allVersions = $rootScope.deployToolFactory.getAllVersions();
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    if(selectedTools.length>0)
    {
        $scope.request_type = 'deploy';
        deployment_type = 'toolgroup';
        for(var id_1=0; id_1<selectedTools.length; id_1++)
        {
            var version_id = selectedTools[id_1].version_id;
            var build_number = selectedTools[id_1].build_number;
            var build_id = selectedTools[id_1].build_id;
            $scope.getToolDetails(version_id, build_number, build_id);
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

    $scope.copyToAllMachines = function(tool, machine)
    {
        $rootScope.deployToolFactory.copyToAllMachines(tool, machine);
        document.getElementById("copy_attenation_popup").style.display = "none";
    };

    $scope.cancelCopy = function()
    {
        document.getElementById("copy_attenation_popup").style.display = "none";
    };

    $scope.restoreDefaultValues = function(tool, machine)
    {
        $rootScope.deployToolFactory.restoreDefaultValues(tool, machine);
    };

    $scope.copyfieldValueToAllMachines = function(tool, machine, fieldIndex)
    {
        $rootScope.deployToolFactory.copyfieldValueToAllMachines(tool, machine, fieldIndex);
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
        $state.go('dashboard');
    };

    GetAllMachine.get({
    },
    function(machineSucessResponse)
    {
        $scope.allMachines = machineSucessResponse.data.data;
        $scope.machines  = machineSucessResponse.data;
        for(var mIndx=0; mIndx<$scope.allMachines.length; mIndx++)
        {
            if($stateParams.machine_id===$scope.allMachines[mIndx]._id.$oid)
            {
                $scope.machines.selected = $scope.allMachines[mIndx];
            }
            $scope.allMachines[mIndx].isSelected = false;
        }

        if($stateParams.id)
        {
            selectedTools.push($stateParams.id);
            $scope.request_type="deploy";
            deployment_type = 'toolgroup';
            $scope.applications = GetToolByID.get({
                id : 'version/'+$stateParams.id
            },
            function(response)
            {
                toolData.tool_id = response.data._id.$oid;
                toolData.tool_name = response.data.name;
                toolData.version_id = response.data.version._id.$oid;
                toolData.version_name = response.data.version.version_name;
                toolData.version_number = response.data.version.version_number;
                toolData.deployment_fields = response.data.version.deployment_field;

                if($stateParams.build_number)
                {
                    var build_number = parseInt($stateParams.build_number, 10);
                    for(var buildIndx=0; buildIndx<response.data.version.build.length; buildIndx++)
                    {
                        if(response.data.version.build[buildIndx].build_number === build_number)
                        {
                            $scope.buildDetailsToDeploy = response.data.version.build[buildIndx];
                        }
                    }
                }
                else if(response.data.version.build)
                {
                    if(response.data.version.build.length>0)
                    {
                        $scope.buildDetailsToDeploy = response.data.version.build[0];
                    }
                }
                else
                {
                    $scope.buildDetailsToDeploy = {
                    'build_number' : 0,
                    '_id' : {
                        '$oid' : 0
                        }
                    };
                }
                toolData.build_id = $scope.buildDetailsToDeploy._id.$oid;
                toolData.build_number = $scope.buildDetailsToDeploy.build_number;

                $rootScope.deployToolFactory.addTool(toolData);
                $rootScope.deployToolFactory.addVersions(toolData);
                $scope.toolsSelectedToDeploy = [];
                $scope.allVersions = [];
                $scope.toolsSelectedToDeploy = $rootScope.deployToolFactory.getTools();
                $scope.selectedTool.tool_name = $scope.toolsSelectedToDeploy[0].tool_name;
                $scope.selectedTool.version_number = $scope.toolsSelectedToDeploy[0].version_number;
                $scope.selectedTool.version_id = $scope.toolsSelectedToDeploy[0].version_id;
                $scope.selectedTool.build_id = $scope.toolsSelectedToDeploy[0].build_id;
                $scope.selectedTool.build_number = $scope.toolsSelectedToDeploy[0].build_number;
                $scope.allVersions = $rootScope.deployToolFactory.getAllVersions();
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
        else if($stateParams.version_id && $stateParams.machine_id)
        {
            if(($location.path()).indexOf("redeploy") >= 1)
            {
                $scope.request_type="redeploy";
                deployment_type = 'toolgroup';
                $scope.applications = GetToolByID.get({
                    id : 'version/'+$stateParams.version_id+'/prevversion/'+$stateParams.version_id+'/machine/'+$stateParams.machine_id
                },
                function(response)
                {
                    $scope.previousBuildDetails = {
                        build_id : $stateParams.build_id,
                        build_number : $stateParams.build_number
                    };
                    toolData.tool_id = response.data._id.$oid;
                    toolData.tool_name = response.data.name;
                    toolData.version_id = response.data.version._id.$oid;
                    toolData.version_name = response.data.version.version_name;
                    toolData.version_number = response.data.version.version_number;
                    toolData.deployment_fields = response.data.version.deployment_field;
                    toolData.build_id = $stateParams.build_id;
                    toolData.build_number = $stateParams.build_number;
                    $rootScope.deployToolFactory.addTool(toolData);
                    $rootScope.deployToolFactory.addVersions(toolData);

                    $scope.toolsSelectedToDeploy = [];
                    $scope.allVersions = [];
                    $scope.toolsSelectedToDeploy = $rootScope.deployToolFactory.getTools();
                    $scope.selectedTool.tool_name = $scope.toolsSelectedToDeploy[0].tool_name;
                    $scope.selectedTool.version_number = $scope.toolsSelectedToDeploy[0].version_number;
                    $scope.allVersions = $rootScope.deployToolFactory.getAllVersions();
                    if(response.data.version.build)
                    {
                        for(var buildIndx=0; buildIndx<response.data.version.build.length; buildIndx++)
                        {
                            if(response.data.version.build[buildIndx].build_number === $stateParams.build_number)
                            {
                                $scope.buildDetailsToDeploy = response.data.version.build[buildIndx];
                            }
                        }
                    }
                    var tool_name = $scope.selectedTool.tool_name;
                    for(var c=0; c<$scope.allMachines.length; c++)
                    {
                        if($stateParams.machine_id === $scope.allMachines[c]._id.$oid)
                        {
                            $scope.selectedMachine.machine_name = $scope.allMachines[c].machine_name;
                            $scope.selectedMachine.machine_id = $scope.allMachines[c]._id.$oid;
                            $scope.addMachine($scope.allMachines[c], tool_name, 'current',undefined, $scope.skip_deployment, $scope.is_build_already_deployed);
                        }
                    }
                },
                function(errorResponse)
                {
                    $rootScope.handleResponse(errorResponse);
                });
            }
            else if(($location.path()).indexOf("undeploy") >= 1)
            {
                $scope.request_type="undeploy";
                deployment_type = 'toolgroup';
                $scope.applications = GetToolByID.get({
                    id : 'version/'+$stateParams.version_id+'/prevversion/'+$stateParams.version_id+'/machine/'+$stateParams.machine_id
                },
                function(response)
                {
                    $scope.previousBuildDetails = {
                        build_id : $stateParams.build_id,
                        build_number : $stateParams.build_number
                    };
                    toolData.tool_id = response.data._id.$oid;
                    toolData.tool_name = response.data.name;
                    toolData.version_id = response.data.version._id.$oid;
                    toolData.version_name = response.data.version.version_name;
                    toolData.version_number = response.data.version.version_number;
                    toolData.deployment_fields = response.data.version.deployment_field;
                    toolData.build_id = $stateParams.build_id;
                    toolData.build_number = $stateParams.build_number;
                    $rootScope.deployToolFactory.addTool(toolData);
                    $rootScope.deployToolFactory.addVersions(toolData);

                    $scope.toolsSelectedToDeploy = [];
                    $scope.allVersions = [];
                    $scope.toolsSelectedToDeploy = $rootScope.deployToolFactory.getTools();
                    $scope.selectedTool.tool_name = $scope.toolsSelectedToDeploy[0].tool_name;
                    $scope.selectedTool.version_number = $scope.toolsSelectedToDeploy[0].version_number;
                    $scope.allVersions = $rootScope.deployToolFactory.getAllVersions();
                    var tool_name = $scope.selectedTool.tool_name;
                    for(var c=0; c<$scope.allMachines.length; c++)
                    {
                        if($stateParams.machine_id === $scope.allMachines[c]._id.$oid)
                        {
                            $scope.selectedMachine.machine_name = $scope.allMachines[c].machine_name;
                            $scope.selectedMachine.machine_id = $scope.allMachines[c]._id.$oid;
                            $scope.addMachine($scope.allMachines[c], tool_name, 'current',undefined, $scope.skip_deployment, $scope.is_build_already_deployed);
                        }
                    }
                },
                function(errorResponse)
                {
                    $rootScope.handleResponse(errorResponse);
                });
            }
        }
        else
        {
            if(($location.path()).indexOf("upgrade") >= 1)
            {
                $scope.request_type="upgrade";
                deployment_type = 'toolgroup';
                $scope.applications = GetToolByID.get({
                    id : 'version/'+$stateParams.new_version_id+'/prevversion/'+$stateParams.old_version_id+'/machine/'+$stateParams.machine_id
                },
                function(response)
                {
                    $scope.deployment_field_value = response.data.version.deployment_field;
                    for(var buildIndx=0; buildIndx<response.data.version.build.length; buildIndx++)
                    {
                        if(response.data.version.build[buildIndx].build_number === $stateParams.build_number)
                        {
                            $scope.buildDetailsToDeploy = response.data.version.build[buildIndx];
                        }
                    }
                },
                function(errorResponse)
                {
                    $rootScope.handleResponse(errorResponse);
                });
            }
        }

        if($stateParams.request_id)
        {
            $scope.request_type="deploy";
            deployment_type = 'toolgroup';
            ViewSavedDeploymentRequest.get({
                id : $stateParams.request_id
            },
            function(viewSavedDeploymentRequestsSuccessReponse)
            {
                $scope.savedRequestData = viewSavedDeploymentRequestsSuccessReponse.data.data;
                $rootScope.deployToolFactory.cloneRequestObject($scope.savedRequestData);
                $scope.toolsSelectedToDeploy = [];
                $scope.allVersions = [];
                $scope.toolsSelectedToDeploy = $rootScope.deployToolFactory.getTools();
                $scope.selectedTool.tool_name = $scope.toolsSelectedToDeploy[0].tool_name;
                $scope.selectedTool.version_number = $scope.toolsSelectedToDeploy[0].version_number;
                $scope.allVersions = $rootScope.deployToolFactory.getAllVersions();
                var tool_name = $scope.selectedTool.tool_name;
                $scope.selectedMachine.machine_name = $scope.toolsSelectedToDeploy[0].requests[0].machine_name;
                $scope.selectedMachine.machine_id = $scope.toolsSelectedToDeploy[0].requests[0]._id.$oid;
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
        function(testMachineErrorResponse)
        {
            $scope.connectionResponse = testMachineErrorResponse.data.result;
            $rootScope.handleResponse(testMachineErrorResponse);
        });
        return $scope.connectionResponse;
    };

    $scope.uploadDeploymentFields = function(tool, machine)
    {
        var file = $scope.fileToImport;
        if(file)
        {
            var uploadUrl = "/deploymentrequest/deploymentfield/upload";
            deploymentFieldFileUpload.uploadFileToUrl(file, uploadUrl, 'tool', tool, machine, function(response){
            });
            $scope.toolsSelectedToDeploy = $rootScope.deployToolFactory.getTools();
        }
    };

    $scope.addToInputValue = function(input_name, value)
    {
        var duIndex = 0;
        var requestIndex = 0;
        var fieldIndex = 0;
        for(var d=0;  d<$scope.toolsSelectedToDeploy.length; d++)
        {
            if($scope.toolsSelectedToDeploy[d].tool_name === $scope.selectedTool.tool_name)
            {
                duIndex = d;
                for(var e=0;  e<$scope.toolsSelectedToDeploy[d].requests.length; e++)
                {
                    if($scope.toolsSelectedToDeploy[d].requests[e].machine_name === $scope.selectedMachine.machine_name)
                    {
                        requestIndex = e;
                        for(var f=0;  f<$scope.toolsSelectedToDeploy[d].requests[e].tool_deployment_value.length; f++)
                        {
                            if($scope.toolsSelectedToDeploy[d].requests[e].tool_deployment_value[f].input_name === input_name)
                            {
                                fieldIndex = f;
                            }
                        }
                    }
                }
            }
        }
        if($scope.toolsSelectedToDeploy[duIndex].requests[requestIndex].tool_deployment_value[fieldIndex].input_value)
        {
            var result = $.inArray(value, $scope.toolsSelectedToDeploy[duIndex].requests[requestIndex].tool_deployment_value[fieldIndex].input_value);
            if(result < 0)
            {
                $scope.toolsSelectedToDeploy[duIndex].requests[requestIndex].tool_deployment_value[fieldIndex].input_value.push(value);
            }
            else
            {
                $scope.toolsSelectedToDeploy[duIndex].requests[requestIndex].tool_deployment_value[fieldIndex].input_value.splice(result, 1);
            }
        }
    };

    $scope.isFieldSelected = function(fieldName, fieldValue)
     {
        var duIndex = 0;
        var requestIndex = 0;
        var fieldIndex = 0;
        for(var d=0;  d<$scope.toolsSelectedToDeploy.length; d++)
        {
            if($scope.toolsSelectedToDeploy[d].tool_name === $scope.selectedTool.tool_name)
            {
                duIndex = d;
                for(var e=0;  e<$scope.toolsSelectedToDeploy[d].requests.length; e++)
                {
                    if($scope.toolsSelectedToDeploy[d].requests[e].machine_name === $scope.selectedMachine.machine_name)
                    {
                        requestIndex = e;
                        for(var f=0;  f<$scope.toolsSelectedToDeploy[d].requests[e].tool_deployment_value.length; f++)
                        {
                            if($scope.toolsSelectedToDeploy[d].requests[e].tool_deployment_value[f].input_name === fieldName)
                            {
                                fieldIndex = f;
                            }
                        }
                    }
                }
            }
        }

        if($scope.toolsSelectedToDeploy[duIndex].requests[requestIndex].tool_deployment_value[fieldIndex].default_value)
        {
            var result = $.inArray(fieldValue, $scope.toolsSelectedToDeploy[duIndex].requests[requestIndex].tool_deployment_value[fieldIndex].default_value);
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
        }
        else
        {
            $scope.scheduledDateISO = $scope.scheduled_timestamp;
        }

        $scope.userData = $rootScope.userFactory.getUserDetails();
        var jsonData = {
            deployment_requests : []
        };
        var tool_deployment_value =[];
        for(var a=0; a<$scope.toolsSelectedToDeploy.length; a++)
        {
            var tool_name = $scope.toolsSelectedToDeploy[a].tool_name;
            var tool_id = $scope.toolsSelectedToDeploy[a].tool_id;
            var version_id = $scope.toolsSelectedToDeploy[a].version_id;
            var build_id = $scope.toolsSelectedToDeploy[a].build_id;
            var build_number = $scope.toolsSelectedToDeploy[a].build_number;
            var deployment_field_values = [];
            var requests = [];

            if($scope.toolsSelectedToDeploy[a].requests.length === 0)
            {
                $rootScope.handleResponse("Please select machine for tool "+$scope.toolsSelectedToDeploy[a].tool_name);
                return false;
            }
            else
            {
                for(var b=0; b<$scope.toolsSelectedToDeploy[a].requests.length; b++)
                {
                    var deployment_fields = [];
                    deployment_field_values = [];
                    angular.copy($scope.toolsSelectedToDeploy[a].requests[b].tool_deployment_value, deployment_fields);
                    if($scope.request_type!== 'deploy')
                    {
                        $scope.toolsSelectedToDeploy[a].requests[b].skip_deployment = false;
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
                                        if (atpos<1 || dotpos<atpos+2 || dotpos+2>=support.length)
                                        {
                                            $rootScope.handleResponse('Please enter valid email address!');
                                            return false;
                                        }
                                    }
                                }
                                else if((deployment_fields[c].is_mandatory === true || deployment_fields[c].is_mandatory === 'true') && (deployment_fields[c].input_type !== 'checkbox') && (deployment_fields[c].default_value === null || deployment_fields[c].default_value === undefined || deployment_fields[c].default_value === '' || (!deployment_fields[c].default_value)) && ($scope.request_type!=='undeploy'))
                                {
                                    $rootScope.handleResponse('Field '+deployment_fields[c].input_name+' in tool '+$scope.toolsSelectedToDeploy[a].requests[b].tool_name+' for machine '+$scope.toolsSelectedToDeploy[a].requests[b].machine_name+' can not be empty!');
                                    return false;
                                }
                                else if((deployment_fields[c].is_mandatory === true || deployment_fields[c].is_mandatory === 'true') && (deployment_fields[c].input_type === 'checkbox') && (deployment_fields[c].input_value === null || deployment_fields[c].input_value === undefined || deployment_fields[c].input_value === '' || deployment_fields[c].input_value.length === 0 || (!deployment_fields[c].input_value)) && ($scope.request_type!=='undeploy'))
                                {
                                    $rootScope.handleResponse('Field '+deployment_fields[c].input_name+' in tool '+$scope.toolsSelectedToDeploy[a].requests[b].tool_name+' for machine '+$scope.toolsSelectedToDeploy[a].requests[b].machine_name+' can not be empty!');
                                    return false;
                                }
                                else if((deployment_fields[c].is_mandatory === true || deployment_fields[c].is_mandatory === 'true') && (deployment_fields[c].input_type === 'date') && (deployment_fields[c].default_value === null || deployment_fields[c].default_value === undefined || deployment_fields[c].default_value === '' || (!deployment_fields[c].default_value) || (isNaN(deployment_fields[c].default_value.getTime()))) && ($scope.request_type!=='undeploy'))
                                {
                                    $rootScope.handleResponse('Field '+deployment_fields[c].input_name+' in tool '+$scope.toolsSelectedToDeploy[a].requests[b].tool_name+' for machine '+$scope.toolsSelectedToDeploy[a].requests[b].machine_name+' can not be empty!');
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
                    requests.push({'machine_id' : $scope.toolsSelectedToDeploy[a].requests[b].machine_id, 'tool_deployment_value' : deployment_field_values, 'warning_flag' : $scope.toolsSelectedToDeploy[a].requests[b].warning_flag, 'skip_dep_ind' : $scope.toolsSelectedToDeploy[a].requests[b].skip_deployment,'machine_group_id':$scope.toolsSelectedToDeploy[a].requests[b].machine_group_id});
                }
                jsonData.deployment_requests.push({'parent_entity_id' : version_id, 'requested_by' : $rootScope.userProfile.userData.user, 'request_type' : $scope.request_type, 'deployment_type' : deployment_type, 'requests' : requests, 'scheduled_date' : $scope.scheduledDateISO, 'build_number' : $scope.toolsSelectedToDeploy[a].build_number, 'build_id' : $scope.toolsSelectedToDeploy[a].build_id});
            }
        }

        if(deploymentParam === 'deploy')
        {
            Ticket.save (jsonData, function (response) {
                $scope.responseID = response.data.id;
                $state.go('runningToolDeploymentStatus', {'request_id' : response.data.id});
                $rootScope.handleResponse(response);
                $rootScope.selectedTools = [];
                selectedTools = [];
                $scope.selectedTool = {
                    tool_name : '',
                    version_number : ''
                };
                $scope.selectedMachine = {
                    machine_name : "",
                    machine_id : ''
                };
            },
            function(errorResponse)
            {
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
                deployment_type : 'toolgroup',
                data : []
            };
            savedData.data = $scope.toolsSelectedToDeploy;
            if($stateParams.request_id)
            {
                savedData.status = 'saved';
                savedData._id.oid = $stateParams.request_id;
                EditSavedDeploymentRequest.update(savedData, function (response) {
                    $scope.requestStatusMessages.push(response.message);
                    $state.go('dashboard');
                    $rootScope.handleResponse(response);
                    $rootScope.selectedTools = [];
                    selectedTools = [];
                    $scope.selectedTool = {
                        tool_name : '',
                        version_number : ''
                    };
                    $scope.selectedMachine = {
                        machine_name : "",
                        machine_id : ''
                    };
                },
                function(errorResponse)
                {
                    $rootScope.handleResponse(errorResponse);
                });
            }
            else
            {
                delete savedData._id;
                delete savedData.status;
                SaveDeploymentRequest.save(savedData, function (response) {
                    $scope.requestStatusMessages.push(response.message);
                    $state.go('dashboard');
                    $rootScope.handleResponse(response);
                    $rootScope.selectedTools = [];
                    selectedTools = [];
                    $scope.selectedTool = {
                        tool_name : '',
                        version_number : ''
                    };
                    $scope.selectedMachine = {
                        machine_name : "",
                        machine_id : ''
                    };
                },
                function(errorResponse)
                {
                    $rootScope.handleResponse(errorResponse);
                });
            }
        }
    };
});
});