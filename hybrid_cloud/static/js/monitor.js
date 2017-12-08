

$(document).ready(function(){
    var cpu_list = [];
    var mem_list = [];
    $.ajax({
        url:"/action/getserverinfo/",
        data:{
			"limit":"20",
		},
        type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
        cpu_list = data['cpu'];
        //alert(data['cpu']);
        mem_list = data['memory'];
		},
		error:function(xhr,type){
			swal("服务器出现故障，请稍后再试");
			//cpu_list = data['cpu']
            //mem_list = data['memory']
		}
	});

Highcharts.setOptions({

    global: {
        useUTC: false
    }
});

    $("#container1").highcharts({

    chart: {
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {
                // set up the updating of the chart each second
	});
                var series = this.series[0],
                    chart = this;
                setInterval(function () {
                    $.ajax({
                        url:"/action/getserverinfo/",
                        data:{
			                "limit":"1",
		                },
                        type:'POST',//action:post or get
		                dataType:'json',
		                beforeSend:function(){
			                //alert("beforeSend!");
		                },
		                success:function(data){
                        cpu_list[0] = data['cpu'][0];
                        //alert(cpu_list[0]);
		                },
		                error:function(xhr,type){
			                //swal("服务器出现故障，请稍后再试");
			                //cpu_list = data['cpu']
                            //mem_list = data['memory']
		                }
                    var x = (new Date()).getTime(), // current time
                        y = cpu_list[0];
                        series.addPoint([x, y], true, true);

                }, 10000);
            }
        }
    },
    title: {
        text: 'vCPU'
    },
    xAxis: {
        type: 'datetime',

        tickInterval: 10 * 1000
    },
    yAxis: {



        title: {
            text: 'percent'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                Highcharts.numberFormat(this.y, 2);
        }
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    credits:{
     enabled: false
    },
    series: [{
        name: 'cpu_usage',
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;

            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 10 * 1000,
                    y: 0,
                });
            }
            return data;
        }())
    }]
} );

$("#container2").highcharts({

    chart: {
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {
                // set up the updating of the chart each second

                var series = this.series[0],
                    chart = this;
                setInterval(function () {
                    $.ajax({
                        url:"/action/getserverinfo/",
                        data:{
			                "limit":"1",
		                },
                        type:'POST',//action:post or get
		                dataType:'json',
		                beforeSend:function(){
			                //alert("beforeSend!");
		                },
		                success:function(data){
                        mem_list[0] = data['memory'][0];
		                },
		                error:function(xhr,type){
			                swal("服务器出现故障，请稍后再试");
			                //cpu_list = data['cpu']
                            //mem_list = data['memory']
		                }
	                });
                    var x = (new Date()).getTime(), // current time
                        y = mem_list[0];
                    series.addPoint([x, y], true, true);
                }, 10000);
            }
        }
    },
    title: {
        text: 'memory'
    },
    xAxis: {
        type: 'datetime',

        tickInterval: 10 * 1000
    },
    yAxis: {
        title: {
            text: 'using'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#FF0000'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                Highcharts.numberFormat(this.y, 2) + 'M';

        }

    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    credits:{
     enabled: false
    },
    series: [{
        name: 'memory_usage',
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;
            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 10 * 1000,
                    y: 0,
                });
            }
            return data;
        }())
    }]
} );
})