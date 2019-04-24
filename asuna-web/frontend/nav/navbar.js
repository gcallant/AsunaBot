angular.module('AsunaWeb')
.component('navbar', {
	templateUrl: './nav/navbar.html',
	controller: 'NavController',
	controllerAs: 'vm',
	bindings: {
		signedIn: '<',
		user: '<',
	}
})
.controller('NavController', [ '$scope', '$location', '$restservices', function($scope, $location, $restservices){
	var vm = this;

	vm.logout = function() {
		$restservices.logout()
		.then(function success(response){
      $restservices.invalidateApiToken();
      console.log("Logout success.");
      $scope.$parent.updateLoggedIn();
      $location.path("/signin");
    }, function error(response){
			$restservices.invalidateApiToken();
      console.log("Logout fail: invalidated token anyway.");
      $scope.$parent.updateLoggedIn();
      $location.path("/signin");
    });
	}

}]);
