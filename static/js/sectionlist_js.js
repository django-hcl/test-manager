
    $(function() {

    $(".edit-icon").on('click', function(e) {
        if($(this).closest('tr').hasClass('inactive_row'))
            e.preventDefault()
    })

    var delete_section_id;
    var action_name;
     var action;
    $(".glyphicon-trash").on('click', function() {
        action = "disable";
        if($(this).closest('tr').hasClass('active_row')){
            delete_section_id= $(this).closest('tr').data('section_id');
            $("#myDeleteModal").modal("show");
            action_name = "INACTIVE";
        }else{
            action_name = "ACTIVE";
        }

    });

    $(".glyphicon-check").on('click', function() {
        action = "enable";
        if($(this).closest('tr').hasClass('inactive_row')){
            delete_section_id= $(this).closest('tr').data('section_id');
            $("#myDeleteModal3").modal("show");
            action_name = "ACTIVE";
        }else{
            action_name = "INACTIVE";
        }

    });

    $("#delete_submit, #enable_submit").on('click', function() {

        $.ajax({
            url:  "section/delete/",
            type: "post",
            dataType: 'json',
            data: { 'id': delete_section_id, 'action' : action },
            success: function(datas)
            {
                    if (datas){
                      $('#message_content').text(datas);
                      $("#myDeleteModal2").modal("show");
                      }

                   var current_tr = $("#section_table tbody tr.section_"+delete_section_id);
                   if(current_tr.hasClass('active_row')){
                        current_tr.removeClass('active_row')
                        current_tr.addClass('inactive_row')
                    }
            }
        });

});
});



