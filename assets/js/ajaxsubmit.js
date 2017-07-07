function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#images').attr('src', e.target.result).attr('width', 200).attr('height', 200);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

function display_form_errors(errors, $form) {
    for (var k in errors) {
        for (var i = 0; i < errors[k].length; i++){
            $form.find('input[id= id_' + k + ']').after('<div class="errors">' + errors[k][i] + '</div>');
            $form.find('textarea[id= id_' + k + ']').after('<div class="errors">' + errors[k][i] + '</div>');
        }
    }
}

function disable_form($form) {
    $form.find('input').prop('disabled', true);
    $form.find('textarea').prop('disabled', true);
}

function enable_form($form) {
    $('input').prop('disabled', false);
    $('textarea').prop('disabled', false);
}

$(function(){
    $("#progress").hide();
    $("#id_photo").change(function(){
        readURL(this);
    });
    var options = {
        beforeSend: function()
        {
            $("#progress").show();
            $("#bar").width('0%');
            $("#message").html("").hide();
            $("#percent").html("0%");
        },
        uploadProgress: function(event, position, total, percentComplete, $form)
        {
            $("#bar").width(percentComplete+'%');
            $("#percent").html(percentComplete+'%');

        },
        beforeSubmit: function(arr, $form, options) {
            disable_form($form);
        },
        success: function(data, statusText, xhr, $form)
        {
            $("#bar").width('100%');
            $("#percent").html('100%');
            $form.find('.errors').remove();
            if (data['result'] == 'success') {
                $("#message").css('color', '#98FB98');
                $('#photodiv a').text(data['picture']).attr('href', data['pict_url']);
                $('#contactform #id_photo').clearFields();
            }
            else if (data['result'] == 'error') {
                $("#message").css('color', '#F0E68C');
                display_form_errors(data['response'], $form);
            }
            enable_form($form);
            $("#progress").fadeOut();
            $("#message").append(data['result']).fadeIn();
        },
        dataType: 'json'
    };
    $("#contactform").ajaxForm(options);
});