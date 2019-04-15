from datetime import datetime, timedelta
from pandas_datareader import data
import pandas as pd
import plotly.graph_objs as plotlyGraphObj
import dash_table  as dashtable
import constant

class Analysis:
    def __init__(self):
        end_dateTime = datetime.utcnow()
        self.end_date = end_dateTime.date()
        #Check if stockdata for the day is available
        if (self.end_date.isoweekday() <= 5 and end_dateTime.hour < constant.stockExchangeClosingHour):
            self.end_date = self.end_date - timedelta(days=1)
        self.start_date = self.end_date - timedelta(days=constant.noOfDaysOfHistoricalData)
        dateList = pd.date_range(start=self.start_date, end=self.end_date, freq= constant.DateRangeSliderFrequency)
        self.dateMarks = {i: dateList[i] for i in range(0, len(dateList))}

    def getStockData(self, ticker):
        #df.to_csv(index=False) - write to csv using pandas
       return data.DataReader(ticker, 'yahoo', self.start_date, self.end_date)

    def clean_transform_stockData(self,stockData):
        if (type(stockData.index[0]) == pd.Timestamp):
            new_stockData = stockData.dropna(how='all')
            new_stockData= new_stockData.dropna(subset=['High', 'Low', 'Open', 'Close'])
            new_stockData.insert(0, "Date", list(new_stockData.index))
            #Calculate % Change based on daily closing prices
            series = new_stockData['Close']
            new_stockData["% Change"] = (series.pct_change(periods=1, fill_method='pad')*100).round(2)
            return new_stockData

    def create_table(self,stockData):
        columns=[]
        for i in stockData.columns:
            if i != "% Change":
                columns.append({"name": i, "id": i})
        return dashtable.DataTable(
            id='stockDataTable',
            columns=columns,
            data=stockData.to_dict("rows"),
            n_fixed_rows=1,
            style_table={
                'height': '310px',
                'overflowY': 'scroll',
                'border': 'thin lightgrey solid',
            },
            pagination_settings={
                'current_page': 0,
                'page_size': 20
            }
        )

    def create_graph_layout(self):
        return dict(
            hovermode='x',
            showlegend=True,
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                )
            ),
            legend=dict(
                orientation='h',
                y=1.2,
                x=0.4,
                yanchor='bottom',
                bgcolor='#E2E2E2',
                bordercolor='#FFFFFF',
                borderwidth=2
            )
        )

    def getVolumeBarChartColors(self,stockData):
        barColors = []
        for x in stockData.index:
            if(stockData.loc[x, 'Open'] < stockData.loc[x, 'Close']):
                barColors.append("#34AA7F")
            else:
                barColors.append("red")
        return barColors

    def create_visualization_chart(self,stockData):
        trace1 = {
                "x":stockData.index,
                "open": stockData['Open'],
                "high": stockData['High'],
                "low": stockData['Low'],
                "close": stockData['Close'],
                "type": "candlestick",
                "name": "OHLC",
                "text": ["% change: {}".format(x) for x in stockData['% Change']],
                "hoverinfo":['all'],
                "yaxis":"y",
                "showlegend":False,
                "visible": True,
                "legendgroup" : "visualizationCharts"
             }
        # Create Line of open values
        trace2 ={
                    "x":stockData.index,
                    "y":stockData.Volume,
                    "type":"bar",
                    "name":"Volume",
                    "yaxis":"y2",
                    "marker":dict(color=self.getVolumeBarChartColors(stockData)),
                    "showlegend":False,
                    "visible": True,
                    "legendgroup": "visualizationCharts"
        }
        layout = self.create_graph_layout()
        layout["yaxis"] = dict(
                domain=[0.2, 1.0]
            )
        layout["yaxis2"] = dict(
                domain=[0.0, 0.2],
                showticklabels=False
            )

        fig = plotlyGraphObj.Figure(data=([trace1,trace2]), layout=plotlyGraphObj.Layout(layout))
        return fig
