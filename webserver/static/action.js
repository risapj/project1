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
	var url = window.location.href;
      window.location.href = url + '?title=' + title;
    });
});

function getInnerHTML(input){
	var value = document.getElementById(input);
	return value[value.selectedIndex].innerHTML;
}
