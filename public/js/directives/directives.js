'use strict';

/* Directives */
var Directives = angular.module('advdb.directives', []);

Directives.directive("advdb", [function () {
    return {
        restrict: 'E',
        templateUrl: 'public/partials/directive.html',
        link: function (scope, element, attributes) {

        },
        controller: ['$scope',function($scope){

        }]
    }
}]);