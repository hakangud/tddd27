(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$rootScope', '$location','$http', '$scope', 'FridgeService', 'MsgService', 'SocketService','$uibModal'];
    function HomeController($rootScope, $location, $http, $scope, FridgeService, MsgService, SocketService, $uibModal) {
        var vm = this;

        vm.SocketService = SocketService;
        vm.add_groceries_to_database = add_groceries_to_database;
        vm.getRecipeTitles = getRecipeTitles;
        vm.getRecipeDetailed = getRecipeDetailed;
        vm.remove_grocery_from_database = remove_grocery_from_database;
        vm.open =  open;
        vm.addFridgeToDatabase = addFridgeToDatabase;

        $scope.enableCustomerDirective = false;
        $scope.showdiv = function(){
//            if ($scope.enableCustomerDirective){
//                $scope.enableCustomerDirective = false;
//            }
//            else {
                $scope.enableCustomerDirective = true;
            //}

        };


         function open (recipeDetailed) {
            console.log('modal')
            console.log(vm.recipeDetailed.title)
            var modalInstance = $uibModal.open({
                ariaLabelledBy: 'modal-title',
                ariaDescribedBy: 'modal-body',
                templateUrl: 'myModalContent.html',
                //controller: 'HomeController', function() {
                //    vm.recipeDetailed = recipeDetailed;
                //},
                //controllerAs: 'vm'
                controller: function($scope) {
                    $scope.recipeDetailed = recipeDetailed;
                }
                });
            }


        vm.name = 'hej'
        vm.recipeDetailed = FridgeService.getRecipe

        var updateFridge = function () {
            console.log('update fridge');
            console.log(SocketService.actions[0]);
            vm.items = SocketService.actions[0].data;
        };

        SocketService.registerCallback(updateFridge);

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

        function addFridgeToDatabase() {
            console.log('klickade vm.addFridgeToDatabase()');

            FridgeService.addFridgeToDatabase(vm.fridgeId)
                .then(function (response) {
                    console.log(response.data.data);
                    vm.hasFridge = true;
                    vm.items = response.data.data;

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

                    vm.recipeDetailed = response.data.recipe_detailed;
                    vm.recipeDetailed.title = response.data.recipe_detailed['title'];
                    vm.open(response.data.recipe_detailed);
                    //MsgService.Success(response.data.data);

                },
                function (errResponse) {
                    console.log(errResponse.data.message);
                    MsgService.Error(errResponse.data.message);
                }
            );



        }

        $scope.logout2 = function() {
            console.log('clicked logout');

            $http.post('/signout')
                .then(function (response) {
                    //SocketService.ws.close();
                    gapi.load('auth2', function() {
                        gapi.auth2.init({
                            client_id: '192085420693-gnet8a4sjhn89ll6ejjho1tudv3l2oaa.apps.googleusercontent.com',
                            scope: "profile email"
                        }).then(function () {
                                var auth = gapi.auth2.getAuthInstance();
                                if (auth.isSignedIn.get()) {
                                    auth.signOut();
                                }
                        })
                    });

                    console.log(response.data.message);
                    $location.path('/login');
                },
                function (errResponse) {
                    console.log(errResponse.data.message);
                    $location.path('/login');
                }
            );
        };


        vm.items = FridgeService.getFridgeContent();
        vm.hasFridge = FridgeService.getHasFridge();



    }
})();