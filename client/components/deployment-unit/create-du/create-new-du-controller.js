define(['angular', 'ngResource', 'uiRouter', 'ngCookies','toolTips', 'jquery', 'deploymentUnitsServicesApp','repositoryServicesApp' ,'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp'], function (app) {
  'use strict';

var addNewDUControllerApp = angular.module('addNewDUControllerApp', ['ui.router','720kb.tooltips', 'deploymentUnitsServicesApp', 'prerequisitesServicesApp', 'authenticationServicesApp','tagsServicesApp','flexAttributeDirectiveApp','repositoryServicesApp']);

addNewDUControllerApp.controller('CreateNewDUController', function ($scope, $rootScope, $state, PrerequisitesViewAll, ApprovalStatusAll, DUTypesAll, UserDetails, CreateDU, TagsAll,GetAllDeploymentPlugins,repositoryViewAll) {
    $scope.flexibleAttributes = {};
    $scope.faNameValueMap = {};
    $scope.faDefLoaded = function(faDef){
        $scope.flexibleAttributes = faDef;
    };

    $scope.prerequisites = [];

    $scope.application = {
        data:{
            name : '',
            tag : [],
            release_notes : '',
            branch:'',
            type : '',
            pre_requiests : [],
            deployer_to_use : 'DefaultDeploymentPlugin',
            repository_to_use:'',
            deployment_field : {
                fields : []
            }
        }
    };

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

    ApprovalStatusAll.get({
    },
    function(successResponse)
    {
        $scope.approvalStatusAll = successResponse;
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
    },
    function(errorResponse)
    {
      $rootScope.handleResponse(errorResponse);
    });

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

    repositoryViewAll.get({
    },
    function(successResponse)
    {
        $scope.repositoryAll = successResponse;
        var RepoInd = "false";
        for(var i=0; i<$scope.repositoryAll.data.length; i++)
        {
            if($scope.repositoryAll.data[i].is_default_repo_ind && $scope.repositoryAll.data[i].is_default_repo_ind.toLowerCase() === "true")
            {
                $scope.application.data.repository_to_use = $scope.repositoryAll.data[i].name;
                RepoInd = true;
                break;
            }
        }
        if(RepoInd === "false")
        {
            $scope.application.data.repository_to_use = $scope.repositoryAll.data[0].name;
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

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

    $scope.prerequisiteData = PrerequisitesViewAll.get({
    },
    function(prerequisiteSuccessResponse){
        for(var a=0; a<$scope.prerequisiteData.data.length; a++)
        {
            for(var b=0; b<$scope.prerequisiteData.data[a].version_list.length; b++)
            {
                $scope.prerequisites.push({'prerequisites_name' : $scope.prerequisiteData.data[a].prerequisites_name, 'version' : $scope.prerequisiteData.data[a].version_list[b]});
            }

        }
    },function(prerequisiteErrorResponse){
           $rootScope.handleResponse(prerequisiteErrorResponse);
    });

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
        if($scope.application.data.deployment_field.fields.length === 0)
        {
            $scope.fieldIndex = $scope.application.data.deployment_field.fields.length;
            $scope.application.data.deployment_field.fields.push({
                order_id : 1,
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

   $scope.createNewDU = function(form)
   {
        if (! validateDuData($scope, $rootScope)){
            return;
        }

        var duData = setuDuCreateData($scope);

        $scope.nreDUStatus = CreateDU.save(duData, function(duCreateSuccessResponse)
        {
            $rootScope.handleResponse(duCreateSuccessResponse);
            $state.go('viewDU', { "id": duCreateSuccessResponse.data._id});
        },
        function(duCreateErrorResponse)
        {
            $rootScope.handleResponse(duCreateErrorResponse);
        });
   };

    function setuDuCreateData(scope){
        var duData = {};

        var type = JSON.parse(scope.application.data.type);
        duData.name = scope.application.data.name;
        duData.type = type.name;
        duData.tag = scope.application.data.tag;
        duData.release_notes = scope.application.data.release_notes;
        duData.branch = scope.application.data.branch;
        duData.pre_requiests = scope.application.data.pre_requiests;
        duData.deployer_to_use = scope.application.data.deployer_to_use;
        duData.deployment_field = setupDuDeploymentFields(scope.application.data.deployment_field);
        duData.approval_status = 'Created';
        duData.repository_to_use = $scope.application.data.repository_to_use;
        scope.userData = $rootScope.userFactory.getUserDetails();
        duData.approval_list = [];

        var date = new Date();
        duData.approval_list.push({
            approval_status : 'Created',
            approved_by : scope.userData.user,
            approved_date : date.toISOString()

        });

        duData.flexible_attributes = scope.faNameValueMap;

        return duData;
    }

    function setupDuDeploymentFields(deployment_field){
        if(deployment_field !== null)
        {
            if(deployment_field._id)
            {
                var dfd =  deployment_field._id.$oid;
                delete deployment_field._id.$oid;
                deployment_field._id = {
                    oid : ''
                };
                deployment_field._id.oid = dfd;
            }
            for(var f=0; f<deployment_field.fields.length; f++)
            {
                if((deployment_field.fields[f].input_type !== 'checkbox') && (deployment_field.fields[f].input_type !== 'dropdown') && (deployment_field.fields[f].input_type !== 'radio'))
                {
                    delete deployment_field.fields[f].valid_values;
                }
                else if(deployment_field.fields[f].input_type === 'checkbox')
                {
                    if (!deployment_field.fields[f].default_value)
                    {
                        deployment_field.fields[f].default_value=[];
                    }
                }
                if(deployment_field.fields[f].input_type === 'date')
                {
                    var longDate = Date.parse(deployment_field.fields[f].default_value);
                    deployment_field.fields[f].default_value = longDate;
                }
            }
        }

        return deployment_field;
    }

    function validateDuData(scope, rootScope){
        if(scope.application.data.name === '')
        {
            rootScope.handleResponse('Please enter the DU name');
            return false;
        }

        if(scope.application.data.type === '')
        {
            rootScope.handleResponse('Please select the DU type');
            return false;
        }

        return validateDeploymentFields(scope);
    }

    function validateDeploymentFields(scope){
        if(scope.application.data.deployment_field)
        {
            for(var n=0; n<scope.application.data.deployment_field.fields.length;n++)
            {
                if(scope.application.data.deployment_field.fields.length>0)
                {
                    if(scope.application.data.deployment_field.fields[n].input_type ==='' ||  scope.application.data.deployment_field.fields[n].input_type===undefined || scope.application.data.deployment_field.fields[n].input_type === null)
                    {
                        scope.fieldIndex = n;
                        $('#add_settings').show(700);
                        scope.du_errors.deployment_field_errors.input_type = 'Please enter input type!';
                        return false;
                    }
                    else
                    {
                    scope.du_errors.deployment_field_errors.input_type = '';
                    }
                    if(scope.application.data.deployment_field.fields[n].input_name==='' || scope.application.data.deployment_field.fields[n].input_name=== undefined ||  scope.application.data.deployment_field.fields[n].input_name=== null)
                    {
                        scope.fieldIndex = n;
                        $('#add_settings').show(700);
                        scope.du_errors.deployment_field_errors.input_name = 'Please select input name!';
                        return false;
                    }
                    else
                    {
                        scope.du_errors.deployment_field_errors.input_name = '';
                    }
                    if(scope.application.data.deployment_field.fields[n].input_type==='radio' || scope.application.data.deployment_field.fields[n].input_type==='dropdown' || scope.application.data.deployment_field.fields[n].input_type==='checkbox')
                    {
                        delete scope.application.data.deployment_field.fields[n].selected_values;
                        if(scope.application.data.deployment_field.fields[n].valid_values.length===0)
                        {
                            scope.fieldIndex = n;
                            $('#add_settings').show(700);
                            scope.du_errors.deployment_field_errors.valid_values = 'Please enter at least one valid value!';
                            return false;
                        }
                        else
                        {
                        scope.du_errors.deployment_field_errors.valid_values = '';
                        }
                    }
                    if(!scope.application.data.deployment_field.fields[n].is_mandatory)
                    {
                        scope.application.data.deployment_field.fields[n].is_mandatory = false;
                    }
                }
                delete scope.application.data.deployment_field.fields[n].is_existing;
            }
        }

        return true;
    }

});
});