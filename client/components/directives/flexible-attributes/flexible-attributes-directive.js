define(['angular', 'ngResource', 'flexAttributeServicesApp', 'dropDownMultiSelect', 'disableSectionDirective'], function (app) {
  'use strict';
var flexAttributeDirectiveApp = angular.module('flexAttributeDirectiveApp', ['flexAttributeServicesApp', 'angularjs-dropdown-multiselect', 'disableSectionDirective']);

flexAttributeDirectiveApp.directive('flexibleAttributes', function () {
    return {
        restrict: 'E',
        templateUrl :'static/components/directives/flexible-attributes/flexible-attributes-directive.html',
        scope:{
            entity: '@',
            onFaLoad: '&',
            disabled: '@',
            faNameValueMap: '='
        },
        controller: function($scope, $rootScope, flexAttributeByEntity){
            validate($scope);
            init($scope);

            flexAttributeByEntity.get({
                entity:$scope.entity
            },
            function(successResponse)
            {
                $scope.flexAttrs = successResponse.data;
                setupFas($scope);
                $scope.onFaLoad({faDef: $scope.flexAttrs});
            },
            function(errorResponse)
            {
                $rootScope.handleResponse(errorResponse);
            });
        }
    };
});
});

function setupFas($scope){
    var flexAttrArr = $scope.flexAttrs;
    var faNameValueMap = $scope.faNameValueMap;
    for (var i = 0; i < flexAttrArr.length; i++){
        var fa = flexAttrArr[i];
        setFaInitialValue(fa);
        
        if (faNameValueMap[fa.name]){
            fa['value'] = faNameValueMap[fa.name];
            setFaSelectedOptions(fa);
        } else{
            faNameValueMap[fa.name] = fa['value'];
        }
    }

    $scope.$watch("flexAttrs", function (newValue, oldValue, $scope) {
        if (newValue){
            for (var i = 0; i < newValue.length; i++){
                var fa = newValue[i];
                if (fa.selectedOptions){
                    fa.value = fa.selectedOptions.join();
                }
                
                $scope.faNameValueMap[fa.name] = fa.value;
            }
        }
    }, true);

    $scope.$watch("faNameValueMap", function (newValue, oldValue, $scope) {
        if (newValue){
            var flexAttrArr = $scope.flexAttrs;
            for (var k in newValue){
                for (var i = 0; i < flexAttrArr.length; i++){
                    var fa = flexAttrArr[i];
                    if (fa.name === k){
                        fa.value = newValue[k];
                        setFaSelectedOptions(fa);
                        break;
                    }
                }
            }
            
        }
    }, true);
}

function setFaInitialValue(fa){
    fa['value'] = fa['default_value'];
    setFaSelectedOptions(fa);
}

function setFaSelectedOptions(fa){
    if (isSelectType(fa.type)){
        if (fa.value){
            fa.selectedOptions = fa.value.split(',');
        } else {
            fa.selectedOptions = [];
        }
    }
}

function isSelectType(faType){
    return faType === 'MultiSelect' || faType === 'Select';
}

function validate($scope){
    if (! $scope.faNameValueMap){
        console.error('fa-name-value-map is not defined for directive flexible-attributes');
    }
}

function init($scope){
    setupMultiSelectDropdown($scope);

    if ($scope.disabled == null){
        $scope.disabled = false;
    }
}

function setupMultiSelectDropdown($scope){
    $scope.multiSelectSettings = { enableSearch: true, 
        showSelectAll: true, 
        keyboardControls: true, 
        smartButtonMaxItems: 3,
        template: '{{option}}',
        smartButtonTextConverter: function(skip, option) { return option; }
    };

    $scope.singleSelectSettings = { enableSearch: true, 
        keyboardControls: true, 
        selectionLimit: 1,
        showUncheckAll: false,
        smartButtonMaxItems: 1,
        selectedToTop: true,
        template: '{{option}}',
        smartButtonTextConverter: function(skip, option) { return option; }
    };
}
