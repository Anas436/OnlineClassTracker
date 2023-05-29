form = document.getElementById("loginForm")

form.addEventListener("submit", function (event) {
    event.preventDefault();

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;


    if (email == '') {
        console.log(email);
        document.getElementById("error_msg").innerText = "Please enter Email";

    }
    else if (password == '') {
        console.log(password);
        document.getElementById("error_msg").innerText = "Please enter Password";
    }
    else {
        form.submit();
    }

});