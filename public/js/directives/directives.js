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

Directives.directive("header", [function () {
    return {
        restrict: 'E',
        templateUrl: 'public/partials/header.html',
        scope: {},
        link: function (scope, element, attributes) {
            if( attributes.hasOwnProperty('nouser')){
                scope.noLogin = true;
            }
        },
        controller: ['$scope','Login',function($scope,Login){
            if( !$scope.noLogin ){
                Login.registerScope($scope);

            	$scope.data = {
            		user: Login.user,
                    Login: Login
            	};
            }
        }]
    }
}]);

Directives.directive("matchFooter", [function () {
    return {
        restrict: 'E',
        templateUrl: 'public/partials/footer.html',
        scope: {},
        link: function (scope, element, attributes) {
    
        },
        controller: ['$scope',function($scope){
   
        }]
    }
}]);