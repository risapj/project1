$(document).ready(function() {
	$(".btn-primary").click(function(){
        //$(".Dominos").collapse('toggle');
        var elements = $(this).parent().parent().next();
        while(elements.attr('class') === 'review'){
        trigger(elements);
        elements = elements.next();
        }
    });

// switch the status of display
function trigger(element) {
    if (element.css('display') !== 'none') {
      element.hide();
    } else {
      element.show();
    }
  }


    $("#submit").click(function(){
    	var title = getInnerHTML("title");
	var url = 'http://13.82.29.208:8111/movie-search';
      window.location.href = url + '?title=' + title;
    });
});

function getInnerHTML(input){
	var value = document.getElementById(input);
	return value[value.selectedIndex].innerHTML;
}
