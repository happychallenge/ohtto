<script type="text/javascript">
$(document).on("click", ".btnMapMarker", function(){

    var photo_id = $(this).attr('data-url');
    animateMarker(photo_id);
});

function animateMarker(photo_id){
    for (var i = 0; i < markers.length; i++) {
        if(markers[i].id == photo_id){
            markers[i].setAnimation(google.maps.Animation.BOUNCE);
            map.setZoom(15);
            map.setCenter(markers[i].position);
        }
    }
}

// Like and Cancel
$(document).on('click', '.like', function(){
  var pk = $(this).attr('data-url');
  console.log('PK : ' + pk);

  $.ajax({
    type: 'POST',
    url: "{% url 'blog:post_like' %}",
    data: {'pk': pk, 'csrfmiddlewaretoken': '{{csrf_token}}' },
    dataType: 'json',

    // response expression from Server 
    // { 'like_count': post.like_count, 'message': message }
    success: function(response){
      $("#lcount-"+pk).html(response.like_count);
    },

    error: function(request, status, error) {
        console.log(error);
        // alert("Have to login");
        // window.location.replace("/accounts/login/");
    },
  });
});

// Bucket
$(document).on('click', '.bucket', function(){
  var pk = $(this).attr('data-url');
  console.log('PK : ' + pk);

  $.ajax({
    type: 'POST',
    url: "{% url 'blog:post_bucket' %}",
    data: {'pk': pk, 'csrfmiddlewaretoken': '{{csrf_token}}' },
    dataType: 'json',

    // response expression from Server 
    // { 'like_count': post.like_count, 'message': message }
    success: function(response){
      alert(response.message);
      $("#bcount-"+pk).html(response.bucket_count);
    },

    error: function(request, status, error) {
        console.log(error);
        // alert("Have to login");
        // window.location.replace("/accounts/login/");
    },
  });
});

// .comment 버턴을 누르면 하단에 커멘트가 리스트로 나옴
$(document).on("click", ".comment", function(){

    var post = $(this).closest(".ibox");

    if ($(".comment_list", post).hasClass("tracking")) {
        $(".comment_list", post).slideUp();
        $(".comment_list", post).removeClass("tracking");

    } else {
        $(".comment_list", post).show();
        $(".comment_list", post).addClass("tracking");
        $(".comment_list input[name='content']", post).focus();

        var post_id = $(post).attr('post-id');
        // var post_id = 12;
        $.ajax({
            url: "{% url 'comment:post_comment' %}", 
            data: {'post_id': post_id },
            cache: false,
            beforeSend: function(){
                $("div.comment_list", post).html("<img src='/static/images/loading.gif'");
            },
            success: function(data){
                $("div.comment_list", post).html(data);
                $(".comment-count", post).text($(".commentCount", post).length)
            },
        });
        return false;
    }
});

// .comment 입력하고 Enter 키를 누르면 Comment가 입력이 됨
$(document).on("keydown", ".comment_list textarea[name='comment']", function(evt){

    var keyCode = evt.which?evt.which:evt.keyCode;
    var post = $(this).closest(".ibox");

    if (keyCode == 13) {
        var form = $(this).closest("form");
        var container = $(this).closest(".comment_list")
        var input = $(this);

        $.ajax({
            url: "{% url 'comment:post_comment' %}", 
            data: $(form).serialize(),
            type: "POST",
            cache: false,
            beforeSend: function(){
                $(input).val("");
            },
            success: function(data){
                $("div.comment_list", post).html(data);
                $(".comment-count", post).text($(".commentCount", post).length)
            },
        });
        return false;
    } 
});

</script>