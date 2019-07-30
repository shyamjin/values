define(['angular', 'ngResource', 'uiRouter', 'ngCookies','toolTips', 'jquery', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp'], function (app) {
  'use strict';

var viewDUSetControllerApp = angular.module('viewDUSetControllerApp', ['ui.router','720kb.tooltips', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp']);

viewDUSetControllerApp.controller('ViewDUSetController', function ($scope, $stateParams, $rootScope, $state, ApprovalStatusAll, DUTypesAll, ViewDUSet,ViewDU, GetAllDUBuildData, GetDULatestBuildData, GetDUStateData, GetDUSetStateData, DUStateViewById, GetDUSetStateByID) {
    $scope.show = true;
    $scope.BuildFlag =false;
    $scope.StateFlag = false;
    $scope.PackageStateFlag = false;
    $scope.preLoader = false;

    $scope.showMore = function()
    {
        $scope.show = true;
    };

    $scope.showLess = function()
    {
        $scope.show = false;
    };

    $scope.deploymentTypeToSelect = {
        type : ""
    };



    ViewDUSet.get({
        id : $stateParams.id
    },
    function(viewDUSetSuccessResponse)
    {
        $scope.application = viewDUSetSuccessResponse;
        $scope.deployDUSetData = {
            'duset_id' : $scope.application.data._id.$oid,
            'duDataList' : [],
            'du_set_details1':{}
        };
        var approval_status = $scope.application.data.approval_status;

        ApprovalStatusAll.get({
        },
        function(successResponse)
        {
            $scope.approvalStatusAll = successResponse;
            for(var i=0; i<$scope.approvalStatusAll.length; i++)
            {
                if($scope.approvalStatusAll[i]._id.$oid === approval_status)
                {
                    $scope.application.data.approval_status = $scope.approvalStatusAll[i].name;
                }
            }
        },
        function(errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    },
    function(viewDUErrorResponse)
    {
        $rootScope.handleResponse(viewDUErrorResponse);
    });

    function reset_array_details()
    {

       var data = [];
        if($scope.application.data.du_set_details)
        {
            for (var i=0; i <$scope.application.data.du_set_details.length; i++)
        {
            if (!$scope.application.data.du_set_details[i].hasOwnProperty("added_manually_ind") == true )
            {

                  $scope.application.data.du_set_details[i]["state_details"] = null;
                  $scope.application.data.du_set_details[i]["state_details_error"] = false;
                  data.push($scope.application.data.du_set_details[i]);
            }
        }

         $scope.application.data.du_set_details = data;
        }
    }

    $scope.getDUBuildDetails = function()
    {
        $scope.preLoader = true;
        GetAllDUBuildData.get({
            id : $scope.application.data._id.$oid
        },
        function(viewDUBuildSuccessResponse)
        {
            $scope.application.data.du_set_details = viewDUBuildSuccessResponse.data.du_set_details;
            $scope.preLoader = false;
        },
        function(viewDUBuildErrorResponse)
        {
            $rootScope.handleResponse(viewDUBuildErrorResponse);
        });

    };

    $scope.getDUStateDetails = function()
    {
        $scope.preLoader = true;
        GetDUSetStateByID.get({
            parent_entity_id : $scope.application.data._id.$oid
        },
        function(viewDUBuildSuccessResponse)
        {
            $scope.application.data.du_set_details = viewDUBuildSuccessResponse.data.du_set_details;
            $scope.preLoader = false;
        },
        function(viewDUBuildErrorResponse)
        {
            $rootScope.handleResponse(viewDUBuildErrorResponse);
        });
    };

    $scope.getDUSetStateDetails = function()
    {
        $scope.preLoader = true;
        GetDUSetStateData.get({
            parent_entity_id : $scope.application.data._id.$oid,
            type : "dusetstate",
            page : 0,
            perpage : 0
        },
        function(viewDUBuildSuccessResponse)
        {
            $scope.application.data.state = viewDUBuildSuccessResponse.data.data;
            $scope.preLoader = false;
        },
        function(viewDUBuildErrorResponse)
        {
            $rootScope.handleResponse(viewDUBuildErrorResponse);
        });
    };

    $scope.setDUDeployType = function(value)
    {
        $scope.deploymentTypeToSelect.type = value;
        $scope.deployDUSetData.duDataList = [];
        $scope.deployDUSetData.du_set_details1 = {};
        $scope.packageData = null;
        reset_array_details();
        if($scope.deploymentTypeToSelect.type === "")
        {
            $scope.BuildFlag =false;
            $scope.StateFlag = false;
            $scope.PackageStateFlag = false;
            $scope.application.data.du_set_details = [];
        }
        if($scope.deploymentTypeToSelect.type === "Build")
        {
            $scope.BuildFlag =true;
            $scope.StateFlag = false;
            $scope.PackageStateFlag = false;
            // Call the function to get DU details by ID
            $scope.getDUBuildDetails();
        }
        else if($scope.deploymentTypeToSelect.type === "State")
        {
            $scope.BuildFlag =false;
            $scope.PackageStateFlag = false;
            $scope.StateFlag = true;
            // Call the function to get DU details with DU states
            $scope.getDUStateDetails();
        }
        else if($scope.deploymentTypeToSelect.type === "PackageState")
        {
            $scope.BuildFlag =false;
            $scope.StateFlag = false;
            $scope.PackageStateFlag = true;
            // Call the function to get DU states
            $scope.getDUSetStateDetails();
        }
        else if($scope.deploymentTypeToSelect.type === "Latest Build")
        {
            $scope.BuildFlag =false;
            $scope.StateFlag = false;
            $scope.PackageStateFlag = false;
            $scope.getDUBuildDetails();
        }

        if($scope.application.data.du_set_details)
        {
            for(var du=0; du<$scope.application.data.du_set_details.length; du++)
            {
                if($scope.application.data.du_set_details[du].state_approval_status)
                {
                    delete $scope.application.data.du_set_details[du].state_approval_status;
                }
            }
        }
    };

    $scope.showStateDetails = function(state_data)
    {
        var stateData = JSON.parse(state_data);
        var added_dus_list = [];
        $scope.preLoader = true;

        // this for loop is for those DU's that are part of du package as well du package state
        reset_array_details();
        GetAllDUBuildData.get({
            id : $scope.application.data._id.$oid
        },
        function(viewDUBuildSuccessResponse)
        {
            $scope.application.data.du_set_details = viewDUBuildSuccessResponse.data.du_set_details;
            DUStateViewById.get({
                id : stateData._id.$oid
            },
            function(viewStateSuccessResponse){
                $scope.packageData = viewStateSuccessResponse.data;
                for (var i=0; i <$scope.application.data.du_set_details.length; i++)
                {
                    $scope.application.data.du_set_details[i]["state_details"] = null;
                    if($scope.packageData.states)
                    {
                        for(var j=0; j<$scope.packageData.states.length; j++)
                        {
                            if($scope.application.data.du_set_details[i]._id.$oid ===  $scope.packageData.states[j].parent_entity_id)
                            {
                                 $scope.application.data.du_set_details[i]["state_details"] = {};
                                 $scope.application.data.du_set_details[i]["state_details"]["state_name"]=$scope.packageData.states[j].name;
                                 $scope.application.data.du_set_details[i]["state_details"]["state_id"]=$scope.packageData.states[j]._id.$oid;
                                 $scope.application.data.du_set_details[i]["state_details"]["build_id"]=$scope.packageData.states[j].build._id.$oid;
                                 $scope.application.data.du_set_details[i]["state_details"]["build_number"]=$scope.packageData.states[j].build.build_number;
                                 $scope.application.data.du_set_details[i]["state_details"]["deployment_field_value"]=$scope.packageData.states[j].deployment_field;
                                 $scope.application.data.du_set_details[i]["state_details"]["package_state_id"]=$scope.packageData._id.$oid;
                                 $scope.application.data.du_set_details[i]["state_details_error"] = false;
                                 $scope.application.data.du_set_details[i]["state_approval_status"] = $scope.packageData.states[j].approval_status;
                                 added_dus_list.push($scope.packageData.states[j].parent_entity_id); // to be used to filter dus added from states lists manually
                                 break;
                            }
                            $scope.application.data.du_set_details[i]["state_details_error"] = true;

                        }
                    }
                }
                // this forEach function is used when du get deleted from Du package but not exits in du package state.
                angular.forEach($scope.packageData.states, function(selectedStatesValues, key)
                {
                    if (added_dus_list.indexOf(selectedStatesValues.parent_entity_id) < 0)
                    {
                        ViewDU.get({
                            id : selectedStatesValues.parent_entity_id
                        },
                        function(viewDUSuccessResponse)
                        {
                             var data = {"_id":{},"state_details":{}};
                             data["_id"]["$oid"]=viewDUSuccessResponse.data._id.$oid;
                             data["name"]=viewDUSuccessResponse.data.name;
                             data["type"]=viewDUSuccessResponse.data.type;
                             data["dependent"]=viewDUSuccessResponse.data.dependent;
                             data["order"]= viewDUSuccessResponse.data.order;
                             data["flexible_attributes"] = viewDUSuccessResponse.data.flexible_attributes;
                             data["state_details"]["state_name"]=selectedStatesValues.name;
                             data["state_details"]["state_id"]=selectedStatesValues._id.$oid;
                             data["state_details"]["build_id"]=selectedStatesValues.build._id.$oid;
                             data["state_details"]["build_number"]=selectedStatesValues.build.build_number;
                             data["state_details"]["deployment_field_value"]=selectedStatesValues.deployment_field;
                             data["state_details"]["package_state_id"]=$scope.packageData._id.$oid;
                             data["state_details_error"] = false;
                             data["state_approval_status"] = $scope.packageData.approval_status;
                             data["added_manually_ind"] = true; //to be deleted later as added manually added for package states
                             $scope.application.data.du_set_details.push(data);

                        },
                        function(viewDUErrorResponse)
                        {
                            $rootScope.handleResponse(viewDUErrorResponse);
                        });

                    }
                });
                $scope.preLoader = false;
            },
            function(viewStateErrorResponse){

            });
        },
        function(viewDUBuildErrorResponse)
        {
            $rootScope.handleResponse(viewDUBuildErrorResponse);
        });

    };

    $scope.selectDU = function(duFullData, value)
    {
        var duData = JSON.parse(value);
        var duId = duFullData._id.$oid;
        var value = JSON.parse(value);
        if ($scope.deployDUSetData.du_set_details1[duId] === undefined)
        {
            $scope.deployDUSetData.du_set_details1[duId]={};
        }

        if($scope.deploymentTypeToSelect.type === "Build")
        {
            if (value !== undefined)
            {
                $scope.deployDUSetData.du_set_details1[duId]["du_id"]=duId;
                $scope.deployDUSetData.du_set_details1[duId]["name"]=duFullData.name;
                $scope.deployDUSetData.du_set_details1[duId]["type"]=duFullData.type;
                $scope.deployDUSetData.du_set_details1[duId]["dependent"]=duFullData.dependent;
                $scope.deployDUSetData.du_set_details1[duId]["order"]=duFullData.order;
                $scope.deployDUSetData.du_set_details1[duId]["flexible_attributes"]=duFullData.flexible_attributes;
                $scope.deployDUSetData.du_set_details1[duId]["deployment_field"]=duFullData.deployment_field;
                $scope.deployDUSetData.du_set_details1[duId]["build_id"]=duData._id.$oid;
                $scope.deployDUSetData.du_set_details1[duId]["build_number"]=duData.build_number;
                $scope.deployDUSetData.du_set_details1[duId]["package_state_id"]=undefined;
                $scope.deployDUSetData.du_set_details1[duId]["state_id"]=undefined;
            }
        }
        if($scope.deploymentTypeToSelect.type === "State")
        {
            if (value !== undefined)
            {
                $scope.deployDUSetData.du_set_details1[duId]["du_id"]=duId;
                $scope.deployDUSetData.du_set_details1[duId]["name"]=duFullData.name;
                $scope.deployDUSetData.du_set_details1[duId]["type"]=duFullData.type;
                $scope.deployDUSetData.du_set_details1[duId]["dependent"]=duFullData.dependent;
                $scope.deployDUSetData.du_set_details1[duId]["order"]=duFullData.order;
                $scope.deployDUSetData.du_set_details1[duId]["flexible_attributes"]=duFullData.flexible_attributes;
                $scope.deployDUSetData.du_set_details1[duId]["state_id"]=duData._id.$oid;
                $scope.deployDUSetData.du_set_details1[duId]["build_id"]=duData.build._id.$oid;
                $scope.deployDUSetData.du_set_details1[duId]["build_number"]=duData.build.build_number;
                $scope.deployDUSetData.du_set_details1[duId]["deployment_field"]=duData.deployment_field;
                $scope.deployDUSetData.du_set_details1[duId]["package_state_id"]=undefined;
                for(var du=0; du<$scope.application.data.du_set_details.length; du++)
                {
                    if($scope.application.data.du_set_details[du]._id.$oid === duFullData._id.$oid)
                    {
                        $scope.application.data.du_set_details[du].state_approval_status = value.approval_status;
                    }
                }
            }
        }
    };
    $scope.duSetDeploy = function()
    {
        var errMessage =[];
        $scope.deployDUSetData.duDataList=[];
        if($scope.deploymentTypeToSelect.type === "State" || $scope.deploymentTypeToSelect.type === "Build")
        {
            for(var j=0; j<$scope.application.data.du_set_details.length; j++)
            {
                 var data=$scope.deployDUSetData.du_set_details1[$scope.application.data.du_set_details[j]._id.$oid];
                 if (( data === undefined) || (data["build_id"] === undefined))
                 {
                    errMessage.push($scope.application.data.du_set_details[j].name.toString());
                 }
            }

            if (errMessage.length > 0)
            {
                $rootScope.handleResponse('Please enter details for : '+ errMessage.join(','));
                return false;
            }

            for(var m in $scope.deployDUSetData.du_set_details1)
            {
                var key = m;
                var val = $scope.deployDUSetData.du_set_details1[m];
                if (val["build_id"] !== undefined)
                {
                    $scope.deployDUSetData.duDataList.push(val);
                }

            }
        }
        else if ($scope.deploymentTypeToSelect.type === "Latest Build")
        {
            for(var i=0; i<$scope.application.data.du_set_details.length; i++)
            {
                if($scope.application.data.du_set_details[i].build)
                {
                    if($scope.application.data.du_set_details[i].build[0]._id.$oid === null || $scope.application.data.du_set_details[i].build[0]._id.$oid === undefined || $scope.application.data.du_set_details[i].build[0]._id.$oid === '')
                    {
                        $rootScope.handleResponse("Unable to deploy as "+$scope.application.data.du_set_details[i].name+" does not have a valid build");
                        return false;
                    }
                    else
                    {
                        var defaultToPush= {
                            "name" : $scope.application.data.du_set_details[i].name,
                            "type" : $scope.application.data.du_set_details[i].type,
                            "dependent" : $scope.application.data.du_set_details[i].dependent,
                            "order" : $scope.application.data.du_set_details[i].order,
                            "flexible_attributes": $scope.application.data.du_set_details[i].flexible_attributes,
                            'du_id' : $scope.application.data.du_set_details[i]._id.$oid,
                            "state_id" : undefined,
                            'build_id' : $scope.application.data.du_set_details[i].build[0]._id.$oid,
                            "build_number":$scope.application.data.du_set_details[i].build[0].build_number,
                            "deployment_field":$scope.application.data.du_set_details[i].deployment_field,
                            "package_state_id":undefined
                          };
                        $scope.deployDUSetData.duDataList.push(defaultToPush);
                    }

                }
                else
                {
                    $rootScope.handleResponse("Unable to deploy as "+$scope.application.data.du_set_details[i].name+" does not have a valid build");
                    return false;
                }

            }

        }
        else if($scope.deploymentTypeToSelect.type === "PackageState")
        {

            if(!$scope.packageData)
            {
                $rootScope.handleResponse("Unable to deploy. Please select DU Package state name");
                return false;
            }
            else
            {
                for(var k=0; k<$scope.application.data.du_set_details.length; k++)
                {
                      if(($scope.application.data.du_set_details[k].state_details !== null) || ($scope.application.data.du_set_details[k].state_details === undefined))
                      {
                          var dataToPush= {
                            "name" : $scope.application.data.du_set_details[k].name,
                            "type" : $scope.application.data.du_set_details[k].type,
                            "dependent" : $scope.application.data.du_set_details[k].dependent,
                            "order" : $scope.application.data.du_set_details[k].order,
                            "flexible_attributes": $scope.application.data.du_set_details[k].flexible_attributes,
                            "du_id" : $scope.application.data.du_set_details[k]._id.$oid,
                            "state_id" : $scope.application.data.du_set_details[k].state_details.state_id,
                            "build_id" : $scope.application.data.du_set_details[k].state_details.build_id,
                            "build_number":$scope.application.data.du_set_details[k].state_details.build_number,
                            "deployment_field":$scope.application.data.du_set_details[k].state_details.deployment_field_value,
                            "package_state_id":$scope.application.data.du_set_details[k].state_details.package_state_id
                          };

                        $scope.deployDUSetData.duDataList.push(dataToPush);
                      }
                }
            }
        }
        else if($scope.deploymentTypeToSelect.type === "")
        {
            $rootScope.handleResponse("Unable to deploy. Please select any Deployment Type");
            return false;
        }

        if($scope.deployDUSetData.duDataList.length>0)
        {
            $state.go('deployDUSet', {id:JSON.stringify($scope.deployDUSetData)});
        }
    };
});
});