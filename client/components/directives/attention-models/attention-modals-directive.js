define(['angular', 'ngResource'], function (app) {
  'use strict';
var attentionModelDirectiveApp = angular.module('attentionModelDirectiveApp', []);

attentionModelDirectiveApp.directive('attentionalModel', function () {
    return {
        restrict: 'E',
        templateUrl :'static/components/directives/attention-models/attention-modals-directive.html',
        scope:{
            message :'=',
            atNameValueMap: '=',
            onAtLoad :'&'
        },
        controller: function($scope){
            $scope.confirmToSubmit = function(id)
            {
               $scope.onAtLoad({atDef:id});
            }
        }
    };
});
});