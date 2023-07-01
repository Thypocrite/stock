import requests
from bs4 import BeautifulSoup


def get_stock():
    url='https://tw.stock.yahoo.com/'

    resp=requests.get(url)
    soup=BeautifulSoup(resp.text,'lxml')
    lis=soup.find('nav',class_="indexChartNav").find_all('li')

    stocks=[]

    for li in lis:
        spans=li.find_all('span')[:2]
        data={'分類':spans[0].text.strip(),
            '指數':spans[1].text.strip()}
        stocks.append(data)
        
    return(stocks)

if __name__ == "__main__":
    print(get_stock())