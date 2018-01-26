<script>
//********************************************
// 뉴스에 관련된 사람 추가 하기 
//********************************************
// Modal Window 뜨위기
$(document).on('click', '.invite-person', function(){

    var action = $(this).attr('data-url'); // data-url : /blog/invite_persons/6/
    $("#modal-inviteperson").modal("show");
    $("#form_inviteperson").attr("action", action);
});

// PERSON
$("#id_person").keyup(function(){
    var search = $(this).val();
    $.ajax({
        url: "{% url 'blog:search_persons' %}", 
        data: {
            'keyword': search,
        },
        dataType: 'html',
        success: function(data){
            console.log(data);
            $("#id_person_results").show();
            $("#id_person_results").html(data);
        }
    });
    return false;
});

$("#id_person_results").on('click', 'div.child', function(){
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
</script>