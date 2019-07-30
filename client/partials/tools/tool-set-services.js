define(['angular', 'ngResource'],function (app) {
  'use strict';

var toolSetServicesApp = angular.module('toolSetServicesApp', []);
toolSetServicesApp.factory('ToolSetAdd', function ($resource) {
    return $resource('/toolset/add', {
    }, {

    });
}).factory('ToolSetEdit', function ($resource) {
    return $resource('/toolset/update', {
    },
    {
        update : {
            method : 'PUT'
        }
    });
}).factory('AllToolSet', function ($resource) {
   return $resource('/toolset/all', {
   },
   {
        get : {
            method: 'GET',
            isArray: false,
            transformResponse : function(fulldata, headers) {
                var jsonData = JSON.parse(fulldata);
                return jsonData;
            }
        }
    });
}).factory('ToolSetByID', function ($resource) {
    return $resource('/toolset/view/:id', {
        id: '@_id'
    },
    {
    });
}).factory('ToolSetDelete', function($resource, $http,$rootScope){
    return $resource('/toolset/delete/:id',{
        id:'@_id'
    },
    {
        remove : {
                method : 'DELETE'
        }
    });
}).factory('ToolSetDetailsFactory', function()  {
    var toolSetData = {};
    var logoFile = null;
    var toolList = [];

    return {
        getToolSetData : function()
        {
            return toolSetData;
        },

        setToolSetData : function(tool_set_data)
        {
            toolSetData.name = tool_set_data.name;
            toolSetData.description = tool_set_data.description;
            toolSetData.status = tool_set_data.status;
            toolSetData.support_details = tool_set_data.support_details;
            toolSetData.logo = tool_set_data.logo;
            toolSetData.thumbnail_logo = tool_set_data.thumbnail_logo;
            toolSetData.tag = tool_set_data.tag;
            if(tool_set_data._id)
            {
                toolSetData.toolset_id = tool_set_data._id.$oid;
            }
        },

        getToolList : function()
        {
            return toolList;
        },

        setToolList : function(tool_list)
        {
            toolList = tool_list;
        },

        getToolSetLogo : function()
        {
            return logoFile;
        },

        setToolSetLogo : function(logo)
        {
            logoFile = logo;
        },

        removeTool : function(selectedTool,index)
        {
            toolList = selectedTool;
            toolList.splice(index, 1);
        },

        removeAllTools : function()
        {
            toolList = [];
        },

        cleanToolSetDataObject : function()
        {
            toolSetData = {};
            logoFile = null;
        }
    };
}).factory('ToolSetDataValidatorFactory', function($rootScope)  {
    var response = {
        "message" : "",
        "result" : "success"
    };
    return {
        validateToolSetData : function(tool_set_data)
        {
            if((!tool_set_data.name) || tool_set_data.name === '' || tool_set_data.name === null || tool_set_data.name === undefined)
            {
                response.message = "Please enter tool set name";
                response.result = "failed";
            }
            else
            {
                response.message = "Tool general details validation was successful";
            }
            return response;
        },

        validateToolListData : function(tool_list)
        {
            if(tool_list.length < 2)
            {
                response.message = "Please select atleast two tools for tool set";
                response.result = "failed";
            }
            return response;
        }
    };
});

});

