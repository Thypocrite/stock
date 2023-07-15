import pandas as pd

url = "https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV"

df = None


def get_countys():
    global df
    countys = []
    try:
        if df is None:
            df = pd.read_csv(url).dropna()

        countys = sorted(set(df["county"]))

    except Exception as e:
        print(e)

    return countys


def get_county_pm25(county="臺北市"):
    global df
    sites, pm25 = [], []
    try:
        if df is None:
            df = pd.read_csv(url).dropna()

        datas = df.groupby("county").get_group(county)[["site", "pm25"]].values.tolist()
        sites, pm25 = list(zip(*datas))

    except Exception as e:
        print(e)

    return sites, pm25


# 取得六都數據
def get_six_pm25():
    global df
    countys = ["臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市"]
    pm25 = []
    try:
        if df is None:
            df = pd.read_csv(url).dropna()
        for county in countys:
            pm25.append(round(df.groupby("county").get_group(county)["pm25"].mean(), 2))
    except Exception as e:
        print(e)

    return countys, pm25


# 取得所有數據ㄉ
def get_pm25(sort=False):
    global df
    columns, values = [], []
    try:
        if df is None:
            df = pd.read_csv(url).dropna()
        columns = df.columns.tolist()
        values = df.values.tolist()
        # 取得最高跟最低值
        datas = df.sort_values("pm25")[["site", "pm25"]].values.tolist()
        datas = sorted(datas, key=lambda x: x[-1])
        lowest_data = datas[0]
        highest_data = datas[-1]
        # 是否排序
        if sort:
            values = sorted(values, key=lambda x: x[2], reverse=True)
    except Exception as e:
        print(e)

    return columns, values, lowest_data, highest_data


if __name__ == "__main__":
    print(get_countys())
