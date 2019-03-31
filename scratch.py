from datetime import datetime,timedelta
import pandas as pd
from pandas_datareader import data

ticker = "AMZN"

#Get all data from one year ago from today.
end_date= datetime.today()
print(end_date)
start_date = end_date - timedelta(days=365)
print('Stock Start Date: ', start_date)
print('End Date: ', end_date)

#Get the data from yahoo finance
df = data.DataReader('AMZN', 'yahoo', start_date, end_date)
df.info()
print(df.head())
print(df.tail())
print(df.describe())
print("Display first column using integer loc. The resulting data frame has row index as date")
print(df.iloc[:,[0]])
print("1 row using loc - the index is a timestamp")
print(df.loc['2019-03-20'])
print("Index Values")
print(list(df.index))
if (type(df.index[0]) == pd.Timestamp):
    print("***We have successfully created time series data***")

s = start_date + timedelta(days=30)
e = end_date - timedelta(days=30)
#mask = ((df.index >= s) & (df.index <= e))
#newdf=df.loc[mask]
newdf = df.loc[s:e]
print(newdf.head())
print(newdf.tail())

dateList = pd.date_range(start=start_date, end=end_date + timedelta(days=1))
print("DateList: \n",dateList)
dateList = dateList[::60]
#if(dateList[len(dateList) - 1] != end_date):
    #dateList.insert(len(dateList),end_date)

print("DateList Freq 60 D: \n",dateList)

dateList1 = pd.date_range(start=start_date, end=end_date + timedelta(days=60) , freq='2MS')
print("DateList: \n",dateList1)
pList = pd.period_range(start=start_date, end=end_date , freq='M')
print("PeriodList: \n",pList)
datemarks = {i: dateList[i] for i in range(0, len(dateList))}
print("Date Marks: \n", datemarks)

'''
    trace1 = plotlyGraphObj.Ohlc(x=stockData.index,
                                open=stockData['Open'],
                                high=stockData['High'],
                                low=stockData['Low'],
                                close=stockData['Close'],
                                #text=paste("Text1:", df$AAPL.Open, "<br>Text2:", df$AAPL.Close)

     series = stockData['Close']
        series = series.pct_change(periods=1, fill_method='pad')
        print(series)                           )

    '''





