import dash
import dash_core_components as dashcore
import dash_html_components as html
import pandas as pd
import constant
from analysis import Analysis
from prediction import Prediction


analysis = Analysis()

app = dash.Dash(__name__, external_stylesheets=constant.external_stylesheets)

app.layout = html.Div(children=[
    html.H2(
        children='Market Summary',
        style={
            'textAlign': 'center',
            'color': "#483D8B"
        }
    ),

    html.Div(
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
    )
    ),


    html.H4('Historical Data'),
    html.Div(id="stockTable"),

    html.Div(id="empty"),
    html.Div(
    dashcore.Tabs(id="tabs", value='Tabs', children=[

        dashcore.Tab(label='GAIN/LOSS', id='tab1', value='Tab1', children =[
            dashcore.Graph(id="stockVisualizationChart", figure=""),
            html.Div(
                            dashcore.RangeSlider(
                            id="dateRangeSlider",
                            min=0,
                            max=constant.noOfDateRangeSliderMarks - 1,
                            marks=analysis.dateMarks,
                            value=[0, len(analysis.dateMarks) - 1]
                            ),
                        id = "slider",
                        style={"width": "80%", "margin": "auto"}
                        ),

        ]),

        dashcore.Tab(label='FORECAST', id='tab2', value= 'Tab2', children=[
            dashcore.Graph(id="stockPredictionChart", figure="")
        ])
    ])
    ),
    html.Div(id='intermediateValue', style={'display': 'none'})
])


@app.callback(
    dash.dependencies.Output('intermediateValue', 'children'),
    [dash.dependencies.Input('stockTickers', 'value')])
def get_data(ticker):
    stockData = analysis.getStockData(ticker)
    stockData = analysis.clean_transform_stockData(stockData)
    return stockData.to_json(date_format='iso', orient='split')

@app.callback(
    dash.dependencies.Output('stockTable', 'children'),
    [dash.dependencies.Input('intermediateValue', 'children')])
def update_stockDataTable(stockjson):
    stockData = pd.read_json(stockjson, orient='split')
    return analysis.create_table(stockData)


@app.callback(
    dash.dependencies.Output('stockVisualizationChart', 'figure'),
    [dash.dependencies.Input('dateRangeSlider', 'value'),
     dash.dependencies.Input('intermediateValue', 'children')])
def updateVisualizationGraph(range, stockjson):
    i = 0
    stockData = pd.read_json(stockjson, orient='split')
    filtered_stockData = stockData[analysis.dateMarks[range[0]]: analysis.dateMarks[range[1]]]
    return analysis.create_visualization_chart(filtered_stockData)


@app.callback(
dash.dependencies.Output('stockPredictionChart', 'figure'),
     [dash.dependencies.Input('intermediateValue', 'children')])
def updatePredictionGraph(stockjson):
    stockData = pd.read_json(stockjson, orient='split')
    prediction = Prediction(stockData,constant.predictPeriod)
    return prediction.create_prediction_chart(stockData)


if __name__ == "__main__":
    app.run_server(debug=False)




