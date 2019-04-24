/*
 * Angular root application.
 */

// Instantiate the module to use.
angular.module("AsunaWeb", ['ngRoute', 'ngAnimate'])

    // Configure the application with the routing system.
    .config(['$routeProvider', '$locationProvider',
	     function($routeProvider, $locationProvider) {

	$routeProvider

	    .otherwise({ redirectTo: '/'});

    }])


    .controller("AppController", [ '$scope', '$location', '$restservices', '$localstorage', function($scope, $location, $restservices, $localstorage) {
    	var vm = this;
      vm.signedIn = false;
      vm.user = {};

      $scope.updateLoggedIn = function() {
        if($localstorage.get('api_token')){
          vm.signedIn = true;
          vm.user = $localstorage.getObject('user');
        }
        else {
          vm.signedIn = false;
          vm.user = {};
          $location.path('/signin')
        }
      }

      $scope.updateLoggedIn();

      if(vm.signedIn){
        $restservices.setApiToken($localstorage.get('api_token'));
      }

    }]);
