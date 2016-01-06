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
        link: function (scope, element, attributes) {

        },
        controller: ['$scope','Login',function($scope,Login){
            Login.registerScope($scope);

        	$scope.data = {
        		user: Login.user,
                Login: Login
        	};
            console.log( Login.user.profilePic , '???');
        	$scope.$watch('data.user.profilePic',function(){
                console.log(arguments);
            });
        }]
    }
}]);