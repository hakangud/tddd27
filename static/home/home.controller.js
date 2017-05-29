(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$rootScope', '$location','$http', '$scope', 'FridgeService', 'MsgService'];
    function HomeController($rootScope, $location, $http, $scope, FridgeService, MsgService) {
        var vm = this;
        console.log("homeC");
        console.log();

        vm.add_groceries_to_database = add_groceries_to_database;

        vm.getRecipeTitles = getRecipeTitles;


        function add_groceries_to_database() {
            console.log("reg");
            console.log(vm.grocery);
            FridgeService.removeFromDatabase(vm.grocery)
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

        function remove_grocery_from_database() {
            console.log("reg");
            console.log(vm.grocery);
            FridgeService.removeFromDatabase(vm.grocery)
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

            response = FridgeService.getRecipeTitles();
            console.log(response)



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
            $rootScope.ws.close();
          };


          $scope.items = FridgeService.getFridgeContent();





//            $scope.items = [{
//
//                salary_head_name : 'BASIC',
//                        salary_head_value : 15000,
//                            salary_head_type : 'E'
//
//            }, {
//
//                salary_head_name : 'HRA',
//                         salary_head_value : 7500,
//                            salary_head_type : 'E'
//
//            },{
//
//                salary_head_name : 'Conveyance',
//                         salary_head_value : 1600,
//                            salary_head_type : 'E'
//
//            },{
//
//                salary_head_name : 'Med. Allow',
//                        salary_head_value : 1800,
//                            salary_head_type : 'E'
//
//            },{
//
//                salary_head_name : 'PF',
//                         salary_head_value : 1800,
//                            salary_head_type : 'D'
//
//            }];


    }
})();