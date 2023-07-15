from flask import Flask, render_template, request
from datetime import datetime
from crawler.stock import get_stock
from crawler.lottory import get_lottory
from crawler.pm25 import get_pm25, get_six_pm25, get_county_pm25, get_countys
import json

app = Flask(__name__)


@app.route("/bmi/height=<h>&weight=<w>")
def get_bmi(h, w):
    try:
        bmi = round(eval(w) / (eval(h) / 100) ** 2, 2)
        print(bmi)
        return f"BMI:{bmi}"
    except Exception as e:
        print(e)
        return "資料有誤!"


@app.route("/book/<int:id>")
def book(id):
    books = {1: "Python", 2: "Java", 3: "C++"}
    try:
        return books[id]
    except Exception as e:
        print(e)
        return "沒有書籍資料"


@app.route("/today")
def today():
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"<h1>{datetime.now()}</h1>"


@app.route("/index")
@app.route("/")
def index():
    name = "jerry"
    date = get_today()
    content = {"name": name, "date": date}
    return render_template("index.html", content=content)


def get_today():
    date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return date


@app.route("/pm25-json-table")
def get_pm25_json_table():
    columns, values = get_pm25()

    # 新增要求日期跟目前站點數量
    json_data = {
        "update": get_today(),
        "count": len(values),
        "columns": columns,
        "values": values,
    }
    # 　轉換成json格式輸出(保留名稱/pm25數值)
    return json.dumps(json_data, ensure_ascii=False)


@app.route("/county-pm25-json/<county>", methods=["GET", "POST"])
def get_county_pm25_json(county):
    sites, pm25 = get_county_pm25(county)

    return json.dumps({"sites": sites, "pm25": pm25}, ensure_ascii=False)


@app.route("/six-pm25-json", methods=["GET", "POST"])
def get_six_pm25_json():
    countys, pm25 = get_six_pm25()

    return json.dumps({"sites": countys, "pm25": pm25}, ensure_ascii=False)


@app.route("/pm25-json", methods=["GET", "POST"])
def get_pm25_json():
    columns, values, lowest_data, highest_data = get_pm25()
    sites = [value[0] for value in values]
    pm25 = [value[2] for value in values]

    # 新增要求日期跟目前站點數量
    json_data = {
        "update": get_today(),
        "count": len(sites),
        "sites": sites,
        "pm25": pm25,
        "lowest_data": lowest_data,
        "highest_data": highest_data,
    }

    # return json_data
    # 　轉換成json格式輸出(保留名稱/pm25數值)
    return json.dumps(json_data, ensure_ascii=False)


@app.route("/pm25-charts")
def pm25_charts():
    countys = get_countys()
    return render_template("pm25-charts-bulma.html", countys=countys)


@app.route("/pm25", methods=["GET", "POST"])
def pm25():
    # 檢查是否有勾選(request.GET=>args)
    sort = False
    # (reguest.POST =>form)
    if request.method == "POST":
        sort = request.form.get("sort")
    # None,0,0.0,'' ==> if ==>False
    columns, values = get_pm25(sort)

    return render_template(
        "pm25.html", datetime=get_today(), sort=sort, columns=columns, values=values
    )


@app.route("/lottory")
def lottory():
    datas = get_lottory()
    return render_template("lottory.html", dollars=datas[0], lottorys=datas[1])


@app.route("/stock")
def stock():
    # 呼叫爬蟲程式
    stocks = get_stock()
    for stock in stocks:
        print(stock["分類"], stock["指數"])

    return render_template("stock.html", date=get_today(), stocks=stocks)


if __name__ == "__main__":
    # print(json.dumps(get_pm25_json()))
    # print(stock())

    app.run(debug=True)
