angular.module('AsunaWeb')

.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('/users', {
			templateUrl: '/users/users.html',
			css: '/users/users.css',
			controller: 'UsersController',
			controllerAs: 'vm'
		 })
}])

.controller('UsersController', ['$scope', '$location', '$restservices', function($scope, $location, $restservices) {
		var vm = this;

    vm.currentUser = {};

    vm.users = [];
    vm.keyword = "";
    vm.filter = {};


    vm.getCurrentUser = function() {
      $restservices.getCurrentUser()
      .then(function(response){
        vm.currentUser = response.data;
        console.log(vm.currentUser);
      })
      .catch(function(response){
        $restservices.handleErrors(response, $scope.updateLoggedIn);
      });
    }

    vm.getUsers = function() {
      $restservices.getUsers(vm.filter)
      .then(function(response){
        vm.users = response.data.data;
        console.log(vm.users);
      })
      .catch(function(response){
        $restservices.handleErrors(response, $scope.updateLoggedIn);
      });
    }

    vm.viewUser = function(user){
      $location.path('/users/'+user.id);
    }

    vm.getCurrentUser();
    vm.getUsers();

	}]);
