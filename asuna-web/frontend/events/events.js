angular.module('AsunaWeb')

.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('/events', {
			templateUrl: '/events/events.html',
			css: '/events/events.css',
			controller: 'EventsController',
			controllerAs: 'vm'
		 })
}])

.controller('EventsController', ['$scope', '$location', '$restservices', function($scope, $location, $restservices) {
		var vm = this;

    vm.currentUser = {};
    vm.events = [];
    vm.filter = {};

    vm.getEvents = function(filter) {
      $restservices.getEvents(filter)
      .then(function(response){
        vm.events = response.data.data;
      })
      .catch(function(response){
        $restservices.handleErrors(response, $scope.updateLoggedIn);
      });
    }

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

    vm.viewEvent = function(event){
      $location.path('/events/'+event.id).search(event);
    }

    vm.getEvents({});
    vm.getCurrentUser();
	}]);
