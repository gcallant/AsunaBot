angular.module('AsunaWeb')
.factory('$restservices', ['$http', '$localstorage', function($http, $localstorage){
	var restServices = {};

  var API_URI = "http://asuna.test/api";

  restServices.login = function(authcode){
    return $http.post(API_URI+'/login', {'authcode' : authcode});
  }

  restServices.logout = function(){
    return $http.post(API_URI+'/logout');
  }

  restServices.getCurrentUser = function(){
    return $http.get(API_URI+'/user');
  }

	restServices.getEvents = function(filter){
		return $http.get(API_URI+'/events', filter);
	}

  restServices.getEvent = function(event_id){
    return $http.get(API_URI+'/events/'+event_id);
  }

  restServices.getEventSignups = function(event_id){
    return $http.get(API_URI+'/events/'+event_id+'/signups');
  }

	restServices.getEventUsers = function(event_id){
		return $http.get(API_URI+'/events/'+event_id+'/users');
	}

	restServices.signup = function(signup){
		return $http.post(API_URI+'/events/'+signup.event_id+'/signups', signup);
	}

  restServices.setApiToken = function(token){
    $localstorage.set('api_token', token);
    $http.defaults.headers.common.Authorization = "Bearer " + token;
  }

  restServices.invalidateApiToken = function(){
    $localstorage.remove('api_token');
    $http.defaults.headers.common.Authorization = "";
  }

	restServices.handleErrors = function(response, callback){
		console.log(response);
		switch(response.status) {
			case 401:
				restServices.invalidateApiToken();
				break;
		}

		callback();
	}

	return restServices;
}]);
