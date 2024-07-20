
document.addEventListener('DOMContentLoaded', function () { // necessary when .js is imported in html otherwise elements are not found

    document.querySelector("[name=signup]").onclick = check_pwd_correctness;
    document.querySelector("[name=pwd]").onchange = refresh_entries;
    document.querySelector("[name=pwd_repeat]").onchange = refresh_entries;



})

function refresh_entries(){

    document.querySelector("[id=incorrect_pwd").textContent = ""
}


function check_pwd_correctness() {
    if (document.getElementsByName("pwd")[0].value != document.getElementsByName("pwd_repeat")[0].value) {
        document.getElementsByName("pwd_repeat")[0].value = "" //removes second pwd if pwds dont match
        document.querySelector("[id=incorrect_pwd").textContent = "Passwords do not match"
    }
    else {

        document.querySelector("[id=incorrect_pwd").textContent = ""

    }

}



