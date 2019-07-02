//password matching function

$(document).ready(function() {
    $("#pass2").keyup(validate);
        });
function validate() {
    var password = $("#pass1").val();
    var password2 = $("#pass2").val();
if(password == password2) {
    $("#validate-status").html("Match").css("color","green");}
    else {
        $("#validate-status").html("Not match").css("color","red");
      }
    }

//password field toggle
$(document).ready(
    function() {
        $("#passworField").click(function() {
            $("#changePassword").fadeToggle(1000);
            });
        });