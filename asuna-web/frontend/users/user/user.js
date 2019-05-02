angular.module('AsunaWeb')

.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('/users/:id', {
			templateUrl: '/users/user/user.html',
			css: '/users/user/user.css',
			controller: 'UserController',
			controllerAs: 'vm'
		 })
}])

.controller('UserController', ['$routeParams', '$location', '$scope', '$restservices', function($routeParams, $location, $scope, $restservices) {
		var vm = this;

		vm.now = new Date();

		vm.userId = $routeParams.id;

		vm.currentUser = {};

    vm.user = {};

    vm.signups = [];
		vm.completedSignups = [];
		vm.upcomingSignups = [];
		vm.activeTab = "upcoming-tab";

		vm.getUser = function(user_id) {
      $restservices.getUser(user_id)
      .then(function(response){
        vm.user = response.data.user;
      })
      .catch(function(response){
        if(response.status == 404){
          vm.error = "No user";
          return;
        }
        $restservices.handleErrors(response, callback=$scope.updateLoggedIn);
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

    vm.getSignups = function(user_id){
      $restservices.getUserSignups(user_id)
			.then(function success(response){
				response.data.signups.forEach(function(signup){
					signup.event.completed = vm.now >= new Date(signup.event.event_time);
					if(signup.event.completed){
						vm.completedSignups.push(signup);
					}
					else{
						vm.upcomingSignups.push(signup);
					}
				});
				vm.signups = vm.upcomingSignups;
				console.log(vm.signups);
			})
			.catch(function(response){
				$restservices.handleErrors(response, callback=$scope.updateLoggedIn);
			});
    }

    vm.viewEvent = function(event_id){
      $location.path('/events/'+event_id);
    }

		vm.viewSignups = function($event){
			vm.activeTab = $event.target.attributes.id.value;
			switch(vm.activeTab){
				case 'upcoming-tab':
					vm.signups = vm.upcomingSignups;
					break;
				case 'completed-tab':
					vm.signups = vm.completedSignups;
					break;
			}
		}

    vm.getCurrentUser();
    vm.getUser(vm.userId);
    vm.getSignups(vm.userId);

	}]);
