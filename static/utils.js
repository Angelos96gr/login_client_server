
document.addEventListener('DOMContentLoaded', function(){ // necessary when .js is imported in html otherwise elements are not found
    

    document.querySelector("[name=pwd_repeat]").onmouseleave = check_correctness;


})

function check_correctness(){
    if ( document.getElementsByName("pwd")[0].value != document.getElementsByName("pwd_repeat")[0].value){
        document.getElementsByName("pwd_repeat")[0].value = "" //removes second pwd if incorrect when the user moves their mouse
    }

}


document.querySelector('form').addEventListener('submit', (e) => {
    e.preventDefault();
    documennt.querySelector('message').innerText = "Signup successful"

})