$(function(){
    $("#top_search").keyup(function(){
        var search = $(this).val();

        $.ajax({
            url: "/records/top_search/", 
            data: {
                'keyword': search,
            },
            dataType: 'json',
            success: function(data){
                $("#top_results").show();
                $("#top_results").html(data);
            }
        });
        return false;
    });

    $('#notifications').click(function(){
        $.ajax({
            url: "/activity/last_notifications/", 
            beforeSend: function(){
                $("#noti").addClass("open");
                $('.noti-content').html("<div style='text-align:center'><img src='/static/images/loading.gif'></div>");
            },
            success: function(data){
                data = data.trim();
                if(data != "0"){
                    $('.noti-content').html(data);
                } else {
                    $("#noti").removeClass("open");
                }
            }
        });
        return false;
    });

    function check_notifications(){
        $.ajax({
            url: "/activity/check_notifications/", 
            cache: false,
            success: function(data){
                if(data != "0"){
                    $('#notifications').addClass("new-notifications");
                    $("span.noti_count .count").text(data);
                } else {
                    $('#notifications').removeClass("new-notifications");
                }
            },
            complete: function(){
                window.setTimeout(check_notifications, 600000);
            }
        });
    };
    check_notifications();

});