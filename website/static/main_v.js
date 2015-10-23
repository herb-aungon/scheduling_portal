var data_post = [];
var token_id = 0;
var data = 0;
var user = 0;
var url = "http://192.168.1.69/"

$("#login").click(function() {
    var get_token = 0;
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
	    user = json_result['username'];
	},
	async: false
    });

    if(token_id){
    	console.log("valid");
    	console.log(token_id);
	// $.ajax({
	//     type : "GET",
	//     url : "months",
	//     headers: {
	// 	'X-token':token_id,
	// 	'Content-Type':'application/json'
	//     },
	//     success: function(get_result) {
	// 	//console.log(result);
	// 	json_get_result = JSON.parse(get_result);
	// 	data = json_get_result;
		
	//     },
	//     async: false
	// });
	window.location.href = url + "home" ;
    }else{
    	console.log("invalid");
	location.reload();
    }

    
}); 


