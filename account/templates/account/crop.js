<script>

$(function(){
// SCRIPT TO OPEN the MODAL With the Preview
    $('#id_picture').change(function() {
        if(this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#image').attr('src', e.target.result);
                $('#modalCrop').modal("show");
            }
            reader.readAsDataURL(this.files[0]);
        }
        
    });

    // SCRIPTS TO HANDLE THE CROPPER BOX
    var $image = $('#image');
    var cropBoxData;
    var canvasData;

    $('#modalCrop').on('shown.bs.modal', function(){
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1/1,
            minCropBoxWidth: 200,
            minCropBoxHeight: 200,
            ready: function(){
                $image.cropper('setCanvasData', canvasData);
                $image.cropper('setCropBoxData', cropBoxData);
            }
        });
    }).on('hidden.bs.modal', function(){
        cropBoxData = $image.cropper('getCropBoxData');
        canvasData = $image.cropper('getCanvasData');
        $image.cropper('destory');
    });

    $(".js-zoom-in").click(function(){
        $image.cropper('zoom', 0.1);
    })
    $(".js-zoom-out").click(function(){
        $image.cropper('zoom', -0.1);
    });

    // SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER
    $('.btn-crop').click(function(){
        var cropData = $image.cropper('getData');
        $('#id_x').val(cropData['x']);
        $('#id_y').val(cropData['y']);
        $('#id_height').val(cropData['height']);
        $('#id_width').val(cropData['width']);
        $("#formProfile").submit();
    });
});


// Add Theme 
var loadForm = function(){
    var btn = $(this);
    $.ajax({
        url : btn.attr('data-url'), // data-url : /blog/theme_add/
        type : 'get',
        dataType : 'json',
        beforeSend: function(){
            $('#modal-theme').modal('show');
        },
        success: function(data) {
            $('#modal-theme .modal-content').html(data.html_form)
        }
    });
}

var saveForm = function(){
    var form = $(this);
    $.ajax({
        url: form.attr("action"),
        data : form.serialize(),
        type : form.attr('method'),
        dataType : 'json',

        success : function(data) {
            if (data.status) {
                console.log("Success");
                $('#modal-theme').modal('hide');
            } else {
                $('#modal-theme .modal-content').html(data.html_form);
            }
        },
        complete: function(data){
            window.location.reload(true);
            console.log("Complete");
        },
    });
    return false;
}

$('.btn-add-theme').click(loadForm);
$('#modal-theme').on("submit", ".add-theme-form", saveForm);

// $(".theme_list").on("click", ".update-theme", loadForm);
// $("#modal-theme").on("submit", ".update-theme-form", saveForm);

// PERSON
$("#modal-theme").on("keyup", "#id_person", function(){
    var search = $(this).val();

    $.ajax({
        url: "{% url 'blog:search_persons' %}", 
        data: {
            'keyword': search,
        },
        success: function(data){
            $("#person_results").show();
            $("#person_results").html(data);
        }
    });
    return false;
});

$("#modal-theme").on('click', '#person_results div.child', function(){
    var person = $(this);
    var dataurl = person.attr("data-url");
    var person_id = dataurl.split(':')[0];
    var person_name = dataurl.split(':')[1];

    $("#id_person").val("").focus();
    $('<input>').attr({
        type: 'text',
        id: 'id_person_name',
        value: person_name
    }).appendTo('#persons_name');

    $('<input>').attr({
        type: 'checkbox',
        id: 'id_person_id',
        name: 'persons_id',
        value: person_id,
        checked: 'checked'
    }).appendTo('#persons_id');

    $("#person_results").hide();
});

$('#id_nickname').bind('input', function() { 
    $("#btn-profile").show();
});
</script>