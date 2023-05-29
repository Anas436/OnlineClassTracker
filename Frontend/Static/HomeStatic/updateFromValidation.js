document.getElementById("UpdatebtnSubmit").onclick = UpdatefromValidation;








function UpdatefromValidation() {

    let course_name = document.getElementById("UpdatecourseName").value;
    let instName = document.getElementById("Update_InstName").value;

    if (course_name == '') {
        document.getElementById("Update_CourseName_Error").innerText = "Please enter the course name";
        document.getElementById("Update_CourseCode_Error").innerText = "";
        document.getElementById("UpdateInstName_Error").innerText = "";
    }
    else if (instName == '') {
        document.getElementById("UpdateInstName_Error").innerText = "Please enter the Instructor Name";
        document.getElementById("Update_CourseName_Error").innerText = "";
        document.getElementById("Update_CourseCode_Error").innerText = "";

    }

    else {
        document.getElementById("update_course_form").submit();
        return false;
    }

}


function clearFields() {
    document.getElementById("Update_CourseName_Error").innerText = "";
    document.getElementById("UpdateInstName_Error").innerText = "";
}