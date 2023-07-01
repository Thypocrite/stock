import requests
from bs4 import BeautifulSoup

def get_lottery():
    def get_ball(name):
        main=soup.find('div',id=f"contents_logo_0{lottery_group[name]}").find_parent('div')
        date=main.find('span').text.strip().replace('\xa0',' ')
        balls=','.join([ball.text.strip() for ball in main.find_all('div',class_="ball_tx")[6:]])
        if main.find('div',class_='ball_red'):
            balls=balls+' 特別號:'+main.find('div',class_='ball_red').text.strip()
            
        return date,balls


    url='https://www.taiwanlottery.com.tw/index_new.aspx'
    lottery_group={
            '威力彩':2,
            '大樂透':4,
            '金彩539':6    
        }

    datas={}
    
    try:
        resp=requests.get(url)
        soup=BeautifulSoup(resp.text,'lxml')

        dollars=[
            dollar.text.strip().replace("\n\n","")
            for dollar in soup.find_all("div",class_="top_dollar_tx")
        ]

        for name in lottery_group:
            datas[name]=get_ball(name)

    except Exception as e:
        print(e)    

    return dollars,datas

    





