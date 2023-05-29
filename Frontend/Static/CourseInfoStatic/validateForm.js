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

    // Validate course name field
    if (courseName.trim() === '') {
        courseNameError.textContent = 'Please enter a file name';
        return;
    }

    // Validate date input field
    if (dateInput.trim() === '') {
        dateInputError.textContent = 'Please select a date';
        return;
    }

    // Validate instructor name field
    if (instName.trim() === '') {
        instNameError.textContent = 'Please upload a file';
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

    // Reset error messages
    document.getElementById("Update_CourseName_Error").textContent = "";
    document.getElementById("date-input-update-Error").textContent = "";
    document.getElementById("UpdateInstName_Error").textContent = "";

    // Validate course name
    if (courseName.trim() === "") {
        document.getElementById("Update_CourseName_Error").textContent =
            "Please enter a file name.";
        isValid = false;
    }

    // Validate date input
    if (dateInput.trim() === "") {
        document.getElementById("date-input-update-Error").textContent =
            "Please select a date.";
        isValid = false;
    }

    // Validate instructor name
    if (instName.trim() === "") {
        document.getElementById("UpdateInstName_Error").textContent =
            "Please upload a file.";
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



