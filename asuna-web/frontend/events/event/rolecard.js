angular.module('AsunaWeb')
.component('rolecard', {
	templateUrl: './events/event/rolecard.html',
	controller: 'RolecardController',
	controllerAs: 'vm',
	bindings: {
    event: '<',
		icon: '<',
    roleName: '<',
    openSlots: '<',
    users: '<',
    roleSignups: '<',
    allSignups: '<',
    currentUser: '<',
    refreshData: '<'
	}
})
.controller('RolecardController', [ '$scope', '$location', '$restservices', function($scope, $location, $restservices){
	var vm = this;

  vm.getRole = function(keyword){
    switch(keyword){
      case 'Tanks':
        return 'TANK';
        break;
      case 'Healers':
        return 'HEALER';
        break;
      case 'Melee':
        return 'MDPS';
        break;
      case 'Ranged':
        return 'RDPS';
        break;
    }
  }

  vm.signUp = function(role, flexRoles){
    if(role == 'RESERVE'){
      flexRoles[0] = vm.getRole(flexRoles[0]);
    }
    else{
      role = vm.getRole(role);
    }

    signup = {
      event_id : vm.event.id,
      player_id : vm.currentUser.id,
      primary_role : role,
      flex_roles : flexRoles.toString(),
    }

    $restservices.signup(signup)
    .then(function(response){
      console.log(response);
      vm.refreshData();
    })
    .catch(function(response){
      console.log(response);
    });
  }


}]);
