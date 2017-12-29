<script type="text/javascript">
function upload_img(input){
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e){
        $("#img_id").attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0])
  }
  $(".preview-bg").remove();
  $(".preview-title").remove();
}

$("#id_pictures").change(function(){
    upload_img(this);
});

$(document).on('click', '.upload', function(){
    $("#id_pictures").click();
});

// $("#id_photo").attr("required", true);
</script>