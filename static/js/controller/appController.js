angular.module('mainApp')
.controller('appController', ['$scope', 'appService',

	function($scope, appService) {		

		$scope.view2 = false;
		$scope.videoUrl = "";

		$scope.triggerSpeech = function() {
			console.log("here1");
			return appService.triggerSpeech()
				.then(function(response) {
	
					$scope.videoUrl = response[0];
					$scope.song     = response[1];
					$scope.view2 = true;
				});
		}
	}
]);