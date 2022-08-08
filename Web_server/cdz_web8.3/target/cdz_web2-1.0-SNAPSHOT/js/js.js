 // $(window).load(function(){$(".loading").fadeOut()})

 var current1=[0,0,0,0];
 var current2=[0,0,0,0];
 var addr=[0.0,0.0];
 var power1=[0,0,0,0];
 var power2=[0,0,0,0];
 var times_2=["0:0","0:0","0:0","0:0"]
 var times_1=["0:0","0:0","0:0","0:0"]
 var kgv_1=0;
 var kgv_2=0;

 var electric_q_1=0;
 var electric_q_2=0;

 // var myZCloudID = "742078577931"; // 智云帐号
 // var myZCloudKey = "BwQCAQUIBwYGCAcEW1tdXlBLWlka"; // 智云密钥
 // var MAC="01:12:4B:00:1D:88:9E:FE"//充电桩节点MAC

 // var myZCloudID ; // 智云帐号
 // var myZCloudKey; // 智云密钥
 // var MAC//充电桩节点MAC

 function getUrlVars() {
     var vars = [], hash;
     var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
     for (var i = 0; i < hashes.length; i++) {
         hash = hashes[i].split('=');
         vars.push(hash[0]);
         vars[hash[0]] = hash[1];
     }
     return vars;
 }
 myZCloudID = getUrlVars()["id"];
 myZCloudKey = getUrlVars()["key"];
 MAC = getUrlVars()["MAC"];




 let rtc = new WSNRTConnect(myZCloudID, myZCloudKey); // 创建数据连接服务对象
 rtc.setServerAddr("api.zhiyun360.com:28080"); // 设置服务器地址
 rtc.connect(); // 数据推送服务连接
$(function () {
    var map = new BMap.Map("container");
    echarts_init();
    rtc.onConnect = function () { // 连接成功回调函数
        rtc.sendMessage(MAC,"{A1=?,A2=?,A3=?,A4=?,A5=?,A6=?,A7=?,V3=?}")
        $("#ConnectState").text("数据服务连接成功！");
    };
    rtc.onConnectLost = function () { // 数据服务掉线回调函数
        $("#ConnectState").text("数据服务掉线！");
    };
    rtc.onmessageArrive = function (mac, dat) { // 消息处理回调函数
        console.log(mac+" >>> "+dat);
        var voltage;
        if (mac == MAC) {
            var nowTime = new Date();
            var time = nowTime.getHours() + ":" + nowTime.getMinutes() + ":" + nowTime.getSeconds();
            for (i = 0; i < times_2.length - 1; i++) {
                times_2[i] = times_2[i + 1];
            }
            times_2[times_2.length - 1] = time;
            if (dat[0] == '{' && dat[dat.length - 1] == '}') { // 判断字符串首尾是否为{}
                dat = dat.substr(1, dat.length - 2); // 截取{}内的字符串
                var its = dat.split(','); // 以‘,’来分割字符串
                for (var x in its) { // 循环遍历
                    var t = its[x].split('='); // 以‘=’来分割字符串
                    if (t.length != 2) continue; // 满足条件时结束当前循环
                    //电压数据更新
                    if (t[0] == "A2") { // 判断参数 A0
                        voltage = parseFloat(t[1]); // 读取数据
                        $(`#voltage_v_2`).text(voltage+"V");
                        voltageValue_2.setOption({
                            series: [
                                {
                                    data: [
                                        {
                                            value: voltage,
                                            name:"电压"
                                        }
                                    ]
                                }
                            ]
                        });
                    }
                    //电流数据更新
                    if (t[0] == "A1") {
                        current = parseFloat(t[1]); // 读取电流数据
                        $(`#current_v_2`).text(current+" A");
                        for (i = 0; i < current2.length - 1; i++) {
                            current2[i] = current2[i + 1];
                        }
                        current2[current2.length - 1] = current;
                        currentValue_2.setOption({
                            xAxis: {
                                type: 'category',
                                data: [times_2[0], times_2[1], times_2[2], times_2[3]]
                            },
                            yAxis: {
                                type: 'category',
                                data: [1, 2, 3, 4]
                            },
                            series: [
                                {
                                    data: [current2[0], current2[1], current2[2], current2[3]],
                                    type: 'line',
                                    smooth: true
                                }
                            ]
                        });
                    }
                    //功率数据更新
                    if (t[0] == "A3") {
                        power = parseFloat(t[1]); // 读取功率数据
                        $(`#power_v_2`).text(power+"W");
                        for (i = 0; i < power2.length - 1; i++) {
                            power2[i] = power2[i + 1];
                        }
                        power2[power2.length - 1] = power;
                        powerValue_2.setOption({
                            series: [
                                {
                                    data: [power2[0], power2[1], power2[2], power2[3]],
                                    type: 'bar',
                                    smooth: true
                                }
                            ]
                        });
                    }
                    //获取地理位置
                    if (t[0] == "V3") {
                        addr = t[1].split("&");
                        lng = parseFloat(addr[0]);
                        lat = parseFloat(addr[1]);
                        p = new BMap.Point(lng, lat);
                        map.centerAndZoom(p, 20);     // 初始化地图,设置中心点坐标和地图级别
                    }
                    //判断开关状态
                    if (t[0] == "D1") { // 判断参数 A0
                        kgv_2=parseFloat(t[1]);
                        if(kgv_2==1){
                            // $(`#kg_2`).removeClass('switch-off').addClass('switch-on').text('已开启');
                            $(`#img3`).attr('src','images/kg_on.png');
                            $(`#img4`).attr('src','images/on.png')
                        }else if(kgv_2==0)
                        {
                            // $(`#kg_2`).removeClass('switch-on').addClass('switch-off').text('已关闭');
                            $(`#img3`).attr('src','images/kg_off.png');
                            $(`#img4`).attr('src','images/off.png')
                        }
                    }
                }
            }
        }
        if (mac == MAC.replace('01','02')) {
            var nowTime = new Date();
            var time = nowTime.getHours() + ":" + nowTime.getMinutes() + ":" + nowTime.getSeconds();
            for (i = 0; i < times_1.length - 1; i++) {
                times_1[i] = times_1[i + 1];
            }
            times_1[times_1.length - 1] = time;
            if (dat[0] == '{' && dat[dat.length - 1] == '}') { // 判断字符串首尾是否为{}
                dat = dat.substr(1, dat.length - 2); // 截取{}内的字符串
                var its = dat.split(','); // 以‘,’来分割字符串
                for (var x in its) { // 循环遍历
                    var t = its[x].split('='); // 以‘=’来分割字符串
                    if (t.length != 2) continue; // 满足条件时结束当前循环
                    //电压数据更新
                    if (t[0] == "A2") { // 判断参数 A0
                        voltage = parseFloat(t[1]); // 读取数据
                        $(`#voltage_v_1`).text(voltage+"V");
                        voltageValue_1.setOption({
                            series: [
                                {
                                    data: [
                                        {
                                            value: voltage,
                                            name:"电压"
                                        }
                                    ]
                                }
                            ]
                        });
                    }
                    //电流数据更新
                    if (t[0] == "A1") {
                        current = parseFloat(t[1]); // 读取电流数据
                        $(`#current_v_1`).text(current+" A");
                        for (i = 0; i < current1.length - 1; i++) {
                            current1[i] = current1[i + 1];
                        }
                        current1[current1.length - 1] = current;
                        currentValue_1.setOption({
                            xAxis: {
                                type: 'category',
                                data: [times_1[0], times_1[1], times_1[2], times_1[3]]
                            },
                            yAxis: {
                                type: 'category',
                                data: [1, 2, 3, 4]
                            },
                            series: [
                                {
                                    data: [current1[0], current1[1], current1[2], current1[3]],
                                    type: 'line',
                                    smooth: true
                                }
                            ]
                        });
                    }
                    //功率数据更新
                    if (t[0] == "A3") {
                        power = parseFloat(t[1]); // 读取功率数据
                        $(`#power_v_1`).text(power+"W");
                        for (i = 0; i < power1.length - 1; i++) {
                            power1[i] = power1[i + 1];
                        }
                        power1[power1.length - 1] = power;
                        powerValue_1.setOption({
                            series: [
                                {
                                    data: [power1[0], power1[1], power1[2], power1[3]],
                                    type: 'bar',
                                    smooth: true
                                }
                            ]
                        });
                    }
                    //获取地理位置
                    if (t[0] == "V3") {
                        addr = t[1].split("&");
                        lng = parseFloat(addr[0]);
                        lat = parseFloat(addr[1]);
                        p = new BMap.Point(lng, lat);
                        map.centerAndZoom(p, 20);     // 初始化地图,设置中心点坐标和地图级别
                    }
                    //判断开关状态
                    if (t[0] == "D1") { // 判断参数 A0
                        kgv_1=parseFloat(t[1]);
                        if(kgv_1==1){
                            // $(`#kg_1`).removeClass('switch-off').addClass('switch-on').text('已开启');
                            $(`#img1`).attr('src','images/kg_on.png');
                            $(`#img2`).attr('src','images/on.png')
                        }else if(kgv_1==0)
                        {
                            // $(`#kg_1`).removeClass('switch-on').addClass('switch-off').text('已关闭');
                            $(`#img1`).attr('src','images/kg_off.png');
                            $(`#img2`).attr('src','images/off.png')
                        }
                    }
                }
            }
        }
        setTimeout(fn, 10)
    }
    rtc.onmessageArrive();
})
 function echarts_init() {
     // 基于准备好的dom，初始化echarts实例
     voltageValue_1 = echarts.init(document.getElementById('voltage_1'));
     voltageValue_2 = echarts.init(document.getElementById('voltage_2'));
     currentValue_1 = echarts.init(document.getElementById("current_1"));
     currentValue_2 = echarts.init(document.getElementById("current_2"));
     powerValue_1 = echarts.init(document.getElementById("power_1"));
     powerValue_2 = echarts.init(document.getElementById("power_2"));
     powerOption_1 = {
         xAxis: {
             type: 'category',
             data: ['0:0', '0:0', '0:0', '0:0']
         },
         yAxis: {
             type: 'value'
         },
         series: [
             {
                 data: [power1[0], power1[1], power1[2], power1[3]],
                 type: 'bar'
             }
         ]
     };
     powerOption_2 = {
         xAxis: {
             type: 'category',
             data: ['0:0', '0:0', '0:0', '0:0']
         },
         yAxis: {
             type: 'value'
         },
         series: [
             {
                 data: [power2[0], power2[1], power2[2], power2[3]],
                 type: 'bar'
             }
         ]
     };
     voltageoption_1 = {
         tooltip: {
             formatter: '{a} <br/>{b} : {c}%'
         },
         series: [
             {
                 radius:'105%',
                 center:['50%','60%'],
                 type: 'gauge',
                 max:300,

                 progress: {
                     show: true
                 },
                 detail: {
                     valueAnimation: true,
                     formatter: '{value}'
                 },
                 data: [
                     {
                         value: 50,
                         name: '电压'
                     }
                 ]
             }
         ]
     };
     voltageoption_2 = {
         tooltip: {
             formatter: '{a} <br/>{b} : {c}%'
         },
         series: [
             {
                 radius:'105%',
                 center:['50%','60%'],
                 type: 'gauge',
                 max:300,

                 progress: {
                     show: true
                 },
                 detail: {
                     valueAnimation: true,
                     formatter: '{value}'
                 },
                 data: [
                     {
                         value: 50,
                         name: '电压'
                     }
                 ]
             }
         ]
     };
     currentOption_2 = {
         xAxis: {
             type: 'category',
             data: ['0:0', '0:0', '0:0', '0:0',]
         },
         yAxis: {
             type: 'value',
             max:50,
             axisLabel : {
                 formatter: '{value}',
                 textStyle: {
                     color: 'white'
                 }
             },

         },
         series: [
             {
                 data: [current2[0], current2[1], current2[2], current2[3]],
                 type: 'line',
                 smooth: true
             }
         ]
     };
     currentOption_1 = {
         xAxis: {
             type: 'category',
             data: ['0:0', '0:0', '0:0', '0:0',]
         },
         yAxis: {
             type: 'value',
             max:50,
             axisLabel : {
                 formatter: '{value}',
                 textStyle: {
                     color: 'white'
                 }
             },

         },
         series: [
             {
                 data: [current1[0], current1[1], current1[2], current1[3]],
                 type: 'line',
                 smooth: true
             }
         ]
     };
     // 使用刚指定的配置项和数据显示图表。
     powerValue_1.setOption(powerOption_1);
     powerValue_2.setOption(powerOption_2);
     voltageValue_1.setOption(voltageoption_1);
     voltageValue_2.setOption(voltageoption_2);
     currentValue_1.setOption(currentOption_1);
     currentValue_2.setOption(currentOption_2);
 }

 setTimeout(function() {$("#kg1").click(function(){
     if(kgv_1==1)
     {
         var mac=MAC.replace('01','02');
         // document.write(mac);
         rtc.sendMessage(mac, "{CD1=1,D1=?,v1=30.0}");                  // 发送关闭灯光指令
     }else{
         var mac=MAC.replace('01','02');
         // document.write(mac);
         rtc.sendMessage(mac, "{OD1=1,D1=?,v1=30.0}");                  // 发送打开灯光指令
     }
 });}, 1000);
 setTimeout(function() {$("#kg2").click(function(){
     if(kgv_2==1)
     {
         var mac=MAC;
         // document.write(mac);
         rtc.sendMessage(mac, "{CD1=1,D1=?,v1=30.0}");                  // 发送关闭灯光指令
     }else{
         var mac=MAC;
         // document.write(mac);
         rtc.sendMessage(mac, "{OD1=1,D1=?,v1=30.0}");                  // 发送打开灯光指令
     }
 });}, 1000);




 // function getUrlVars() {
 //     var vars = [], hash;
 //     var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
 //     for (var i = 0; i < hashes.length; i++) {
 //         hash = hashes[i].split('=');
 //         vars.push(hash[0]);
 //         vars[hash[0]] = hash[1];
 //     }
 //     return vars;
 // }