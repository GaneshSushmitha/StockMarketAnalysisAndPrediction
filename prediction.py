import pandas as pd
from fbprophet import Prophet
import plotly.graph_objs as plotlyGraphObj

class Prediction:
    def __init__(self, stockData, predictPeriod):
        new_data = stockData.loc[:, ['Date', 'Close']]
        new_data.loc[:, "Date"] = pd.to_datetime(new_data.loc[:, "Date"], format='%Y-%m-%d')
        self.stockData = new_data
        self.predictPeriod = predictPeriod

    def forcastStockPrices(self):
        model = Prophet(weekly_seasonality=False, yearly_seasonality=False)
        transformedData = self.stockData
        transformedData.rename(columns={'Close': 'y', 'Date': 'ds'}, inplace=True)
        model.fit(transformedData)
        # predictions
        future = model.make_future_dataframe(periods=self.predictPeriod)
        future['day_week'] = future.ds.dt.weekday_name
        future = future[future.day_week != 'Sunday']
        future = future[future.day_week != 'Saturday']
        forecastValues = model.predict(future)
        return forecastValues

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
                x=0.3,
                yanchor='bottom',
                bgcolor='#E2E2E2',
                bordercolor='#FFFFFF',
                borderwidth=2
            )
        )

    def create_prediction_chart(self,stockData):
        forecast = self.forcastStockPrices()
        trace1 = {
            "x": stockData.Date,
            "y": stockData.Close,
            "name": "Actual Stock Prices",
            "type": "scatter",
            "mode": "markers"
        }
        trace2 = {
            "x": forecast.ds,
            "y": forecast.yhat,
            "name": "Best Fit Line",
            "type": "scatter",
            "mode": "lines",
            "line": {"color": "#ff6d22"}
        }
        trace3 = {
            "x": forecast.ds,
            "y": forecast.yhat_lower,
            "name": "Lower Band",
            "type": "scatter",
            "mode": "lines",
            "fill": "none",
            "line": {"color": "#57b8ff"},
        }
        trace4 = {
            "x": forecast.ds,
            "y": forecast.yhat_upper,
            "name": "Upper Band",
            "type": "scatter",
            "mode": "lines",
            "fill": "tonexty",
            "line": {"color": "#57b8ff"},

        }
        figure = plotlyGraphObj.Figure(data=([trace1, trace2, trace3, trace4]),
                                       layout=plotlyGraphObj.Layout(self.create_graph_layout()))
        return figure





