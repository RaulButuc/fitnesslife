angular.module('mainApp')
.controller('appController', ['$scope', 'appService',

	function($scope, appService) {		

		console.log("in contr");
		$scope.triggerSpeech = function() {
			console.log("here1");
			return appService.triggerSpeech()
				.then(function(response) {

					console.log(response);
					$scope.videoUrl = response;
				});
		}
	}
]);