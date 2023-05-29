let table_for_delete = document.getElementById('course_table');
var code;
for (let i = 1; i < table_for_delete.rows.length; i++) {

    // getting the delete_button
    let delete_button = document.getElementById('course_table').rows[i].cells[5].getElementsByTagName('button')[0]
    delete_button.onclick = function () {
        code = table.rows[i].cells[1].innerText;

    }
}

let delete_modal_button = document.getElementById("DeletebtnSubmit");

delete_modal_button.onclick = function () {

    let code_input = document.getElementById("deleteCode");
    code_input.value = code;

    delete_form = document.getElementById("deleteForm");
    delete_form.submit();
}