$(document).ready(function(){
    $form = $('#request_form')
    $('input').change(function(){
        $form.ajaxSubmit();
    });
});