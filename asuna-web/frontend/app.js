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
      vm.discord_name = "";

      $scope.updateLoggedIn = function() {
        if($localstorage.get('api_token')){
          vm.signedIn = true;
          vm.discord_name = $localstorage.get('discord_name');
        }
        else {
          vm.signedIn = false;
          vm.discord_name = "";
          $location.path('/signin')
        }
      }

      $scope.updateLoggedIn();

      if(vm.signedIn){
        $restservices.setApiToken($localstorage.get('api_token'));
      }

    }]);
