from flask import Flask, render_template
from datetime import datetime


app=Flask(__name__)


@app.route("/bmi/height=<h>&weight=<w>")
def get_bmi(h,w):
    try:
        bmi =round(eval(w)/(eval(h)/100)**2,2)
        print(bmi)
        return f"bmi:{bmi}"
    except Exception as e:
        print(e)
        return "資料有誤!"


@app.route("/book/<int:id>")
def book(id):
    try:
        books={1:"Python",2:"Java",3:"C++"}
        return books[id]
    except Exception as e:
        print(e)
        return "沒有書籍資料"



@app.route("/today")
def today():
    datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'<h1>{datetime.now()}</h1>'


@app.route('/')
def index():
    name='jerry'
    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content= {"name":name,"date":date}
    
    return render_template("index.html",content=content)

@app.route("/stock")
def stock():
    

    for stock in stocks:
        print(stock['分類'],stock["指數"])

    return render_template('stock.html',date=get_today(),stocks=stocks)

def get_today():
    date=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    return date

if __name__=="__main__":
    stocks=[
        {'分類': '日經指數', '指數': '22,920.30'},
        {'分類': '韓國綜合', '指數': '2,304.59'},
        {'分類': '香港恆生', '指數': '25,083.71'},
        {'分類': '上海綜合', '指數': '3,380.68'}
    ]
    #print(stock())
    app.run(debug=True)

