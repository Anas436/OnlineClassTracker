document.getElementById('btnSubmit').addEventListener('click', function () {
    var courseName = document.getElementById('courseName').value;
    var dateInput = document.getElementById('date-input').value;
    var instName = document.getElementById('InstName').value;

    var courseNameError = document.getElementById('CourseName_Error');
    var dateInputError = document.getElementById('DateInput_Error');
    var instNameError = document.getElementById('InstName_Error');

    // Reset error messages
    courseNameError.textContent = '';
    dateInputError.textContent = '';
    instNameError.textContent = '';

    // url find pattern
    var urlPattern = /^https?:\/\/drive\.google\.com\/(?:file\/d\/|open\?id=)([a-zA-Z0-9_-]{28,})/;

    // Validate course name field
    if (courseName.trim() === '') {
        courseNameError.textContent = 'Please enter a Recording name';
        return;
    }

    // Validate date input field
    if (dateInput.trim() === '') {
        dateInputError.textContent = 'Please select a date';
        return;
    }

    // Validate instructor name field
    if (instName.trim() === '') {
        instNameError.textContent = 'Please enter google drive link';
        return;
    }

    if (urlPattern.test(instName) === false) {
        instNameError.textContent = 'Please enter valid link';
        return;
    }

    // All fields are valid, submit the form
    document.getElementById('course_form').submit();
});

function clearFieldsAdd() {
    document.getElementById("courseName").value = "";
    document.getElementById("date-input").value = "";
    document.getElementById("InstName").value = "";
    document.getElementById("CourseName_Error").textContent = "";
    document.getElementById("DateInput_Error").textContent = "";
    document.getElementById("InstName_Error").textContent = "";
}


function validateUpdateCourseForm() {
    var courseName = document.getElementById("UpdatecourseName").value;
    var dateInput = document.getElementById("date-input-update").value;
    var instName = document.getElementById("InstNameUpdate").value;
    var isValid = true;

    var urlPattern = /^https?:\/\/drive\.google\.com\/(?:file\/d\/|open\?id=)([a-zA-Z0-9_-]{28,})/;

    // Reset error messages
    document.getElementById("Update_CourseName_Error").textContent = "";
    document.getElementById("date-input-update-Error").textContent = "";
    document.getElementById("UpdateInstName_Error").textContent = "";

    // Validate course name
    if (courseName.trim() === "") {
        document.getElementById("Update_CourseName_Error").textContent =
            "Please enter a recording name.";
        isValid = false;
    }

    // Validate date input
    if (dateInput.trim() === "") {
        document.getElementById("date-input-update-Error").textContent =
            "Please select a date.";
        isValid = false;
    }

    // Validate url 
    if (instName.trim() === "") {
        document.getElementById("UpdateInstName_Error").textContent =
            "Please enter google drive link.";
        isValid = false;
    }

    if (urlPattern.test(instName) === false) {
        document.getElementById("UpdateInstName_Error").textContent =
            "Please enter google drive link.";
        isValid = false;
    }

    return isValid;
}

// Clear form fields
function clearFields() {
    document.getElementById("UpdatecourseName").value = "";
    document.getElementById("date-input-update").value = "";
    document.getElementById("InstNameUpdate").value = "";
    document.getElementById("Update_CourseName_Error").textContent = "";
    document.getElementById("date-input-update-Error").textContent = "";
    document.getElementById("UpdateInstName_Error").textContent = "";
}

document.getElementById("UpdatebtnSubmit").addEventListener("click", function () {
    if (validateUpdateCourseForm()) {
        document.getElementById("update_course_form").submit();
    }
});



