function redirectionToSignUpPage() {
    window.location.href = '/index';
}

function onSignIn() {
    var signInInfo = {
        'username': $('#inputUserName').val(),
        'password': $('#inputPassword').val()
    }
    
    $.ajax({
        url: '/verifySignIn',
        type: 'POST',
        data: JSON.stringify(signInInfo),
        cache: false,
        dataType: 'json',
        contentType: 'application/json',
        success: function(response){
            if(response.userInfo.length > 0) {
                if(response.userInfo[0].isActiveUser) {
                    alert(response.message);
                    localStorage.clear();
                    localStorage.setItem('emailId', signInInfo.username);
                    localStorage.setItem('isAdmin', response.userInfo[0].isAdmin);
                    window.location.href = response.redirect; 
                } else {
                    $('#inactiveUserMessage').css('display', 'block');
                }
            } else {
                $('#invalidUserMessage').css('display', 'block');
            }
            
        }, 
        error: function(err) {
            console.log(err);
        }
    });
}