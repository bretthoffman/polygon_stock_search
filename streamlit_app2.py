import pandas as pd
import streamlit as st
import plotly.express as px
import urllib.request
from PIL import Image
import requests

st.set_page_config(page_title='Market Data')
st.header('Stock market prices & patterns')
st.text('POLYGON.IO API')
st.text('--Streamlit--Python--Pandas--Matplotlib--')

#Image
urllib.request.urlretrieve('https://www.investopedia.com/thmb/0r46QYJ4bTFn_6rFnePQkpMkJP8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-1307804823-6dc786663e77453e82b74e62c8e059fe.jpg', "stockpic.png")
image = Image.open('stockpic.png')
# Streamlit UI
st.image(image, caption="", use_column_width=True)
st.title("Find your data")
### --- Load Dataframe
input_ticker = st.text_input("Ticker (ex: AAPL, TSLA, AMZN, DIS) ------ if Crypto, format as X:(Ticker)USD").upper()
input_timespan = st.radio("By the...",key = 'time',options = ['minute', 'hour', 'day', 'week', 'month', 'quarter', 'year']).lower()
#input_multiplier = st.text_input("Size of the Timespan(ex: 1,2,3)")
input_fromdate = st.date_input("Start Date (API data will reach back 5 years)")
input_todate = st.date_input("End Date")

ticker = input_ticker
multiplier = '1'
timespan = input_timespan
fromdate = input_fromdate
todate = input_todate
response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{fromdate}/{todate}?adjusted=true&limit=50000&apiKey=NF6fM5lz1m9crDksTVh0iXQcjGs5sOXG")
if response.ok==True:
    stockdata = response.json()
    indexlist = []
    df = pd.DataFrame(stockdata)
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
    data = pd.DataFrame({'Trading Volume':trading_volume_list,
                         #'volume_weighted_avg_price':volume_weighted_list,
                         'Open Price':open_price_list,
                         'Close Price':close_price_list,
                         'Highest Price':highest_price_list,
                         'Lowest Price':lowest_price_list,
                         'Date/Time':date_time_list,
                         'Transaction Amt':transaction_amt_list})
    data['Date/Time'] = data['Date/Time'].astype(str).astype(int)
    if str(input_ticker)[0] == 'X':
        input_ticker2 = str(input_ticker[2:-3])
    else: input_ticker2 = input_ticker
    data['ID'] = input_ticker2
    data = data[['Date/Time','Open Price','Close Price','Highest Price','Lowest Price','Trading Volume','Transaction Amt']]
    datelist = data['Date/Time']
    datelist = list(datelist)
    datelist = pd.to_datetime(datelist, unit='ms').to_pydatetime()
    data['Date/Time'] = datelist
    df = data
    st.dataframe(df)
else: st.write('Data is either incomplete or incorrect')

# Streamlit UI

st.title("Interact")

    # Data for chart

answer = st.radio("Is it graphin' time?",key = 'stockvalue',options = ['Open Price', 'Close Price', 'Highest Price', 'Lowest Price', 'All Prices', 'Trading Volume', 'Transaction Amount'])
if answer == 'Open Price':
    thetype = 'Open Price'
elif answer == 'Close Price':
    thetype = 'Close Price'
elif answer == 'Trading Volume':
    thetype = 'Trading Volume'
elif answer == 'Highest Price':
    thetype = 'Highest Price'
elif answer == 'Lowest Price':
    thetype = 'Lowest Price'
elif answer == 'Transaction Amount':
    thetype = 'Transaction Amt'    
elif answer == 'All Prices':
    thetype = df.columns[1:5] 
    

    # Chart type

answer2 = st.radio("Which type?",key = 'graphtype',options = ['Line', 'Bar', 'Scatter'])

if response.ok==True:
    if answer2 == 'Line':
        fig = px.line(df, x='Date/Time', y=thetype, title=f"{input_ticker2}")
        fig.update_traces(marker=dict(color='purple'))
        st.plotly_chart(fig)
    if answer2 == 'Bar':
        if answer == 'All Prices':
            fig = px.bar(df, x='Date/Time', y=thetype, title=f"{input_ticker2  }")
            st.plotly_chart(fig)
        else:
            fig = px.bar(df, x='Date/Time', y=thetype, title=f"{input_ticker2  }")
            fig.update_traces(marker=dict(color='purple'))
            st.plotly_chart(fig)
    if answer2 == 'Scatter':
        if answer == 'All Prices':
            fig = px.scatter(df, x='Date/Time', y=thetype, title=f"{input_ticker2  }")
            st.plotly_chart(fig)
        else:
            fig = px.scatter(df, x='Date/Time', y=thetype, title=f"{input_ticker2  }")
            fig.update_traces(marker=dict(color='purple'))
            st.plotly_chart(fig)
else: pass