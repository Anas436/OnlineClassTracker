document.getElementById("btnSubmit").onclick = fromValidation;
document.getElementById("btnCancel").onclick = clearFrom;


function clearFrom() {
    document.getElementById("courseName").value = "";
    document.getElementById("courseCode").value = "";
    document.getElementById("InstName").value = "";

    document.getElementById("CourseName_Error").innerText = "";
    document.getElementById("CourseCode_Error").innerText = "";
    document.getElementById("InstName_Error").innerText = "";
}




function fromValidation() {

    let course_name = document.getElementById("courseName").value;
    let course_code = document.getElementById("courseCode").value;
    let instName = document.getElementById("InstName").value;

    if (course_name == '') {
        document.getElementById("CourseName_Error").innerText = "Please enter the course name";
        document.getElementById("CourseCode_Error").innerText = "";
        document.getElementById("InstName_Error").innerText = "";
    }
    else if (course_code == '') {
        document.getElementById("CourseCode_Error").innerText = "Please enter the course code";
        document.getElementById("CourseName_Error").innerText = "";
        document.getElementById("InstName_Error").innerText = "";

    }
    else if (instName == '') {
        document.getElementById("InstName_Error").innerText = "Please enter the Instructor Name";
        document.getElementById("CourseCode_Error").innerText = "";
        document.getElementById("CourseName_Error").innerText = "";

    }

    else {
        document.getElementById("course_form").submit();
        return false;
    }

}