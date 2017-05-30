(function () {
    'use strict';

    angular
        .module('fs', [])
        .factory('FridgeService', FridgeService);

    FridgeService.$inject = ['$http'];

    console.log("fs");
    function FridgeService($http) {
        var service = {};

        service.setFridgeContent = setFridgeContent;
        service.getFridgeContent = getFridgeContent;
        service.setHasFridge = setHasFridge;
        service.getHasFridge = getHasFridge;
        service.updateDatabase = updateDatabase;
        service.removeFromDatabase = removeFromDatabase;
        service.getRecipeTitles = getRecipeTitles;
        service.getRecipeDetailed = getRecipeDetailed;
        service.addFridgeToDatabase = addFridgeToDatabase;

        return service;


        function setFridgeContent(fridgeContent){
            console.log('set fridge content');
            this.fridgeContent = fridgeContent;
            console.log(this.fridgeContent);
        };

        function getFridgeContent(){

            return this.fridgeContent;
        };

        function setHasFridge(hasFridge){
            console.log('set fridge content');
            this.hasFridge = hasFridge;
            console.log(this.hasFridge);
        };

        function getHasFridge(){

            return this.hasFridge;
        };


        function addFridgeToDatabase(fridgeId) {
            console.log('add fridge to database database');
            return $http.post('/addfridge', fridgeId);
        }


        function updateDatabase(ingredientInFridge) {
            console.log('update database');
            return $http.post('/addgrocery', ingredientInFridge);
        }


        function removeFromDatabase(ingredientInFridge) {
            console.log('remove from database');
            return $http.post('/removegrocery', ingredientInFridge);
        }

        function getRecipeTitles() {
            console.log('get recipes');

            return $http.get('/getrecipes');
        }

        function getRecipeDetailed(title) {
            console.log('get recipes');

            return $http.get('/getrecipedetailed/'+ title);
        }


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