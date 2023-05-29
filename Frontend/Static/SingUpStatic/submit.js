form = document.getElementById("registerForm")

function isValidEmail(email_address) {
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email_address);
}

function isPasswordStrong(password_arg) {
    // Check length of password
    if (password_arg.length < 8) {
        return false;
    }
    // Check for presence of lowercase letter, uppercase letter, digit, and special character
    var regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@#!%*?&])[A-Za-z\d$@#!%*?&]+$/;
    if (!password_arg.match(regex)) {
        return false;
    }
    // All criteria met, password is strong
    return true;
}

form.addEventListener("submit", function (event) {
    event.preventDefault();

    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let cpassword = document.getElementById("cpassword").value;


    if (email == '') {
        document.getElementById("error").innerText = "Please enter Email";

    }
    else if (password == '') {
        document.getElementById("error").innerText = "Please enter Password";

    }
    else if (cpassword == '') {
        document.getElementById("error").innerText = "Please Confirm your Password";

    }
    else if (!isPasswordStrong(password)) {
        document.getElementById("error").innerText = "Password must contain lowercase letter, uppercase letter, digit, and special character";
    }
    else if (password != cpassword) {
        document.getElementById("error").innerText = "password don't match";
    }
    else {
        form.submit();
    }

});