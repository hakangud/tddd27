(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$rootScope', '$location','$http', '$scope', 'FridgeService', 'MsgService', 'SocketService'];
    function HomeController($rootScope, $location, $http, $scope, FridgeService, MsgService, SocketService) {
        var vm = this;
        console.log("homeC");
        console.log();

        //$scope.SocketService = SocketService;
        vm.add_groceries_to_database = add_groceries_to_database;
        vm.getRecipeTitles = getRecipeTitles;
        vm.getRecipeDetailed = getRecipeDetailed;
        vm.remove_grocery_from_database = remove_grocery_from_database;

        var updateFridge = function () {
            console.log('update fridge');
            console.log(SocketService.actions[0]);
            vm.items = SocketService.actions[0].data;
        };

        SocketService.registerCallback(updateFridge);

        // deep watch for websocket event
        //$scope.$watch(SocketService.collection, function () {
        //    console.log("running watch function");
        //    console.log(SocketService);
        //    angular.forEach(SocketService.collection, function (value, key) {
        //
        //        console.log(value);
        //        console.log(value.action);
        //        if (value.action === 'updategroceries') {
        //            console.log(value.data[0]);
        //            console.log('message = ' + value.message);
        //            vm.items = value.data;
        //        }
        //
        //    }, true);
        //

            //for (var x in SocketService.collection) {
            //    console.log(x);
            //}
            //console.log(SocketService.collection[0].action);

        //});

        //$rootScope.$apply(function () {
        //    SocketService
        //})

        function add_groceries_to_database() {
            console.log("reg");
            console.log(vm.grocery);
            FridgeService.updateDatabase(vm.grocery)
                .then(function (response) {
                    console.log(response.data.message);
                    MsgService.Success(response.data.message);

                },
                function (errResponse) {
                    console.log(errResponse.data.message);
                    MsgService.Error(errResponse.data.message);
                }
            );
        }

        function remove_grocery_from_database(index) {
            console.log("reg");
            console.log(vm.items[index]);
            FridgeService.removeFromDatabase(vm.items[index])
                .then(function (response) {
                    console.log(response.data.message);
                    MsgService.Success(response.data.message);

                },
                function (errResponse) {
                    console.log(errResponse.data.message);
                    MsgService.Error(errResponse.data.message);
                }
            );
        }

        function getRecipeTitles() {
            console.log('klickade recipe-titles');

            FridgeService.getRecipeTitles()
                .then(function (response) {
                    console.log(response.data.recipes);
                    vm.titles = response.data.recipes;
                    //MsgService.Success(response.data.data);

                },
                function (errResponse) {
                    console.log(errResponse.data.message);
                    MsgService.Error(errResponse.data.message);
                }
            );


        }

        function getRecipeDetailed(index) {
            console.log('klickade recipe-detailed');

            console.log(vm.titles[index]);


            FridgeService.getRecipeDetailed(vm.titles[index])
                .then(function (response) {
                    console.log(response.data.recipe_detailed);
                    //MsgService.Success(response.data.data);

                },
                function (errResponse) {
                    console.log(errResponse.data.message);
                    MsgService.Error(errResponse.data.message);
                }
            );



        }



          //create a seperate controller for logout
          $scope.logout2 = function() {
            console.log('clicked loguot');

            $http.post('/signout')
            .then(function (response) {
                console.log(response.data.message);
                $location.path('/login');

            },
            function (errResponse) {
                console.log(errResponse.data.message);
            }
            );
            //$rootScope.ws.close();
          };


          //vm.items = FridgeService.getFridgeContent();



    }
})();