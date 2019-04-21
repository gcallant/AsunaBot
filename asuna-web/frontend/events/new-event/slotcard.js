angular.module('AsunaWeb')
.component('slotcard', {
	templateUrl: './events/new-event/slotcard.html',
	controller: 'SlotcardController',
	controllerAs: 'vm',
	bindings: {
		icon: '<',
    roleName: '<',
    openSlots: '='
	}
})
.controller('SlotcardController', [ '$scope', '$location', '$restservices', function($scope, $location, $restservices){
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

  vm.increaseSlots = function() {
    vm.openSlots += 1;
  }

  vm.decreaseSlots = function() {
    if(vm.openSlots > 0) {
      vm.openSlots -= 1;
    }
  }

}]);
