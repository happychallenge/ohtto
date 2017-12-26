<script>
//********************************************
// 뉴스에 관련된 사람 추가 하기 
//********************************************
// Modal Window 뜨위기
$(".invite-person").click(function(){
    var action = $(this).attr('data-url');
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
        dataType: 'json',
        success: function(data){
            $("#person_results").show();
            $("#person_results").html(data);
        }
    });
    return false;
});

$("#person_results").on('click', 'div.child', function(){
    var person_id = this.id.split(':')[0];
    var person_name = this.id.split(':')[1];

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