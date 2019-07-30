require.config({
    baseUrl: "",
    waitSeconds: 0,
    deps : ['manageSyncServicesComponent', 'syncDetailsTabsComponent']
});

define(['angular', 'ngResource', 'uiRouter', 'ngCookies', 'manageSyncServicesComponent', 'syncDetailsTabsComponent'],function (app) {
  'use strict';

var settingsViewControllerApp = angular.module('settingsViewControllerApp', ['ui.router', 'settingsServicesApp', 'manageSyncServicesComponent', 'syncDetailsTabsComponent', 'machineServicesApp']);

settingsViewControllerApp.controller('SettingsViewController', function ($state, $scope, $rootScope, $http, $timeout, Settings, ConfigEdit, $location) {
    Settings.get({
        id : 'all'
    },
    function(successResponse)
    {
        $scope.configData = successResponse;      
    },
    function ( errorResponse)
    {
        $rootScope.handleResponse(errorResponse);
    });
    $scope.showConfirmationPopUp = false;
    $scope.currentTab = 'SettingsTab';
    $scope.showCurrentTab = function(tab)
    {
        $scope.currentTab = tab;
        if($scope.currentTab !='SettingsTab')
        {
           $scope.userSelected=false;
           $scope.isSelectedFlag=false;
        }
    };

    $scope.getCurrentTab = function(tab)
    {
        if($scope.currentTab === tab)
        {
            return 'vp-tabs__tab vp-tabs__tab--active pointer pr--sm pl--sm left';
        }
        else
        {
            return 'vp-tabs__tab pointer pr--sm pl--sm left';
        }
    };

    $scope.getSettingsClass = function(category)
    {
        if(category.enable==='true')
        {
            return "vp-search__item--enabled";
        }
        else if(category.enable==='false')
        {
            return "vp-search__item--disabled";
        }
    };

    $scope.discardSettingsData=function()
    {
         delete $scope.settings_fields;
    };

    $scope.getConfigDetails = function(config_id)
    {
        $scope.userSelected=true;
        $scope.isSelectedFlag=true;
        $scope.editEnableFlag=true;
        Settings.get({
            id : 'view/'+config_id
        },
        function(successResponse)
        {
            for(var i=0; i<successResponse.data.field_types.length; i++)
            {
                if(successResponse.data.field_types[i].name)
                {
                    var value = successResponse.data[successResponse.data.field_types[i].name];      
                    if(successResponse.data.field_types[i].type === 'number')
                    {
                        successResponse.data.field_types[i].value = parseFloat(value, 10);
                    }
                    else if(successResponse.data.field_types[i].type === 'date')
                    {
                        var date =new Date(value);
                        successResponse.data.field_types[i].value = date;
                    }
                    else
                    {
                        successResponse.data.field_types[i].value = value;
                    }
                }
            }
            $scope.settings_fields = successResponse.data;
        },
        function ( errorResponse)
        {
            $rootScope.handleResponse(errorResponse);
        });
    };

    $scope.getSettingsUlClass = function()
    {
        if($scope.userSelected === true)
        {
            if($scope.currentTab!='SettingsTab')
            {
                $scope.userSelected = false;
            }
            return "vp-settingform__selectedsettingform__fieldslist text--cs03 pr--lg";
        }
        else
       {
            return "vp-settingform__selectedsettingform__fieldslist text--cs03 pr--lg hidden";
       }
    };

    $scope.getSettingFormClass = function()
    {
        if($scope.userSelected === true)
        {
            if($scope.currentTab!='SettingsTab')
            {
                $scope.userSelected = false;
            }
            return "vp-settingform__selectedsettingform--active  vp-settingform vp-control max";
        }
        else
        {
            return "vp-selectedsettingform vp-settingform vp-control max";
        }
    };

    $scope.isReadOnly = false;
    $scope.editConfig = function()
    {
        $scope.isReadOnly = false;
    };
    $scope.resetReadOnly = function()
    {
        $scope.isReadOnly = true;
    };
    $scope.atDefLoaded = function(atDef)
    {
        $('#show_confirmation_popup').hide(700);
        if(atDef)
        {
            $scope.updateConfig(atDef,false);
        }
    };

    $scope.updateConfig = function(id,validate_ind)
    {
        var _id = "_"+id;
        var jsonData = {};
        jsonData._id = {
            oid : id
        };
        if(validate_ind === true && $scope.settings_fields.run_status === "Running")
        {
            $scope.showConfirmationPopUp = true;
            $('#show_confirmation_popup').show(700);
            $scope.atNameValueMap = jsonData._id.oid = id;
            $scope.attentionMessage = "The Service is currently running. Saving might cause the service to abort/fail. Do you want to continue ? ";
            return;
        }
        $.each($scope.settings_fields.field_types, function() {
            var name = this.name;
            var value = this.value;
            jsonData[name] = value;
        });
        jsonData._id.oid = id;

        $scope.configUpdateStatus = "Configuration Updated";
        $scope.configUpdateStatus = ConfigEdit.update(jsonData, function(configUpdateSuccessResponse){
            delete $scope.settings_fields;
            $rootScope.handleResponse(configUpdateSuccessResponse);
            Settings.get({
                id : 'all'
            },
            function (successResponse)
            {    
                $scope.configData = successResponse;      
            },
            function (errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
            $rootScope.handleResponse(configUpdateSuccessResponse);
        },
        function(configUpdateErrorResponse) {
            $rootScope.handleResponse(configUpdateErrorResponse);
        });
    };

});
});