(function () {
    'use strict';

    angular
        .module('vpwd', [])
        .directive('verifyPassword', verifyPassword);

    //Verifies if two passwords are equal.
    function verifyPassword() {
        return {
            restrict: 'A',
            require: 'ngModel',
            link: function (scope, elem, attrs, ctrl) {
                var firstPassword = '#' + attrs.verifyPassword;
                $(elem).add(firstPassword).on('keyup', function () {
                    scope.$apply(function () {
                        ctrl.$setValidity('pwmatch', elem.val() === $(firstPassword).val());
                    });
                });
            }
        }
    }
})();