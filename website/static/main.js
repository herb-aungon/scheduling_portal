var url = "http://192.168.1.69/"
var current_url = window.location.href
var data = []
var sched_url;
var initials;
$( document ).ready(function() {
    initials=document.getElementById("initials").value;
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
    $('.form-control').val("");
    history.go(0)
});


$(".view_profile").click(function () {
    var id = $(this).attr("id");
    var token = localStorage.getItem("token");
    var current = window.location.href + "/" + id;
    console.log(current);
    window.location.replace(current);
});



$("#reset2").click(function() {
    history.go(0)
});


$("#update").click(function() {

    var details = $('#_id,#initials, #first_name, #last_name')
    var json_obj = {}

    details.each(function() {
    	json_obj[this.id] = $(this).val();
    });
    var json_details= JSON.stringify( json_obj);
    console.log(json_details);

    $.ajax({
        type : "PUT",
        url : current_url,
        data: json_details,
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            console.log(result);
        },
        async: false
    });
    history.go(0)
});

$("#delete").click(function() {
    var token = localStorage.getItem("token");
    window.location.href = url + "home/" + token + "/staff_management";
    var t= url + "home/" + token + "/staff_management";
    console.log(t);

    var details = $('#_id,#initials, #first_name, #last_name')
    var json_obj = {}

    details.each(function() {
    	json_obj[this.id] = $(this).val();
    });
    var json_details= JSON.stringify( json_obj);
    console.log(json_details);

    // $.ajax({
    //     type : "DELETE",
    //     url : current_url,
    //     data: json_details,
    //     contentType: 'application/json;charset=UTF-8',
    //     success: function(result) {
    //         console.log(result);
    //     },
    //     async: false
    // });
});


$('#select_month').on('change', function() {
    $("#date_picker").show();
    var json_month = {}
    json_month["month"] = document.getElementById("select_month").value;
    var json_data= JSON.stringify( json_month);
    
    console.log(json_data);

    var token = localStorage.getItem("token");
    var init=document.getElementById("initials").value;
    var gen_url = url + "home/" + token + "/staff_management/" + init + "/create_sched"
    console.log(gen_url);

    $.ajax({
        type : "POST",
        url : gen_url,
        data: json_data,
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            console.log(result);
            json_result = JSON.parse(result);
            data_ = json_result['data'];
            console.log(data_);
	    //localStorage.setItem("data", data);
	    data = data_
        },
        async: false
    });

    //disable dropdown once selected
    $("#select_month").prop("disabled", true);
    //enable dropdown once selected
    $("#select_date").prop("disabled", false);
    $("#assignment").prop("disabled", false);

    //write response data from ajax to dropdown list
    $.each(data, function( index, value ) {
    	//console.log( index + ": " + value );
    	$('#select_date').append( new Option(index + ": " + value) );
    });


});

$('#select_date').on('change', function() {
    $("#time_from").prop("disabled", false);
    $("#time_to").prop("disabled", false);
    console.log(data);

    for (hours =1; hours < 25; hours++) {
        var time = hours + ":00";
	//console.log(time);
	$('#time_from').append( new Option(time) );
	$('#time_to').append( new Option(time) );
    }

});

$("#create_schedule").click(function() {
    var get_sched=0;
    var init=document.getElementById("initials").value;
    var full_name=document.getElementById("first_name").value + document.getElementById("last_name").value;
    var sched_raw = {}
    sched_raw["date"] = document.getElementById("select_date").value;
    sched_raw["from"] = document.getElementById("time_from").value;
    sched_raw["to"] = document.getElementById("time_to").value;
    sched_raw["initials"] = init;
    sched_raw["name"] = full_name;
    sched_raw["month"] = document.getElementById("select_month").value;
    sched_raw["assignment"] = document.getElementById("assignment").value;
    var sched= JSON.stringify(sched_raw);
    console.log(sched);

    var token = localStorage.getItem("token");
    var add_sched_url = url + "home/" + token + "/staff_management/" + init + "/create_sched"
    url_sched = url + "home/" + token + "/staff_management/" + init
    console.log(add_sched_url);

    // if (document.getElementById("time_from").value > document.getElementById("time_to").value) {
    // 	console.log("valid");
    // } else {
    // 	console.log("invalid");
    // }
    $.ajax({
        type : "PUT",
        url : add_sched_url,
        data: sched,
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            console.log(result);
        },
        async: false
    });


    console.log(url_sched);
    window.location.href = url_sched
    location.reload(); 
});


$("#reset_sched_form").click(function() {
    history.go(0)
});



$(".delete_sched").click(function() {
    var id = $(this).attr("id");
    console.log(id)
    var token = localStorage.getItem("token");
    var del_sched_url = url + "home/" + token + "/staff_management/" + initials + '/'+ id


    console.log(del_sched_url);

    $.ajax({
        type : "DELETE",
        url : del_sched_url,
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            console.log(result);
        },
        async: false
    });

    history.go(0)

});

$(".view_sched_btn").click(function() {
    var id = $(this).attr("id");
    console.log(id);
    var token = localStorage.getItem("token");
    var view_sched_url = url + "home/" + token + "/view_schedule/" + id
    console.log(view_sched_url)
    window.location.replace(view_sched_url);

});

$("#back").click(function() {
    window.history.back();
});



$('ul.nav > li').click(function(){
    $(this).children('a').toggleClass('active');
    $(this).siblings('li').children('a').removeClass('active');
});


