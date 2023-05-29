const deletedbtn = document.querySelectorAll(".file-right-part button");

deletedbtn.forEach((button) => {
    button.addEventListener("click", () => {
        const fileNameDate = button.parentNode.parentNode.querySelectorAll(".file-left-part .file-name-date");

        var filename = fileNameDate[0].innerText;
        var filedate = fileNameDate[1].innerText;


        var deletebtnSubmit = document.getElementById("DeletebtnSubmit");

        deletebtnSubmit.onclick = function () {

            let file_name = document.getElementById("deleteName");
            let date = document.getElementById('fileDateDelete')
            file_name.value = filename;
            date.value = filedate


            delete_form = document.getElementById("deleteForm");
            delete_form.submit();
        }

    });
});