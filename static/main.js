let chart1 = echarts.init(document.getElementById("main"));
let chart2 = echarts.init(document.getElementById("six"));
let chart3 = echarts.init(document.getElementById("county"));

// 選擇框
let selectCountyEl = document.querySelector("#select_county");
// 按鈕
let countyBtnEl = document.querySelector("#county_btn");
let dateEl = document.querySelector("#date");

// 監聽按鈕點擊
countyBtnEl.addEventListener("click", () => {
    drawCountyPM25(selectCountyEl.value);
});
// 監聽選擇-option
selectCountyEl.addEventListener("change", () => {
    drawCountyPM25(selectCountyEl.value);
});

window.onresize = () => {
    chart1.resize();
    chart2.resize();
    chart3.resize();
};

$(document).ready(() => {
    drawPM25();
    drawSixPM25();
    // 繪製預設第一個option
    drawCountyPM25(selectCountyEl.value);
});

function drawCountyPM25(county) {
    chart3.showLoading();
    // 顯示讀取條
    $.ajax(
        {
            url: `/county-pm25-json/${county}`,
            type: "POST",
            dataType: "json",
            // 成功的時候
            success: (data) => {
                console.log(data);
                chart3.hideLoading();
                drawChart(chart3, data, "#ff7f50");
            },
            // 失敗的時候
            error: (data) => {
                console.log(data);
                chart3.hideLoading();
                alert("取得資料失敗!");
            }
        }
    )
}

function drawSixPM25() {
    chart2.showLoading();
    // 顯示讀取條
    $.ajax(
        {
            url: "/six-pm25-json",
            type: "POST",
            dataType: "json",
            // 成功的時候
            success: (data) => {
                console.log(data);
                chart2.hideLoading();
                drawChart(chart2, data, "#008000");
            },
            // 失敗的時候
            error: (data) => {
                console.log(data);
                chart2.hideLoading();
                alert("取得資料失敗!");
            }
        }
    )
}

function drawPM25() {
    chart1.showLoading();
    // 顯示讀取條
    $.ajax(
        {
            url: "/pm25-json",
            type: "POST",
            dataType: "json",
            // 成功的時候
            success: (data) => {
                console.log(data);
                chart1.hideLoading();
                drawChart(chart1, data);
                updateHighLowData(data);
                dateEl.innerText = data["update"];
            },
            // 失敗的時候
            error: (data) => {
                console.log(data);
                chart1.hideLoading();
                alert("取得資料失敗!");
            }
        }
    )
}

function updateHighLowData(data) {
    $('#pm25_high_site').text(data['highest_data'][0]);
    $('#pm25_high_value').text(data['highest_data'][1]);
    $('#pm25_low_site').text(data['lowest_data'][0]);
    $('#pm25_low_value').text(data['lowest_data'][1]);
}

function drawChart(chart, data, color = '#191970') {
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
                itemStyle: {
                    color: color
                },
                name: 'PM2.5',
                type: 'bar',
                data: data['pm25']
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    chart.setOption(option);
}
