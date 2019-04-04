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
    vm.loginSuccess = false;

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
          console.log("Login success.");
          console.log(response);
          $scope.updateLoggedIn();
          vm.loginSuccess = true;
          $location.path('/');
        }, function error(response){
          vm.showSignInError = true;
          vm.submitEnabled = true;
        });
			}
		}

    }]);
