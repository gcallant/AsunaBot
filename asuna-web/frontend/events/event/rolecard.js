angular.module('AsunaWeb')
.component('rolecard', {
	templateUrl: './events/event/rolecard.html',
	controller: 'RolecardController',
	controllerAs: 'vm',
	bindings: {
    event: '<',
		icon: '<',
    roleName: '<',
		role: '<',
    openSlots: '<',
    roleSignups: '<',
    currentUser: '<',
    refreshData: '<',
		mySignup: '<',
	}
})
.controller('RolecardController', [ '$scope', '$location', '$restservices', function($scope, $location, $restservices){
	var vm = this;

	vm.signupText = "Sign Up";
	vm.waitlistText = "Waitlist";

	vm.initialize = function(){
		if(vm.mySignup){
			if(vm.mySignup.primary_role == vm.role){
				vm.signupText = "Cancel";
			}
			else if(vm.mySignup.primary_role != 'RESERVE'){
				vm.signupText = "Switch";
			}
			else{
				vm.signupText = "Sign Up";
			}

			if(vm.mySignup.flex_roles.split(',').includes(vm.role)){
				vm.waitlistText = "Cancel";
			}
		}
	}

  vm.signUp = function(role, flexRoles){

		var signup = {};

		if(vm.mySignup){
			if(role != 'RESERVE'){
				if(vm.mySignup.primary_role != 'RESERVE'){
					flexRoles.push(vm.mySignup.primary_role);
				}
				signup.primary_role = role;
			}
			else if(flexRoles[0] == vm.mySignup.primary_role){
				signup.primary_role = 'RESERVE';
			}
			else{
				signup.primary_role = vm.mySignup.primary_role;
			}

			if(vm.mySignup.flex_roles){
				signup.flex_roles = vm.mySignup.flex_roles.split(',').concat(flexRoles.filter(function (item) {
    			return vm.mySignup.flex_roles.indexOf(item) < 0;
				}));
			}
			else{
				signup.flex_roles = flexRoles;
			}

			signup.flex_roles = signup.flex_roles.filter(function(item){
				return signup.primary_role != item;
			}).toString();;

			signup.id = vm.mySignup.id;
			signup.event_id = vm.mySignup.event_id;
			signup.player_id = vm.mySignup.player_id;

			vm.updateSignup(signup);
		}
		else {
	    signup = {
	      event_id : vm.event.id,
	      player_id : vm.currentUser.id,
	      primary_role : role,
	      flex_roles : flexRoles.toString(),
	    }
			vm.createSignup(signup);
		}
  }

	vm.drop = function(){
		$restservices.deleteSignup(vm.mySignup.id)
		.then(function(response){
			console.log(response);
			vm.refreshData();
			vm.initialize();
		})
		.catch(function(response){
			console.log(response);
		});
	}

	vm.dropFlex = function(dropRole){
		updateSignup = JSON.parse(JSON.stringify(vm.mySignup));
		updateSignup.flex_roles = updateSignup.flex_roles.split(',').filter(function (item) {
			return item != dropRole;
		}).toString();

		if(updateSignup.primary_role == 'RESERVE' && updateSignup.flex_roles == ""){
			vm.drop();
		}
		else{
			vm.updateSignup(updateSignup);
		}
	}

	vm.createSignup = function(signup){
		$restservices.signup(signup)
		.then(function(response){
			console.log(response);
			vm.refreshData();
			vm.initialize();
		})
		.catch(function(response){
			console.log(response);
		});
	}

	vm.updateSignup = function(signup){
		$restservices.updateSignup(signup)
		.then(function(response){
			console.log(response);
			vm.refreshData();
			vm.initialize();
		})
		.catch(function(response){
			console.log(response);
		});
	}

	vm.initialize();

}]);
