let table_to_update = document.getElementById('course_table');

for (let i = 1; i < table_to_update.rows.length; i++) {

    // getting the view_button
    let update_button = document.getElementById('course_table').rows[i].cells[4].getElementsByTagName('button')[0]
    update_button.onclick = function () {
        let course_name = table.rows[i].cells[0].innerText;
        let course_code = table.rows[i].cells[1].innerText;
        let inst_name = table.rows[i].cells[2].innerText;

        // modal from input element

        let from_name = document.getElementById("UpdatecourseName");
        let from_code = document.getElementById("Update_courseCode");
        let from_inst_name = document.getElementById("Update_InstName");

        from_name.value = course_name;
        from_code.value = course_code;
        from_inst_name.value = inst_name;


    }
}