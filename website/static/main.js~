var url = "http://192.168.1.69/"


$( document ).ready(function() {
    if(localStorage.getItem("user")){
    var elem = document.getElementById("logout");
    elem.value = "Logout: " + localStorage.getItem("user");
    }
});


$("#logout").click(function() {
    window.location.href = url + "login";
    data_post.push({
        id: localStorage.getItem("token"),
    });

    $.ajax({
        type : "DELETE",
        url : url + "logout",
        data: JSON.stringify(data_post, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        headers: {
            'X-token':'',
            'Content-Type':'application/json'
        },
        success: function(result) {
            console.log(result);
        },
        async: false
    });

    localStorage.removeItem("user");
    localStorage.removeItem("token");

});


$("#staff").click(function() {
    var token = localStorage.getItem("token");
    window.location.href = url + "home/" + token + "/staff_management";
});

$("#home").click(function() {
    var token = localStorage.getItem("token");
    window.location.href = url + "home/" + token;
});


$("#reset").click(function() {
$('.form-control').val("");
});


$("#input_submit").click(function() {

    var details = $('#initials, #first_name, #last_name')
    var json_obj = {}

    details.each(function() {
    	json_obj[this.id] = $(this).val();
    });
    var json_details= JSON.stringify( json_obj);
    console.log(json_details);
    var token = localStorage.getItem("token");

    $.ajax({
        type : "POST",
        url : url + "home/" + token + "/staff_management",
        data: json_details,
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            console.log(result);
        },
        async: false
    });
    history.go(0)
    $('.form-control').val("");
});

$(".view_profile").click(function () {
    var id = $(this).attr("id");
    var token = localStorage.getItem("token");
    var current = window.location.href + "/" + id;
    console.log(current);
    window.location.replace(current);
});


$(".view_t").click(function () {
    var id = $(this).attr("id");
    var token = localStorage.getItem("token");
    var current = window.location.href + "/" + id;
    console.log(current);
    window.location.replace(current);
});
