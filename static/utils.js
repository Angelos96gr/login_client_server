

const singup_btn = document.querySelector("[name=signup]");
const pwd =  document.querySelector("[name=pwd]");
const pwd_repeat = document.querySelector("[name=pwd_repeat]");
const incorrect_pwd_msg = document.querySelector("[id=incorrect_pwd]")



document.addEventListener('DOMContentLoaded', function () { // necessary when .js is imported at top of the html otherwise elements are not found


    singup_btn.onclick = check_pwd_correctness;
    pwd.onchange = refresh_entries;
    pwd_repeat.onchange = refresh_entries;



})


function refresh_entries(){

    incorrect_pwd_msg.textContent = ""
}


function check_pwd_correctness() {
    if (pwd.value != pwd_repeat.value) {
        pwd_repeat.value = "" //removes second pwd if pwds dont match
        incorrect_pwd_msg.textContent = "Passwords do not match"
    }
    else {

        incorrect_pwd_msg.textContent = ""

    }

}



