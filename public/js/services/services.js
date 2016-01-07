'use strict';

window.getService = function(service){
	return angular.element('body').injector().get( service );
};


/* Services */
var Services = angular.module('advdb.services', []);

Services.service('Login',function(){
	var result = {
		user: undefined,
		scopes: [],
		registerScope: function( scope ){
			this.scopes.push(scope);
		}
	};

	function statusChangeCallback(response) {
		if (response.status === 'connected') {
			FB.api('/me', function(response) {
				result.user = response;
				FB.api("/" + result.user.id + "/picture",
				    function (response) {
				    	if (response && !response.error) {
				    		result.user.profilePic = response.data.url;
				    		for( var i = 0 ; i < result.scopes.length ; i++ )
				    			result.scopes[i].$digest();
				    	} 
				    }
				);
				if( result.success )
					result.success();
			});
		} else if (response.status === 'not_authorized') {
			if( result.fail )
				result.fail();
		} else {
			if( result.fail )
				result.fail();
		}
	}

	window.checkLoginState = function() {
		FB.getLoginStatus(function(response) {
			statusChangeCallback(response);
		});
	}

	window.fbAsyncInit = function() {
		FB.init({
			appId: '164561877237144',
			xfbml: true,
			version: 'v2.5'
		});

		FB.getLoginStatus(function(response){
	    	result.loaded();
	    });
	};

	window.fb_login = function(){
	    FB.login(function(response) {
	    	window.checkLoginState();
	    }, {
	        scope: 'public_profile,email,user_friends'
	    });
	};

	(function(d, s, id){
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id)) {return;}
		js = d.createElement(s); js.id = id;
		js.src = "//connect.facebook.net/en_US/sdk.js";
		fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk'));

	return result;
});

Services.service('Data',function(){
	function new_Endpoint(){
		return {
			callback: function(){},
			callbackError: function(){},
			success: function( callback ){
				this.callback = callback;
				return this;
			},
			error: function( callback ){
				this.callback = callback;
				return this;
			},
			_fakeResponse: function( data ){
				var _self = this;
				setTimeout(function(){
					_self.callback( data );
				},1000);
			}
		};
	};

	var _fakeUSer = {
		"id": "10153733372723548",
		"name": "Carlos Sanchez",
		"interestedIn": "female",
		"physicalAppearance": {
			"gender": "male",
			"height": 172,
			"weight": 80,
			"country": "Honduras"
		},
		"likes": {
			"movies": ["Dawn of The Dead","Star Wars"],
			"music": ["Red Hot Chilli Peppers","Disturbed"],
			"tvSeries": []
		}
	};


	var Data = {
		//first endpoint to get the user data
		sendUser: function( user ){
			console.log('UserID',user.id);
			var endpoint = new_Endpoint();
			endpoint._fakeResponse({
				success: true,
				user: _fakeUSer
			});
			return endpoint;
		},
		getLikes: function(){
			var endpoint = new_Endpoint();
			endpoint._fakeResponse({
				"genders": ["male","female","other"], 
				"interestedIn": ["male","female","other","all"], 
				"movies": ["Titanic","Star Wars","Dawn of the Dead"],
				"tvSeries": ["Lost","The Walking Dead","The Simpsons"],
				"music": ["The beatles","Disturbed","Slipknot"],
				"countries": ["Honduras","United States","Guatemala","Nicaragua","El Salvador"]
			});
			return endpoint;
		},
		saveUser: function( id , profile ){
			console.log('UserID',id, profile);
			var endpoint = new_Endpoint();
			endpoint._fakeResponse({
				success: true,
				user: _fakeUSer
			});
			return endpoint;
		},
		getMatches: function( id , filters ){
			console.log('UserID',id, filters);
			var endpoint = new_Endpoint();
			endpoint._fakeResponse({
				"suggestions": [{
					"id":'100000304973925'
				},{
					"id":'100000170168144'
				},{
					"id":'502184878'
				},{
					"id":'100001524085465'
				}],
				"matches": [{
					"id":'574890965'
				}]
			});
			return endpoint;
		},
		like: function( userId , otehrId , dislike ){
			console.log('UserID',userId, otehrId);
			var endpoint = new_Endpoint();
			endpoint._fakeResponse({
				success: true,
				match: true
			});
			return endpoint;
		}
	};
	return Data; 
});