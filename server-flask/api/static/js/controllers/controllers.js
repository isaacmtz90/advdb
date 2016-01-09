'use strict';

/* Controllers */
var Controllers = angular.module('advdb.controllers', []);

Controllers.controller('loginCtrl', ['$scope','$http','Login',function($scope,$http,Login) {
	$scope.facebook_loaded = false;
	Login.loaded = function(){
		FB.getLoginStatus(function(response) {
			if (response.status === 'connected') {
				window.fb_login();
			} else {
				$scope.facebook_loaded = true;
				$scope.$digest();
			}
		});
	};
}]);

Controllers.controller('homeCtrl', ['$scope','$http','Data','Login',function($scope,$http,Data,Login) {
	if( !Login.user.profile ){
		Data.sendUser(Login.user).success(function( response ){
			if( response.data.name ){
				Login.user.profile = response.data;
			}else{
				window.location = '#/profile';
			}
		}).error(function(){
			window.location = '#/profile';
		});
	}
	$scope.matchNow = function(){
		window.location = '#/matches';
	};
}]);

Controllers.controller('profileCtrl', ['$scope','$http','Data','Login',function($scope,$http,Data,Login) {
	$scope.profile = {
		loading: true,
		profile: null,
		validate: false,
		showError: false,
		disabled: false
	};

	if( !Login.user.profile ){
		$scope.profile.profile = {
			person_id: Login.user.id,
			name: Login.user.name,
			email: Login.user.email,
			age: 0,
			interested_in: "",
			gender: Login.user.gender,
			height: 0,
			country: "",
			likes: {
				movies_liked: [],
				tvshows_liked: []
			}
		};
	}else{
		$scope.profile.profile = JSON.parse(JSON.stringify(Login.user.profile));
	}

	$scope.save = function(){
		$scope.profile.validate = true;

		if( !$scope.profile.profile.gender ){
			$scope.profile.showError = true;
			return;
		}
		if( !$scope.profile.profile.interested_in ){
			$scope.profile.showError = true;
			return;
		}
		if( !$scope.profile.profile.height ){
			$scope.profile.showError = true;
			return;
		}
		if( !$scope.profile.profile.age ){
			$scope.profile.showError = true;
			return;
		}
		/*if( !$scope.profile.profile.country ){
			$scope.profile.showError = true;
			return;
		}*/

		$scope.profile.disabled = true;		
		Data.saveUser( Login.user.id , $scope.profile.profile ).success(function( response ){
			Login.user.profile = response.user;
			window.location = '#/home';
		});
	};	

	$scope.likeInterest = function( type , id ){
		var interest = $scope.profile.likes[type][id];
		var interestId = interest.tvshow_id || interest.movie_id;

		Data.interest( Login.user.id , type , interestId, false ).success(function( response ){
			if( response.data.success ){
				if( !$scope.profile.profile.likes[type] )
					$scope.profile.profile.likes[type] = [];

				$scope.profile.profile.likes[type].push(interestId);
				$scope.$digest();
			}
		});
	};

	$scope.dislikeInterest = function( type , id ){
		var interest = $scope.profile.likes[type][id];
		Data.interest( Login.user.id , type , interest , true ).success(function( response ){
			if( response.data.success ){
				$scope.profile.profile.likes[type] = $scope.profile.profile.likes[type].filter(function(a){
					return a != interest;
				});
				$scope.$digest();
			}
		});
	};

	Data.getMovies().success(function( response ){
		$scope.profile.likes = {
			"genders": ["male","female","other"], 
			"interested_in": ["male","female","other","all"], 
			"movies_liked": response.data.movies,
			"tvshows_liked": null,
			"countries": ["Honduras","United States","Guatemala","Nicaragua","El Salvador"]
		};
		Data.getTVShows().success(function( response ){
			$scope.profile.likes.tvshows_liked = response.data.tv_shows;

			setTimeout(function(){
				$('select').material_select();
				$('ul.tabs').tabs();
			});
		});
	});
}]);

Controllers.controller('matchesCtrl', ['$scope','$http','Data','Login',function($scope,$http,Data,Login) {
	if( !Login.user.profile ){
		window.location = '#/home';
	}

	$scope.suggestions = {
		suggestions: null
	};

	$scope.like = function(){
		$scope.suggestions.disabled = true;
		Data.like( Login.user.id , $scope.suggestions.prospect.id , false ).success(function(){
			$scope.suggestions.prospect = $scope.suggestions.suggestions.pop();
			$scope.suggestions.disabled = false;
			$scope.$digest();
			if( !$scope.suggestions.prospect ){
				//get more suggestions
			}
		});
	};

	$scope.dislike = function(){
		$scope.suggestions.disabled = true;
		Data.like( Login.user.id , $scope.suggestions.prospect.id , true ).success(function(){
			$scope.suggestions.suggestions = $scope.suggestions.suggestions.filter(function(a){
				return a != $scope.suggestions.prospect.id;
			});
			$scope.suggestions.disabled = false;
			$scope.suggestions.prospect = $scope.suggestions.suggestions.pop();
			$scope.$digest();
			if( !$scope.suggestions.prospect ){
				//get more suggestions
			}
		});
	};

	$scope.profile = function( element ){
		window.open( 'http://www.facebook.com/' + element.item.id );
	};

	Data.getMatches( Login.user.id , {} ).success(function( response ){
		$scope.suggestions.suggestions = response.suggestions;
		$scope.suggestions.matches = response.matches;
		$scope.suggestions.prospect = $scope.suggestions.suggestions.pop();
		$scope.$digest();
	});
}]);