angular.module('AsunaWeb')

.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('/events/:id', {
			templateUrl: '/events/event/event.html',
			css: '/events/event/event.css',
			controller: 'EventController',
			controllerAs: 'vm'
		 })
}])

.controller('EventController', ['$routeParams', '$scope', '$restservices', function($routeParams, $scope, $restservices) {
		var vm = this;

		vm.eventId = $routeParams.id;

		vm.event = {
      event_name : "Late Night Poopy Party",
      trial_name : "vSO",
      event_leader : "Blitznacht",
      description : "Everybody compare your shits with Blitz while getting shitted on by poisonous cave trolls!",
      min_rank : "Shitstreaker",
      TANK : 2,
      HEALER : 2,
      MDPS : 4,
      RDPS : 4,
    };

    vm.signups = [];

    vm.getEventSignups = function(){
      $restservices.getEventSignups(vm.eventId)
      .then(function success(response){
        vm.signups = response.data.signups;
        console.log(vm.signups);
      }, function error(response){
        if(response.status == 401){
          $restservices.invalidateApiToken();
          $scope.updateLoggedIn();
          return;
        }
      });
    }

    vm.getEvent = function(){
      $restservices.getEvent(vm.eventId)
      .then(function success(response){
        vm.event = response.data.event;
      }, function error(response){
        if(response.status == 401){
          $restservices.invalidateApiToken();
          $scope.updateLoggedIn();
          return;
        }
        console.log(response);
      });
    }

    vm.getEvent();
    vm.getEventSignups();
	}]);
