// Get a coocki provided the name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function resetAlert() {
    $("#repeat-password").removeClass("is-invalid");
    $("#alert-message").removeClass("wrong");
    $("#alert-message").removeClass("ok");
    $("#alert-message").text("");
}

function setAlert(message, ok) {
    $("#alert-message").addClass(ok?'ok':'wrong');
    $("#alert-message").text(message);
}