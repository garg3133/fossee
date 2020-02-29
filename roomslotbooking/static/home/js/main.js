// Login Modal

var login_modal = document.getElementById('login-modal');
var signup_modal = document.getElementById('signup-modal');

window.onclick = function(event) {
    if (event.target == login_modal) {
        login_modal.style.display = "none";
    }
    else if(event.target == signup_modal){
        signup_modal.style.display = "none";
    }
}

function show_login_modal(){
    signup_modal.style.display = "none";
    login_modal.style.display = "flex";
}

function show_signup_modal(){
    login_modal.style.display = "none";
    signup_modal.style.display = "flex";
}