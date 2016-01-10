'use strict';

/* Filters */
var Filters = angular.module('advdb.filters', []);

Filters.filter('capitalize',function(){
	return function(text){
		return text[0].toUpperCase() + text.substring(1).toLowerCase();
	};
});

Filters.filter('UpperCase',function(){
	return function(text){
		return text.toUpperCase();
	};
});

Filters.filter('Math',function(){
	return function(text,func){
		return Math[func](text);
	};
});

Filters.filter('i18n',['i18n',function(i18n){
	return function(text){
		i18n._registerScope(this);
		return i18n[text];
	};
}]);

Filters.filter('date',[function(){
	return function(text){
		return (new Date(text)).toLocaleString();
	};
}]);

Filters.filter('removeLast',[function(){
	return function(array){
		return array.filter(function(a,i){return (i!=array.length-1);});
	};
}]);

Filters.filter('removeFirst',[function(){
	return function(array){
		return array.filter(function(a,i){return i;});
	};
}]);

Filters.filter('gsort',function(){
	return function(objArray, attr ){
		return objArray.sort(function( a , b ){
			if( attr )
				return b[attr] - a[attr];
			return b - a;
		});
	};
});

Filters.filter('lsort',function(){
	return function(objArray, attr ){
		return objArray.sort(function( a , b ){
			if( attr )
				return a[attr] - b[attr];
			return a - b;
		});
	};
});

Filters.filter('interestsort',function(){
	return function(objArray, type , profile ){
		if( objArray ){
			return objArray.sort(function(a,b){
				if( profile.likes[type] ){
					var aid = a.movie_id || a.tvshow_id;
					var bid = b.movie_id || b.tvshow_id;

					if( profile.likes[type].indexOf(aid)!=-1 && profile.likes[type].indexOf(bid)==-1 ){
						return -1;
					}
					if( profile.likes[type].indexOf(aid)==-1 && profile.likes[type].indexOf(bid)!=-1 ){
						return 1
					}
				}
				return b.title<a.title?1:-1;
			});
		}
		return [];
	};
});