angular.module('mainApp')
.directive('appDirective', ['appService',

	function(appService) {

		function _link(scope, element, attrs) {

			console.log("hereee");
			
			// var video = $('#video');
			// video[0].pause();
			// video.prop('src','');
			// video.find('source').remove();
			// video.remove();

			scope.triggerSpeech = function() {
				console.log("here1");
				return appService.triggerSpeech()
					.then(function(response) {

						console.log(response);
						scope.videoUrl = response;
					});
			}

			angular.element('.video').on('ended',
				function() {
					console.log("GONEEE");
				}
			);
		}

		return {

			restrict: 'E',
			link: _link
		}
	}
]);