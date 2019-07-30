define(['angular', 'ngResource','deploymentPluginServicesApp'], function (app) {
  'use strict';

var deploymentPluginDirectiveApp = angular.module('deploymentPluginDirectiveApp', ['deploymentPluginServicesApp']);

deploymentPluginDirectiveApp.directive('pluginFileModel', ['$parse', '$rootScope',  function ($parse, $rootScope) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var _validFileExtensions = [".py"];
            var blnValid = false;
            var model = $parse(attrs.pluginFileModel);
            var modelSetter = model.assign;
            element.bind('change', function (evt) {
                scope.$apply(function () {
                    var files = evt.target.files;
                    var file = files[0];
                    if (file.type == "text/plain")
                    {
                        var sFileName = file.name;
                        if (sFileName.length > 0) {
                            for (var j = 0; j < _validFileExtensions.length; j++) {
                                var sCurExtension = _validFileExtensions[j];
                                if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                                    blnValid = true;
                                    break;
                                }
                            }

                            if (!blnValid) {
                                return false;
                            }
                        }
                    }
                    if(blnValid)
                    {
                        scope.pluginFileSelected = files[0].name;
                        modelSetter(scope, element[0].files[0]);
                    }
                    else
                    {
                        $rootScope.handleResponse('Invalid file format... Please select .py file');
                        return false;
                    }
                });
            });
        }
    };
}]);

});