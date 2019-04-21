angular.module('AsunaWeb')

.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('/events/create/new', {
			templateUrl: '/events/new-event/new-event.html',
			css: '/events/new-event/new-event.css',
			controller: 'NewEventController',
			controllerAs: 'vm'
		 })
}])

.controller('NewEventController', ['$scope', '$location', '$restservices', function($scope, $location, $restservices) {
		var vm = this;

    vm.currentUser = {};

    vm.users = [];

    vm.ranks = [
      'Follower',
      'Citizen',
      'Thrall',
      'Marauder',
      'Shieldbreaker',
      'Valkyrie',
      'Thane'
    ];

    vm.tankIcon = "fa fa-shield";
    vm.healerIcon = "fa fa-medkit";
    vm.meleeIcon = "ra ra-crossed-swords";
    vm.rangedIcon = "ra ra-arrow-cluster";

    vm.tankRoleName = "Tanks";
    vm.healerRoleName = "Healers";
    vm.mdpsRoleName = "Melee";
    vm.rdpsRoleName = "Ranged";

    vm.newEvent = {
      min_rank : vm.ranks[0],
      eventDate : new Date(),
      eventTime : "10:56",
      TANK : 0,
      HEALER : 0,
      MDPS : 0,
      RDPS : 0,
    };

    vm.errorMessages = {};

    vm.getCurrentUser = function() {
      $restservices.getCurrentUser()
      .then(function(response){
        vm.currentUser = response.data;
        if(vm.currentUser.role == 'MEMBER'){
          $location.path('/events/');
        }
        vm.newEvent.created_by_id = vm.currentUser.id;
        vm.newEvent.event_leader = vm.currentUser.discord_name;
        console.log(vm.currentUser);
      })
      .catch(function(response){
        $restservices.handleErrors(response, $scope.updateLoggedIn);
      });
    }

    vm.getUsers = function() {
      $restservices.getUsers({})
      .then(function(response){
        vm.users = response.data.data;
        console.log(vm.users);
      })
      .catch(function(response){
        $restservices.handleErrors(response, $scope.updateLoggedIn);
      });
    }

    vm.createEvent = function(){
      try{
        vm.newEvent.event_time = (vm.newEvent.eventDate.getTime() + vm.newEvent.eventTime.getTime()) / 1000;
      }
      catch{
        vm.errorMessages.event_time = ["Please specify a valid date and time."];
        return;
      }

      $restservices.createEvent(vm.newEvent)
      .then(function(response){
        console.log(response);
        $location.path('/events/'+response.data.event.id)
      })
      .catch(function(response){
        console.log(response);
        if(response.status == 400){
          vm.errorMessages = response.data;
        }
      });
    }

    vm.autogrow = function(element) {
      element.style.height = "5px";
      element.style.height = (element.scrollHeight)+"px";
    }

    vm.getCurrentUser();
    vm.getUsers();

	}]);
