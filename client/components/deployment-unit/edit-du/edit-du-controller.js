define(['angular', 'ngResource', 'uiRouter', 'ngCookies','toolTips', 'jquery', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp'], function (app) {
  'use strict';

var editDUControllerApp = angular.module('editDUControllerApp', ['ui.router','720kb.tooltips', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp']);

editDUControllerApp.controller('EditDUController', function ($scope, $stateParams, $rootScope, $state, $cookieStore, PrerequisitesViewAll, ApprovalStatusAll, DUTypesAll, UserDetails, ViewDU, EditDU, TagsAll, DUDelete, GetAllDeploymentPlugins) {
    var date = new Date();
    $scope.prerequisites = [];
    $scope.du_errors = {
         deployment_field_errors : {
            input_name : '',
            input_type : '',
            default_value : '',
            valid_values : '',
            tooltip : ''
        }
    };
    $scope.userData = $rootScope.userFactory.getUserDetails();
    window.onclick=function ()
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
    GetAllDeploymentPlugins.get({
        value:"deployment"
    },
    function(successResponse)
    {
        $scope.allDeploymentPlugins = successResponse.data;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.flexibleAttributes = {};
    $scope.faNameValueMap = {};
    $scope.faDefLoaded = function(faDef){
        $scope.flexibleAttributes = faDef;

        ViewDU.get({
        id : $stateParams.id
        },
        function(viewDUSuccessResponse)
        {
            $scope.application = viewDUSuccessResponse;
            if(viewDUSuccessResponse.data.deployment_field)
            {
                for(var d=0; d<viewDUSuccessResponse.data.deployment_field.fields.length; d++)
                {
                    if(viewDUSuccessResponse.data.deployment_field.fields[d].input_type === 'date')
                    {
                        var date = new Date(viewDUSuccessResponse.data.deployment_field.fields[d].default_value);
                        delete viewDUSuccessResponse.data.deployment_field.fields[d].default_value;
                        viewDUSuccessResponse.data.deployment_field.fields[d].default_value = date;
                    }
                    viewDUSuccessResponse.data.deployment_field.fields[d].is_existing = true;
                }
            }
            if(!$scope.application.data.deployer_to_use)
            {
                $scope.application.data.deployer_to_use = $scope.allDeploymentPlugins[0];
            }
            var approval_status = $scope.application.data.approval_status;
            $scope.oldStatus = '';
            var du_type = $scope.application.data.type;
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
                        $scope.oldStatus = $scope.approvalStatusAll[i].name;
                    }
                }
            },
            function(errorResponse)
            {
                 $rootScope.handleResponse(errorResponse);
            });

            DUTypesAll.get({
            },
            function(successResponse)
            {
                $scope.DUTypes = successResponse.data;
                for(var j=0; j<$scope.DUTypes.length; j++)
                {
                    if($scope.DUTypes[j]._id.$oid === du_type)
                    {
                        $scope.application.data.type = $scope.DUTypes[j].name;
                    }
                }
            },
            function(errorResponse)
            {
                 $rootScope.handleResponse(errorResponse);
            });

            $scope.prerequisiteData = PrerequisitesViewAll.get({
            },
            function(prerequisiteSuccessResponse)
            {
                for(var a=0; a<$scope.prerequisiteData.data.length; a++)
                {
                    for(var b=0; b<$scope.prerequisiteData.data[a].version_list.length; b++)
                    {
                        $scope.prerequisites.push({'prerequisites_name' : $scope.prerequisiteData.data[a].prerequisites_name, 'version' : $scope.prerequisiteData.data[a].version_list[b], 'isSelected' : false});
                    }
                }

                for(var d=0; d<$scope.application.data.pre_requiests.length; d++)
                {
                    for(var c=0; c<$scope.prerequisites.length; c++)
                    {
                        if(($scope.application.data.pre_requiests[d].name === $scope.prerequisites[c].prerequisites_name) && ($scope.application.data.pre_requiests[d].version === $scope.prerequisites[c].version))
                        {
                            $scope.prerequisites[c].isSelected = true;
                            c++;
                        }
                        else
                        {
                            $scope.prerequisites[c].isSelected = false;
                            c++;
                        }
                    }
                }

            },function(prerequisiteErrorResponse){
                   $rootScope.handleResponse(prerequisiteErrorResponse);
            });

            if ($scope.application.data.flexible_attributes){
                for(var k in $scope.application.data.flexible_attributes){
                    $scope.faNameValueMap[k]=$scope.application.data.flexible_attributes[k];
                }
            }
        },
        function(viewDUErrorResponse)
        {
            $rootScope.handleResponse(viewDUErrorResponse);
        });
    };

    $scope.removeThisDU = function(du_id)
    {
        $scope.removeDUId = du_id;
        $scope.entity_name = 'du';
        if(document.getElementById("delete_attenation_popup").style.display === "none" || document.getElementById("delete_attenation_popup").style.display === "")
        {
            $('#delete_attenation_popup').show(700);
        }
        else
        {
            $('#delete_attenation_popup').hide(700);
        }
    };

    $scope.continueRemoveDU = function()
    {
        $('#delete_attenation_popup').hide(700);
        DUDelete.remove({
            id : $scope.removeDUId
        },
        function (duDeleteSuccess)
        {
            $state.go('duDashboard');
            $rootScope.handleResponse(duDeleteSuccess);
        },
        function (duDeleteError){
            $rootScope.handleResponse(duDeleteError);
        });
    };

    $scope.cancelRemoveDU = function()
    {
        $('#delete_attenation_popup').hide(700);
    };

    $scope.showEditPrerequisites = function(index)
    {
        $scope.vIndex = index;
        if(document.getElementById("edit_prerequisite").style.display === "none" || document.getElementById("edit_prerequisite").style.display === "")
        {
            remaining_up();
            $('#edit_prerequisite').slideDown();
        }
        else
        {
           $('#edit_prerequisite').slideUp();
        }
    };

    $scope.closeEditPrerequisites = function()
    {
        $('#edit_prerequisite').slideUp();
    };

    $scope.showSettings = function()
    {
        if(document.getElementById("add_settings").style.display === "none" || document.getElementById("add_settings").style.display === "")
        {
            document.getElementById("add_settings").style.display = "block";
            $scope.addNewField();
        }
        else
        {
           document.getElementById("add_settings").style.display = "none";
        }
    };

    $scope.showEditSettings = function(index)
    {
        $scope.fieldIndex = index;
        if(document.getElementById("add_settings").style.display === "none" || document.getElementById("add_settings").style.display === "")
        {
            document.getElementById("add_settings").style.display = "block";
        }
        else
        {
           document.getElementById("add_settings").style.display = "none";
        }
    };

    $scope.closeSettings = function(fieldIndex)
    {
        if($scope.application.data.deployment_field.fields[fieldIndex].is_existing ===  false)
        {
            $scope.removeField(fieldIndex);
        }
        $('#add_settings').hide(700);
    };
    $scope.removeValidValue = function(fieldIndex, valueIndex)
    {
        $scope.application.data.deployment_field.fields[fieldIndex].valid_values.splice(valueIndex, 1);
    };

    $scope.saveSettings = function(fieldIndex)
    {
        if(!$scope.application.data.deployment_field.fields[fieldIndex].input_name)
        {
            $scope.du_errors.deployment_field_errors.input_name = 'Input name can not be empty';
            return false;
        }
        else
        {
            $scope.du_errors.deployment_field_errors.input_name = '';
        }
        if($scope.application.data.deployment_field.fields[fieldIndex].input_type === 'checkbox' || $scope.application.data.deployment_field.fields[fieldIndex].input_type === 'radio' || $scope.application.data.deployment_field.fields[fieldIndex].input_type === 'dropdown'  )
        {
            if($scope.application.data.deployment_field.fields[fieldIndex].valid_values.length>0)
            {
                 var validFieldFlag = 0;
                 for(var validFieldIndex = 0; validFieldIndex<$scope.application.data.deployment_field.fields[fieldIndex].valid_values.length; validFieldIndex++)
                 {
                    if($scope.application.data.deployment_field.fields[fieldIndex].valid_values[validFieldIndex] === '' || $scope.application.data.deployment_field.fields[fieldIndex].valid_values[validFieldIndex] === null || $scope.application.data.deployment_field.fields[fieldIndex].valid_values[validFieldIndex] === undefined)
                    {
                       validFieldFlag++;
                    }
                 }
                 if(validFieldFlag>0)
                 {
                     $scope.du_errors.deployment_field_errors.valid_values = 'Options can not be empty for this field';
                     return false;
                 }
                 else
                 {
                    $scope.du_errors.deployment_field_errors.valid_values = '';
                    $('#add_settings').hide(700);
                 }
            }
            else
            {
                $scope.du_errors.deployment_field_errors.valid_values = 'Please provide options for this field';
                return false;
            }
        }
        else
        {
          $('#add_settings').hide(700);
        }
        $scope.application.data.deployment_field.fields[fieldIndex].is_existing = true;
    };

    $scope.isFieldSelected = function(fieldName, fieldValue)
    {
        var duIndex = 0;
        for(var d=0;  d<$scope.application.data.deployment_field.fields.length; d++)
        {
            if($scope.application.data.deployment_field.fields[d].input_name === fieldName)
            {
                duIndex = d;
            }
        }

        if($scope.application.data.deployment_field.fields[duIndex].default_value)
        {
            var result = $.inArray(fieldValue, $scope.application.data.deployment_field.fields[duIndex].default_value);
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

    $scope.addDefaultValueToCheckbox = function(fieldName, fieldValue)
    {
        var fieldIndex = 0;
        for(var validFieldIndex = 0; validFieldIndex<$scope.application.data.deployment_field.fields.length; validFieldIndex++)
        {
            if($scope.application.data.deployment_field.fields[validFieldIndex].input_name === fieldName)
            {
                fieldIndex = validFieldIndex;
            }
        }

        if($scope.application.data.deployment_field.fields[fieldIndex].default_value)
        {
            var result = $.inArray(fieldValue, $scope.application.data.deployment_field.fields[fieldIndex].default_value);
            if(result < 0)
            {
                $scope.application.data.deployment_field.fields[fieldIndex].default_value.push(fieldValue);
            }
            else
            {
                var index = $scope.application.data.deployment_field.fields[fieldIndex].default_value.indexOf(fieldValue);
                $scope.application.data.deployment_field.fields[fieldIndex].default_value.splice(index, 1);
            }
        }
        else
        {
            $scope.application.data.deployment_field.fields[fieldIndex].default_value = [];
            $scope.application.data.deployment_field.fields[fieldIndex].default_value.push(fieldValue);
        }
    };
    $scope.showAddTag = function()
    {
        if(document.getElementById("add_tag").style.display === "none" || document.getElementById("add_tag").style.display === "")
        {
            remaining_up();
            $('#add_tag').slideDown();
        }
        else
        {
           $('#add_tag').slideUp();
        }
    };

    $scope.closeAddTag = function()
    {
        $('#add_tag').slideUp();
    };

    $scope.isPrerequisiteSelected = function(prerequisite)
    {
        var flag = 0;
        if(!$scope.application.data.pre_requiests)
        {
            $scope.application.data.pre_requiests = [];
        }
        for(var j=0; j<$scope.application.data.pre_requiests.length; j++)
        {
            if((prerequisite.prerequisites_name === $scope.application.data.pre_requiests[j].name) && (prerequisite.version === $scope.application.data.pre_requiests[j].version))
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

    $scope.selectTag = function(tag)
    {
        var tag_flag = 0;
        var ind = 0;
        if($scope.application.data.tag.length>0)
        {
            for(var c=0;  c<$scope.application.data.tag.length; c++)
            {
                if(tag.name===$scope.application.data.tag[c])
                {
                    tag_flag++;
                    ind = c;
                }
            }

            if(tag_flag===0)
            {
                $scope.application.data.tag.push(tag.name);
            }
            else
            {
                $scope.application.data.tag.splice(ind, 1);
            }
        }
        else
        {
            $scope.application.data.tag = [];
            $scope.application.data.tag.push(tag.name);
        }
    };

    $scope.removeTag = function(tag)
    {
        var tag_flag = 0;
        var ind = 0;
        for(var c=0;  c<$scope.application.data.tag.length; c++)
        {
            if(tag===$scope.application.data.tag[c])
            {
                tag_flag++;
                ind = c;
            }
        }

        if(tag_flag > 0)
        {
            $scope.application.data.tag.splice(ind, 1);
        }
    };

    TagsAll.get({
    },
    function(successResponse)
    {
        $scope.allTags = successResponse;
        $scope.tagsAll = successResponse;
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    $scope.isTagSelected = function(tag)
    {
        var flag = 0;
        if($scope.application)
        {
            for(var j=0; j<$scope.application.data.tag.length; j++)
            {
                if(tag === $scope.application.data.tag[j])
                {
                    flag++;
                }
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

    var duData = {};
    var Deployment_fields = {};

    $scope.input_types = [
        "text",
        "password",
        "email",
        "date",
        "checkbox",
        "dropdown",
        "radio",
        "number"
    ];

    $scope.addNewChoice = function(index, name, version)
    {
        if($scope.application.data.pre_requiests)
        {
            $scope.application.data.pre_requiests.push({'name' : name, 'version' : version});
        }
        else
        {
            $scope.application.data.pre_requiests = [];
            $scope.application.data.pre_requiests.push({'name' : name, 'version' : version});
        }
    };

    $scope.addNewField = function()
    {
        if($scope.application.data.deployment_field !== null)
        {
            if($scope.application.data.deployment_field.fields.length === 0)
            {
               $scope.application.data.deployment_field = {
                    fields : []
                };
                $scope.fieldIndex = $scope.application.data.deployment_field.fields.length;
                $scope.application.data.deployment_field.fields.push({
                    order_id : $scope.fieldIndex,
                    valid_values : [],
                    is_existing : false
                });
            }
            else
            {
                $scope.fieldIndex = $scope.application.data.deployment_field.fields.length;
                $scope.application.data.deployment_field.fields.push({
                    order_id : $scope.fieldIndex,
                    valid_values : [],
                    is_existing : false
                });
            }
        }
        else
        {
            $scope.application.data.deployment_field = {
                fields : []
            };
            $scope.fieldIndex = $scope.application.data.deployment_field.fields.length;
            $scope.application.data.deployment_field.fields.push({
                order_id : $scope.fieldIndex,
                valid_values : [],
                is_existing : false
            });
        }
    };

    $scope.addNewValidValueField = function(index, version)
    {
        if($scope.application.data.deployment_field.fields[index].valid_values)
        {
            var len = ($scope.application.data.deployment_field.fields[index].valid_values).length;
        }
        else
        {
            $scope.application.data.deployment_field.fields[index].valid_values = [];
        }

        $scope.application.data.deployment_field.fields[index].valid_values.push("");
    };

    $scope.removeChoice = function(index)
    {
        var lastItem = $scope.application.data.pre_requiests.length-1;
        $scope.application.data.pre_requiests.splice(lastItem);
    };

    $scope.removeField = function(index) {
        $scope.application.data.deployment_field.fields.splice(index, 1);
    };

    $scope.removeValidValueField = function(index, version) {
        var lastItem = $scope.application.data.deployment_field.fields[index].valid_values.length-1;
        $scope.application.data.deployment_field.fields[index].valid_values.splice(lastItem,1);
    };

    $scope.selectPrerequisite = function(prerequisite)
    {
        var prerequisite_flag = 0;
        var ind = 0;
        if($scope.application.data.pre_requiests)
        {
            for(var c=0;  c<$scope.application.data.pre_requiests.length; c++)
            {
                if((prerequisite.prerequisites_name===$scope.application.data.pre_requiests[c].name) && (prerequisite.version===$scope.application.data.pre_requiests[c].version))
                {
                    prerequisite_flag++;
                    ind = c;
                }
            }

            if(prerequisite_flag===0)
            {
                $scope.application.data.pre_requiests.push({'name' : prerequisite.prerequisites_name, 'version' : prerequisite.version});
            }
            else
            {
                $scope.application.data.pre_requiests.splice(ind, 1);
            }

        }
        else
        {
            $scope.application.data.pre_requiests = [];
            $scope.application.data.pre_requiests.push({'name' : prerequisite.prerequisites_name, 'version' : prerequisite.version});
        }
    };

    $scope.addApproval = function(approval_status)
    {
        var flag = 0;
        var approval_flag = false;
        var newStatus = approval_status;
        $scope.userData = JSON.parse(sessionStorage.getItem('ga_userprofile'));
        for(var e=0; e<$scope.application.data.approval_list.length; e++)
        {
            if(newStatus!== $scope.application.data.approval_list[e].approval_status)
            {
                flag++;
            }
        }
        if(flag === $scope.application.data.approval_list.length)
        {
            $scope.application.data.approval_list.push({
                'approval_status' : newStatus,
                'approved_by' : $scope.userData.user,
                'approved_date' : date.toISOString()
            });
            $scope.application.data.approval_status = newStatus;
        }
        else
        {
            var length = $scope.application.data.approval_list.length;
            $scope.application.data.approval_status = $scope.application.data.approval_list[length-1].approval_status;
        }

    };

    $scope.selectDUType = function(du_type)
    {
        var type = du_type;
        $scope.application.data.type = type;
    };

   $scope.editDU = function(form)
   {
        var duData = {
            _id : {
                oid : ''
            }
        };
        if($scope.application.data.name === '')
        {
            $rootScope.handleResponse('Please enter the DU name');
            return false;
        }

        if($scope.application.data.tag === '')
        {
            $rootScope.handleResponse('Please enter the tags');
            return false;
        }

        if($scope.application.data.type === '')
        {
            $rootScope.handleResponse('Please select the DU type');
            return false;
        }
        if($scope.application.data.deployment_field)
        {
                for(var n=0; n<$scope.application.data.deployment_field.fields.length;n++)
                {
                    if($scope.application.data.deployment_field.fields.length>0)
                    {
                        if($scope.application.data.deployment_field.fields[n].input_type ==='' ||  $scope.application.data.deployment_field.fields[n].input_type===undefined || $scope.application.data.deployment_field.fields[n].input_type === null)
                        {
                            $scope.fieldIndex = n;
                            $('#add_settings').show(700);
                            $scope.du_errors.deployment_field_errors.input_type = 'Please enter input type!';
                            return false;
                        }
                        else
                        {
                        $scope.du_errors.deployment_field_errors.input_type = '';
                        }
                        if($scope.application.data.deployment_field.fields[n].input_name==='' || $scope.application.data.deployment_field.fields[n].input_name=== undefined ||  $scope.application.data.deployment_field.fields[n].input_name=== null)
                        {
                            $scope.fieldIndex = n;
                            $('#add_settings').show(700);
                            $scope.du_errors.deployment_field_errors.input_name = 'Please select input name!';
                            return false;
                        }
                        else
                        {
                            $scope.du_errors.deployment_field_errors.input_name = '';
                        }
                        if($scope.application.data.deployment_field.fields[n].input_type==='radio' || $scope.application.data.deployment_field.fields[n].input_type==='dropdown' || $scope.application.data.deployment_field.fields[n].input_type==='checkbox')
                        {
                            delete $scope.application.data.deployment_field.fields[n].selected_values;
                            if($scope.application.data.deployment_field.fields[n].valid_values.length===0)
                            {
                                $scope.fieldIndex = n;
                                $('#add_settings').show(700);
                                $scope.du_errors.deployment_field_errors.valid_values = 'Please enter at least one valid value!';
                                return false;
                            }
                            else
                            {
                            $scope.du_errors.deployment_field_errors.valid_values = '';
                            }
                        }
                        if(!$scope.application.data.deployment_field.fields[n].is_mandatory)
                        {
                            $scope.application.data.deployment_field.fields[n].is_mandatory = false;
                        }
                    }
                    delete $scope.application.data.deployment_field.fields[n].is_existing;
                }
        }
        else
        {
            $scope.application.data.deployment_field={
            fields : []
            };
        }
        duData.name = $scope.application.data.name;
        duData._id.oid = $scope.application.data._id.$oid;
        duData.type = $scope.application.data.type;
        if(!angular.isArray($scope.application.data.tag))
        {
            duData.tag = $scope.application.data.tag.split(",");
        }
        else
        {
            duData.tag = $scope.application.data.tag;
        }

        duData.release_notes = $scope.application.data.release_notes;
        duData.branch = $scope.application.data.branch;
        duData.pre_requiests = $scope.application.data.pre_requiests;
        duData.deployer_to_use = $scope.application.data.deployer_to_use;
        duData.repository_to_use = $scope.application.data.repository_to_use;
        duData.deployment_field = $scope.application.data.deployment_field;
        if(duData.deployment_field !== null)
        {
            if(duData.deployment_field._id)
            {
                var dfd =  duData.deployment_field._id.$oid;
                delete duData.deployment_field._id.$oid;
                duData.deployment_field._id = {
                    oid : ''
                };
                duData.deployment_field._id.oid = dfd;
            }
            for(var f=0; f<duData.deployment_field.fields.length; f++)
            {
                if((duData.deployment_field.fields[f].input_type !== 'checkbox') && (duData.deployment_field.fields[f].input_type !== 'dropdown') && (duData.deployment_field.fields[f].input_type !== 'radio'))
                {
                    delete duData.deployment_field.fields[f].valid_values;
                }
                else if(duData.deployment_field.fields[f].input_type === 'checkbox')
                {
                    if (!duData.deployment_field.fields[f].default_value)
                    {
                        duData.deployment_field.fields[f].default_value=[];
                    }
                }
                if(duData.deployment_field.fields[f].input_type === 'date')
                {
                    var longDate = new Date(duData.deployment_field.fields[f].default_value);
                    delete duData.deployment_field.fields[f].default_value;
                    duData.deployment_field.fields[f].default_value = longDate;
                }
            }
        }

        duData.approval_status = $scope.application.data.approval_status;
        duData.approval_list = $scope.application.data.approval_list;
        duData.flexible_attributes = $scope.faNameValueMap;

        $scope.editDUStatus = EditDU.update(duData, function(duCreateSuccessResponse)
        {
            $state.go('duDashboard');
            $rootScope.handleResponse(duCreateSuccessResponse);
        },
        function(duCreateErrorResponse)
        {
            $rootScope.handleResponse(duCreateErrorResponse);
        });
   };

});
});