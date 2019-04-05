angular.module('AsunaWeb')
    .config(['$routeProvider', function($routeProvider) {
	$routeProvider.when('/signin', {
	    templateUrl: './signin/signin.html',
	    controller: 'SigninController',
	    controllerAs: 'vm'
	})
    }])
    .controller('SigninController', ['$scope', '$location', '$restservices', '$localstorage', function($scope, $location, $restservices, $localstorage) {
		var vm = this;

		vm.authcode;

		vm.submitEnabled = true;

		vm.submit = function() {
			if(vm.submitEnabled) {
				vm.submitEnabled = false;

        $restservices.login(vm.authcode)
        .then(function success(response){

          if(response.data.data == "Login failed."){
            vm.showSignInError = true;
            vm.submitEnabled = true;
            return;
          }
          $restservices.setApiToken(response.data.api_token);
          $restservices.getCurrentUser()
          .then(function success(response){
            $localstorage.set('discord_name', response.data.discord_name);
            console.log("Login success.");
            console.log(response);
            $scope.updateLoggedIn();
            $location.path('/');

          }, function error(response){
            console.log(response);
          });
        }, function error(response){
          vm.showSignInError = true;
          vm.submitEnabled = true;
        });
			}
		}

    }]);
