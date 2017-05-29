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

        vm.SocketService = SocketService;
        vm.add_groceries_to_database = add_groceries_to_database;

        // deep watch for websocket event
        $scope.$watch(SocketService.collection, function () {
            angular.forEach(SocketService.collection, function (value, key) {
                console.log(value.action);
            }, true);
            //for (var x in SocketService.collection) {
            //    console.log(x);
            //}
            //console.log(SocketService.collection[0].action);
            console.log("running watch function");
        });

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