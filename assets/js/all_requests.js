$(document).ready(function(){
    $form = $('#request_form')
    $("#myTable").tablesorter({
    	theme : 'blue',
    	sortReset: true,
    }); 
    $('input').change(function(){
        $form.ajaxSubmit();
        if ($(this).closest('td').prev('td').text() === "True"){
        	$(this).closest('td').prev('td').text("False");
        }
        else{
        	$(this).closest('td').prev('td').text("True");
        }
        var resort = "",
        	callback = function(table){};
        $("#myTable").trigger("updateAll", [ resort, callback ]);
    });
});