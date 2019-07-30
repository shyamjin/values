/*
Author - nlate
Description -
    1. Controller that handles with the details of each version in tool
Methods -
    1. showSettings(index) - Shows a popup box for the deployment field of selected index of activer version
    2. showEditSettings(index, version_number) - Shows a popup box for the deployment field of selected index of activer version
    3. showCertified(index) - Shows popup for certified options
    4. closeCertified() - Closes a certified popup
    5. resetValidation() - Resets all validation messages in screen to empty
    6. closeSettings(version_index, field_index) - Closes the deployment field add or update popup
    7. saveSettings(version_index, field_index) - Saves the deployment field for the specific version of the tool
    8. addDefaultValueToCheckbox(field_name, field_value) - Selects and adds the default value for the checkbox
    9. showEditPrerequisites(index) - Shows popup for prerequisite add
    10. closeEditPrerequisites() - Closes popup for prerequisite add
    11. showDependentTools(index) - Shows popup for dependent tool add
    12. closeDependentTools() - Closes popup for dependent tool add
    13. showEditScreenshot(version_id, index) - Shows a popup for selecting screenshot files and sets version id and screenshot index
    14. closeEditScreenshot() - Opens a popup for screenshot
    15. selectMPSCertification(certificate) - Adds a vertificate from the list of certified popup
    16. selectPrerequisite(prerequisite) - Add a prerequisite from the list
    17. selectDependentTool(tool, version_index) - Adds a tool in dependent tool list for selected version
    18. isToolSelected(tool, version_index) - Returns true if tool is selected
    19. showDocument(index) - Shows a popup for add document
    20. showEditDocument(version_index, document_index) - Shows popup for edit document
    21. closeDocument() - Validates the document data in popup and closes the popup
    22. closeAddDocument(version_index, document_index) - Closes the document add popup and removes the document
    23. addNewChoice(index, name, version) - Adds a new prerequisite entry
    24. removeChoice(index) - Removes a prerequisite of selected index
    25. addNewField(index) - Adds new deployment field
    26. removeField(index) - Removes a field from deployment field at selected index
    27. addNewDocField(index) - Adds new document field
    28. removeDocField(index, version_index) - Removes a field from document fields
    29. addNewValidValueField(index, version) - Adds new valid value field
    30. removeValidValueField(index, version) - Removes a valid value of selected field
    31. removeValidValue(vIndex, fieldIndex, valueIndex)
    32. clearSnap(version_index, index) - Clears a screenshotfrom popup
    33. removeMediaFile(parent_index, file_index) - Removes a media file
Uses -
    1. Show Tool - components/tools/show-tool/version-form/versionsform.component.html
*/

define(['angular','repositoryServicesApp'],function (app) {
  'use strict';

var createToolVersionComponentControllerApp = angular.module('createToolVersionComponentControllerApp', ['repositoryServicesApp']);

createToolVersionComponentControllerApp.controller('CreateToolVersionController', function ($scope, $state, $rootScope, $window, GetAllTools, CreateTool, toolFileUpload, $timeout, PrerequisitesViewAll, TagsAll, GetAllDeploymentPlugins, repositoryViewAll) {
    $scope.version_date = new Date();
    $rootScope.displayTab = 0;
    $rootScope.vIndex  = 0;
    $rootScope.version_errors = {
        version_status: '',
        version_number : '',
        version_name : '',
        branch_tag : '',
        gitlab_repo :'',
        gitlab_branch : '',
        jenkins_job :'',
        backward_compatible : '',
        document_errors : {
            name : '',
            url : '',
            type : ''
        },
        deployment_field_errors : {
            input_name : '',
            input_type : '',
            default_value : '',
            valid_values : '',
            tooltip : ''
        }
    };

    $rootScope.versionData = [{
        version_number : null,
        version_name : '',
        version_date : new Date(),
        pre_requiests : [],
        gitlab_repo : '',
        gitlab_branch : '',
        jenkins_job : '',
        backward_compatible : 'no',
        mps_certified : [],
        release_notes : '',
        document : {
            documents : []
        },
        deployment_field : {
            fields : []
        },
        deployer_to_use : 'DefaultDeploymentPlugin',
        repository_to_use : ''
    }];

    $scope.date = new Date();
    var toolData = {};
    var versionData = {};
    versionData.version_date = {
        $date : ""
    };

    var documentData = {};
    var mediaData = {};
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

    $scope.mps_certification = [
        "MPS 7.5",
        "MPS 8.0",
        "MPS 8.1",
        "MPS 8.1.1",
        "MPS 8.1.2",
        "MPS 8.2",
        "MPS 8.3",
        "MPS 9.0",
        "MPS 9.1",
        "MPS 9.2",
        "MPS 9.3",
        "MPS 10",
        "MPS 10.1"
    ];

    $scope.attribute_types = [
        "Branch",
        "Tag"
    ];

    $scope.attr_type = {
        selected : ""
    };

    $scope.inputtype = {
       selected : ""
    };

    $scope.choices = [{}];
    $scope.Screen = [{}];
    $scope.fields = [{
        valid_values : []
    }];

    $scope.docs = [{}];
    $scope.valid_values = [{}];
    $scope.doc = {
      url : ""
    };
    $scope.screenshots = [];
    $rootScope.addScreenshotFiles = [];
    $scope.prerequisites = [];
    $scope.DependentTools = [];

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
                $rootScope.versionData[0].repository_to_use = $scope.repositoryAll.data[i].name;
                RepoInd = true;
                break;
            }
        }
        if(RepoInd === "false")
        {
            $rootScope.versionData.repository_to_use = $scope.repositoryAll.data[0].name;
        }
    },
    function(errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });

    GetAllTools.get({
        id: "all",
        status: "active,indevelopment,deprecated",
        page: 0,
        perpage: 0
    },
    function(toolViewSuccessResponse)
    {
        $scope.applications = toolViewSuccessResponse.data.data;
        for(var t1=0; t1<toolViewSuccessResponse.data.data.length; t1++)
        {
            for(var t2=0; t2<toolViewSuccessResponse.data.data[t1].versions.length; t2++)
            {
                $scope.DependentTools.push({'tool_id' : toolViewSuccessResponse.data.data[t1]._id.$oid, 'tool_name' : toolViewSuccessResponse.data.data[t1].name, 'version_id' : toolViewSuccessResponse.data.data[t1].versions[t2].version_id, 'version_name' : toolViewSuccessResponse.data.data[t1].versions[t2].version_name, 'version_number' : toolViewSuccessResponse.data.data[t1].versions[t2].version_number});
            }
        }
    },
    function(errorResponse)
    {
            $rootScope.handleResponse(errorResponse);
    });

    PrerequisitesViewAll.get({
    },
    function(prerequisiteSuccessResponse)
    {
        $scope.prerequisiteData = prerequisiteSuccessResponse;
        for(var a=0; a<$scope.prerequisiteData.data.length; a++)
        {
            for(var b=0; b<$scope.prerequisiteData.data[a].version_list.length; b++)
            {
                $scope.prerequisites.push({'prerequisites_name' : $scope.prerequisiteData.data[a].prerequisites_name, 'version' : $scope.prerequisiteData.data[a].version_list[b]});
            }

        }
    },
    function(prerequisiteErrorResponse)
    {
        $rootScope.handleResponse(prerequisiteErrorResponse);
    });

    //function for slideUp of all inactive button
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

    $scope.showSettings = function(index)
    {
        if(document.getElementById("add_settings").style.display === "none" || document.getElementById("add_settings").style.display === "")
        {
            $('#add_settings').show(700);
            $scope.addNewField(index);
        }
        else
        {
            $('#add_settings').hide(700);
        }
    };

    $scope.showEditSettings = function(index, version_number)
    {
        for(var version=0; version<$rootScope.versionData.length; version++)
        {
            if($rootScope.versionData[version].version_number === version_number)
            {
                $rootScope.vIndex  = version;
                $rootScope.fieldIndex = index;
            }
        }
        if(document.getElementById("add_settings").style.display === "none" || document.getElementById("add_settings").style.display === "")
        {
            $('#add_settings').show(700);
        }
        else
        {
            $('#add_settings').hide(700);
        }
    };

    $scope.showCertified = function(index)
    {
        $rootScope.vIndex  = index;
        if(document.getElementById("add_certificate").style.display === "none" || document.getElementById("add_certificate").style.display === "")
        {

            remaining_up();
            $('#add_certificate').slideDown();

        }
        else
        {
            $('#add_certificate').slideUp();
        }
    };
    $scope.closeCertified = function()
    {
        $('#add_certificate').slideUp();
    };

    $scope.resetValidation = function()
    {
        $scope.version_errors.version_name = "";
        $scope.version_errors.branch_tag = "";
    };

    $scope.closeSettings = function(vIndex, fieldIndex)
    {
        if($rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].is_existing ===  false)
        {
            $scope.removeField(fieldIndex);
        }
        $('#add_settings').hide(700);
    };

    $scope.saveSettings = function(vIndex, fieldIndex)
    {
        if(!$rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].input_name)
        {
            $scope.version_errors.deployment_field_errors.input_name = 'Input name can not be empty';
            return false;
        }
        else
        {
            $scope.version_errors.deployment_field_errors.input_name = '';
        }
        if($rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].input_type === 'checkbox' || $rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].input_type === 'radio' || $rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].input_type === 'dropdown')
        {
            if($rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].valid_values.length>0)
            {
                var validFieldFlag = 0;
                for(var validFieldIndex = 0; validFieldIndex<$rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].valid_values.length; validFieldIndex++)
                {
                    if($rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].valid_values[validFieldIndex] === '' || $rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].valid_values[validFieldIndex] === null || $rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].valid_values[validFieldIndex] === undefined)
                    {
                        validFieldFlag++;
                    }
                }
                if(validFieldFlag>0)
                {
                    $scope.version_errors.deployment_field_errors.valid_values = 'Options can not be empty for this field';
                    return false;
                }
                else
                {
                    $scope.version_errors.deployment_field_errors.valid_values = '';
                    $('#add_settings').hide(700);
                }
            }
            else
            {
                $scope.version_errors.deployment_field_errors.valid_values = 'Please provide options for this field';
                return false;
            }
        }
        else
        {
            $('#add_settings').hide(700);
        }
        $rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].is_existing = true;
    };

    $scope.addDefaultValueToCheckbox = function(fieldName, fieldValue)
    {
        var fieldIndex = 0;
        for(var validFieldIndex = 0; validFieldIndex<$rootScope.versionData[0].deployment_field.fields.length; validFieldIndex++)
        {
            if($rootScope.versionData[0].deployment_field.fields[validFieldIndex].input_name === fieldName)
            {
                fieldIndex = validFieldIndex;
            }
        }

        if($rootScope.versionData[0].deployment_field.fields[fieldIndex].default_value)
        {
            var result = $.inArray(fieldValue, $rootScope.versionData[0].deployment_field.fields[fieldIndex].default_value);
            if(result < 0)
            {
                $rootScope.versionData[0].deployment_field.fields[fieldIndex].default_value.push(fieldValue);
            }
            else
            {
                var index = $rootScope.versionData[0].deployment_field.fields[fieldIndex].default_value.indexOf(fieldValue);
                $rootScope.versionData[0].deployment_field.fields[fieldIndex].default_value.splice(index, 1);
            }
        }
        else
        {
            $rootScope.versionData[0].deployment_field.fields[fieldIndex].default_value = [];
            $rootScope.versionData[0].deployment_field.fields[fieldIndex].default_value.push(fieldValue);
        }
    };

    $scope.showEditPrerequisites = function(index)
    {
        $rootScope.vIndex  = index;
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

    $scope.showDependentTools = function(index)
    {
        $rootScope.vIndex  = index;
        if(document.getElementById("edit_dependent_tools").style.display === "none" || document.getElementById("edit_dependent_tools").style.display === "")
        {
           remaining_up();
            $('#edit_dependent_tools').slideDown();
        }
        else
        {
            $('#edit_dependent_tools').slideUp();
        }
    };

    $scope.closeDependentTools = function()
    {
        $('#edit_dependent_tools').slideUp();
    };

    $scope.showEditScreenshot = function(version_id, index)
    {
        $scope.version_id = version_id;
        $scope.sc_index = index;
        if(document.getElementById("edit_screenshot").style.display === "none" || document.getElementById("edit_screenshot").style.display === "")
        {
            remaining_up();
            $('#edit_screenshot').slideDown();
        }
        else
        {
            $('#edit_screenshot').slideUp();
        }
    };

    $scope.closeEditScreenshot = function()
    {
        $('#edit_screenshot').slideUp();
        delete $scope.editscreenshots;
    };

    $scope.loadScreenshot = function(file)
    {
        var srcId = null;
        if(!file)
        {
            $rootScope.handleResponse('Please select a image file for screenshot upload');
            return false;
        }
        else if(file.type==='image/jpeg' || file.type==='image/png' || file.type==='image/jpg' || file.type==='image/bmp' || file.type==='image/gif')
        {
            var length = $scope.screenshotFiles.length-1;
            var id = 'media_file_0_'+length;
            id = id.toString();
            var srcId = document.getElementById(id);
            if(srcId !== null)
            {
                srcId.src = URL.createObjectURL($scope.screenshotFiles[$scope.screenshotFiles.length-1][0]);
            }
            $('#edit_screenshot').slideUp(700);
        }
        else
        {
            $rootScope.handleResponse('Please select a image file for screenshot upload');
            return false;
        }
    };

    $scope.selectMPSCertification = function(certificate)
    {
        var mps_flag = 0;
        var ind = 0;
        if($rootScope.versionData[0].mps_certified)
        {
            for(var c=0;  c<$rootScope.versionData[0].mps_certified.length; c++)
            {
                if(certificate===$rootScope.versionData[0].mps_certified[c])
                {
                    mps_flag++;
                    ind = c;
                }
            }

            if(mps_flag===0)
            {
                $rootScope.versionData[0].mps_certified.push(certificate);
            }
            else
            {
                $rootScope.versionData[0].mps_certified.splice(ind, 1);
            }
        }
        else
        {
            $rootScope.versionData[0].mps_certified = [];
            $rootScope.versionData[0].mps_certified.push(certificate);
        }
    };

    $scope.selectPrerequisite = function(prerequisite)
    {
        var prerequisite_flag = 0;
        var ind = 0;
        if($rootScope.versionData[0].pre_requiests)
        {
            for(var c=0;  c<$rootScope.versionData[0].pre_requiests.length; c++)
            {
                if((prerequisite.prerequisites_name===$rootScope.versionData[0].pre_requiests[c].name) && (prerequisite.version===$rootScope.versionData[0].pre_requiests[c].version))
                {
                    prerequisite_flag++;
                    ind = c;
                }
            }

            if(prerequisite_flag===0)
            {
                $rootScope.versionData[0].pre_requiests.push({'name' : prerequisite.prerequisites_name, 'version' : prerequisite.version});
            }
            else
            {
                $rootScope.versionData[0].pre_requiests.splice(ind, 1);
            }
        }
        else
        {
            $rootScope.versionData[0].pre_requiests = [];
            $rootScope.versionData[0].pre_requiests.push({'name' : prerequisite.prerequisites_name, 'version' : prerequisite.version});
        }
    };

    $scope.selectDependentTool = function(tool, version_index)
    {
        var dependent_tool_flag = 0;
        var ind = 0;
        if($rootScope.versionData[version_index].dependent_tools)
        {
            for(var c=0;  c<$rootScope.versionData[version_index].dependent_tools.length; c++)
            {
                if((tool.tool_id===$rootScope.versionData[version_index].dependent_tools[c].tool_id))
                {
                    dependent_tool_flag++;
                    ind = c;
                }
            }

            if(dependent_tool_flag===0)
            {
                $rootScope.versionData[version_index].dependent_tools.push({'tool_id' : tool.tool_id, 'tool_name' : tool.tool_name, 'version_id' : tool.version_id, 'version_name' : tool.version_name, 'version_number' : tool.version_number});
            }
            else
            {
                if($rootScope.versionData[version_index].dependent_tools[ind].version_id === tool.version_id)
                {
                    $rootScope.versionData[version_index].dependent_tools.splice(ind, 1);
                }
                else
                {
                    $rootScope.versionData[version_index].dependent_tools.splice(ind, 1);
                    $rootScope.versionData[version_index].dependent_tools.push({'tool_id' : tool.tool_id, 'tool_name' : tool.tool_name, 'version_id' : tool.version_id, 'version_name' : tool.version_name, 'version_number' : tool.version_number});
                }
            }
        }
        else
        {
            $rootScope.versionData[version_index].dependent_tools = [];
            $rootScope.versionData[version_index].dependent_tools.push({'tool_id' : tool.tool_id, 'tool_name' : tool.tool_name, 'version_id' : tool.version_id, 'version_name' : tool.version_name, 'version_number' : tool.version_number});
        }
    };

    $scope.isToolSelected = function(tool, version_index)
    {
            var flag = 0;
            if(!$rootScope.versionData[version_index].dependent_tools)
            {
                $rootScope.versionData[version_index].dependent_tools = [];
            }
            else
            {
                for(var j=0; j<$rootScope.versionData[version_index].dependent_tools.length; j++)
                {
                    if(tool.version_id === $rootScope.versionData[version_index].dependent_tools[j].version_id)
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
            }
        };

    $scope.showDocument = function(version_index)
    {
        if($rootScope.versionData[version_index].document === null)
        {
            $scope.title = "Add a document";
            $rootScope.versionData[version_index].document = {
                documents : []
            };
            $scope.docIndex = $rootScope.versionData[version_index].document.documents.length;
        }
        else
        {
            $scope.title = "Add a document";
            $scope.docIndex = $rootScope.versionData[version_index].document.documents.length;
        }

        if(document.getElementById("add_document").style.display === "none" || document.getElementById("add_document").style.display === "")
        {
            $('#add_document').show(700);
            $scope.addNewDocField(version_index);
        }
        else
        {
           $('#add_document').hide(700);
        }
    };

    $scope.showEditDocument = function(version_number, doc_index)
    {
        for(var version=0; version<$rootScope.versionData.length; version++)
        {
            if($rootScope.versionData[version].version_number === version_number)
            {
                $scope.title = "Edit Document";
                $rootScope.vIndex  = version;
                $scope.docIndex = doc_index;
            }
        }

        if(document.getElementById("add_document").style.display === "none")
        {
            $('#add_document').show(700);
        }
        else
        {
            $('#add_document').hide(700);
        }
    };

    $scope.closeDocument = function()
    {
        var docIndex = $scope.docIndex;
        var url = $rootScope.versionData[0].document.documents[docIndex].url;
        if($rootScope.versionData[0].document.documents[docIndex].name===null || $rootScope.versionData[0].document.documents[docIndex].name==='' || $rootScope.versionData[0].document.documents[docIndex].name===undefined)
        {
            $scope.version_errors.document_errors.name = 'Please enter document name!';
        }
        if($rootScope.versionData[0].document.documents[docIndex].url===null || $rootScope.versionData[0].document.documents[docIndex].url==='' || $rootScope.versionData[0].document.documents[docIndex].url===undefined)
        {
            $scope.version_errors.document_errors.url = 'Please enter document url!';
        }
        if($rootScope.versionData[0].document.documents[docIndex].url!=='' && $rootScope.versionData[0].document.documents[docIndex].name==='')
        {
            $scope.version_errors.document_errors.name = 'Please enter document name!';
        }
        else if($rootScope.versionData[0].document.documents[docIndex].name!=='' && $rootScope.versionData[0].document.documents[docIndex].type==='')
        {
            $scope.version_errors.document_errors.type = 'Please enter document type!';
        }
        else if($rootScope.versionData[0].document.documents[docIndex].name!=='' && $rootScope.versionData[0].document.documents[docIndex].url==='')
        {
            $scope.version_errors.document_errors.url = 'Please enter document url!';
        }
        else if(((!url.includes("http://")) && (!url.includes("https://"))) || (url.lastIndexOf(".") < 0))
        {
            $scope.version_errors.document_errors.url = 'Please enter a valid document url!';
        }
        else
        {
            $('#add_document').hide(700);
            $scope.version_errors.document_errors.url = "";
            $scope.version_errors.document_errors.name = "";
            $scope.version_errors.document_errors.type = "";
        }
    };

    $scope.closeAddDocument = function(vIndex, document_index)
    {
        $('#add_document').hide(700);
        $scope.removeDocField(document_index, vIndex);
        $scope.version_errors.document_errors.url = "";
        $scope.version_errors.document_errors.name = "";
        $scope.version_errors.document_errors.type = "";
    };

    $scope.addNewChoice = function(index, name, version)
    {
        if($rootScope.versionData[index].pre_requiests)
        {
            $rootScope.versionData[index].pre_requiests.push({'name' : name, 'version' : version});
        }
        else
        {
            $rootScope.versionData[index].pre_requiests = [];
            $rootScope.versionData[index].pre_requiests.push({'name' : name, 'version' : version});
        }
    };

    $scope.addNewField = function(index)
    {
        $rootScope.vIndex  = index;
        if($rootScope.versionData[index].deployment_field===null)
        {
            $rootScope.versionData[index].deployment_field = {
                fields : []
            };
            $rootScope.fieldIndex = $rootScope.versionData[index].deployment_field.fields.length;
        }
        else
        {
            $rootScope.fieldIndex = $rootScope.versionData[index].deployment_field.fields.length;
            $rootScope.versionData[index].deployment_field.fields.push({
                valid_values : [],
                is_existing : false
            });
        }
    };

    $scope.addNewDocField = function(index)
    {
        if($rootScope.versionData[index].document===null)
        {
            $rootScope.versionData[index].document = {
                documents : []
            };
            $rootScope.versionData[index].document.documents.push({
                name : '',
                url : '',
                type : '',
                description : ''
            });
        }
        else
        {
            $rootScope.versionData[index].document.documents.push({
                name : '',
                url : '',
                type : '',
                description : ''
            });
        }
    };

    $scope.addNewValidValueField = function(index, version)
    {
        if($rootScope.versionData[version].deployment_field.fields[index].valid_values)
        {
            var len = ($rootScope.versionData[version].deployment_field.fields[index].valid_values).length;
        }
        else
        {
            $rootScope.versionData[version].deployment_field.fields[index].valid_values = [];
        }
        $rootScope.versionData[version].deployment_field.fields[index].valid_values.push("");
    };

    $scope.removeChoice = function(index)
    {
        var lastItem = $rootScope.versionData[index].pre_requiests.length-1;
        $rootScope.versionData[index].pre_requiests.splice(lastItem);
    };

    $scope.removeField = function(index)
    {
        $rootScope.versionData[0].deployment_field.fields.splice(index, 1);
    };

    $scope.removeDocField = function(index, version)
    {
        $rootScope.versionData[version].document.documents.splice(index,1);
    };

    $scope.removeValidValueField = function(index, version)
    {
        var lastItem = $rootScope.versionData[version].deployment_field.fields[index].valid_values.length-1;
        $rootScope.versionData[version].deployment_field.fields[index].valid_values.splice(lastItem,1);
    };

    $scope.removeValidValue = function(vIndex, fieldIndex, valueIndex)
    {
        $rootScope.versionData[vIndex].deployment_field.fields[fieldIndex].valid_values.splice(valueIndex, 1);
    };

    $scope.clearSnap = function(version_id, index)
    {
        for(var fileIndex=0;fileIndex<$rootScope.screenshotFiles.length;fileIndex++)
        {
            if(version_id===$rootScope.screenshotFiles[fileIndex].version_id)
            {
                $rootScope.screenshotFiles[fileIndex].screenshotFileSelected = "";
                $rootScope.screenshotFiles.splice(fileIndex,1);
                $scope.editscreenshots = null;
            }
            else
            {
                var newfileIndex = $rootScope.screenshotFiles.length-1;
                $rootScope.screenshotFiles.splice(newfileIndex,1);
                $scope.editscreenshots = null;
            }
        }
    };

    $scope.removeMediaFile = function(parentIndex, fileIndex)
    {
        $scope.screenshotFiles.splice(parentIndex, 1);
    };

    $rootScope.$on("setVersionData", function (event, args) {
        $rootScope.toolDetailsFactory.setVersionList($rootScope.versionData);
    });

    $rootScope.$on("setMediaFiles", function (event, args) {
        $rootScope.toolDetailsFactory.setMediaFiles($rootScope.screenshotFiles);
    });
});

});