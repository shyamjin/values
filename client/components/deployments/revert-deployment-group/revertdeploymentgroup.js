define(['angular','deploymentPartialControllerApp'],function (app) {
  'use strict';

var revertDeploymentGroupControllerApp = angular.module('revertDeploymentGroupControllerApp', ['deploymentPartialControllerApp']);

revertDeploymentGroupControllerApp.controller('RevertDeploymentGroupController', function ($scope,  $rootScope ,$state) {
    $rootScope.$on("revertDeploymentGroup", function (event, args) {
        $scope.deploymentsGroupData = args;
        $scope.deploymentTypeToSelect = {
        type : ""
        };
        $scope.PackageStateFlag = false;
    });

    $scope.deploymentTypeToSelect = {
        type : ""
    };
    $scope.revertDeploymentGroupData = {
            'deploymentGroup_id' : $scope.deploymentsGroupData.data._id.$oid,
            'duDataList' : []
    };

    $scope.setDUDeployType = function(value)
    {
        $scope.revertDeploymentGroupData.duDataList = [];
        $scope.deploymentTypeToSelect.type = value;
        $scope.packageData = null;
        for (var i=0; i <$scope.deploymentsGroupData.data.du_set_details.length; i++)
        {
            $scope.deploymentsGroupData.data.du_set_details[i]["state_details"] = null;
            $scope.deploymentsGroupData.data.du_set_details[i]["state_details_error"] = false;
        }
        if($scope.deploymentTypeToSelect.type === "PackageState")
        {
            $scope.PackageStateFlag = true;
        }
        else if($scope.deploymentTypeToSelect.type === "")
        {
            $scope.PackageStateFlag = false;
        }
    };
    $scope.showStateDetails = function(value)
    {
        $scope.packageData = JSON.parse(value);
        for (var i=0; i <$scope.deploymentsGroupData.data.du_set_details.length; i++)
        {
            $scope.deploymentsGroupData.data.du_set_details[i]["state_details"] = null;
            if($scope.packageData.states)
            {
                for(var j=0; j<$scope.packageData.states.length; j++)
                {
                    if($scope.deploymentsGroupData.data.du_set_details[i]._id.$oid ===  $scope.packageData.states[j].parent_entity_id)
                    {
                         $scope.deploymentsGroupData.data.du_set_details[i]["state_details"] = {};
                         $scope.deploymentsGroupData.data.du_set_details[i]["state_details"]["state_name"]=$scope.packageData.states[j].name;
                         $scope.deploymentsGroupData.data.du_set_details[i]["state_details"]["state_id"]=$scope.packageData.states[j]._id.$oid;
                         $scope.deploymentsGroupData.data.du_set_details[i]["state_details"]["build_id"]=$scope.packageData.states[j].build._id.$oid;
                         $scope.deploymentsGroupData.data.du_set_details[i]["state_details"]["build_number"]=$scope.packageData.states[j].build.build_number;
                         $scope.deploymentsGroupData.data.du_set_details[i]["state_details"]["deployment_field_value"]=$scope.packageData.states[j].deployment_field;
                         $scope.deploymentsGroupData.data.du_set_details[i]["state_details"]["package_state_id"]=$scope.packageData._id.$oid;
                         $scope.deploymentsGroupData.data.du_set_details[i]["state_details_error"] = false;
                         break;
                    }
                    $scope.deploymentsGroupData.data.du_set_details[i]["state_details_error"] = true;

                }
            }
        }

    };
    $scope.revertDeploymentGroup = function()
    {
        $scope.revertDeploymentGroupData.duDataList = [];
        if($scope.deploymentTypeToSelect.type === "")
        {
            $rootScope.handleResponse('Please select the Revert Type');
            return false;
        }
        if($scope.deploymentTypeToSelect.type === "PackageState")
        {

            if(!$scope.packageData)
            {
                $rootScope.handleResponse("Unable to revert. Please select Package state name");
                return false;
            }
            else
            {
                for(var k=0; k<$scope.deploymentsGroupData.data.du_set_details.length; k++)
                {
                      if(($scope.deploymentsGroupData.data.du_set_details[k].state_details !== null) || ($scope.deploymentsGroupData.data.du_set_details[k].state_details === undefined))
                      {
                        $scope.revertDeploymentGroupData.duDataList.push({"du_id" : $scope.deploymentsGroupData.data.du_set_details[k]._id.$oid,
                        "new_state_id" : $scope.deploymentsGroupData.data.du_set_details[k].state_details.state_id,
                        "new_build_id" : $scope.deploymentsGroupData.data.du_set_details[k].state_details.build_id,
                        "new_build_number":$scope.deploymentsGroupData.data.du_set_details[k].state_details.build_number,
                        "deployment_field":$scope.deploymentsGroupData.data.du_set_details[k].state_details.deployment_field_value,
                        "package_state_id":$scope.deploymentsGroupData.data.du_set_details[k].state_details.package_state_id,
                        "previous_state_id":$scope.deploymentsGroupData.data.du_set_details[k].old_deployment_details.old_state_id,
                        "previous_build_id":$scope.deploymentsGroupData.data.du_set_details[k].old_deployment_details.old_build_id,
                        "previous_build_number":$scope.deploymentsGroupData.data.du_set_details[k].old_deployment_details.old_build_number,
                        "machine_id":$scope.deploymentsGroupData.data.du_set_details[k].machine_id_list,
                        "parent_entity_set_id":$scope.deploymentsGroupData.data.du_set_details[k].old_deployment_details.parent_entity_set_id});
                      }
                }
            }
        }
        if($scope.revertDeploymentGroupData.duDataList.length>0)
        {
            $state.go('revertDU', {id:JSON.stringify($scope.revertDeploymentGroupData)});
        }
    }

    $scope.discardRevertChanges = function()
    {
        delete $scope.deploymentsGroupData;
        $scope.revertDeploymentGroupData.duDataList = [];
        $scope.selectDeploymentGroup($scope.selectedGroupID);
        $scope.selectDeployment(0);
    };

 });

});