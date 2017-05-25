(function () {
    'use strict';

    angular
        .module('app')
        .controller('HomeController', HomeController);

    HomeController.$inject = ['$location','$http', '$scope', 'FridgeService'];
    function HomeController($location, $http, $scope, FridgeService) {
        var vm = this;
        console.log("homeC");
        console.log();



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

          }


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