define(['angular'], function (app) {
  'use strict';

  app = angular.module("disableSectionDirective", []);
  app.directive("disableSection", function() {
    return {
      restrict : "A",
      link:function(scope, element, attr){
        var isDisabled = scope[attr.disableSection];
        if (isDisabled && isDisabled === "true"){
          element.css({
            'pointer-events': "none",
            opacity: "0.5"
          });
        }
      }
    };
  });
});