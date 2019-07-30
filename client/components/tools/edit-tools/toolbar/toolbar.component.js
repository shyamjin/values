/*
Author - nlate
Description -
    1. Shows the toolbar with create and discard button
    2. Controller that handles with the operations to create new tool and discard all changes
Methods -
    1. createNewTool() - Creates a new tool
    2. discardChanges() - Discards all changes and redirects user to tool dashboard
Uses -
    1. Create Tool - components/tools/edit-tools/toolbar/toolbar.component.html
*/

define(['angular'],function (app) {
  'use strict';

var editToolBarComponentControllerApp = angular.module('editToolBarComponentControllerApp', []);

editToolBarComponentControllerApp.controller('EditToolBarController', function ($scope, $stateParams, GetAllTools, $state, EditTool, toolFileUpload, $rootScope, MediaUpdate, MediaDelete, PrerequisitesViewAll, DeleteTool, TagsAll, GetAllDeploymentPlugins, SystemData) {
    var toolMedia = {};
    var mediaFileData = [];
    SystemData.get({
    },
    function(SystemDataSuccessResponse)
    {
        $scope.dpm_type = SystemDataSuccessResponse.data.dpm_type;
    },
    function(SystemDataErrorResponse)
    {
        $rootScope.handleResponse(SystemDataErrorResponse);
    });

    $scope.editTool = function(form)
    {
        $rootScope.$emit('setToolData', {});
        $rootScope.$emit('setVersionData', {});
        $rootScope.$emit('setToolLogo', {});
        $rootScope.$emit('setMediaFiles', {});
        // Get tool general data and version data
        $rootScope.toolData = $rootScope.toolDetailsFactory.getToolData();
        $scope.versionData = $rootScope.toolDetailsFactory.getVersionList();

        // Validate tool general data and all version data
        var toolValidationResponse = $rootScope.toolDataValidatorFactory.validateToolData($rootScope.toolData);
        if(toolValidationResponse.result === "failed")
        {
            $rootScope.handleResponse(toolValidationResponse);
            return false;
        }
        else
        {

        }

        var versionValidationResponse = $rootScope.toolDataValidatorFactory.validateVersionData($scope.versionData);
        if(versionValidationResponse.result === "failed")
        {
            $rootScope.version_errors = versionValidationResponse.version_errors;
            $rootScope.displayTab = versionValidationResponse.display_tab;
            $rootScope.fieldIndex = versionValidationResponse.fieldIndex;
            return false;
        }

        var toolData = {};
        var versionData = {};
        var version_date = '';
        var vdate = '';
        var vdateISO = '';
        var full_version_date = '';

        // Set Tool General data
        toolData._id = {
            oid : ""
        };
        toolData._id.oid = $rootScope.toolData.tool_id;
        toolData.name = $rootScope.toolData.name;
        toolData.tag = $rootScope.toolData.tag;
        toolData.support_details = $rootScope.toolData.support_details;
        toolData.logo = $rootScope.toolData.logo;
        toolData.description = $rootScope.toolData.description;
        if(!angular.isArray($rootScope.toolData.tag))
        {
            toolData.tag = $rootScope.toolData.tag.split(",");
        }
        else
        {
            toolData.tag = $rootScope.toolData.tag;
        }
        toolData.support_details = $rootScope.toolData.support_details;
        $scope.logo = $rootScope.toolDetailsFactory.getToolLogo();
        if(!$scope.logo)
        {
            toolData.logo = $rootScope.toolData.logo;
        }
        toolData.description = $rootScope.toolData.description;
        if($scope.dpm_type === 'dpm_master')
        {
            toolData.is_tool_cloneable = $rootScope.toolData.is_tool_cloneable;
            toolData.artifacts_only = $rootScope.toolData.artifacts_only;
        }
        if($rootScope.toolData.status==='Active')
        {
            toolData.status = '1';
        }
        else if($rootScope.toolData.status==='In Development')
        {
            toolData.status = '2';
        }
        else if($rootScope.toolData.status==='Deprecated')
        {
            toolData.status = '3';
        }
        else
        {
            toolData.status = '0';
        }

        if($rootScope.toolData.allow_build_download==='Yes')
        {
            toolData.allow_build_download = 'true';
        }
        else
        {
            toolData.allow_build_download = 'false';
        }

        // Set version data
        for(var id_app_2=0; id_app_2<$scope.versionData.length; id_app_2++)
        {
                if($scope.versionData[id_app_2]._id)
                {

                    if ($scope.versionData[id_app_2]._id.oid === undefined)
                    {
                        var vid =  $scope.versionData[id_app_2]._id.$oid;
                        $scope.versionData[id_app_2]._id = {
                            oid : ""
                        };
                        $scope.versionData[id_app_2]._id.oid = vid;
                    }
                }

                if($scope.versionData[id_app_2].document)
                {
                    if($scope.versionData[id_app_2].document._id)
                    {
                        var did =  $scope.versionData[id_app_2].document._id.$oid;
                        $scope.versionData[id_app_2].document._id = {
                            oid : ""
                        };
                        $scope.versionData[id_app_2].document._id.oid = did;
                    }
                }

                if($scope.versionData[id_app_2].media_file)
                {
                    if($scope.versionData[id_app_2].media_file._id)
                    {
                        var mid =  $scope.versionData[id_app_2].media_file._id.$oid;
                        $scope.versionData[id_app_2].media_file._id = {
                            oid : ""
                        };
                        $scope.versionData[id_app_2].media_file._id.oid = mid;
                    }
                }

                if($scope.versionData[id_app_2].deployment_field)
                {
                    if($scope.versionData[id_app_2].deployment_field._id)
                    {
                        var dfd_id =  $scope.versionData[id_app_2].deployment_field._id.$oid;
                        $scope.versionData[id_app_2].deployment_field._id = {
                            oid : ""
                        };
                        $scope.versionData[id_app_2].deployment_field._id.oid = dfd_id;
                    }

                    for(var df=0;df<$scope.versionData[id_app_2].deployment_field.fields.length;df++)
                    {
                        if($scope.versionData[id_app_2].deployment_field.fields[df].input_type !== 'dropdown' && $scope.versionData[id_app_2].deployment_field.fields[df].input_type !== 'checkbox' && $scope.versionData[id_app_2].deployment_field.fields[df].input_type !== 'radio')
                        {
                            delete $scope.versionData[id_app_2].deployment_field.fields[df].valid_values;
                        }
                        if(!$scope.versionData[id_app_2].deployment_field.fields[df].is_mandatory)
                        {
                            $scope.versionData[id_app_2].deployment_field.fields[df].is_mandatory = false;
                        }
                        if($scope.versionData[id_app_2].deployment_field.fields[df].input_type==='date' && $scope.versionData[id_app_2].deployment_field.fields[df].default_value)
                        {
                            var fieldDate =  $scope.versionData[id_app_2].deployment_field.fields[df].default_value;
                            var dateFormat = new Date(fieldDate);
                            delete $scope.versionData[id_app_2].deployment_field.fields[df].default_value;
                            $scope.versionData[id_app_2].deployment_field.fields[df].default_value = dateFormat;
                        }
                    }
                }

                    var version_date =  $scope.versionData[id_app_2].version_date;
                    var vdate = new Date(version_date);
                    var vdateISO = vdate.toISOString();
                    var full_version_date = vdateISO.replace('T',' ');
                    full_version_date = full_version_date.replace('Z',' ');
                    delete $scope.versionData[id_app_2].version_date.$date;
                    $scope.versionData[id_app_2].version_date = full_version_date;


                if($scope.versionData[id_app_2].status==='Active')
                {
                    $scope.versionData[id_app_2].status = '1';
                }
                else
                {
                    $scope.versionData[id_app_2].status = '0';
                }
        }

        toolData.version = $scope.versionData;
        angular.copy(toolData, toolMedia);
        for(var id_ver=0;id_ver<toolData.version.length;id_ver++)
        {
            if(toolData.version[id_ver].media_file)
            {
                delete toolData.version[id_ver].media_file;
                delete toolData.version[id_ver].build;

            }
        }

        EditTool.update(toolData, function(toolEditResponse){
            $scope.removeMedia = function(media_id)
            {
                 $scope.mediaDeletion = MediaDelete.remove({
                      id :   media_id
                 },
                 function(mediaDeleteSuccess)
                 {
                    $rootScope.handleResponse(mediaDeleteSuccess);
                 },
                 function (mediaDeleteError){
                    $rootScope.handleResponse(mediaDeleteError);
                 });
            };

            for(var indx=0;indx<toolMedia.version.length;indx++)
            {
                for(var indx_1=0; indx_1<$rootScope.mediaFilesOriginalLength.length; indx_1++)
                {
                    if(toolMedia.version[indx].version_number === $rootScope.mediaFilesOriginalLength[indx_1].version_number)
                    {
                        if(toolMedia.version[indx].media_file.media_files.length>0)
                        {
                            if(toolMedia.version[indx].media_file.media_files.length !== $rootScope.mediaFilesOriginalLength[indx_1].length)
                            {
                                mediaFileData.push(toolMedia.version[indx].media_file);
                            }
                        }
                        else
                        {
                            var m_id = toolMedia.version[indx].media_file._id.oid;
                            $scope.removeMedia(m_id);
                        }
                    }
                }
            }

            if(mediaFileData.length>0)
            {
                $scope.mediaFileUpdate = MediaUpdate.update({"data":mediaFileData}, function(mediaUpdateResponse){
                    $rootScope.handleResponse(mediaUpdateResponse);
                },
                function(mediaUpdateErrorResponse)
                {
                        $rootScope.handleResponse(mediaUpdateErrorResponse);
                });
            }

            $scope.logo = $rootScope.toolDetailsFactory.getToolLogo();
            var file = $scope.logo;
            if(file)
            {
                file.tool_id = $rootScope.toolData.tool_id;

                var uploadUrl = "/tool/upload/logo";
                toolFileUpload.uploadFileToUrl(file, uploadUrl);
            }

           var screenshot = [];
           for(var l=0;l<$rootScope.screenshotFiles.length;l++)
           {
               screenshot = $rootScope.screenshotFiles[l];
               if(screenshot)
               {
                     if($rootScope.screenshotFiles[l].version_id)
                     {
                        screenshot.version_id= $rootScope.screenshotFiles[l].version_id;
                     }
                     else
                     {
                        screenshot.version_id= toolEditResponse.data.version_inserted;
                     }

                     var uploadScreenshotUrl = "/tool/versions/uploadScreenshot";
                     toolFileUpload.uploadScreenShotToUrl(screenshot, uploadScreenshotUrl);
               }
           }

            $rootScope.screenshotFiles = null;
            $rootScope.handleResponse(toolEditResponse);
            $state.go('dashboard');
        },
        function(toolEditErrorResponse) {
            $rootScope.handleResponse(toolEditErrorResponse);
        });
   };
});

});