$(document).ready(function(){
    
    $form = $('#request_form');

    $("#myTable").tablesorter({
        theme : 'blue',
        sortReset: true,
        widgets: ["zebra", "filter"],
        widgetOptions : {
            filter_columnFilters : false,
            filter_reset : 'button.reset',
        }
    });

    $('button[data-filter-column]').click(function(){
        var filters = [],
            $t = $(this),
            col = $t.data('filter-column'),
            txt = $t.data('filter-text') || $t.text();

        filters[col] = txt;
        $.tablesorter.setFilters( $('#myTable'), filters, true );
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