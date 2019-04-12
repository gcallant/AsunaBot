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

		vm.currentUser = {};
    vm.signups = [];
		vm.users = [];
		vm.tanks = [];
		vm.healers = [];
		vm.melee = [];
		vm.ranged = [];

		vm.tankRole = "Tanks";
		vm.healRole = "Healers";
		vm.meleeRole = "Melee";
		vm.rangedRole = "Ranged";

		vm.tankIcon = "fa fa-shield";
		vm.healIcon = "fa fa-medkit";
		vm.meleeIcon = "ra ra-crossed-swords";
		vm.rangedIcon = "ra ra-arrow-cluster";

    vm.getEventSignups = function(){
      $restservices.getEventSignups(vm.eventId)
      .then(function success(response){
				vm.signups = response.data.signups;
	      console.log(vm.signups);
				vm.sortRoles();
      })
			.catch(function(response){
				$restservices.handleErrors(response, $scope.updateLoggedIn);
			});
    }

		vm.getEventUsers = function(){
			$restservices.getEventUsers(vm.eventId)
			.then(function success(response){
				vm.users = response.data.users;
				console.log(vm.users);
			})
			.catch(function(response){
				$restservices.handleErrors(response, callback=$scope.updateLoggedIn);
			});
		}

    vm.getEvent = function(){
      $restservices.getEvent(vm.eventId)
      .then(function success(response){
				vm.event = response.data.event;
				console.log(vm.event);
      })
			.catch(function(response){
				$restservices.handleErrors(response, callback=$scope.updateLoggedIn);
      });
    }

		vm.getUser = function(user_id) {
			vm.users.find(user => {
			  return user.id === user_id;
			});
		}

		vm.getCurrentUser = function(){
			$restservices.getCurrentUser()
			.then(function success(response){
				vm.currentUser = response.data;
				console.log(vm.currentUser);
			})
			.catch(function(response){
				$restservices.handleErrors(response, callback=$scope.updateLoggedIn);
			});
		}

		vm.sortRoles = function() {
			vm.tanks = vm.signups.filter(su => {
				return su.primary_role == "TANK";
			});

			vm.healers = vm.signups.filter(su => {
				return su.primary_role == "HEALER";
			});

			vm.melee = vm.signups.filter(su => {
				return su.primary_role == "MDPS";
			});

			vm.ranged = vm.signups.filter(su => {
				return su.primary_role == "RDPS";
			});
		}

		vm.refreshData = function(){
			vm.getEvent();
			vm.getEventUsers();
	    vm.getEventSignups();
			vm.getCurrentUser();
		}

		vm.populateEvent = function(){
			for(prop in Object.keys($routeParams)){
				if(vm.event[prop]){
					vm.event[prop] = $routeParams[prop];
				}
			}
		}

		vm.populateEvent();
		vm.refreshData();


	}]);
