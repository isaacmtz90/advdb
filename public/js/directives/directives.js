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
            console.log( attributes );
            if( attributes.hasOwnProperty('nouser')){
                scope.noLogin = true;
            }
            window._X = scope;
        },
        controller: ['$scope','Login',function($scope,Login){
            if( !$scope.noLogin ){
                Login.registerScope($scope);

            	$scope.data = {
            		user: Login.user,
                    Login: Login
            	};
                
            	$scope.$watch('data.user.profilePic',function(){
                    console.log(arguments);
                });
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