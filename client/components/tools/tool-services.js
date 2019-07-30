define(['angular', 'ngResource'],function (app) {
  'use strict';

var toolServicesApp = angular.module('toolServicesApp', []);
toolServicesApp.factory('GetAllTools', function ($resource) {
    return $resource('/tool/:id', {
        id: '@_id'
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
}).factory('GetToolByID', function ($resource) {
    return $resource('/tool/view/:id', {
        id: '@_id'
    },
    {

    });
}).factory('CreateTool', function ($resource) {
    return $resource('/tool/add', {
    }, {

    });
}).factory('EditTool', function ($resource) {
    return $resource('/tool/update', {
    },
    {
        update :{
            method : 'PUT'
        }
    });
}).factory('MediaUpdate', function ($resource) {
    return $resource('/mediafiles/update', {
    }, {
            update :{
                    method : 'PUT'
            }
    });
}).factory('MediaDelete', function ($resource) {
    return $resource('/mediafiles/delete/:id', {
        id : '@_id'
    },
    {
        remove :{
            method : 'DELETE'
        }
    });
}).factory('DeleteTool', function($resource, $http,$rootScope){
    return $resource('/tool/delete/:id',{
        id:'@_id'
    },
    {
        remove : {
            method : 'DELETE'
        }
    });
}).factory('BuildById', function($resource, $http,$rootScope){
    return $resource('/build/view/:id',{
        id:'@_id'
    },
    {
    });
}).factory('ToolDetailsFactory', function()  {
    var toolData = {};
    var versionData = [];
    var activeVersionData = {};
    var logoFile = null;
    var mediaFiles = null;

    return {
        getToolData : function()
        {
            return toolData;
        },

        setToolData : function(tool_data)
        {
            toolData.name = tool_data.name;
            toolData.description = tool_data.description;
            toolData.status = tool_data.status;
            toolData.support_details = tool_data.support_details;
            toolData.logo = tool_data.logo;
            toolData.thumbnail_logo = tool_data.thumbnail_logo;
            toolData.allow_build_download = tool_data.allow_build_download;
            toolData.artifacts_only = tool_data.artifacts_only;
            toolData.is_tool_cloneable = tool_data.is_tool_cloneable;
            toolData.tag = tool_data.tag;
            if(tool_data._id)
            {
                toolData.tool_id = tool_data._id.$oid;
            }
            if(tool_data.master_clone_request_id)
            {
                toolData.master_clone_request_id = tool_data.master_clone_request_id;
            }
        },

        getVersionList : function()
        {
            return versionData;
        },

        setVersionList : function(version_list)
        {
            versionData = version_list;
        },

        getActiveVersionData : function()
        {
            return activeVersionData;
        },

        setActiveVersionData : function(version_data)
        {
            activeVersionData = version_data;
        },

        addNewVersion : function(new_version)
        {
            versionData.splice(0, 0, new_version);
        },

        removeVersion : function(ind)
        {
            versionData.splice(0, 1);
        },

        getToolLogo : function()
        {
            return logoFile;
        },

        setToolLogo : function(logo)
        {
            logoFile = logo;
        },

        getMediaFiles : function()
        {
            return mediaFiles;
        },

        setMediaFiles : function(files)
        {
            mediaFiles = files;
        },

        cleanToolDataObject : function()
        {
            toolData = {};
            versionData = [];
            activeVersionData = {};
            logoFile = null;
            mediaFiles = null;
        }
    };
}).factory('ToolDataValidatorFactory', function($rootScope)  {

    return {
        validateToolData : function(tool_data)
        {
            var response = {
                "message" : "",
                "result" : "success"
            };
            if((!tool_data.name) || tool_data.name === '' || tool_data.name === null || tool_data.name === undefined)
            {
                response.message = "Please enter tool name";
                response.result = "failed";
            }
            else if((!tool_data.support_details) || tool_data.support_details === '' || tool_data.support_details === null || tool_data.support_details === undefined)
            {
                response.message = "Please enter email address";
                response.result = "failed";
            }
            else if(tool_data.support_details)
            {
                var support = tool_data.support_details;
                var atpos = support.indexOf("@");
                var dotpos = support.lastIndexOf(".");
                if (atpos<1 || dotpos<atpos+2 || dotpos+2>=support.length) {
                    response.message = "Please enter valid email address!";
                    response.result = "failed";
                }
            }
            else
            {
                response.message = "Tool general details validation was successful";
            }
            return response;
        },

        validateVersionData : function(version_data)
        {
            var versionData = version_data;
            var version_length = versionData.length;
            var response = {
                version_errors : {
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
                },
                display_tab : 0,
                result : "success"
            };

            for(var j=0; j<version_length; j++)
            {
                if(versionData[j].version_name === "" || versionData[j].version_name === null || versionData[j].version_name === undefined)
                {
                    response.display_tab = j;
                    response.version_errors.version_name = 'Please enter version name!';
                    response.result = "failed";
                }

                if(versionData[j].version_number === "" || versionData[j].version_number === null || versionData[j].version_number === undefined)
                {
                    response.display_tab = j;
                    response.version_errors.version_number = 'Please enter version number!';
                    response.result = "failed";
                }

                if(versionData[j].backward_compatible === "" || versionData[j].backward_compatible === null || versionData[j].backward_compatible === undefined)
                {
                    response.display_tab = j;
                    response.version_errors.backward_compatible = 'Please select backward compatibility!';
                    response.result = "failed";
                }

                if(versionData[j].branch_tag === "" || versionData[j].branch_tag === null || versionData[j].branch_tag === undefined)
                {
                    response.display_tab = j;
                    response.version_errors.branch_tag = 'Please select branch or tag!';
                    response.result = "failed";
                }

                if(versionData[j].gitlab_repo!=='' && versionData[j].gitlab_branch === "" || versionData[j].gitlab_repo!=='' && versionData[j].gitlab_branch === null || versionData[j].gitlab_repo!=='' && versionData[j].gitlab_branch === undefined)
                {
                    response.display_tab = j;
                    response.version_errors.gitlab_branch = 'Please enter branch name!';
                    response.result = "failed";
                }

                if(versionData[j].gitlab_repo!=='' && versionData[j].jenkins_job === "" || versionData[j].gitlab_repo!=='' && versionData[j].jenkins_job === null || versionData[j].gitlab_repo!=='' && versionData[j].jenkins_job === undefined)
                {
                    response.display_tab = j;
                    response.version_errors.jenkins_job = 'Please enter jenkins job name!';
                    response.result = "failed";
                }

                if(versionData[j].gitlab_branch!=='' && versionData[j].gitlab_repo === "" || versionData[j].gitlab_branch!=='' && versionData[j].gitlab_repo === null || versionData[j].gitlab_branch!=='' && versionData[j].gitlab_repo === undefined)
                {
                    response.display_tab = j;
                    response.version_errors.gitlab_repo = 'Please enter gitlab repository url!';
                    response.result = "failed";
                }

                if(versionData[j].document)
                {
                    for(var k=0; k<versionData[j].document.documents.length; k++)
                    {
                        var url = versionData[j].document.documents[k].url;
                        if(versionData[j].document.documents[k].name === "" || versionData[j].document.documents[k].name === undefined || versionData[j].document.documents[k].name === null)
                        {
                            response.display_tab = j;
                            response.fieldIndex = k;
                            $('#add_document').show(700);
                            response.version_errors.document_errors.name = 'Please enter document name!';
                            response.result = "failed";
                        }
                        if(versionData[j].document.documents[k].url === "" || versionData[j].document.documents[k].url === undefined || versionData[j].document.documents[k].url === null)
                        {
                            response.display_tab = j;
                            response.fieldIndex = k;
                            $('#add_document').show(700);
                            response.version_errors.document_errors.url = 'Please enter document url!';
                            response.result = "failed";
                        }
                        if(versionData[j].document.documents[k].url !== "" && versionData[j].document.documents[k].name === "")
                        {
                            response.display_tab = j;
                            response.fieldIndex = k;
                            $('#add_document').show(700);
                            response.version_errors.document_errors.name = 'Please enter document name!';
                            response.result = "failed";
                        }
                        else if(versionData[j].document.documents[k].name !== "" && versionData[j].document.documents[k].url === "")
                        {
                            response.display_tab = j;
                            response.fieldIndex = k;
                            $('#add_document').show(700);
                            response.version_errors.document_errors.url = 'Please enter document url!';
                            response.result = "failed";
                        }
                        else if(versionData[j].document.documents[k].name !== "" && versionData[j].document.documents[k].type === "")
                        {
                            response.display_tab = j;
                            response.fieldIndex = k;
                            $('#add_document').show(700);
                            response.version_errors.document_errors.type = 'Please enter document type!';
                            response.result = "failed";
                        }
                        else if(((!url.includes("http://")) && (!url.includes("https://"))) || (url.lastIndexOf(".") < 0))
                        {
                            $('#add_document').show(700);
                            response.version_errors.document_errors.url = 'Please enter a valid document url!';
                            response.result = "failed";
                        }
                    }
                }

                if(versionData[j].deployment_field)
                {
                    if(versionData[j].deployment_field.fields.length>0)
                    {
                        for(var n=0; n<versionData[j].deployment_field.fields.length;n++)
                        {
                            if(versionData[j].deployment_field.fields[n].input_name === "" || versionData[j].deployment_field.fields[n].input_name === null || versionData[j].deployment_field.fields[n].input_name === undefined)
                            {
                                response.display_tab = j;
                                response.fieldIndex = n;
                                response.version_errors.deployment_field_errors.input_name = 'Please enter input name!';
                                response.result = "failed";
                                $('#add_settings').show(700);
                            }
                            if(versionData[j].deployment_field.fields[n].input_type === "" || versionData[j].deployment_field.fields[n].input_type === null || versionData[j].deployment_field.fields[n].input_type === undefined)
                            {
                                response.display_tab = j;
                                response.fieldIndex = n;
                                response.version_errors.deployment_field_errors.input_type = 'Please select input type!';
                                response.result = "failed";
                                $('#add_settings').show(700);
                            }
                            if(versionData[j].deployment_field.fields[n].input_type === 'radio' || versionData[j].deployment_field.fields[n].input_type === 'dropdown' || versionData[j].deployment_field.fields[n].input_type === 'checkbox')
                            {
                                delete versionData[j].deployment_field.fields[n].selected_values;
                                if(versionData[j].deployment_field.fields[n].valid_values.length===0)
                                {
                                    response.display_tab = (versionData.length -1)- j;
                                    response.fieldIndex = n;
                                    response.version_errors.deployment_field_errors.valid_values = 'Please enter at least one valid value!';
                                    response.result = "failed";
                                    $('#add_settings').show(700);
                                }
                            }
                            if(versionData[j].deployment_field.fields[n].input_type === 'checkbox')
                            {
                                if(!versionData[j].deployment_field.fields[n].default_value)
                                {
                                    versionData[j].deployment_field.fields[n].default_value = [];
                                }
                            }
                            if(!versionData[j].deployment_field.fields[n].is_mandatory)
                            {
                                versionData[j].deployment_field.fields[n].is_mandatory = false;
                            }
                            delete versionData[j].deployment_field.fields[n].is_existing;
                        }

                    }
                    else
                    {
                        versionData[j].deployment_field = {
                            fields : []
                        };
                    }
                }

                for(var o=0; o<version_length; o++)
                {
                    if((j!==o)&& parseFloat(versionData[j].version_number, 10) === parseFloat(versionData[o].version_number, 10))
                    {
                        response.display_tab = 0;
                        response.version_errors.version_number = 'Version number can not be duplicate!';
                        response.result = "failed";
                    }
                }
            }
            return response;
        }
    };
}).factory('BuildMarkup', function ($resource) { // For Build markup
    return $resource('/tool/update/buildmarkup', {
    },
    {
        update :{
            method : 'POST'
        }
    });
});

toolServicesApp.directive('fileModel', ['$parse', '$rootScope', function ($parse, $rootScope) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;
            element.bind('change', function (evt) {
                scope.$apply(function () {
                    var srcId = null;
                    var files = evt.target.files;
                    if(files[0].type==='image/jpeg' || files[0].type==='image/png' || files[0].type==='image/jpg' || files[0].type==='image/bmp' || files[0].type==='image/gif')
                    {
                        modelSetter(scope, element[0].files[0]);
                        scope.logoFileSelected = files[0].name;
                        return true;
                    }
                    else
                    {
                        model = $parse(attrs.fileModel);
                        modelSetter = model.assign;
                        delete scope.logoFileSelected;
                        delete scope.logoFile;
                        scope.$root.handleResponse('Please select image file for logo!');
                        return false;
                    }
                });
            });
        }
    };
}]);

toolServicesApp.directive('screenshotModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.screenshotsModel);
            var modelSetter = model.assign;
            if(scope.$root.screenshotFiles)
            {
                scope.$root.screenshotFiles = scope.$root.screenshotFiles;
            }
            else
            {
                scope.$root.screenshotFiles = [];
            }
            element.bind('change', function (evt) {
                scope.$apply(function () {
                var files = evt.target.files;

                    if(element[0])
                    {
                        if(files[0].type==='image/jpeg' || files[0].type==='image/png' || files[0].type==='image/jpg' || files[0].type==='image/bmp' || files[0].type==='image/gif')
                        {
                            var index = scope.$root.screenshotFiles.length;
                            scope.$root.screenshotFiles[index] = files;
                            scope.$root.screenshotFiles[index].version_id = element[0].accessKey;
                            scope.$root.screenshotFiles[index].screenshotFileSelected = files[0].name+', '+scope.$root.screenshotFiles[index].screenshotFileSelected;
                            modelSetter(scope, element[0].files[0]);
                            var srcId = document.getElementById('media_file'+scope.screenshotFiles.length);
                            srcId.src = URL.createObjectURL(element[0].files[0]);
                            if(scope.$root.screenshotFiles)
                            {
                                var lastIndexOfComma =  scope.$root.screenshotFiles[index].screenshotFileSelected.lastIndexOf(',');
                                scope.$root.screenshotFiles[index].screenshotFileSelected = scope.$root.screenshotFiles[index].screenshotFileSelected.slice(0,lastIndexOfComma);
                            }
                        }
                        else
                        {
                            model = $parse(attrs.fileModel);
                            modelSetter = model.assign;
                            delete scope.editscreenshots;
                            scope.$root.handleResponse('Please select image file for screenshot!');
                            return false;
                        }
                    }

                });
            });
        }
    };
}]);

toolServicesApp.directive('screenshotsModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.screenshotsModel);
            var modelSetter = model.assign;
            if(scope.$root.screenshotFiles)
            {
                scope.$root.screenshotFiles = scope.$root.screenshotFiles;
            }
            else
            {
                scope.$root.screenshotFiles = [];
            }
            element.bind('change', function (evt) {
                scope.$apply(function () {
                var files = evt.target.files;

                    if(element[0])
                    {
                        if(files[0].type==='image/jpeg' || files[0].type==='image/png' || files[0].type==='image/jpg' || files[0].type==='image/bmp' || files[0].type==='image/gif')
                        {
                            var index = scope.$root.screenshotFiles.length;
                            scope.$root.screenshotFiles[index] = files;
                            scope.$root.screenshotFiles[index].version_id = element[0].accessKey;
                            scope.$root.screenshotFiles[index].screenshotFileSelected = files[0].name+', '+scope.$root.screenshotFiles[index].screenshotFileSelected;
                            modelSetter(scope, element[0].files[0]);
                            if(scope.$root.screenshotFiles)
                            {
                                var lastIndexOfComma =  scope.$root.screenshotFiles[index].screenshotFileSelected.lastIndexOf(',');
                                scope.$root.screenshotFiles[index].screenshotFileSelected = scope.$root.screenshotFiles[index].screenshotFileSelected.slice(0,lastIndexOfComma);
                            }
                        }
                        else
                        {
                            model = $parse(attrs.fileModel);
                            modelSetter = model.assign;
                            delete scope.editscreenshots;
                            scope.$root.handleResponse('Please select image file for screenshot!');
                            return false;
                        }
                    }

                });
            });
        }
    };
}]);

toolServicesApp.service('toolFileUpload', ['$http', function ($http) {
    this.uploadFileToUrl = function (file, uploadUrl) {
        var fd = new FormData();
        fd.append('logo', file);
        fd.append('tool_id',file.tool_id);
               $http.post(uploadUrl, fd, {
                  transformRequest: angular.identity,
                  headers: {'Content-Type': undefined}
               })

               .success(function(){
               })

               .error(function(){
               });
    };
    this.uploadToolSetLogoFileToUrl = function (file, uploadUrl) {
        var fd = new FormData();
        fd.append('logo', file);
        fd.append('toolset_id',file.toolset_id);
            $http.post(uploadUrl, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
            .success(function(){
            })
            .error(function(){
            });
    };
    this.uploadScreenShotToUrl = function (screenshot, uploadUrl) {
        var fd = new FormData();

        for(var i=0;i<screenshot.length;i++)
        {
            fd.append('screenshot_'+[i], screenshot[i]);
            fd.append('version_id',screenshot.version_id);
        }
            $http.post(uploadUrl, fd, {
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            })
            .success(function(){
            })
            .error(function(){
            });
    };
}]);

});

