import pandas as pd
import requests
import json

class Base():
    """
    All connections to the API take place here
    API services the past 5 year of data
    API service allows for unlimited calls
    Data updated every 15 minutes
    """
 
    # initializing the class
    def __init__(self, ticker, multiplier, timespan, fromdate, todate):
        # initializations
        self.ticker = ticker
        self.fromdate = fromdate
        self.todate = todate
        self.multiplier = multiplier
        self.timespan = timespan
 
        # the request link lego pieces
        self.BASE_URL = 'https://api.polygon.io'
        self.API_KEY = 'NF6fM5lz1m9crDksTVh0iXQcjGs5sOXG'
        self.ENDCAP = '?adjusted=true&limit=50000&apiKey='
        self.CHUNK = f'/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{fromdate}/{todate}'
        self.Data()
        
    def return_url(self):
        return f'{self.BASE_URL}{self.CHUNK}{self.ENDCAP}{self.API_KEY}'
 
        # Get aggregate bars for a stock over a given date range in custom time window sizes
    def Data(self):
        URL = f'{self.BASE_URL}{self.CHUNK}{self.ENDCAP}{self.API_KEY}'
        response = requests.get(URL)
        if response.ok==True:
            stockdata = response.json()
            indexlist = []
            for i in (range(len(stockdata['results']))):
                indexlist.append(i)
            df = pd.DataFrame(stockdata, index=indexlist)
            newdf = df['results']
            result = pd.DataFrame(newdf)
            #result.rename(columns = {'v':'trading_volume','vw':'volume_weighted_avg_price','o':'open_price','c':'close_price','h':'highest_price','l':'lowest_price','t':'date_time','n':'transaction_amt'}, inplace=True)
            trading_volume_list = [row['v'] for row in result['results']]
            #volume_weighted_list = [row['vw'] for row in result['results']]
            open_price_list = [row['o'] for row in result['results']]
            close_price_list = [row['h'] for row in result['results']]
            highest_price_list = [row['h'] for row in result['results']]
            lowest_price_list = [row['l'] for row in result['results']]
            date_time_list = [row['t'] for row in result['results']]
            transaction_amt_list = [row['t'] for row in result['results']]
            data = pd.DataFrame({'trading_volume':trading_volume_list,
                                 #'volume_weighted_avg_price':volume_weighted_list,
                                 'open_price':open_price_list,
                                 'close_price':close_price_list,
                                 'highest_price':highest_price_list,
                                 'lowest_price':lowest_price_list,
                                 'date_time':date_time_list,
                                 'transaction_amt':transaction_amt_list})
            data['date_time'] = data['date_time'].astype(str).astype(int)
            data['ID'] = self.ticker
            data = data[['ID','date_time','open_price','close_price','trading_volume','highest_price','lowest_price','transaction_amt']]
            datelist = data['date_time']
            datelist = list(datelist)
            datelist = pd.to_datetime(datelist, unit='ms').to_pydatetime()
            data['date_time'] = datelist
            self.df = data
            return self.df
            
if __name__ == '__main__':
    ticker='AAPL'
    multiplier="1"
    timespan='day'
    fromdate='2018-09-05'
    todate='2023-09-03'
    c = Base(ticker=ticker, multiplier=multiplier, timespan=timespan, fromdate=fromdate, todate=todate)
    c.df.to_csv('src/data/stockdata.csv', index=False) 