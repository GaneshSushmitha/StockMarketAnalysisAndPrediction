import dash
import dash_core_components as dashcore
import dash_html_components as html
import dash_table as dashtable
from datetime import datetime, timedelta
import pandas as pd
from pandas_datareader import data
import plotly.graph_objs as plotlyGraphObj


def getRangeSliderMarks(start_date, end_date):
    dateList = pd.date_range(start=start_date, end=end_date, freq='90D')
    datemarks = {i: dateList[i] for i in range(0, len(dateList))}
    return datemarks

def getBarColors(stockData):
    barColors = []
    for x in stockData.index:
        if(stockData.loc[x, 'Open'] < stockData.loc[x, 'Close']):
            barColors.append(colors["increasing"])
        else:
            barColors.append(colors["decreasing"])
    return barColors


def clean_transform_stockData(stockData):
    if (type(stockData.index[0]) == pd.Timestamp):
        percentChangeList=[0]
        previousDateIndex = start_date
        # remove rows if all columns have NaN values
        stockData = stockData.dropna(how='all')
        # remove rows that have Nan values in the column subset
        stockData = stockData.dropna(subset=['High', 'Low', 'Open', 'Close'])
        #Insert Date as a column
        stockData.insert(0, "Date", list(stockData.index))
        #Calculate % Change based on daily closing prices
        indices = stockData.index
        for i in indices :
            if(i == start_date):
                percentChangeList.append('0%')
            else:
                if(indices.contains(previousDateIndex)):
                    value = ((stockData.loc[i,'Close'] - stockData.loc[previousDateIndex,'Close'])/stockData.loc[previousDateIndex,'Close'])*100
                    percentChangeList.append(value)
                previousDateIndex = i
    stockData["% Change"] = percentChangeList
    return stockData


def create_table(stockData):
    return dashtable.DataTable(
        id='stockDataTable',
        columns=[{"name": i, "id": i} for i in stockData.columns],
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


def create_chart(stockData):
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
            "yaxis":"y2"
         }
    # Create Line of open values
    trace2 ={
                "x":stockData.index,
                "y":stockData.Volume,
                "type":"bar",
                "name":"Volume",
                "yaxis":"y",
                "marker":dict(color=getBarColors(stockData))
    }

    layout = plotlyGraphObj.Layout(
        title='Time Series Plot',
        hovermode='closest',
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        ),
        yaxis=dict(
            domain=[0, 0.2],
            showticklabels=False
        ),
        yaxis2=dict(
            domain=[0.2, 1.0]
        )
    )
    fig = plotlyGraphObj.Figure(data=([trace1,trace2]), layout=layout)
    return fig


colors = {
    'background': '#111111',
    'text': '#483D8B',
    'increasing': "#17BECF",
    'decreasing': "#7F7F7F"
}

end_date = datetime.utcnow().date()
start_date = end_date - timedelta(days=365)

dateMarks = getRangeSliderMarks(start_date, end_date)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H2(
        children='Market Summary',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dashcore.Dropdown(
        id='stockTickers',
        options=[{'label': 'AMZN', 'value': 'AMZN'}, {'label': 'MSFT', 'value': 'MSFT'},
                 {'label': 'AAPL', 'value': 'AAPL'}, {'label': 'GOOGL', 'value': 'GOOGL'},
                 {'label': 'FB', 'value': 'FB'}],
        value='AMZN',
        placeholder="Select Stock",
        style={
            "width": "50%",
            "position": "relative",
            "zIndex": "999"
        }
    ),

    html.H4('Historical Data'),
    html.Div(id="stockTable"),

    html.H4('Chart'),
    dashcore.Graph(id="stockCandleStickChart", figure=""),

    html.Div(dashcore.RangeSlider(
        id="dateRangeSlider",
        min=0,
        max=4,
        marks=dateMarks,
        value=[0, len(dateMarks) - 1]
    ),
        style={"width": "80%", "margin": "auto"}
    ),

    html.Div(id='intermediateValue', style={'display': 'none'})
])


@app.callback(
    dash.dependencies.Output('intermediateValue', 'children'),
    [dash.dependencies.Input('stockTickers', 'value')])
def get_data(ticker):
    end_date = datetime.now()
    #Check if stockdata for the day is available
    if(end_date.isoweekday() <= 5 and end_date.hour < 19 ):
        end_date = end_date - timedelta(days=1)
    start_date = end_date - timedelta(days=365)
    stockData = data.DataReader(ticker, 'yahoo', start_date, end_date)
    stockData = clean_transform_stockData(stockData)
    return stockData.to_json(date_format='iso', orient='split')


@app.callback(
    dash.dependencies.Output('stockTable', 'children'),
    [dash.dependencies.Input('intermediateValue', 'children')])
def update_stockDataTable(stockjson):
    stockData = pd.read_json(stockjson, orient='split')
    stockTable = create_table(stockData)
    return stockTable


@app.callback(
    dash.dependencies.Output('stockCandleStickChart', 'figure'),
    [dash.dependencies.Input('dateRangeSlider', 'value'),
     dash.dependencies.Input('intermediateValue', 'children')])
def updateGraph(range, stockjson):
    i = 0
    stockData = pd.read_json(stockjson, orient='split')
    filtered_stockData = stockData[dateMarks[range[0]]: dateMarks[range[1]]]
    graphFigure = create_chart(filtered_stockData)
    return graphFigure


if __name__ == "__main__":
    app.run_server(debug=True)



