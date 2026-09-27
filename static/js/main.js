(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$(".toggle-password").click(function() {

	  $(this).toggleClass("fa-eye fa-eye-slash");
	  var input = $($(this).attr("toggle"));
	  if (input.attr("type") == "password") {
	    input.attr("type", "text");
	  } else {
	    input.attr("type", "password");
	  }
	});

})(jQuery);


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function like(slug) {
    var element = document.getElementById("like-" + slug);
    var count = document.getElementById("count-" + slug);

    $.ajax({
        url: '/post/' + slug + '/like/',
        type: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
    }).then(response => {
        if (response['liked']) {
            element.className = "fa fa-heart";
            element.style.color = "orange";
            count.innerText = Number(count.innerText) + 1;
        } else {
            element.className = "fa fa-heart-o";
            element.style.color = "";
            count.innerText = Number(count.innerText) - 1;
        }
    });
}
