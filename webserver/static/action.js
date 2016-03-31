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
    $("#submit-award").click(function(){
	var year = getInnerHTML("year");
	var atype = getInnerHTML("atype");
	var category = getInnerHTML("category");
        var url = 'http://104.41.144.56:8111/award-search';
	window.location.href = url + "?year="+year+"&atype="+atype+"&category="+category;
    });

    $("#submit").click(function(){
	var title = getInnerHTML("title");
	var url = 'http://104.41.144.56:8111/movie-search';
	window.location.href = url + '?title=' + title;
    });

    $("#submit-person").click(function(){
    	var name = getInnerHTML("name");
	var url = 'http://104.41.144.56:8111/person-search';
        window.location.href = url + '?name=' + name;
    });

    $("#submit-char").click(function(){
        var char_name = getInnerHTML("char_name");
        var url = 'http://104.41.144.56:8111/character-search';
        window.location.href = url + '?char_name=' + char_name;
    });

    $("#submit-username").click(function(){
        var username = getInnerHTML("username");
        var url = 'http://104.41.144.56:8111/user-search';
        window.location.href = url + '?username=' + username;
    });
});

function getInnerHTML(input){
	var value = document.getElementById(input);
	return value[value.selectedIndex].innerHTML;
}
