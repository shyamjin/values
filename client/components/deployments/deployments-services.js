define(['angular', 'ngResource'],function (app) {
  'use strict';

var deploymentServicesApp = angular.module('deploymentServicesApp', []);

deploymentServicesApp.factory('Ticket', function($resource,$rootScope) {
    return $resource('/deploymentrequest/group/add', {
    }, {
        update: {
            method: 'PUT'
        }
      });
    }).factory('TicketStatus', function($resource,$rootScope) {
        return $resource('/deploymentrequest/:id', {
            id:'@_id'
        }, {
                query : {
                    method: 'GET',
                    isArray:true,
                    transformResponse : function(fulldata,headers) {
                        var jsonData = JSON.parse(fulldata);
                        return JSON.parse(jsonData.data[0]);
                      }
                  }
          });
    }).factory('DeploymentRequestView', function ($resource, $rootScope) {
        return $resource('/deploymentrequest/group/all', {
        }, {

            });
    }).factory('OneDeploymentRequestView', function ($resource, $rootScope) {
        return $resource('/deploymentrequest/group/view/:id', {
            id: '@_id'
        }, {

            });
    }).factory('SingleDeploymentRequestDetails', function ($resource, $rootScope) {
        return $resource('/deploymentrequest/view/:id', {
            id: '@_id'
        }, {

        });
    }).factory('DeploymentRequestAll', function ($resource, $rootScope) {
        return $resource('/deploymentrequest/all', {
        },
        {
            get : {
                method: 'GET',
                isArray:false,
                transformResponse : function(fulldata, headers) {
                    var jsonData = JSON.parse(fulldata);
                    return jsonData;
                }
            }
        });
    }).factory('ServerTime', function ($resource, $rootScope) {
        return $resource('/currenttime', {
        }, {

            });
    }).factory('RequestStatus', function($resource,$rootScope) {
    return $resource('/deploymentrequest/view/:id', {
        id:'@_id'
    }, {
     query : {
                method: 'GET',
                isArray: true,
                transformResponse : function(response, headers) {
                    var jsonData = JSON.parse(response);
                    return jsonData;
                  }
              }
      });
     }).factory('RetryDeploymentRequest', function($resource,$rootScope) {
        return $resource('/deploymentrequest/retry', {
        }, {
            update : {
                  method: 'PUT'
                  }
         });
     }).factory('RetryDeploymentRequestGroup', function($resource,$rootScope) {
     return $resource('/deploymentrequest/group/retry', {
     }, {
        update : {
                  method: 'PUT'
                  }
         });
     }).factory('UndeployDeploymentRequestGroup', function($resource,$rootScope) {
     return $resource('/deploymentrequest/group/add/undeploy', {
     }, {
         });
     }).factory('RevertDeploymentGroup', function ($resource, $rootScope) {
        return $resource('/deploymentrequest/group/view/revert/:id', {
            id: '@_id'
        }, {

        });
    }).factory('DeployToolSet', function($resource,$rootScope) {
        return $resource('/deploymentrequest/group/toolset/add', {
        }, {

          });
     }).factory('DeployToolOnMachineGroup', function($resource,$rootScope) {
        return $resource('/deploymentrequest/group/add', {
        }, {

          });
     }).factory('GetCurrentServerTime', function($resource,$rootScope) {
        return $resource('/currenttime', {
        }, {

          });
     }).factory('GetAllSavedDeploymentRequests', function($resource,$rootScope) {
        return $resource('/deploymentrequest/group/saved/all', {
        }, {
    
          });
    }).factory('ViewSavedDeploymentRequest', function($resource,$rootScope) {
        return $resource('/deploymentrequest/group/saved/view/:id', {
        id: '@_id'
    }, {

      });
    }).factory('SaveDeploymentRequest', function($resource,$rootScope) {
        return $resource('/deploymentrequest/group/saved/add', {
        }, {

      });
    }).factory('EditSavedDeploymentRequest', function($resource,$rootScope) {
        return $resource('/deploymentrequest/group/saved/update', {
        }, {
            update : {
                method : 'PUT'
            }
        });
    }).factory('DeleteSavedDeploymentRequest', function($resource,$rootScope) {
        return $resource('/deploymentrequest/group/saved/delete/:id', {
            id: '@_id'
        }, {

        });
    }).factory('IsBuildDeployedOnMachine', function($resource,$rootScope) {
        return $resource('/deployed/view/machine_id/:machine_id/parent_entity_id/:parent_entity_id/build_id/:build_id' , {
            machine_id: '@_machine_id',
            parent_entity_id: '@_parent_entity_id',
            build_id: '@_build_id'
        }, {

        });
    }).factory('DeployTool', function()  {
        var deployTool = {};
        var allVersions = [];
        var deployMachine= {};
        deployTool.tools = [];

        deployMachine.machines=[];
        return {
        addTool : function(toolData)
        {
            var tool_id = toolData.tool_id;
            var tool_name = toolData.tool_name;
            var version_id = toolData.version_id;
            var version_name = toolData.version_name;
            var version_number = toolData.version_number;
            var deployment_fields = toolData.deployment_fields;
            var build_id = toolData.build_id;
            var build_number = toolData.build_number;

            var tool_deployment_fields = [];
            if(deployment_fields!==null && deployment_fields!==undefined && deployment_fields!=='')
            {
                angular.copy(deployment_fields.fields, tool_deployment_fields);
                for(var d=0; d<tool_deployment_fields.length; d++)
                {
                    if(tool_deployment_fields[d].input_type === 'date')
                    {
                        var date = new Date(tool_deployment_fields[d].default_value);
                        delete tool_deployment_fields[d].default_value;
                        tool_deployment_fields[d].default_value = date;
                    }
                }
            }
            else
            {
                tool_deployment_fields = [];
            }
            var length = deployTool.tools.length;
            var flag = 0;
            var tool_flag = 0;
            if(length>0)
            {
                for(var key=0; key<deployTool.tools.length; key++)
                {
                    if(deployTool.tools[key].tool_name !== tool_name)
                    {
                         tool_flag++;
                    }
                }

                if(tool_flag === deployTool.tools.length)
                {
                    var toolLength = deployTool.tools.length;
                    deployTool.tools.push({
                        'tool_id' : tool_id,
                        'tool_name' : '',
                        'version_number' : '',
                        'version_id' : '',
                        'tool_deployment_value' : [],
                        'build_number' : '',
                        'build_id' : '',
                        'requests' : []
                    });
                    deployTool.tools[length].tool_id = tool_id;
                    deployTool.tools[length].tool_name = tool_name;
                    deployTool.tools[length].version_number = version_number;
                    deployTool.tools[length].version_id = version_id;
                    deployTool.tools[length].build_id = build_id;
                    deployTool.tools[length].build_number = build_number;
                    if(deployment_fields)
                    {
                        for(var key_3=0; key_3<tool_deployment_fields.length; key_3++)
                        {
                            if(tool_deployment_fields[key_3].input_type === "checkbox")
                            {
                                if(tool_deployment_fields[key_3].default_value)
                                {
                                    tool_deployment_fields[key_3].input_value = tool_deployment_fields[key_3].default_value;
                                }
                            }
                        }
                        angular.copy(tool_deployment_fields, deployTool.tools[length].tool_deployment_value);
                    }
                    else
                    {
                        deployTool.tools[length].tool_deployment_value = [];
                    }
                }
            }
            else
            {
                deployTool.tools = [{
                    tool_id : '',
                    tool_name : '',
                    version_number : '',
                    tool_deployment_value : [],
                    build_number : '',
                    build_id : '',
                    requests : []
                }];
                deployTool.tools[0].tool_id = tool_id;
                deployTool.tools[0].tool_name = tool_name;
                deployTool.tools[0].version_number = version_number;
                deployTool.tools[0].version_id = version_id;
                deployTool.tools[0].build_id = build_id;
                deployTool.tools[0].build_number = build_number;
                if(deployment_fields)
                {
                    for(var key_2=0; key_2<tool_deployment_fields.length; key_2++)
                    {
                        if(tool_deployment_fields[key_2].input_type === "checkbox")
                        {
                            if(tool_deployment_fields[key_2].default_value)
                            {
                                tool_deployment_fields[key_2].input_value = tool_deployment_fields[key_2].default_value;
                            }
                        }
                    }
                    angular.copy(tool_deployment_fields, deployTool.tools[length].tool_deployment_value);
                }
                else
                {
                    deployTool.tools[length].tool_deployment_value = [];
                }
            }
        },
        getTools : function()
        {
            return deployTool.tools;
        },
        removeTool : function(id)
        {
            deployTool.tools.splice(id,1);
            if(deployTool.tools.length===0)
            {
                deployTool.selectedTool = '';
            }
            else
            {
                deployTool.selectedTool = deployTool.tools[0].name;
            }
            console.log('Printing all tools after removal');
            console.log(deployTool);
        },
        addMachine : function(machineData)
        {
            var machines = machineData.machines;
            var tool = machineData.tool;
            var entity = machineData.entity;
            var skip_deployment = machineData.skip_deployment;
            var is_build_already_deployed = machineData.is_build_already_deployed;
            var machine_group_id = machineData.machine_group_id;

            length = deployTool.tools.length;
            var tool_deployment_fields = [];
            if(length>=1)
            {
                if(entity === 'current')
                {
                    for(var key_1=0; key_1<deployTool.tools.length; key_1++)
                    {

                        var machine_length_1 = deployTool.tools[key_1].requests.length;
                        if(deployTool.tools[key_1].tool_name === tool)
                        {
                            if(deployTool.tools[key_1].requests.length>0)
                            {
                                var addMachineFlag_1 = 0;
                                for(var key_1_2=0; key_1_2<deployTool.tools[key_1].requests.length; key_1_2++)
                                {
                                    if(deployTool.tools[key_1].requests[key_1_2].machine_name === machines.machine_name)
                                    {
                                       console.log('This machie is already present for this tool.. select another');
                                    }
                                    else
                                    {
                                        addMachineFlag_1++;
                                    }
                                }
                                if(addMachineFlag_1 === machine_length_1)
                                {
                                        deployTool.tools[key_1].requests.push({
                                            tool_name : '',
                                            tool_deployment_value : [],
                                            machine_id : '',
                                            machine_name : '',
                                            skip_deployment : '',
                                            is_build_already_deployed : '',
                                            machine_group_id:''
                                        });
                                        deployTool.tools[key_1].requests[machine_length_1].tool_name = deployTool.tools[key_1].requests[machine_length_1-1].tool_name;
                                        angular.copy(deployTool.tools[key_1].tool_deployment_value, deployTool.tools[key_1].requests[machine_length_1].tool_deployment_value);
                                        deployTool.tools[key_1].requests[machine_length_1].machine_name = machines.machine_name;
                                        deployTool.tools[key_1].requests[machine_length_1].machine_id = machines._id.$oid;
                                        deployTool.tools[key_1].requests[machine_length_1].isDefault = true;
                                        deployTool.tools[key_1].requests[machine_length_1].isCopiedToAllMachines = false;
                                        deployTool.tools[key_1].requests[machine_length_1].warning_flag = false;
                                        deployTool.tools[key_1].requests[machine_length_1].skip_deployment = skip_deployment;
                                        deployTool.tools[key_1].requests[machine_length_1].is_build_already_deployed = is_build_already_deployed;
                                        deployTool.tools[key_1].requests[machine_length_1].machine_group_id = machine_group_id;
                                }
                            }
                            else
                            {
                                deployTool.tools[key_1].requests.push({
                                    tool_name : '',
                                    tool_deployment_value : [],
                                    machine_id : '',
                                    machine_name : '',
                                    skip_deployment : '',
                                    is_build_already_deployed : '',
                                    machine_group_id:''
                                });
                                deployTool.tools[key_1].requests[0].tool_name = deployTool.tools[key_1].tool_name;
                                angular.copy(deployTool.tools[key_1].tool_deployment_value, deployTool.tools[key_1].requests[0].tool_deployment_value);
                                deployTool.tools[key_1].requests[0].machine_name = machines.machine_name;
                                deployTool.tools[key_1].requests[0].machine_id = machines._id.$oid;
                                deployTool.tools[key_1].requests[0].isDefault = true;
                                deployTool.tools[key_1].requests[0].isCopiedToAllMachines = false;
                                deployTool.tools[key_1].requests[0].warning_flag = false;
                                deployTool.tools[key_1].requests[0].skip_deployment = skip_deployment;
                                deployTool.tools[key_1].requests[0].is_build_already_deployed = is_build_already_deployed;
                                deployTool.tools[key_1].requests[0].machine_group_id = machine_group_id;
                            }
                        }
                    }
                }
                else
                {
                    for(var key_2=0; key_2<deployTool.tools.length; key_2++)
                    {

                        var machine_length_2 = deployTool.tools[key_2].requests.length;
                        if(deployTool.tools[key_2].tool_name === tool)
                        {
                            if(deployTool.tools[key_2].requests.length>0)
                            {
                                var addMachineFlag_2 = 0;
                                for(var key_3=0; key_3<deployTool.tools[key_2].requests.length; key_3++)
                                {
                                    if(deployTool.tools[key_2].requests[key_3].machine_name === machines.machine_name)
                                    {
                                       console.log('This machie is already present for this tool.. select another');
                                    }
                                    else
                                    {
                                        addMachineFlag_2++;
                                    }
                                }
                                if(addMachineFlag_2 === machine_length_2)
                                {
                                        deployTool.tools[key_2].requests.push({
                                            tool_name : '',
                                            tool_deployment_value : [],
                                            machine_id : '',
                                            machine_name : '',
                                            machine_group_id:''
                                        });
                                        deployTool.tools[key_2].requests[machine_length_2].tool_name = deployTool.tools[key_2].requests[machine_length_2-1].tool_name;
                                        angular.copy(deployTool.tools[key_2].tool_deployment_value, deployTool.tools[key_2].requests[machine_length_2].tool_deployment_value);
                                        deployTool.tools[key_2].requests[machine_length_2].machine_name = machines.machine_name;
                                        deployTool.tools[key_2].requests[machine_length_2].machine_id = machines._id.$oid;
                                        deployTool.tools[key_2].requests[machine_length_2].isDefault = true;
                                        deployTool.tools[key_2].requests[machine_length_2].isCopiedToAllMachines = false;
                                        deployTool.tools[key_2].requests[machine_length_2].warning_flag = false;
                                        deployTool.tools[key_2].requests[machine_length_2].skip_deployment = skip_deployment;
                                        deployTool.tools[key_2].requests[machine_length_2].is_build_already_deployed = is_build_already_deployed;
                                        deployTool.tools[key_2].requests[machine_length_2].machine_group_id = machine_group_id;
                                }
                            }
                            else
                            {
                            deployTool.tools[key_2].requests.push({
                                tool_name : '',
                                tool_deployment_value : [],
                                machine_id : '',
                                machine_name : '',
                                machine_group_id:''
                            });
                            deployTool.tools[key_2].requests[0].tool_name = deployTool.tools[key_2].tool_name;
                            angular.copy(deployTool.tools[key_2].tool_deployment_value, deployTool.tools[key_2].requests[0].tool_deployment_value);
                            deployTool.tools[key_2].requests[0].machine_name = machines.machine_name;
                            deployTool.tools[key_2].requests[0].machine_id = machines._id.$oid;
                            deployTool.tools[key_2].requests[0].isDefault = true;
                            deployTool.tools[key_2].requests[0].isCopiedToAllMachines = false;
                            deployTool.tools[key_2].requests[0].warning_flag = false;
                            deployTool.tools[key_2].requests[0].skip_deployment = skip_deployment;
                            deployTool.tools[key_2].requests[0].is_build_already_deployed = is_build_already_deployed;
                            deployTool.tools[key_2].requests[0].machine_group_id = machine_group_id;
                        }
                        }
                    }
                }
            }
            else
            {
                    deployTool.tools[0].requests[0].machine_name = machines.machine_name;
                    deployTool.tools[0].requests[0].machine_id = machines._id.$oid;
                    deployTool.tools[0].requests[0].isDefault = true;
                    deployTool.tools[0].requests[0].isCopiedToAllMachines = false;
                    deployTool.tools[0].requests[0].warning_flag = false;
                    deployTool.tools[0].requests[0].skip_deployment = skip_deployment;
                    deployTool.tools[0].requests[0].is_build_already_deployed = is_build_already_deployed;
            }
        },
        removeMachine : function(tool_name, machine)
        {
            var length = deployTool.tools.length;
            for(var n=0; n<length; n++)
            {
                if(deployTool.tools[n].tool_name === tool_name)
                {
                    if(machine !== 'all')
                    {
                        for(var o=0; o<deployTool.tools[n].requests.length; o++)
                        {
                            if(deployTool.tools[n].requests[o].machine_name === machine)
                            {
                                deployTool.tools[n].requests.splice(o, 1);
                            }
                        }
                    }
                    else
                    {
                        deployTool.tools[n].requests = [];
                    }
                }
            }
        },
        addVersions : function(tool_name, versions)
        {
            allVersions.push({'tool_name':tool_name, 'versions': versions});
        },
        getAllVersions : function()
        {
            return allVersions;
        },
        selectVersion : function(tool_name, version_id, version_name, version_number)
        {
            var length = deployTool.tools.length;
            for(var o=0; o<length; o++)
            {
                if(tool_name===deployTool.tools[o].tool_name)
                {
                    deployTool.tools[o].version_id = version_id;
                    deployTool.tools[o].version_name = version_name;
                    deployTool.tools[o].version_number = version_number;
                }
            }
        },
        copyToAllMachines : function(tool, machine)
        {
            length = deployTool.tools.length;
            var mIndex = 0;
            var tool_deployment_fields = [];
            if(length>=1)
            {
                for(var n=0; n<deployTool.tools.length; n++)
                {
                    if(deployTool.tools[n].tool_name === tool)
                    {
                        var machine_length = deployTool.tools[n].requests.length;
                        if(deployTool.tools[n].requests.length>0)
                        {
                            for(var o=0; o<deployTool.tools[n].requests.length; o++)
                            {
                                if(deployTool.tools[n].requests[o].machine_name === machine.machine_name)
                                {
                                    deployTool.tools[n].requests[o].isDefault = true;
                                    deployTool.tools[n].requests[o].isCopiedToAllMachines = true;
                                    mIndex = o;
                                }
                            }
                            for(var p=0; p<deployTool.tools[n].requests.length; p++)
                            {
                                if(p!==mIndex)
                                {

                                    angular.copy(deployTool.tools[n].requests[mIndex].tool_deployment_value, deployTool.tools[n].requests[p].tool_deployment_value);
                                    deployTool.tools[n].requests[p].isDefault = false;
                                    deployTool.tools[n].requests[p].isCopiedToAllMachines = false;
                                }
                            }
                        }
                    }
                }
            }
        },
        copyfieldValueToAllMachines : function(tool, machine, fieldIndex)
        {
            length = deployTool.tools.length;
            var mIndex = 0;
            var copyField = [];
            if(length>=1)
            {
                for(var n=0; n<deployTool.tools.length; n++)
                {
                    if(deployTool.tools[n].tool_name === tool)
                    {
                        var machine_length = deployTool.tools[n].requests.length;
                        if(deployTool.tools[n].requests.length>0)
                        {
                            for(var o=0; o<deployTool.tools[n].requests.length; o++)
                            {
                                if(deployTool.tools[n].requests[o].machine_name === machine)
                                {
                                    for(var p=0; p<deployTool.tools[n].requests[o].tool_deployment_value.length; p++)
                                    {
                                        if(p===fieldIndex)
                                        {
                                            angular.copy(deployTool.tools[n].requests[o].tool_deployment_value[p], copyField);
                                            deployTool.tools[n].requests[o].tool_deployment_value[p].isDefault = false;
                                            deployTool.tools[n].requests[o].tool_deployment_value[p].isCopiedToAllMachines = true;
                                        }
                                    }
                                }
                            }
                            for(var r=0; r<deployTool.tools[n].requests.length; r++)
                            {
                                var fieldFlag = 0;
                                var ind = 0;
                                if(deployTool.tools[n].requests[r].machine_name !== machine)
                                {
                                    for(var q=0; q<deployTool.tools[n].requests[r].tool_deployment_value.length; q++)
                                    {
                                        if(deployTool.tools[n].requests[r].tool_deployment_value[q].input_name === copyField.input_name)
                                        {
                                            fieldFlag++;
                                            ind = q;
                                        }
                                    }
                                    if(fieldFlag > 0)
                                    {
                                        deployTool.tools[n].requests[r].tool_deployment_value[ind].default_value = copyField.default_value;
                                        deployTool.tools[n].requests[r].tool_deployment_value[ind].input_value = copyField.input_value;
                                        deployTool.tools[n].requests[r].tool_deployment_value[ind].isDefault = false;
                                        deployTool.tools[n].requests[r].tool_deployment_value[ind].isCopiedToAllMachines = false;
                                    }
                                    else
                                    {
                                        deployTool.tools[n].requests[r].tool_deployment_value.push({'input_type' : copyField.input_type, 'input_name' : copyField.input_name, 'input_value' : copyField.input_value, 'default_value' : copyField.default_value, 'is_mandatory' : copyField.is_mandatory, 'isFieldUploaded' : copyField.isFieldUploaded});
                                        var fieldLength = deployTool.tools[n].requests[r].tool_deployment_value.length;
                                        deployTool.tools[n].requests[r].tool_deployment_value[fieldLength-1].isDefault = false;
                                        deployTool.tools[n].requests[r].tool_deployment_value[fieldLength-1].isCopiedToAllMachines = false;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        restoreDefaultValues : function(tool, machine)
        {
            length = deployTool.tools.length;
            var mIndex = 0;
            var copyField = [];
            if(length>=1)
            {
                for(var n=0; n<deployTool.tools.length; n++)
                {
                    if(deployTool.tools[n].tool_name === tool)
                    {
                        var machine_length = deployTool.tools[n].requests.length;
                        if(deployTool.tools[n].requests.length>0)
                        {
                            for(var o=0; o<deployTool.tools[n].requests.length; o++)
                            {
                                if(deployTool.tools[n].requests[o].machine_name === machine)
                                {
                                    angular.copy(deployTool.tools[n].tool_deployment_value, deployTool.tools[n].requests[o].tool_deployment_value);
                                    deployTool.tools[n].requests[o].isDefault = true;
                                    deployTool.tools[n].requests[o].isCopiedToAllMachines = false;
                                }
                            }
                        }
                    }
                }
            }
        },
        cleanDeployFactoryObject : function()
        {
            deployTool.tools = [];
            allVersions = [];
            deployMachine = [];
        },
        cloneRequestObject : function(requestObj)
        {
            deployTool.tools = requestObj;
        },
        addUploadedDeploymentFields : function(tool, machine, fields)
        {
            length = deployTool.tools.length;
            var tool_deployment_fields = [];
            if(length>=1)
            {
                for(var key=0; key<deployTool.tools.length; key++)
                {
                    if(deployTool.tools[key].tool_name === tool)
                    {
                        var machine_length = deployTool.tools[key].requests.length;
                        var addMachineFlag = 0;
                        for(var key_2=0; key_2<deployTool.tools[key].requests.length; key_2++)
                        {
                            if(deployTool.tools[key].requests[key_2].machine_name===machine)
                            {
                                for(var key_4=0; key_4<fields.length; key_4++)
                                {
                                    var deploymentfieldFlag = 0;
                                    var ind = 0;
                                    for(var key_3=0; key_3<deployTool.tools[key].requests[key_2].tool_deployment_value.length; key_3++)
                                    {
                                        if(deployTool.tools[key].requests[key_2].tool_deployment_value[key_3].input_name === fields[key_4].input_name)
                                        {
                                            deploymentfieldFlag++;
                                            ind = key_3;
                                        }
                                    }
                                    if(deploymentfieldFlag > 0)
                                    {
                                        deployTool.tools[key].requests[key_2].tool_deployment_value[ind].default_value = fields[key_4].default_value;
                                        deployTool.tools[key].requests[key_2].tool_deployment_value[ind].isDefault = true;
                                        deployTool.tools[key].requests[key_2].tool_deployment_value[ind].isCopiedToAllMachines = false;
                                        deployTool.tools[key].requests[key_2].tool_deployment_value[ind].isFieldUploaded = true;
                                    }
                                    else
                                    {
                                        var fieldLength = deployTool.tools[key].requests[key_2].tool_deployment_value.length;
                                        deployTool.tools[key].requests[key_2].tool_deployment_value.push({'input_name' : fields[key_4].input_name, 'input_type' : fields[key_4].input_type, 'default_value' : fields[key_4].default_value, 'is_mandatory' : fields[key_4].is_mandatory, 'is_default' : true, 'isCopiedToAllMachines' : false, 'isFieldUploaded' : true});
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        };
     }).factory('DeployDUFactory', function()  {
        var deployDU = {};
        var deployMachine= {};
        deployDU.du = [];

        deployMachine.machines=[];
        return {
        addDU : function(duData)
        {
//            du_id, du_name, du_type, build_number, build_id, deployment_fields, dependent, order
            var data = duData;
            var du_id = data.du_id;
            var du_name = data.du_name;
            var du_type = data.du_type;
            var build_number = data.build_number;
            var build_id = data.build_id;
            var state_id = data.state_id;
            var deployment_fields  = data.deployment_field_value;
            var dependent = data.du_dependent;
            var order = data.du_order;
            var package_state_id= data.package_state_id;
            var parent_entity_set_id= data.parent_entity_set_id;
            var flexible_attributes = data.flexible_attributes;
            var old_build_id = data.old_build_id;
            var old_build_number = data.old_build_number;
            var du_deployment_fields = [];
            if(deployment_fields!==null && deployment_fields!==undefined && deployment_fields!=='')
            {
                angular.copy(deployment_fields.fields, du_deployment_fields);
                for(var d=0; d<du_deployment_fields.length; d++)
                {
                    if(du_deployment_fields[d].input_type === 'date')
                    {
                        var date = new Date(du_deployment_fields[d].default_value);
                        delete du_deployment_fields[d].default_value;
                        du_deployment_fields[d].default_value = date;
                    }
                }
            }
            else
            {
                du_deployment_fields = [];
            }
            var length = deployDU.du.length;
            var flag = 0;
            var du_flag = 0;
            if(length>0)
            {
                for(var key=0; key<deployDU.du.length; key++)
                {
                    if(deployDU.du[key].du_name !== du_name)
                    {
                         du_flag++;
                    }
                }

                if(du_flag === deployDU.du.length)
                {
                    var duLength = deployDU.du.length;
                    deployDU.du.push({
                        'du_id' : du_id,
                        'du_name' : '',
                        'du_type' : '',
                        'build_number' : '',
                        'build_id' : '',
                        'state_id': '',
                        'dependent' : '',
                        'order' : '',
                        'package_state_id':'',
                        'parent_entity_set_id':'',
                        'du_deployment_value' :[],
                        'flexible_attributes':'',
                        'old_build_id':'',
                        'old_build_number':'',
                        'requests' : []
                    });
                    deployDU.du[length].du_id = du_id;
                    deployDU.du[length].du_name = du_name;
                    deployDU.du[length].du_type = du_type;
                    deployDU.du[length].build_id = build_id;
                    deployDU.du[length].build_number = build_number;
                    deployDU.du[length].state_id = state_id;
                    deployDU.du[length].dependent = dependent;
                    deployDU.du[length].package_state_id = package_state_id;
                    deployDU.du[length].parent_entity_set_id = parent_entity_set_id;
                    deployDU.du[length].order = order;
                    deployDU.du[length].flexible_attributes = flexible_attributes;
                    deployDU.du[length].old_build_id = old_build_id;
                    deployDU.du[length].old_build_number = old_build_number;
                    if(du_deployment_fields)
                    {
                        for(var key_3=0; key_3<du_deployment_fields.length; key_3++)
                        {
                            if(du_deployment_fields[key_3].input_type === "checkbox")
                            {
                                if(du_deployment_fields[key_3].default_value)
                                {
                                    du_deployment_fields[key_3].input_value = du_deployment_fields[key_3].default_value;
                                }
                            }
                        }
                        angular.copy(du_deployment_fields, deployDU.du[length].du_deployment_value);
                    }
                }
            }
            else
            {
                deployDU.du = [{
                    du_id : '',
                    du_name : '',
                    du_type : '',
                    build_number : '',
                    build_id : '',
                    state_id: '',
                    dependent : '',
                    package_state_id:'',
                    parent_entity_set_id:'',
                    order : '',
                    flexible_attributes:'',
                    old_build_id:'',
                    old_build_number:'',
                    du_deployment_value : [],
                    requests : []
                }];
                deployDU.du[0].du_id = du_id;
                deployDU.du[0].du_name = du_name;
                deployDU.du[0].build_id = build_id;
                deployDU.du[0].build_number = build_number;
                deployDU.du[0].state_id = state_id;
                deployDU.du[0].du_type = du_type;
                deployDU.du[0].dependent = dependent;
                deployDU.du[0].package_state_id = package_state_id;
                deployDU.du[0].parent_entity_set_id = parent_entity_set_id;
                deployDU.du[0].order = order;
                deployDU.du[0].flexible_attributes = flexible_attributes;
                deployDU.du[0].old_build_id = old_build_id;
                deployDU.du[0].old_build_number = old_build_number;
                if(du_deployment_fields)
                {
                    for(var key_2=0; key_2<du_deployment_fields.length; key_2++)
                    {
                        if(du_deployment_fields[key_2].input_type === "checkbox")
                        {
                            if(du_deployment_fields[key_2].default_value)
                            {
                                du_deployment_fields[key_2].input_value = du_deployment_fields[key_2].default_value;
                            }
                        }
                    }
                    angular.copy(du_deployment_fields, deployDU.du[length].du_deployment_value);
                }
            }
        },
        getDU : function()
        {
            return deployDU.du;
        },
        removeDU : function(id)
        {
            deployDU.du.splice(id,1);
            if(deployDU.du.length===0)
            {
                deployDU.selectedDU = '';
            }
            else
            {
                for(var m=0; m<deployDU.du.length; m++)
                {
                    if(deployDU.du[m].du_id === id)
                    {
                        deployDU.du.splice(m, 1);
                    }
                }
            }
        },
        addMachine : function(machineData)
        {
            var machines = machineData.machines;
            var du = machineData.du;
            var entity = machineData.entity;
            var skip_deployment = machineData.skip_deployment;
            var is_build_already_deployed = machineData.is_build_already_deployed;
            var machine_group_id = machineData.machine_group_id;
            var machineMatchingInd = machineData.machineMatchingInd;

            length = deployDU.du.length;
            var du_deployment_fields = [];
            if(length>=1)
            {
                if(entity === 'current')
                {
                    for(var key_1=0; key_1<deployDU.du.length; key_1++)
                    {
                        var machine_length_1 = deployDU.du[key_1].requests.length;
                        if(deployDU.du[key_1].du_name === du)
                        {
                            if(deployDU.du[key_1].requests.length>0)
                            {
                                var addMachineFlag_1 = 0;
                                for(var key_1_2=0; key_1_2<deployDU.du[key_1].requests.length; key_1_2++)
                                {
                                    if(deployDU.du[key_1].requests[key_1_2].machine_name === machines.machine_name)
                                    {
                                       console.log('This machie is already present for this tool.. select another');
                                    }
                                    else
                                    {
                                        addMachineFlag_1++;
                                    }
                                }
                                if(addMachineFlag_1 === machine_length_1)
                                {
                                        deployDU.du[key_1].requests.push({
                                            du_name : '',
                                            du_deployment_value : [],
                                            machine_id : '',
                                            machine_name : '',
                                            skip_deployment: '',
                                            is_build_already_deployed: '',
                                            machineMatchingInd:'',
                                            machine_group_id:''
                                        });
                                        deployDU.du[key_1].requests[machine_length_1].du_name = deployDU.du[key_1].requests[machine_length_1-1].du_name;
                                        angular.copy(deployDU.du[key_1].du_deployment_value, deployDU.du[key_1].requests[machine_length_1].du_deployment_value);
                                        deployDU.du[key_1].requests[machine_length_1].machine_name = machines.machine_name;
                                        deployDU.du[key_1].requests[machine_length_1].machine_id = machines._id.$oid;
                                        deployDU.du[key_1].requests[machine_length_1].isDefault = true;
                                        deployDU.du[key_1].requests[machine_length_1].isCopiedToAllMachines = false;
                                        deployDU.du[key_1].requests[machine_length_1].warning_flag = false;
                                        deployDU.du[key_1].requests[machine_length_1].skip_deployment = skip_deployment;
                                        deployDU.du[key_1].requests[machine_length_1].is_build_already_deployed = is_build_already_deployed;
                                        deployDU.du[key_1].requests[machine_length_1].machineMatchingInd = machineMatchingInd;
                                        deployDU.du[key_1].requests[machine_length_1].machine_group_id = machine_group_id;

                                }
                            }
                            else
                            {
                                deployDU.du[key_1].requests.push({
                                    du_name : '',
                                    du_deployment_value : [],
                                    machine_id : '',
                                    machine_name : '',
                                    skip_deployment : '',
                                    is_build_already_deployed : '',
                                    machineMatchingInd:'',
                                    machine_group_id:''
                                });
                                deployDU.du[key_1].requests[0].du_name = deployDU.du[key_1].du_name;
                                angular.copy(deployDU.du[key_1].du_deployment_value, deployDU.du[key_1].requests[0].du_deployment_value);
                                deployDU.du[key_1].requests[0].machine_name = machines.machine_name;
                                deployDU.du[key_1].requests[0].machine_id = machines._id.$oid;
                                deployDU.du[key_1].requests[0].isDefault = true;
                                deployDU.du[key_1].requests[0].isCopiedToAllMachines = false;
                                deployDU.du[key_1].requests[0].warning_flag = false;
                                deployDU.du[key_1].requests[0].skip_deployment = skip_deployment;
                                deployDU.du[key_1].requests[0].is_build_already_deployed = is_build_already_deployed;
                                deployDU.du[key_1].requests[0].machineMatchingInd = machineMatchingInd;
                                deployDU.du[key_1].requests[0].machine_group_id = machine_group_id;
                            }
                        }
                    }
                }
                else
                {
                    for(var key_2=0; key_2<deployDU.du.length; key_2++)
                    {
                        var machine_length_2 = deployDU.du[key_2].requests.length;
                        if(deployDU.du[key_2].du_name === du)
                        {
                            if(deployDU.du[key_2].requests.length>0)
                            {
                                var addMachineFlag_2 = 0;
                                for(var key_3=0; key_3<deployDU.du[key_2].requests.length; key_3++)
                                {
                                    if(deployDU.du[key_2].requests[key_3].machine_name === machines.machine_name)
                                    {
                                       console.log('This machie is already present for this tool.. select another');
                                    }
                                    else
                                    {
                                        addMachineFlag_2++;
                                    }
                                }
                                if(addMachineFlag_2 === machine_length_2)
                                {
                                        deployDU.du[key_2].requests.push({
                                            du_name : '',
                                            du_deployment_value : [],
                                            machine_id : '',
                                            machine_name : '',
                                            machineMatchingInd:'',
                                            machine_group_id:''
                                        });
                                        deployDU.du[key_2].requests[machine_length_2].du_name = deployDU.du[key_2].requests[machine_length_2-1].du_name;
                                        angular.copy(deployDU.du[key_2].du_deployment_value, deployDU.du[key_2].requests[machine_length_2].du_deployment_value);
                                        deployDU.du[key_2].requests[machine_length_2].machine_name = machines.machine_name;
                                        deployDU.du[key_2].requests[machine_length_2].machine_id = machines._id.$oid;
                                        deployDU.du[key_2].requests[machine_length_2].isDefault = true;
                                        deployDU.du[key_2].requests[machine_length_2].isCopiedToAllMachines = false;
                                        deployDU.du[key_2].requests[machine_length_2].warning_flag = false;
                                        deployDU.du[key_2].requests[machine_length_2].skip_deployment = skip_deployment;
                                        deployDU.du[key_2].requests[machine_length_2].is_build_already_deployed = is_build_already_deployed;
                                        deployDU.du[key_2].requests[machine_length_2].machineMatchingInd = machineMatchingInd;
                                        deployDU.du[key_2].requests[machine_length_2].machine_group_id = machine_group_id;
                                }
                            }
                            else
                            {
                                deployDU.du[key_2].requests.push({
                                    du_name : '',
                                    du_deployment_value : [],
                                    machine_id : '',
                                    machine_name : '',
                                    machineMatchingInd:'',
                                    machine_group_id:''
                                });
                                deployDU.du[key_2].requests[0].du_name = deployDU.du[key_2].du_name;
                                angular.copy(deployDU.du[key_2].du_deployment_value, deployDU.du[key_2].requests[0].du_deployment_value);
                                deployDU.du[key_2].requests[0].machine_name = machines.machine_name;
                                deployDU.du[key_2].requests[0].machine_id = machines._id.$oid;
                                deployDU.du[key_2].requests[0].isDefault = true;
                                deployDU.du[key_2].requests[0].isCopiedToAllMachines = false;
                                deployDU.du[key_2].requests[0].warning_flag = false;
                                deployDU.du[key_2].requests[0].skip_deployment = skip_deployment;
                                deployDU.du[key_2].requests[0].is_build_already_deployed = is_build_already_deployed;
                                deployDU.du[key_2].requests[0].machineMatchingInd = machineMatchingInd;
                                deployDU.du[key_2].requests[0].machine_group_id = machine_group_id;
                            }
                        }

                    }
                }
            }
            else
            {
                    deployDU.du[0].requests[0].machine_name = machines.machine_name;
                    deployDU.du[0].requests[0].machine_id = machines._id.$oid;
                    deployDU.du[0].requests[0].isDefault = true;
                    deployDU.du[0].requests[0].isCopiedToAllMachines = false;
                    deployDU.du[0].requests[0].warning_flag = false;
                    deployDU.du[0].requests[0].skip_deployment = skip_deployment;
                    deployDU.du[0].requests[0].is_build_already_deployed = is_build_already_deployed;
                    deployDU.du[0].requests[0].machineMatchingInd = machineMatchingInd;
            }
        },
        removeMachine : function(du_name, machine)
        {
            var length = deployDU.du.length;
            for(var n=0; n<length; n++)
            {
                if(deployDU.du[n].du_name === du_name)
                {
                    if(machine !== 'all')
                    {
                        for(var o=0; o<deployDU.du[n].requests.length; o++)
                        {
                            if(deployDU.du[n].requests[o].machine_name === machine)
                            {
                                deployDU.du[n].requests.splice(o, 1);
                            }
                        }
                    }
                    else
                    {
                        deployDU.du[n].requests = [];
                    }
                }
            }
        },
        copyToAllMachines : function(du, machine)
        {
            length = deployDU.du.length;
            var mIndex = 0;
            var du_deployment_fields = [];
            if(length>=1)
            {
                for(var n=0; n<deployDU.du.length; n++)
                {
                    if(deployDU.du[n].du_name === du)
                    {
                        var machine_length = deployDU.du[n].requests.length;
                        if(deployDU.du[n].requests.length>0)
                        {
                            for(var o=0; o<deployDU.du[n].requests.length; o++)
                            {
                                if(deployDU.du[n].requests[o].machine_name === machine.machine_name)
                                {
                                    deployDU.du[n].requests[o].isDefault = true;
                                    deployDU.du[n].requests[o].isCopiedToAllMachines = true;
                                    mIndex = o;
                                }
                            }
                            for(var p=0; p<deployDU.du[n].requests.length; p++)
                            {
                                if(p!==mIndex)
                                {
                                    angular.copy(deployDU.du[n].requests[mIndex].du_deployment_value, deployDU.du[n].requests[p].du_deployment_value);
                                    deployDU.du[n].requests[p].isDefault = false;
                                    deployDU.du[n].requests[p].isCopiedToAllMachines = false;
                                }
                            }
                        }
                    }
                }
            }
        },
        copyfieldValueToAllMachines : function(du, machine, fieldIndex)
        {
            length = deployDU.du.length;
            var mIndex = 0;
            var copyField = [];
            if(length>=1)
            {
                for(var n=0; n<deployDU.du.length; n++)
                {
                    if(deployDU.du[n].du_name === du)
                    {
                        var machine_length = deployDU.du[n].requests.length;
                        if(deployDU.du[n].requests.length>0)
                        {
                            for(var o=0; o<deployDU.du[n].requests.length; o++)
                            {
                                if(deployDU.du[n].requests[o].machine_name === machine)
                                {
                                    for(var p=0; p<deployDU.du[n].requests[o].du_deployment_value.length; p++)
                                    {
                                        if(p===fieldIndex)
                                        {
                                            angular.copy(deployDU.du[n].requests[o].du_deployment_value[p], copyField);
                                            deployDU.du[n].requests[o].du_deployment_value[p].isDefault = false;
                                            deployDU.du[n].requests[o].du_deployment_value[p].isCopiedToAllMachines = true;
                                        }
                                    }
                                }
                            }
                            for(var r=0; r<deployDU.du[n].requests.length; r++)
                            {
                                var fieldFlag = 0;
                                var ind = 0;
                                if(deployDU.du[n].requests[r].machine_name !== machine)
                                {
                                    for(var q=0; q<deployDU.du[n].requests[r].du_deployment_value.length; q++)
                                    {
                                        if(deployDU.du[n].requests[r].du_deployment_value[q].input_name === copyField.input_name)
                                        {
                                            fieldFlag++;
                                            ind = q;
                                        }
                                    }
                                    if(fieldFlag > 0)
                                    {
                                        deployDU.du[n].requests[r].du_deployment_value[ind].default_value = copyField.default_value;
                                        deployDU.du[n].requests[r].du_deployment_value[ind].input_value = copyField.input_value;
                                        deployDU.du[n].requests[r].du_deployment_value[ind].isDefault = false;
                                        deployDU.du[n].requests[r].du_deployment_value[ind].isCopiedToAllMachines = false;
                                    }
                                    else
                                    {
                                        deployDU.du[n].requests[r].du_deployment_value.push({'input_type' : copyField.input_type, 'input_name' : copyField.input_name, 'input_value' : copyField.input_value, 'default_value' : copyField.default_value, 'is_mandatory' : copyField.is_mandatory, 'isFieldUploaded' : copyField.isFieldUploaded});
                                        var fieldLength = deployDU.du[n].requests[r].du_deployment_value.length;
                                        deployDU.du[n].requests[r].du_deployment_value[fieldLength-1].isDefault = false;
                                        deployDU.du[n].requests[r].du_deployment_value[fieldLength-1].isCopiedToAllMachines = false;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        restoreDefaultValues : function(du, machine)
        {
            length = deployDU.du.length;
            var mIndex = 0;
            var copyField = [];
            if(length>=1)
            {
                for(var n=0; n<deployDU.du.length; n++)
                {
                    if(deployDU.du[n].du_name === du)
                    {
                        var machine_length = deployDU.du[n].requests.length;
                        if(deployDU.du[n].requests.length>0)
                        {
                            for(var o=0; o<deployDU.du[n].requests.length; o++)
                            {
                                if(deployDU.du[n].requests[o].machine_name === machine)
                                {
                                    angular.copy(deployDU.du[n].du_deployment_value, deployDU.du[n].requests[o].du_deployment_value);
                                    deployDU.du[n].requests[o].isDefault = true;
                                    deployDU.du[n].requests[o].isCopiedToAllMachines = false;
                                }
                            }
                        }
                    }
                }
            }
        },
        cleanDeployDUFactoryObject : function()
        {
            deployDU.du = [];
            deployMachine = [];
        },
        cloneRequestObject : function(requestObj)
        {
            deployDU.du = requestObj;
        },
        addUploadedDeploymentFields : function(du, machine, fields)
        {
            length = deployDU.du.length;
            var du_deployment_fields = [];
            if(length>=1)
            {
                for(var key=0; key<deployDU.du.length; key++)
                {
                    if(deployDU.du[key].du_name === du)
                    {
                        var machine_length = deployDU.du[key].requests.length;
                        var addMachineFlag = 0;
                        for(var key_2=0; key_2<deployDU.du[key].requests.length; key_2++)
                        {
                            if(deployDU.du[key].requests[key_2].machine_name===machine)
                            {
                                for(var key_4=0; key_4<fields.length; key_4++)
                                {
                                    var deploymentfieldFlag = 0;
                                    var ind = 0;
                                    for(var key_3=0; key_3<deployDU.du[key].requests[key_2].du_deployment_value.length; key_3++)
                                    {
                                        if(deployDU.du[key].requests[key_2].du_deployment_value[key_3].input_name === fields[key_4].input_name)
                                        {
                                            deploymentfieldFlag++;
                                            ind = key_3;
                                        }
                                    }
                                    if(deploymentfieldFlag > 0)
                                    {
                                        deployDU.du[key].requests[key_2].du_deployment_value[ind].default_value = fields[key_4].default_value;
                                        deployDU.du[key].requests[key_2].du_deployment_value[ind].isDefault = true;
                                        deployDU.du[key].requests[key_2].du_deployment_value[ind].isCopiedToAllMachines = false;
                                    }
                                    else
                                    {
                                        var fieldLength = deployDU.du[key].requests[key_2].du_deployment_value.length;
                                        deployDU.du[key].requests[key_2].du_deployment_value.push({'input_name' : fields[key_4].input_name, 'input_type' : fields[key_4].input_type, 'default_value' : fields[key_4].default_value, 'is_mandatory' : fields[key_4].is_mandatory, 'is_default' : true, 'isCopiedToAllMachines' : false, 'isFieldUploaded' : true});
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        };
    }).factory('FasMatchingFactory',['$rootScope', function($rootScope)  {
        return {
        checkMachineMatch : function(selectedDUValue ,machine)
        {

            if(machine.flexible_attributes && selectedDUValue.flexible_attributes)
            {
                //only match compType
                if((machine.flexible_attributes["compTypes"]) && (machine.flexible_attributes["compTypes"].includes(selectedDUValue.flexible_attributes["compTypes"])))
                {
                    return true;
                }
                return false;
            }
            else{
                return false;
            }
        }
    };

    }]);

    deploymentServicesApp.directive('uploadModel', ['$parse', '$rootScope', function ($parse, $rootScope) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.uploadModel);
            var modelSetter = model.assign;
            element.bind('change', function (evt) {
                scope.$apply(function () {
                var files = evt.target.files;
                if(files[0].type==='application/vnd.ms-excel')
                {
                    scope.fileToImport = files[0];
                    scope.importFileSelected = files[0].name;
                    modelSetter(scope, element[0].files[0]);
                }
                else if (files[0].name.match(".json$", "i")) {
                    scope.fileToImport = files[0];
                    scope.importFileSelected = files[0].name;
                    modelSetter(scope, element[0].files[0]);
                }
                else
                {
                    $rootScope.handleResponse('Invalid file format... Please select .csv or .json file');
                    return false;
                }

                });
            });
        }
    };
    }]);

    deploymentServicesApp.service('deploymentFieldFileUpload', ['$http','$rootScope', function ($http, $rootScope) {
        this.uploadFileToUrl = function (file, uploadUrl, entity_type, entity, machine) {

                      var fd = new FormData();
                      fd.append('file', file);
                      $http.post(uploadUrl, fd, {
                      transformRequest: angular.identity,
                      headers: {'Content-Type': undefined}
                   })

                   .success(function(successResponse){
                        $rootScope.resultPane = true;
                        $rootScope.preLoader = false;
                        $rootScope.deploymentFieldsToUpload = successResponse.data.fields;
                        $rootScope.handleResponse(successResponse);
                        if(entity_type ===  'tool')
                        {
                            $rootScope.deployToolFactory.addUploadedDeploymentFields(entity, machine, $rootScope.deploymentFieldsToUpload);
                        }
                        else
                        {
                            $rootScope.deployDUFactory.addUploadedDeploymentFields(entity, machine, $rootScope.deploymentFieldsToUpload);
                        }
                        return successResponse.data.fields;
                   })

                   .error(function(errorResponse){
                        $rootScope.resultPane = true;
                        $rootScope.preLoader = false;
                        $rootScope.handleResponse(errorResponse);
                        return null;
                   });
        };
    }]);

  });