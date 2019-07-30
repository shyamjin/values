define(['angular', 'ngResource'],function (app) {
  'use strict';

    var proposedToolServicesApp = angular.module('proposedToolServicesApp', []);

    proposedToolServicesApp.factory('ProposeTool', function ($resource) {
        return $resource('/proposed/tool/new', {
        },
        {
        });
    }).factory('GetAllProposedTools', function ($resource) {
        return $resource('/proposed/tool/view/all', {
        },
        {
        });
    }).factory('GetProposedTool', function ($resource) {
        return $resource('/proposed/tool/view/:id', {
            id: '@_id'
        },
        {
        });
    }).factory('ApproveProposedTool', function ($resource) {
        return $resource('/proposed/tool/approve', {
        },
        {
        });
    }).factory('RejectProposedTool', function ($resource) {
        return $resource('/proposed/tool/delete/:id', {
            id: '@_id'
        },
        {
        });
    }).factory('ToolDetailsFactory', function()  {
        var proposedToolData = {
            version : {
                version_name : '',
                version_number : ''
            }
        };
        return {
            setProposedToolData : function(tool_data)
            {
                if(tool_data._id)
                {
                    proposedToolData.tool_id = tool_data._id;
                }
                proposedToolData.name = tool_data.name;
                proposedToolData.description = tool_data.description;
                proposedToolData.support_details = tool_data.support_details;
                proposedToolData.request_reason = tool_data.request_reason;
                if(tool_data.thumbnail_logo)
                {
                    proposedToolData.thumbnail_logo = tool_data.thumbnail_logo;
                }
                proposedToolData.version.version_number = tool_data.version.version_number;
                proposedToolData.version.version_name = tool_data.version.version_name;
            },

            getProposedToolData : function()
            {
                return proposedToolData;
            },

            cleanProposedToolDataObject : function()
            {
                proposedToolData = {};
            }
        };
    });
});