$(document).ready(function(){
	var cpu = 0;
	var memory = 0;
	var disk = 0;
	var security = 0;
	var private = 0;

	$("#start").on("click",function()
	{
		$("#myModal").modal('show');
	});

	$("#createinstance").on("click",function()
	{


	});

})

function Choose(t) {

    }
function start_create()
{

	$.ajax({
		url:"/action/createAdvanceAction/",
		//async: false, //if we want to lock the screen
		data:{
			"small_num": arguments[0],
			"medium_num": arguments[1],
			"large_num": arguments[2],
			"time":arguments[3],
    		"is_private": arguments[4]
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			$.each(data,function(name,value){
				if("limits" == name){
				    swal(value);
				}
			}
			);
		},
		error:function(xhr,type){
			swal("服务器出现故障，请稍后再试");
		}
	});
}