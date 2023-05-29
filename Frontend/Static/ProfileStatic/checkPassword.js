document.getElementById("btnPasswordSubmit").onclick = passValidation;
document.getElementById("btnCancelPassword").onclick = clearFrom;


function clearFrom() {
    document.getElementById("current_pass").value = "";
    document.getElementById("new_pass").value = "";
    document.getElementById("confirm_pass").value = "";

    document.getElementById("current_pass_Error").innerText = "";
    document.getElementById("new_pass_Error").innerText = "";
    document.getElementById("confirm_pass_Error").innerText = "";
}

function passValidation() {

    let current_pass = document.getElementById("current_pass").value;
    let new_pass = document.getElementById("new_pass").value;
    let confirm_pass = document.getElementById("confirm_pass").value;

    if (current_pass == '') {
        document.getElementById("current_pass_Error").innerText = "Please enter current password";
        document.getElementById("new_pass_Error").innerText = "";
        document.getElementById("confirm_pass_Error").innerText = "";
    }
    else if (new_pass == '') {
        document.getElementById("new_pass_Error").innerText = "Please enter new password";
        document.getElementById("current_pass_Error").innerText = "";
        document.getElementById("confirm_pass_Error").innerText = "";

    }
    else if (confirm_pass == '') {
        document.getElementById("confirm_pass_Error").innerText = "Please confirm new password";
        document.getElementById("new_pass_Error").innerText = "";
        document.getElementById("current_pass_Error").innerText = "";

    }
    else if (new_pass != confirm_pass) {
        document.getElementById("confirm_pass_Error").innerText = "Password does not match!";
        document.getElementById("new_pass_Error").innerText = "";
        document.getElementById("current_pass_Error").innerText = "";
    }

    else if (new_pass == current_pass) {
        document.getElementById("confirm_pass_Error").innerText = "";
        document.getElementById("new_pass_Error").innerText = "Old password cannot be updated.";
        document.getElementById("current_pass_Error").innerText = "";
    }

    else {
        document.getElementById("password_form").submit();
        return false;
    }

}