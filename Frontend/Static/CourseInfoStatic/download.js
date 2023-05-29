const downloadbtn = document.querySelectorAll(".file-right-part button");

downloadbtn.forEach((button) => {
    button.addEventListener("click", () => {
        const fileNameDate = button.parentNode.parentNode.querySelectorAll(".file-left-part .file-name-date");

        var filename = fileNameDate[0].innerText;
        var filedate = fileNameDate[1].innerText;


        let download = document.getElementById("DownloadbtnSubmit");

        download.onclick = function () {

            let file_name = document.getElementById("downloadName");
            let date = document.getElementById('fileDateD')
            file_name.value = filename;
            date.value = filedate

            console.log(filename);
            console.log(filedate);

            download_form = document.getElementById("downloadForm");
            download_form.submit();
        }

    });
});


