
let table = document.getElementById('course_table');

for (let i = 1; i < table.rows.length; i++) {

    // getting the view_button
    let view_button = document.getElementById('course_table').rows[i].cells[3].getElementsByTagName('button')[0]
    view_button.onclick = function () {
        let course_code = table.rows[i].cells[1].innerText;


        // ajax request

        var xml = new XMLHttpRequest();
        xml.open("POST", "/courseCodeAjax", true);
        xml.setRequestHeader("Content-type", "application/x-www-form-urlencoded");


        course_code_json = JSON.stringify({
            course_code: course_code,
        });

        xml.send(course_code_json);

    }
}







