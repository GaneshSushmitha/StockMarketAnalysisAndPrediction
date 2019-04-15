from datetime import datetime,timedelta
import pandas as pd
from pandas_datareader import data
from fbprophet import Prophet
import matplotlib.pyplot as plt


ticker = "AMZN"
#Get all data from one year ago from today.
end_date= datetime.today()
start_date = end_date - timedelta(days=365)
print('Stock Start Date: ', start_date)
print('End Date: ', end_date)

#Get the data from yahoo finance
df = data.DataReader('AMZN', 'yahoo', start_date, end_date)

''' *** Prophet Model Implementation*** '''
df.insert(0, "Date", list(df.index))
new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])
print(new_data.head())

for i in range(0,len(new_data)):
    new_data['Date'][i] = df['Date'][i]
    new_data['Close'][i] = df['Close'][i]

new_data['Date'] = pd.to_datetime(new_data.Date,format='%Y-%m-%d')
new_data.index = new_data['Date']

#preparing data
new_data.rename(columns={'Close': 'y', 'Date': 'ds'}, inplace=True)

'''#train and validation
train = new_data[:200]
valid = new_data[200:]'''

#fit the model
model = Prophet( daily_seasonality=True)
model.fit(new_data)

#predictions
future = model.make_future_dataframe(periods=60)
forecast = model.predict(future)

print("FORECASTED VALUE")
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig1 = model.plot(forecast)
plt.show(fig1)

#rmse
'''forecast_valid = forecast['yhat'][200:]
rms=np.sqrt(np.mean(np.power((np.array(valid['y'])-np.array(forecast_valid)),2)))
rms'''


'''
*** Pandas Data Frame Investigation ***
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


''' *** Gradient Boosting Regressor ***
df.insert(0, "Date", list(df.index))
rows = df.values.tolist()  # convert dataframe into a list
print("ROWS: \n",rows)
x_train = []
y_train = []
x_test = []
y_test = []
X = []
Y = []
for row in rows:
    X.append(int(''.join(str(row[0].date()).split('-'))))
    Y.append(row[4])
x_train, x_test, y_train, y_test = train_test_split(X,Y,train_size=0.5,test_size=0.5, shuffle=False)
print("X TRAIN: \n", x_train)
print("X TEST: \n", x_test)
print("Y TRAIN: \n", y_train)
print("Y TEST: \n", y_test)
# Convert lists into numpy arrays
x_train = np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test = np.array(y_test)
print("X TEST NUMPY ARRAY \n", x_test)
print("Y TRAIN NUMPY ARRAY \n", y_train)
print("X TEST DIMENSIONS\n '{0}'".format(x_test.shape))
print("Y TRAIN DIMENSIONS", y_train.shape)

# reshape the values as we have only one input feature
x_train = x_train.reshape(-1,1)
x_test = x_test.reshape(-1,1)
y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)
print("X TEST NUMPY ARRAY AFTER RESHAPE \n", x_test)
print("X TEST DIMENSIONS AFTER RESHAPE\n '{0}'".format(x_test.shape))
print("Y TRAIN NUMPY ARRAY AFTER RESHAPE \n", y_train)
print("Y TRAIN DIMENSIONS AFTER RESHAPE", y_train.shape)


# Gradient Boosting Regressor
clf_gb = GradientBoostingRegressor(n_estimators=200)
print("clf_gb \n", clf_gb)
clf_gb.fit(x_train,y_train)
y_pred_gb = clf_gb.predict(x_test).reshape(-1,1)
print("y_pred_gb \n", y_pred_gb)
print("Y_TEST", y_test)'''
'''

*** main.py ***
*** Calculating pct_change manually ***
indices = stockData.index
        for i in indices :
            if(i == start_date):
                percentChangeList.append('0%')
            else:
                if(indices.contains(previousDateIndex)):
                    value = ((stockData.loc[i,'Close'] - stockData.loc[previousDateIndex,'Close'])/stockData.loc[previousDateIndex,'Close'])*100
                    percentChangeList.append(value)
                previousDateIndex = i
                
                        yaxis=dict(
            domain=[0, 0.2],
            showticklabels=False
        ),
        
*** Legend Toggling Event Investigation ***     
#Legend Toggling
@app.callback(
    dash.dependencies.Output('slider', 'style'),
    [dash.dependencies.Input('stockChart', 'figure')])
def DisplayDateRangeSlider(figure):
    trace_name = figure
    trace_name = figure['data'][0]['visible']
    if trace_name == "False":
        return {'display': 'none'}
    else:
        return {"width": "80%", "margin": "auto"}
'''






