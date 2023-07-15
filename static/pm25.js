
    var myChart = echarts.init(document.getElementById('main'));
    $(document).ready(() => {
        draw();
    });

    function draw() {
        myChart.showLoading();
        // 顯示讀取條
        $.ajax(
            {
                url: "/pm25-json",
                type: "POST",
                dataType: "json",
                // 成功的時候
                success: (data) => {
                    console.log(data);
                    myChart.hideLoading();
                    drawPM25(data);
                    updateHighLowData(data);
                    //drawPM25_2(data);
                },
                // 失敗的時候
                error: (data) => {
                    console.log(data);
                    myChart.hideLoading();
                    alert("取得資料失敗!");
                }
            }
        )
    }

    function updateHighLowData(data){
        $("#pm25_high_site").text(data["highest_data"][0]);
        $("#pm25_high_value").text(data["highest_data"][1]);
        $("#pm25_low_site").text(data["lowest_data"][0]);
        $("#pm25_low_value").text(data["lowest_data"][1]);
    }



    function drawPM25_2(value) {
        var option;
        // prettier-ignore
        let dataAxis = value['sites']
        // prettier-ignore
        let data = value['pm25']
        let yMax = 500;
        let dataShadow = [];
        for (let i = 0; i < data.length; i++) {
            dataShadow.push(yMax);
        }
        option = {
            title: {
                text: '特性示例：渐变色 阴影 点击缩放',
                subtext: 'Feature Sample: Gradient Color, Shadow, Click Zoom'
            },
            xAxis: {
                data: dataAxis,
                axisLabel: {
                    inside: true,
                    color: '#000'
                },
                axisTick: {
                    show: false
                },
                axisLine: {
                    show: false
                },
                z: 10
            },
            yAxis: {
                axisLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLabel: {
                    color: '#999'
                }
            },
                dataZoom: [
                    {
                        type: 'inside'
                    }
                ],
                series: [
                    {
                        type: 'bar',
                        showBackground: true,
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                { offset: 0, color: '#2e8b57' },
                                { offset: 0.5, color: '#696969' },
                                { offset: 1, color: '#fafad2' }
                            ])
                        },
                        emphasis: {
                            itemStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    { offset: 0, color: '#2378f7' },
                                    { offset: 0.7, color: '#2378f7' },
                                    { offset: 1, color: '#83bff6' }
                                ])
                            }
                        },
                        data: data
                    }
                ]
            };
            // Enable data zoom when user click bar.
            const zoomSize = 6;
            myChart.on('click', function (params) {
                console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
                myChart.dispatchAction({
                    type: 'dataZoom',
                    startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
                    endValue:
                        dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
                });
            });

            option && myChart.setOption(option);
        }

        function drawPM25(data) {
            // 指定图表的配置项和数据
            var option = {
                title: {
                    text: ''
                },
                tooltip: {},
                legend: {
                    data: ['PM2.5']
                },
                xAxis: {
                    data: data['sites']
                },
                yAxis: {},
                series: [
                    {
                        name: 'PM2.5',
                        type: 'bar',
                        data: data['pm25']
                    }
                ]
            };

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        }

