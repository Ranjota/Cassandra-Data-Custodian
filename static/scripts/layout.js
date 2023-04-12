function redirectToHomePage() {
    if(localStorage.getItem('isAdmin') == "true"){
        window.location.href = '/admintableList';
    } else {
        window.location.href = '/tableList';
    } 
}

$(document).ready(function(){
    if(localStorage.getItem('isAdmin') == "true"){
        $('#sidebar').css('display', 'block');
    }
});
