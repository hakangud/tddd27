(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$rootScope', '$location','$http', '$scope', 'FridgeService', 'MsgService', 'SocketService','$uibModal'];
    function HomeController($rootScope, $location, $http, $scope, FridgeService, MsgService, SocketService, $uibModal) {
        var vm = this;
        vm.items = FridgeService.getFridgeContent();
        vm.hasFridge = FridgeService.getHasFridge();
        vm.SocketService = SocketService;
        vm.add_groceries_to_database = add_groceries_to_database;
        vm.getRecipeTitles = getRecipeTitles;
        vm.getRecipeDetailed = getRecipeDetailed;
        vm.remove_grocery_from_database = remove_grocery_from_database;
        vm.open =  open;
        vm.signout = signout;
        vm.addFridgeToDatabase = addFridgeToDatabase;
        var updateFridge = function () {
            vm.items = SocketService.actions[0].data;
        };

        SocketService.registerCallback(updateFridge);

        function add_groceries_to_database() {
            FridgeService.updateDatabase(vm.grocery)
                .then(function (response) {
                    MsgService.Success(response.data.message);
                },
                function (errResponse) {
                    MsgService.Error(errResponse.data.message);
                }
            );
        }

        function open (recipeDetailed) {
            $uibModal.open({
                templateUrl: 'myModalContent.html',
                controller: function($scope) {
                    $scope.recipeDetailed = recipeDetailed;
                }
            });
        }

        function remove_grocery_from_database(index) {
            FridgeService.removeFromDatabase(vm.items[index])
                .then(function (response) {
                    MsgService.Success(response.data.message);
                },
                function (errResponse) {
                    MsgService.Error(errResponse.data.message);
                }
            );
        }

        function addFridgeToDatabase() {
            FridgeService.addFridgeToDatabase(vm.fridgeId)
                .then(function (response) {
                    vm.hasFridge = true;
                    vm.items = response.data.data;
                    MsgService.Success(response.data.message);
                },
                function (errResponse) {
                    MsgService.Error(errResponse.data.message);
                }
            );
        }

        function getRecipeTitles() {
            FridgeService.getRecipeTitles()
                .then(function (response) {
                    vm.titles = response.data.recipes;
                },
                function () {
                    console.log('error');
                }
            );
        }

        function getRecipeDetailed(index) {
            FridgeService.getRecipeDetailed(vm.titles[index])
                .then(function (response) {
                    vm.open(response.data.recipe_detailed);
                },
                function () {
                    console.log('error');
                }
            );
        }

        function signout() {
            $http.post('/signout')
                .then(function (response) {
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

                    MsgService.Success(response.data.message);
                    $location.path('/login');
                },
                function (errResponse) {
                    MsgService.Error(errResponse.data.message);
                    $location.path('/login');
                }
            );
        }
    }

})();