(function () {
    'use strict';

    angular
        .module('fs', [])
        .factory('FridgeService', FridgeService);


    console.log("fs");
    function FridgeService() {
        var service = {};

        service.setFridgeContent = setFridgeContent;
        service.getFridgeContent = getFridgeContent;


        return service;


        function setFridgeContent(fridgeContent){
            console.log('set fridge content');
            this.fridgeContent = fridgeContent;
            console.log(this.fridgeContent);
        };

        function getFridgeContent(){

            return this.fridgeContent;
        };



    };

})();

//
//(function () {
//    'use strict';
//
//    angular
//        .module('fs', [])
//        .service('FridgeService', FridgeService);
//
//    FridgeService.$inject = ['$http'];
//    console.log("fs");
//    function FridgeService($http) {
//        var service = {};
//
//        service.Create2 = Create2;
//
//        return service;
//
//        function Create2(user) {
//            return $http.post('/register', user);
//        }
//
//    }
//
//})();