

 $(document).ready(function(){
    var question_type;
    $('#id_question_type').change(function() {
    question_type = $(this).val()
    if(question_type == 3 || question_type == 0){
        $("#chocieSection").hide();
        clearChoice()
    }
    else
        $("#chocieSection").show();
        clearChoice()
        addChoice()
        addChoice()

    });

    var radioTr = `<tr>
                     <td><input type="radio"  name="choices"></td>
                     <td><input type="text" class="form-control" name="choices_text[]"/></td>
                     <td><input type="button" class="btn btn-primary delete-btn"  value="Delete"/></td>
                  </tr>`
     var checkBoxTr = `<tr>
                     <td><input type="checkbox"  name="choices[]"></td>
                     <td><input type="text" class="form-control" name="choices_text[]" /></td>
                     <td><input type="button" class="btn btn-primary delete-btn"  value="Delete"/></td>
                  </tr>`

     $('#addrow').click(function() {
        addChoice()
    });

   choice_count = 1;
   function addChoice(){

    var $tbody, $row, additionalRows;
        $tbody = $('table tbody');
        //var choiceTr = question_type==2?radioTr:checkBoxTr;
        var choice_name = "choices_"+choice_count
        var choice_text = "choices_text_"+choice_count

        if (question_type == 2){

            choiceTr = '<tr><td><input value="'+choice_count+'" type="radio"  name="choices[]"></td>'
            choiceTr +='<td><input name="'+choice_text+'" type="text" class="form-control"/>'
            choiceTr +='<input name="choices_text" type="hidden" class="form-control" value="'+choice_count+'" /></td>'
            choiceTr +='<td><input type="button" class="btn btn-primary delete-btn"  value="Delete"/></td></tr>'

        }else{

            choiceTr = '<tr><td><input value="'+choice_count+'" type="checkbox"  name="choices[]"></td>'
            choiceTr +='<td><input name="'+choice_text+'" type="text" class="form-control"/></td>'
            choiceTr +='<input name="choices_text" type="hidden" class="form-control" value="'+choice_count+'" /></td>'
            choiceTr +='<td><input type="button" class="btn btn-primary delete-btn"  value="Delete"/></td></tr>'
        }
        choice_count++
        $tbody.append(choiceTr);

   }

   function clearChoice(){
        choice_count = 1
        $('table tbody').html("");
   }

   $("#chocieSection").on('click','.delete-btn',function(){
        var trLength = $(this).closest('tbody').find('tr').length
        if(trLength>2)
            $(this).closest('tr').remove()
        else
            $('#myModal').modal('show');
   })

});

