$(document).ready(function(){

	$("#addDAG").on("click",function()
	{
		$("#DAGtablebody").append("<tr><td><div class=\"input-group\"><input type=\"text\" class=\"form-control"+
		"\"id=\"parent\"><span class=\"input-group-addon\"></span></div></td><td><div class=\"input-group\">"+
        "<input type=\"text\" class=\"form-control\" id=\"successor\"><span class=\"input-group-addon\"></span>"+
        "</div></td></tr>");
	});

	$("#addLOAD").on("click",function()
	{
		$("#LOADtablebody").append("<tr><td><div class=\"input-group\"><input type=\"text\" class=\"form-control"+
		"\"id=\"parent\"><span class=\"input-group-addon\"></span></div></td><td><div class=\"input-group\">"+
        "<input type=\"text\" class=\"form-control\" id=\"successor\"><span class=\"input-group-addon\"></span>"+
        "</div></td></tr>");

	});

	$("#ensure").on("click",function()
	{
	    var dag = "";
	    var dagList = $("#DAGtablebody").children("tr")
        for (var i=0;i<dagList.length;i++) {
            var tdArr = dagList.eq(i).find("td");
            dag = dag + tdArr.eq(0).find("input").val();
            dag = dag + ":";
            dag = dag + tdArr.eq(1).find("input").val();
            dag = dag + " ";
        }
	    var load = "";
	    $("#LOADtablebody").find("tr").each(function(){
            var tdArr = $(this).children();
            load= load+tdArr.eq(0).find("input").val();
            load= load+":";
            load= load+tdArr.eq(1).find("input").val();
            load= load+" ";
        });

	    var deadline = $("#taskdeadline").val();
	    var datasize = $("#datasize").val();
	    Trans(dag,load,deadline,datasize);

	});

})

function Trans(dag,load,deadline,datasize)
{
	//alert("Trans!\n");
	$.ajax({
		url:"/action/appAction/",
		//async: false, //if we want to lock the screen
		data:{
			"dag":dag,
			"load":load,
			"deadline":deadline,
			"datasize":datasize,
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function()
		{
			//alert("beforeSend!");
		},
		success:function(data)
		{
			//do something here
			$.each(data,function(name,value){
				if("Aliyun" == name){
				    ins_num=JSON.stringify(value);
				    sche_resu="scheduler result:\n cloud provider:Aliyun\n instance:"+ins_num;

				    swal(sche_resu);
				}
			}
			);
//			window.location.href = "/dag/";
		},
		error:function(xhr,type){
			swal("failed");
		}
	});
}