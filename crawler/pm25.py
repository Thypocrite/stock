import pandas as pd

url='https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV'

def get_pm25(sort=False):
    columns,values =[],[]
    try:
        df = pd.read_csv(url).dropna()
        columns=df.columns.tolist()
        values =df.values.tolist()
        
        lowest_data=df.sort_values("pm25").iloc[0][["site","pm25"]].tolist()
        highest_data=df.sort_values("pm25").iloc[-1][["site","pm25"]].tolist()
        
        if sort:
            values =sorted(values,key=lambda x:x[2],reverse=True)
    except Exception as e:
        print(e)
    
    return columns,values,lowest_data,highest_data

if __name__=="__main__":
    print(get_pm25(True))