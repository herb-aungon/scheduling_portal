var data_post = [];
var token_id = 0;
var data = 0;
var user = 0;
var url_1 = "http://herbportal.ddns.net/home/"

$("#login").click(function() {
    var username = $('#username').val();
    var password = $('#userpassword').val();
    data_post.push({
	username:username,
	password:password
    });
    console.log(data_post);


    $.ajax({
	type : "POST",
	url : "login",
	data: JSON.stringify(data_post, null, '\t'),
	contentType: 'application/json;charset=UTF-8',
	headers: {
            'X-token':'',
            'Content-Type':'application/json'
	},
	success: function(result) {
	    //console.log(result);
	    
	    json_result = JSON.parse(result);
	    token_id = json_result['data'];
	    user = json_result['reason'];
	    console.log(json_result);
	},
	async: false
    });

    if(token_id){
    	console.log("valid");
    	console.log(token_id);
	localStorage.setItem("token", token_id);
	localStorage.setItem("user", user);
	window.location.href = url_1 + token_id;
    }else{
    	console.log(user);
	alert(user);
	location.reload();
    }

}); 

