angular.module('mainApp')
.controller('appController', ['$scope', 'appService',

	function($scope, appService) {		

		$scope.view2 = false;
		$scope.videoUrl = "";
		
		$scope.triggerSpeech = function() {

			return appService.triggerSpeech()
				.then(function(response) {
					
					if(!response[0]) {
						
						$scope.repeatMsg = true;
					} else {

						$scope.repeatMsg = false;
						$scope.videoUrl = response[0];
						$scope.song = response[1];
						$scope.view2 = true;
						$scope.startMusic();
					}
				});
		}

		$scope.startMusic = function(songName) {

			$scope.audio = new Audio('../static/music/' + songName);
			$scope.audio.play();
		}

		$scope.goToMain = function() {

			$scope.view2 = false;
			$scope.stopSong();
		}

		$scope.stopSong = function() {
			$scope.audio.pause();
		}
	}
]);