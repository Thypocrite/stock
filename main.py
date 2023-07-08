from flask import Flask, render_template, request
from datetime import datetime
from crawler.stock import get_stock
from crawler.lottory import get_lottory
from crawler.pm25 import get_pm25
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


@app.route("/lottory",methods=["GET","POST"])
def lottory():
    return render_template("lottory.html", lottorys=get_lottory())


@app.route("/stock",methods=["GET","POST"])
def stock():
    # 呼叫爬蟲程式
    stocks = get_stock()
    for stock in stocks:
        print(stock["分類"], stock["指數"])

    return render_template("stock.html", date=get_today(), stocks=stocks)

@app.route("/pm25", methods=["GET", "POST"])
def pm25():
    # 檢查是否有勾選(request.GET=>args)
    sort = False
    # (reguest.POST =>form)
    if request.method == "POST":
        sort = request.form.get("sort")
        print(sort)
    # None,0,0.0,'' ==> if ==>False
    columns, values = get_pm25(sort)

    return render_template(
        "pm25.html", datetime=get_today(), sort=sort, columns=columns, values=values
    )

@app.route("/pm25-json")
def get_pm25_json():
    columns,values =get_pm25()
    sites=[value[0] for value in values]
    pm25=[value[2] for value in values]
    # 新增耀球日期跟目前站點數量
    json_data={"update":get_today(),"count":len(sites),"sites":sites,"pm25":pm25}

    return json.dumps(json_data,ensure_ascii=False)

@app.route("/pm25-charts")
def pm25_charts():
    return render_template("pm25-charts.html")

if __name__ == "__main__":
    # print(get_bmi(167, 67.5))
    # print(stock())
    app.run(debug=True)