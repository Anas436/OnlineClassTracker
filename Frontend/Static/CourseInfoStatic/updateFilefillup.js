

const buttons = document.querySelectorAll(".file-right-part button");

buttons.forEach((button) => {
    button.addEventListener("click", () => {
        const fileNameDate = button.parentNode.parentNode.querySelectorAll(".file-left-part .file-name-date");

        var filename = fileNameDate[0].innerText;
        var filedate = fileNameDate[1].innerText;


        let existing_course_name = document.getElementById("ExistingcourseName");
        let date = document.getElementById("date-input-update");


        existing_course_name.value = filename;
        date.value = filedate;


    });
});


