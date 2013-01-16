

var alter = function(id) {
    return {
        alert: function (text,type) {
            $(id).html('<div class="alert fade in alert-'+type+'"><a class="close" data-dismiss="alert">x</a>'+text+'</div>');
        },
        success: function(text) {
            this.alert(text,"success");
        },
        error: function(text) {
            this.alert(text,"error");
        },
    };
};



$(document).ready(function() {

    //判断登陆态
    console.log($.cookie("user"));

    //绑定事件
    $("#login_btn").click(function() {
        console.log("login");
        $.ajax({
            url: "http://localhost:6060/login", 
            data: JSON.stringify({
                "email":$("#login_email").val(),
                "password":$("#login_password").val(),
                "remember_me":$("#remember_me").val()
            }), 
            type: "POST",
            contentType: "application/json", 
            success: function(res) { 
                console.log(res);
                if(res.ret == 0) {
                    $("#login_email").val("");
                    $("#login_password").val("");
                    alter("#login_info_placeholder").success("login success!!!");
                } else {
                    alter("#login_info_placeholder").error(res.msg);
                }
            }, 
            error: function(err, status, thrown) { 
                console.log("err");
                alter("#login_info_placeholder").error("login failed!!!");
            }
          });
    });

    $("#register_btn").click(function() {
        console.log("register");
        $.ajax({
            url: "http://localhost:6060/register", 
            data: JSON.stringify({
                    "password":$("#register_password").val(),
                    "email":$("#register_email").val()
                }),
            type: "POST",
            contentType: "application/json",
            success: function(res) {
                if(res.ret == 0) {//login success
                    $("#register_email").val("");
                    $("#register_password").val("");
                    $("#register_password_again").val("");
                    alter("#login_info_placeholder").success("register success, please login!!!");
                    $("#tab_login").tab("show");
                } else {
                    alter("#regist_info_placeholder").error(res.msg);
                }
            }, 
            error: function(err, status, thrown) { 
                console.log("err!"); 
            }
          });
    });
});

